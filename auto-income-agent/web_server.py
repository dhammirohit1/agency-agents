"""
Auto-Income AI Agent - Web Dashboard & API Server
Run this file to start the web interface accessible via browser
"""

import os
import sys
import json
import asyncio
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, Any, List

from fastapi import FastAPI, Request, HTTPException, BackgroundTasks, Form
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
import plotly.graph_objects as go
from plotly.utils import PlotlyJSONEncoder

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

import config
from agents.trading_agent import TradingAgent
from agents.freelance_agent import FreelanceAgent
from agents.content_agent import ContentAgent
from agents.lead_agent import LeadAgent

# Create a simple Config class wrapper for compatibility
class Config:
    TEST_MODE = getattr(config, 'TEST_MODE', True)
    MIN_DAILY_PROFIT = getattr(config, 'MIN_DAILY_REVENUE_USD', 10.0)
    MAX_CONSECUTIVE_LOSS_DAYS = getattr(config, 'MAX_CONSECUTIVE_LOSSES', 7)

app = FastAPI(title="Auto-Income AI Agent", version="1.0.0")

# Setup templates and static files
BASE_DIR = Path(__file__).parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Global state
class AgentState:
    def __init__(self):
        self.is_running = False
        self.start_time: Optional[datetime] = None
        self.total_earned = 0.0
        self.today_earned = 0.0
        self.last_profit_check = datetime.now()
        self.consecutive_loss_days = 0
        self.trades_executed = 0
        self.freelance_bids = 0
        self.content_created = 0
        self.leads_generated = 0
        self.logs: List[Dict[str, Any]] = []
        self.profit_history: List[Dict[str, float]] = []
        
    def add_log(self, message: str, level: str = "INFO", source: str = "SYSTEM"):
        self.logs.append({
            "timestamp": datetime.now().isoformat(),
            "level": level,
            "source": source,
            "message": message
        })
        # Keep only last 500 logs
        if len(self.logs) > 500:
            self.logs = self.logs[-500:]
    
    def record_profit(self, amount: float):
        self.profit_history.append({
            "timestamp": datetime.now().timestamp(),
            "amount": amount,
            "cumulative": self.total_earned + amount
        })
        # Keep only last 100 data points
        if len(self.profit_history) > 100:
            self.profit_history = self.profit_history[-100:]
        
        if amount > 0:
            self.total_earned += amount
            self.today_earned += amount
            self.consecutive_loss_days = 0
        else:
            # Check if we had a loss day
            if self.today_earned <= 0:
                self.consecutive_loss_days += 1

state = AgentState()
trading_agent: Optional[TradingAgent] = None
freelance_agent: Optional[FreelanceAgent] = None
content_agent: Optional[ContentAgent] = None
lead_agent: Optional[LeadAgent] = None
scheduler: Optional[AsyncIOScheduler] = None

async def initialize_agents():
    """Initialize all agent instances"""
    global trading_agent, freelance_agent, content_agent, lead_agent
    
    # Create simple config dict for agents
    agent_config = {
        "test_mode": Config.TEST_MODE,
        "strategy": "conservative",
        "trading_pairs": ["BTC/USDT", "ETH/USDT"],
        "exchanges": {}
    }
    
    # Initialize with proper signatures
    trading_agent = TradingAgent("trading-agent-1", agent_config)
    freelance_agent = FreelanceAgent("freelance-agent-1", agent_config)
    content_agent = ContentAgent(agent_config)
    lead_agent = LeadAgent(agent_config)
    
    state.add_log("All agents initialized successfully", "INFO", "SYSTEM")

async def run_trading_cycle():
    """Execute one trading cycle"""
    if not state.is_running or not trading_agent:
        return
    
    try:
        state.add_log("Starting trading cycle...", "INFO", "TRADING")
        
        if Config.TEST_MODE:
            # Simulate trading in test mode
            import random
            profit = random.uniform(-5, 15)
            state.record_profit(profit)
            state.trades_executed += 1
            state.add_log(f"Test trade executed: Profit ${profit:.2f}", "INFO" if profit > 0 else "WARNING", "TRADING")
        else:
            # Real trading logic would go here
            result = await trading_agent.execute_safe_trade()
            if result:
                state.record_profit(result.get('profit', 0))
                state.trades_executed += 1
                state.add_log(f"Trade executed: {result}", "INFO", "TRADING")
    except Exception as e:
        state.add_log(f"Trading error: {str(e)}", "ERROR", "TRADING")

