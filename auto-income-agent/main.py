"""
Main Orchestrator - Controls all sub-agents, monitors revenue,
and enforces self-termination if revenue targets aren't met.
"""

import asyncio
from datetime import datetime, timedelta
from typing import Dict, Any, List
from loguru import logger
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import (
    AGENT_NAME,
    MIN_DAILY_REVENUE_USD,
    TERMINATION_GRACE_PERIOD_DAYS,
    ENABLE_SUB_AGENTS,
    SUB_AGENTS,
    LOG_FILE,
    DEBUG_MODE
)
from agents.trading_agent import TradingAgent
from agents.freelance_agent import FreelanceAgent


class AgentOrchestrator:
    """
    Main controller that manages all sub-agents and enforces
    revenue-based self-termination policy.
    """
    
    def __init__(self):
        self.agent_name = AGENT_NAME
        self.sub_agents: Dict[str, BaseAgent] = {}
        self.is_running = False
        self.start_time = None
        self.revenue_history = []
        self.days_below_threshold = 0
        self.total_revenue = 0.0
        
    async def initialize(self) -> bool:
        """Initialize all sub-agents."""
        try:
            logger.info(f"{self.agent_name} - Initializing orchestrator...")
            
            # Initialize trading agent
            if SUB_AGENTS.get("trading_agent", {}).get("enabled"):
                trading_config = {
                    "exchanges": {
                        "binance": {
                            "api_key": os.getenv("BINANCE_API_KEY", ""),
                            "secret_key": os.getenv("BINANCE_SECRET_KEY", ""),
                            "testnet": True
                        }
                    },
                    "trading_pairs": ["BTC/USDT", "ETH/USDT"],
                    "max_trade_size_usd": 100,
                    "require_approval_above_usd": 500,
                    "max_consecutive_losses": 3,
                    "max_daily_drawdown_usd": 50,
                    "strategy": "conservative"
                }
                
                trading_agent = TradingAgent("trading_agent_001", trading_config)
                self.sub_agents["trading"] = trading_agent
                logger.info(f"{self.agent_name} - Trading agent initialized")
            
            # Initialize freelance agent
            if SUB_AGENTS.get("freelance_agent", {}).get("enabled"):
                freelance_config = {
                    "platforms": ["upwork", "fiverr", "freelancer"],
                    "services": [
                        "content_writing",
                        "logo_design",
                        "data_entry",
                        "virtual_assistant",
                        "ai_content_editing"
                    ],
                    "max_daily_bids": 20,
                    "upwork_api_key": os.getenv("UPWORK_API_KEY", ""),
                    "fiverr_api_key": os.getenv("FIVERR_API_KEY", "")
                }
                
                freelance_agent = FreelanceAgent("freelance_agent_001", freelance_config)
                self.sub_agents["freelance"] = freelance_agent
                logger.info(f"{self.agent_name} - Freelance agent initialized")
            
            # Add more agents as needed (content, lead_gen, etc.)
            # Similar pattern for content_agent, lead_gen_agent, etc.
            
            self.is_running = True
            self.start_time = datetime.now()
            
            logger.info(f"{self.agent_name} - Orchestrator initialized with {len(self.sub_agents)} agents")
            return True
            
        except Exception as e:
            logger.error(f"{self.agent_name} - Initialization failed: {str(e)}")
            return False
    
    async def start_all_agents(self) -> bool:
        """Start all sub-agents."""
        try:
            logger.info(f"{self.agent_name} - Starting all agents...")
            
            for agent_name, agent in self.sub_agents.items():
                success = await agent.start()
                if not success:
                    logger.error(f"{self.agent_name} - Failed to start {agent_name}")
                    return False
            
            logger.info(f"{self.agent_name} - All agents started successfully")
            
            # Start monitoring loop
            asyncio.create_task(self._monitoring_loop())
            asyncio.create_task(self._revenue_tracking_loop())
            
            return True
            
        except Exception as e:
            logger.error(f"{self.agent_name} - Error starting agents: {str(e)}")
            return False
    
    async def stop_all_agents(self) -> bool:
        """Gracefully stop all agents."""
        try:
            logger.info(f"{self.agent_name} - Stopping all agents...")
            self.is_running = False
            
            for agent_name, agent in self.sub_agents.items():
                await agent.stop()
            
            logger.info(f"{self.agent_name} - All agents stopped")
            return True
            
        except Exception as e:
            logger.error(f"{self.agent_name} - Error stopping agents: {str(e)}")
            return False
    
    async def _monitoring_loop(self):
        """Monitor agent health and performance."""
        while self.is_running:
            try:
                # Check health of all agents
                for agent_name, agent in self.sub_agents.items():
                    health = await agent.health_check()
                    
                    if not health.get("is_running"):
                        logger.warning(f"{self.agent_name} - {agent_name} is not running!")
                        # Attempt restart
                        await agent.start()
                    
                    # Log performance metrics
                    if health.get("performance", {}).get("errors", 0) > 5:
                        logger.warning(f"{self.agent_name} - {agent_name} has high error count")
                
                await asyncio.sleep(60)  # Check every minute
                
            except Exception as e:
                logger.error(f"{self.agent_name} - Monitoring error: {str(e)}")
                await asyncio.sleep(30)
    
    async def _revenue_tracking_loop(self):
        """Track revenue and enforce termination policy."""
        last_check = datetime.now()
        
        while self.is_running:
            try:
                # Check daily revenue every hour
                now = datetime.now()
                if (now - last_check).total_seconds() >= 3600:
                    daily_revenue = await self._calculate_daily_revenue()
                    self.revenue_history.append({
                        "date": now.date(),
                        "revenue": daily_revenue
                    })
                    
                    logger.info(f"{self.agent_name} - Daily revenue: ${daily_revenue:.2f}")
                    
                    # Check if below threshold
                    if daily_revenue < MIN_DAILY_REVENUE_USD:
                        self.days_below_threshold += 1
                        logger.warning(
                            f"{self.agent_name} - Day {self.days_below_threshold}/{TERMINATION_GRACE_PERIOD_DAYS} "
                            f"below minimum revenue (${daily_revenue:.2f} < ${MIN_DAILY_REVENUE_USD})"
                        )
                        
                        # Self-terminate if grace period exceeded
                        if self.days_below_threshold >= TERMINATION_GRACE_PERIOD_DAYS:
                            logger.critical(
                                f"{self.agent_name} - CRITICAL: Failed to meet revenue target for "
                                f"{TERMINATION_GRACE_PERIOD_DAYS} consecutive days. Initiating self-termination."
                            )
                            await self._self_terminate()
                            return
                    else:
                        self.days_below_threshold = 0
                    
                    last_check = now
                
                await asyncio.sleep(300)  # Check every 5 minutes
                
            except Exception as e:
                logger.error(f"{self.agent_name} - Revenue tracking error: {str(e)}")
                await asyncio.sleep(60)
    
    async def _calculate_daily_revenue(self) -> float:
        """Calculate total revenue generated today."""
        today_revenue = 0.0
        
        for agent_name, agent in self.sub_agents.items():
            revenue = agent.performance_metrics.get("revenue_generated", 0.0)
            today_revenue += revenue
        
        self.total_revenue += today_revenue
        return today_revenue
    
    async def _self_terminate(self):
        """Execute self-termination sequence."""
        try:
            logger.critical(f"{self.agent_name} - SELF-TERMINATION SEQUENCE INITIATED")
            
            # Stop all agents
            await self.stop_all_agents()
            
            # Final revenue report
            total_runtime = (datetime.now() - self.start_time).total_seconds() / 3600
            final_report = f"""
            ════════════════════════════════════════
            FINAL AGENT REPORT
            ════════════════════════════════════════
            Agent Name: {self.agent_name}
            Status: TERMINATED
            Reason: Failed to meet minimum revenue requirement
            Runtime: {total_runtime:.2f} hours
            Total Revenue Generated: ${self.total_revenue:.2f}
            Days Below Threshold: {self.days_below_threshold}
            Minimum Required: ${MIN_DAILY_REVENUE_USD}/day
            Grace Period: {TERMINATION_GRACE_PERIOD_DAYS} days
            ════════════════════════════════════════
            """
            
            logger.critical(final_report)
            
            # Send final notification via Telegram
            await self._send_final_notification()
            
            # Exit process
            logger.critical(f"{self.agent_name} - Process will now exit")
            os._exit(1)
            
        except Exception as e:
            logger.critical(f"{self.agent_name} - Error during self-termination: {str(e)}")
            os._exit(1)
    
    async def _send_final_notification(self):
        """Send final status notification via Telegram."""
        # Implementation would send Telegram message
        logger.info(f"{self.agent_name} - Final notification sent")
    
    def get_status_report(self) -> Dict[str, Any]:
        """Get comprehensive status report."""
        return {
            "agent_name": self.agent_name,
            "is_running": self.is_running,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "total_revenue": self.total_revenue,
            "days_below_threshold": self.days_below_threshold,
            "sub_agents": {
                name: agent.performance_metrics 
                for name, agent in self.sub_agents.items()
            },
            "revenue_history": self.revenue_history[-7:]  # Last 7 days
        }


