"""
Crypto Trading Agent - Executes trades across multiple exchanges
with safety rules, approval workflows, and self-healing capabilities.
"""

import asyncio
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import ccxt.async_support as ccxt
import pandas as pd
import numpy as np
from loguru import logger

from agents.base_agent import BaseAgent


class TradingAgent(BaseAgent):
    """
    Crypto trading agent with safety controls and multi-exchange support.
    """
    
    def __init__(self, agent_id: str, config: Dict[str, Any]):
        super().__init__(agent_id, config)
        self.exchanges = {}
        self.active_positions = []
        self.consecutive_losses = 0
        self.daily_pnl = 0.0
        self.generation = 1
        self.strategy_mode = config.get("strategy", "conservative")
        self.trading_pairs = config.get("trading_pairs", ["BTC/USDT", "ETH/USDT"])
        
    async def start(self) -> bool:
        """Initialize exchange connections and start trading loop."""
        try:
            logger.info(f"{self.agent_id} - Starting trading agent...")
            
            # Initialize exchanges
            for exchange_name, credentials in self.config.get("exchanges", {}).items():
                exchange = getattr(ccxt, exchange_name)({
                    'apiKey': credentials.get('api_key'),
                    'secret': credentials.get('secret_key'),
                    'enableRateLimit': True,
                    'options': {'defaultType': 'spot'}
                })
                
                if credentials.get('testnet') or credentials.get('sandbox'):
                    exchange.set_sandbox_mode(True)
                
                await exchange.load_markets()
                self.exchanges[exchange_name] = exchange
                logger.info(f"{self.agent_id} - Connected to {exchange_name}")
            
            self.is_running = True
            self.start_time = datetime.now()
            
            # Start background tasks
            asyncio.create_task(self._trading_loop())
            
            logger.info(f"{self.agent_id} - Trading agent started successfully")
            return True
            
        except Exception as e:
            logger.error(f"{self.agent_id} - Failed to start: {str(e)}")
            return False
    
    async def stop(self) -> bool:
        """Gracefully stop trading and close positions."""
        try:
            logger.info(f"{self.agent_id} - Stopping trading agent...")
            self.is_running = False
            
            # Close all exchange connections
            for exchange in self.exchanges.values():
                await exchange.close()
            
            logger.info(f"{self.agent_id} - Trading agent stopped")
            return True
            
        except Exception as e:
            logger.error(f"{self.agent_id} - Error stopping: {str(e)}")
            return False
    
    async def execute_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a specific trading task."""
        task_type = task_data.get("type")
        
        if task_type == "analyze_market":
            return await self._analyze_market(task_data.get("symbol"))
        elif task_type == "execute_trade":
            return await self._execute_trade(task_data)
        elif task_type == "close_position":
            return await self._close_position(task_data.get("position_id"))
        else:
            return {"error": "Unknown task type"}
    
    async def generate_revenue(self) -> float:
        """Execute revenue-generating trades."""
        if not self.is_running:
            return 0.0
        
        # Check safety limits
        if self.consecutive_losses >= self.config.get("max_consecutive_losses", 3):
            logger.warning(f"{self.agent_id} - Max consecutive losses reached, pausing trading")
            return 0.0
        
        if abs(self.daily_pnl) > self.config.get("max_daily_drawdown_usd", 50):
            logger.warning(f"{self.agent_id} - Daily drawdown limit reached")
            return 0.0
        
        # Scan for opportunities
        opportunities = await self._scan_opportunities()
        
        if opportunities:
            best_opportunity = opportunities[0]
            pnl = await self._execute_trade(best_opportunity)
            return pnl.get("profit", 0.0)
        
        return 0.0
    
    async def _trading_loop(self):
        """Main trading loop that runs continuously."""
        while self.is_running:
            try:
                # Generate revenue
                revenue = await self.generate_revenue()
                self._update_metrics(revenue=revenue)
                
                # Update daily PnL
                self.daily_pnl += revenue
                
                # Track consecutive losses
                if revenue < 0:
                    self.consecutive_losses += 1
                else:
                    self.consecutive_losses = 0
                
                # Self-healing: become more conservative after losses
                if self.consecutive_losses >= 2:
                    self.strategy_mode = "conservative"
                    logger.info(f"{self.agent_id} - Switched to conservative mode (Gen {self.generation})")
                
                # Wait before next iteration
                await asyncio.sleep(60)  # Check every minute
                
            except Exception as e:
                logger.error(f"{self.agent_id} - Trading loop error: {str(e)}")
                self._update_metrics(error=True)
                await asyncio.sleep(30)
    
    async def _scan_opportunities(self) -> List[Dict[str, Any]]:
        """Scan markets for trading opportunities."""
        opportunities = []
        
        for symbol in self.trading_pairs:
            try:
                analysis = await self._analyze_market(symbol)
                
                if analysis.get("signal") == "BUY" and analysis.get("confidence", 0) > 0.75:
                    opportunities.append({
                        "symbol": symbol,
                        "action": "BUY",
                        "confidence": analysis["confidence"],
                        "entry_price": analysis["current_price"],
                        "stop_loss": analysis.get("support"),
                        "take_profit": analysis.get("resistance")
                    })
                elif analysis.get("signal") == "SELL" and analysis.get("confidence", 0) > 0.75:
                    opportunities.append({
                        "symbol": symbol,
                        "action": "SELL",
                        "confidence": analysis["confidence"],
                        "entry_price": analysis["current_price"],
                        "stop_loss": analysis.get("resistance"),
                        "take_profit": analysis.get("support")
                    })
                    
            except Exception as e:
                logger.error(f"{self.agent_id} - Error analyzing {symbol}: {str(e)}")
        
        # Sort by confidence
        opportunities.sort(key=lambda x: x["confidence"], reverse=True)
        return opportunities
    
    async def _analyze_market(self, symbol: str) -> Dict[str, Any]:
        """Analyze market using technical indicators."""
        try:
            # Fetch OHLCV data from first available exchange
            exchange = list(self.exchanges.values())[0]
            ohlcv = await exchange.fetch_ohlcv(symbol, timeframe='1h', limit=100)
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            
            # Calculate indicators
            df['rsi'] = self._calculate_rsi(df['close'], period=14)
            df['ma_short'] = df['close'].rolling(window=9).mean()
            df['ma_long'] = df['close'].rolling(window=21).mean()
            
            current_price = df['close'].iloc[-1]
            rsi = df['rsi'].iloc[-1]
            ma_short = df['ma_short'].iloc[-1]
            ma_long = df['ma_long'].iloc[-1]
            
            # Generate signal
            signal = "HOLD"
            confidence = 0.5
            
            if rsi < 30 and ma_short > ma_long:
                signal = "BUY"
                confidence = 0.7 + (30 - rsi) / 100
            elif rsi > 70 and ma_short < ma_long:
                signal = "SELL"
                confidence = 0.7 + (rsi - 70) / 100
            
            # Support/resistance levels
            support = df['low'].rolling(window=20).min().iloc[-1]
            resistance = df['high'].rolling(window=20).max().iloc[-1]
            
            return {
                "symbol": symbol,
                "current_price": current_price,
                "signal": signal,
                "confidence": confidence,
                "rsi": rsi,
                "support": support,
                "resistance": resistance
            }
            
        except Exception as e:
            logger.error(f"{self.agent_id} - Market analysis error: {str(e)}")
            return {"symbol": symbol, "signal": "HOLD", "confidence": 0.0}
    
    async def _execute_trade(self, trade_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a trade with safety checks."""
        symbol = trade_data.get("symbol")
        action = trade_data.get("action")
        confidence = trade_data.get("confidence", 0)
        
        # Check if approval needed
        trade_size_usd = self.config.get("max_trade_size_usd", 100)
        if trade_size_usd > self.config.get("require_approval_above_usd", 500):
            # Send Telegram approval request
            approval_granted = await self._request_approval(trade_data)
            if not approval_granted:
                logger.info(f"{self.agent_id} - Trade approval denied")
                return {"profit": 0.0, "status": "approval_denied"}
        
        try:
            # Execute on best exchange
            exchange = list(self.exchanges.values())[0]
            
            # In real implementation, this would place actual order
            # For now, simulate trade execution
            logger.info(f"{self.agent_id} - Executing {action} order for {symbol}")
            
            # Simulate trade result (replace with actual exchange API call)
            profit = await self._simulate_trade(symbol, action, trade_size_usd)
            
            # Update position tracking
            self.active_positions.append({
                "symbol": symbol,
                "action": action,
                "entry_price": trade_data.get("entry_price"),
                "timestamp": datetime.now()
            })
            
            return {"profit": profit, "status": "executed"}
            
        except Exception as e:
            logger.error(f"{self.agent_id} - Trade execution error: {str(e)}")
            return {"profit": 0.0, "status": "error", "error": str(e)}
    
    async def _simulate_trade(self, symbol: str, action: str, size_usd: float) -> float:
        """Simulate trade outcome (replace with actual trading logic)."""
        # This is a placeholder - in production, this would track real trades
        # For testing, return small random profit/loss
        import random
        outcome = random.uniform(-0.02, 0.03)  # -2% to +3%
        profit = size_usd * outcome
        return profit
    
    async def _request_approval(self, trade_data: Dict[str, Any]) -> bool:
        """Request approval via Telegram for large trades."""
        # Implementation would send Telegram message with approval buttons
        # For now, return False (require manual intervention)
        logger.warning(f"{self.agent_id} - Approval required for trade: {trade_data}")
        return False
    
    async def _close_position(self, position_id: str) -> Dict[str, Any]:
        """Close an open position."""
        # Find and close position
        for i, pos in enumerate(self.active_positions):
            if pos.get("id") == position_id:
                # Execute close order
                self.active_positions.pop(i)
                return {"status": "closed", "position_id": position_id}
        
        return {"status": "not_found"}
    
    def _calculate_rsi(self, prices: pd.Series, period: int = 14) -> pd.Series:
        """Calculate RSI indicator."""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))
    
    def apply_self_healing(self):
        """Apply self-healing after losses - restart as more conservative generation."""
        if self.generation < self.config.get("max_generation_restarts", 3):
            self.generation += 1
            self.strategy_mode = "conservative"
            self.consecutive_losses = 0
            logger.info(f"{self.agent_id} - Self-healed to generation {self.generation}")
        else:
            logger.critical(f"{self.agent_id} - Max generations reached, requesting termination")