async def run_freelance_cycle():
    """Execute freelance bidding cycle"""
    if not state.is_running or not freelance_agent:
        return
    
    try:
        state.add_log("Scanning freelance opportunities...", "INFO", "FREELANCE")
        
        if Config.TEST_MODE:
            # Simulate bids in test mode
            import random
            bids = random.randint(0, 3)
            state.freelance_bids += bids
            if bids > 0:
                potential_earnings = random.uniform(20, 150)
                state.add_log(f"Placed {bids} bids. Potential: ${potential_earnings:.2f}", "INFO", "FREELANCE")
        else:
            # Real freelance logic
            opportunities = await freelance_agent.scan_opportunities()
            for opp in opportunities[:5]:  # Limit to 5 per cycle
                await freelance_agent.place_bid(opp)
                state.freelance_bids += 1
    except Exception as e:
        state.add_log(f"Freelance error: {str(e)}", "ERROR", "FREELANCE")

async def run_content_cycle():
    """Execute content creation cycle"""
    if not state.is_running or not content_agent:
        return
    
    try:
        state.add_log("Creating content...", "INFO", "CONTENT")
        
        if Config.TEST_MODE:
            import random
            content_count = random.randint(0, 2)
            state.content_created += content_count
            if content_count > 0:
                state.add_log(f"Created {content_count} content pieces", "INFO", "CONTENT")
        else:
            # Real content creation
            await content_agent.generate_content_batch()
    except Exception as e:
        state.add_log(f"Content error: {str(e)}", "ERROR", "CONTENT")

async def run_lead_cycle():
    """Execute lead generation cycle"""
    if not state.is_running or not lead_agent:
        return
    
    try:
        state.add_log("Generating leads...", "INFO", "LEADS")
        
        if Config.TEST_MODE:
            import random
            leads = random.randint(0, 5)
            state.leads_generated += leads
            if leads > 0:
                state.add_log(f"Generated {leads} new leads", "INFO", "LEADS")
        else:
            # Real lead generation
            await lead_agent.generate_leads()
    except Exception as e:
        state.add_log(f"Lead gen error: {str(e)}", "ERROR", "LEADS")

async def check_self_termination():
    """Check if agent should self-terminate due to poor performance"""
    if not state.is_running:
        return
    
    now = datetime.now()
    hours_since_start = (now - state.start_time).total_seconds() / 3600 if state.start_time else 0
    
    # Only check after running for 24 hours
    if hours_since_start < 24:
        return
    
    # Check consecutive loss days
    if state.consecutive_loss_days >= Config.MAX_CONSECUTIVE_LOSS_DAYS:
        state.add_log(
            f"SELF-TERMINATION: {state.consecutive_loss_days} consecutive loss days. Shutting down.",
            "CRITICAL",
            "SYSTEM"
        )
        await stop_agents()
        sys.exit(0)

async def periodic_tasks():
    """Run all periodic tasks"""
    await asyncio.gather(
        run_trading_cycle(),
        run_freelance_cycle(),
        run_content_cycle(),
        run_lead_cycle(),
        check_self_termination(),
        return_exceptions=True
    )

async def start_scheduler():
    """Start the background scheduler"""
    global scheduler
    
    scheduler = AsyncIOScheduler()
    
    # Run main cycle every 30 seconds for demo (change to 5 minutes in production)
    scheduler.add_job(
        periodic_tasks,
        trigger=IntervalTrigger(seconds=30),
        id='main_cycle',
        replace_existing=True
    )
    
    # Update today's earnings every hour
    def reset_daily_earnings():
        state.today_earned = 0.0
        state.add_log("Daily earnings reset", "INFO", "SYSTEM")
    
    scheduler.add_job(
        reset_daily_earnings,
        trigger=IntervalTrigger(hours=1),
        id='daily_reset',
        replace_existing=True
    )
    
    scheduler.start()
    state.add_log("Scheduler started - running cycles every 5 minutes", "INFO", "SYSTEM")

async def stop_agents():
    """Stop all agents and scheduler"""
    global state, scheduler
    
    state.is_running = False
    
    if scheduler:
        scheduler.shutdown(wait=False)
    
    state.add_log("All agents stopped", "INFO", "SYSTEM")