async def main():
    """Main entry point."""
    # Setup logging
    logger.add(LOG_FILE, rotation="1 MB", retention="7 days")
    logger.info("=" * 60)
    logger.info(f"Starting {AGENT_NAME}")
    logger.info("=" * 60)
    
    # Create orchestrator
    orchestrator = AgentOrchestrator()
    
    # Initialize
    if not await orchestrator.initialize():
        logger.error("Failed to initialize orchestrator")
        sys.exit(1)
    
    # Start all agents
    if not await orchestrator.start_all_agents():
        logger.error("Failed to start agents")
        sys.exit(1)
    
    logger.info(f"{AGENT_NAME} is now running 24/7...")
    logger.info(f"Minimum daily revenue target: ${MIN_DAILY_REVENUE_USD}")
    logger.info(f"Termination grace period: {TERMINATION_GRACE_PERIOD_DAYS} days")
    
    # Keep running until stopped or self-terminated
    try:
        while orchestrator.is_running:
            await asyncio.sleep(60)
            
            # Print periodic status
            if datetime.now().minute == 0:
                status = orchestrator.get_status_report()
                logger.info(f"Status Update: Total Revenue = ${status['total_revenue']:.2f}")
    
    except KeyboardInterrupt:
        logger.info(f"{AGENT_NAME} - Received shutdown signal")
        await orchestrator.stop_all_agents()
    except Exception as e:
        logger.error(f"{AGENT_NAME} - Fatal error: {str(e)}")
        await orchestrator.stop_all_agents()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