# Routes
@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Main dashboard page"""
    uptime = ""
    if state.start_time:
        delta = datetime.now() - state.start_time
        days = delta.days
        hours, remainder = divmod(int(delta.seconds), 3600)
        minutes, seconds = divmod(remainder, 60)
        uptime = f"{days}d {hours}h {minutes}m {seconds}s"
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "is_running": state.is_running,
        "uptime": uptime,
        "total_earned": state.total_earned,
        "today_earned": state.today_earned,
        "trades_executed": state.trades_executed,
        "freelance_bids": state.freelance_bids,
        "content_created": state.content_created,
        "leads_generated": state.leads_generated,
        "consecutive_loss_days": state.consecutive_loss_days,
        "max_loss_days": Config.MAX_CONSECUTIVE_LOSS_DAYS,
        "test_mode": Config.TEST_MODE,
        "logs": reversed(state.logs[-50:])  # Last 50 logs
    })

@app.get("/api/status")
async def get_status():
    """Get current agent status"""
    uptime = ""
    if state.start_time:
        delta = datetime.now() - state.start_time
        uptime = str(delta)
    
    return {
        "is_running": state.is_running,
        "uptime": uptime,
        "total_earned": state.total_earned,
        "today_earned": state.today_earned,
        "trades_executed": state.trades_executed,
        "freelance_bids": state.freelance_bids,
        "content_created": state.content_created,
        "leads_generated": state.leads_generated,
        "consecutive_loss_days": state.consecutive_loss_days,
        "test_mode": Config.TEST_MODE
    }

@app.get("/api/profit-chart")
async def get_profit_chart():
    """Generate profit chart data"""
    if not state.profit_history:
        return {"chart_html": "<p>No data yet</p>"}
    
    timestamps = [datetime.fromtimestamp(p['timestamp']) for p in state.profit_history]
    cumulative = [p['cumulative'] for p in state.profit_history]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=timestamps,
        y=cumulative,
        mode='lines+markers',
        name='Cumulative Profit',
        line=dict(color='green', width=2)
    ))
    
    fig.update_layout(
        title='Profit Over Time',
        xaxis_title='Time',
        yaxis_title='Total Profit ($)',
        hovermode='x unified',
        template='plotly_white',
        height=400
    )
    
    return {"chart_html": fig.to_html(full_html=False, include_plotlyjs='cdn')}

@app.post("/api/start")
async def start_agents_endpoint(background_tasks: BackgroundTasks):
    """Start all agents"""
    global state
    
    if state.is_running:
        return {"status": "already_running", "message": "Agents are already running"}
    
    state.is_running = True
    state.start_time = datetime.now()
    state.add_log("Agents started by user", "INFO", "SYSTEM")
    
    # Start scheduler if not running
    if not scheduler or not scheduler.running:
        background_tasks.add_task(start_scheduler)
    
    return {"status": "started", "message": "Agents started successfully"}

@app.post("/api/stop")
async def stop_agents_endpoint():
    """Stop all agents"""
    await stop_agents()
    return {"status": "stopped", "message": "Agents stopped successfully"}

@app.post("/api/withdraw")
async def withdraw_funds(amount: float = Form(...), address: str = Form(...)):
    """Request withdrawal of funds"""
    if not state.is_running:
        raise HTTPException(status_code=400, detail="Agents must be running to withdraw")
    
    if amount > state.total_earned:
        raise HTTPException(status_code=400, detail="Insufficient funds")
    
    if Config.TEST_MODE:
        state.add_log(f"TEST MODE: Would withdraw ${amount} to {address}", "INFO", "WITHDRAW")
        return {"status": "test_mode", "message": f"Test withdrawal of ${amount} to {address}"}
    else:
        # Real withdrawal logic would integrate with payment gateway
        state.add_log(f"Withdrawal requested: ${amount} to {address}", "INFO", "WITHDRAW")
        # TODO: Implement actual withdrawal via Stripe/Crypto
        return {"status": "pending", "message": "Withdrawal request submitted for processing"}

@app.post("/api/emergency-stop")
async def emergency_stop():
    """Emergency stop - immediately halt all operations"""
    global state
    state.is_running = False
    if scheduler:
        scheduler.shutdown(wait=False)
    state.add_log("EMERGENCY STOP ACTIVATED", "CRITICAL", "SYSTEM")
    return {"status": "emergency_stopped", "message": "All operations halted immediately"}

@app.get("/api/logs")
async def get_logs(limit: int = 100):
    """Get recent logs"""
    return {"logs": state.logs[-limit:]}

@app.on_event("startup")
async def startup_event():
    """Initialize on startup"""
    await initialize_agents()
    state.add_log("Server started - ready to begin", "INFO", "SYSTEM")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    await stop_agents()

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Auto-Income AI Agent - Web Server")
    print("=" * 60)
    print(f"📊 Test Mode: {'ENABLED' if Config.TEST_MODE else 'DISABLED'}")
    print(f"💰 Minimum Daily Target: ${Config.MIN_DAILY_PROFIT}")
    print(f"⚠️  Self-Terminate After: {Config.MAX_CONSECUTIVE_LOSS_DAYS} loss days")
    print("=" * 60)
    print("🌐 Access dashboard at: http://localhost:8000")
    print("📈 For production: Use ngrok or deploy to cloud")
    print("=" * 60)
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
