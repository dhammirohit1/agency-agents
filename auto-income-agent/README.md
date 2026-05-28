# Auto-Income AI Agent

A fully autonomous AI agent system that runs 24/7, generates revenue through multiple legal channels (crypto trading, freelancing, content creation), and **self-terminates if it fails to meet minimum revenue targets**.

## ⚠️ Important Disclaimers

- **This is a framework for educational purposes**. Real money-making requires:
  - Actual API keys for exchanges, freelance platforms, payment processors
  - Legal compliance with your jurisdiction (UAE regulations, tax laws)
  - Human oversight for critical decisions
  - Starting capital for trading activities
  
- **Crypto trading involves significant risk**. Never trade more than you can afford to lose.

- **Self-termination feature**: The agent will automatically shut down if it fails to generate minimum revenue ($10/day by default) for 7 consecutive days.

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Main Orchestrator                       │
│  • Revenue Monitoring                                    │
│  • Self-Termination Logic                                │
│  • Health Checks                                         │
└──────────────┬──────────────────────────────────────────┘
               │
    ┌──────────┼──────────┬──────────┬──────────┐
    │          │          │          │          │
┌───▼───┐  ┌───▼───┐  ┌───▼───┐  ┌───▼───┐  ┌──▼──┐
│Trading│  │Freelance│  │Content│  │Lead Gen│  │Monitor│
│ Agent │  │ Agent  │  │ Agent │  │ Agent  │  │Agent │
└───────┘  └───────┘  └───────┘  └───────┘  └──────┘
```

## 📋 Features

### Core Capabilities
- ✅ **24/7 Autonomous Operation**
- ✅ **Multi-Agent System** (Trading, Freelancing, Content, Lead Generation)
- ✅ **Revenue-Based Self-Termination**
- ✅ **Safety Controls** (Trade limits, approval workflows, drawdown protection)
- ✅ **Self-Healing** (Becomes more conservative after losses)
- ✅ **Telegram Integration** (Alerts, approval buttons, emergency stop)
- ✅ **Multi-Exchange Crypto Trading** (Binance, Coinbase, Kraken, etc.)
- ✅ **Freelance Platform Automation** (Upwork, Fiverr, Freelancer)
- ✅ **Payment Processing** (Stripe, PayPal, Crypto withdrawals)

### Safety & Compliance
- 🔒 Maximum trade size limits
- 🔒 Daily drawdown protection (default: 5%)
- 🔒 Consecutive loss tracking
- 🔒 Telegram approval for large trades (> $500)
- 🔒 Protected reserve (40% of profits)
- 🔒 Strict compliance mode (avoids high-risk activities)
- 🔒 Tax reporting enabled

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- API keys for services you want to use
- Initial capital for trading (optional, start small)

### Installation

```bash
# Clone or navigate to the project directory
cd /workspace/auto-income-agent

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Edit .env and add your API keys
nano .env
```

### Configuration

Edit `config.py` to customize:

```python
# Revenue thresholds
MIN_DAILY_REVENUE_USD = 10.0  # Minimum daily revenue
TERMINATION_GRACE_PERIOD_DAYS = 7  # Days before self-termination

# Trading settings
MAX_TRADE_SIZE_USD = 100.0
REQUIRE_APPROVAL_ABOVE_USD = 500.0
MAX_CONSECUTIVE_LOSSES = 3
MAX_DAILY_DRAWDOWN_PERCENT = 5.0

# Enable/disable agents
SUB_AGENTS = {
    "trading_agent": {"enabled": True},
    "freelance_agent": {"enabled": True},
    "content_agent": {"enabled": False},
    "lead_gen_agent": {"enabled": True}
}
```

### Environment Variables (.env)

```bash
# AI/LLM
OPENAI_API_KEY=sk-your-key-here

# Crypto Exchanges (start with testnet/sandbox!)
BINANCE_API_KEY=your_binance_key
BINANCE_SECRET_KEY=your_binance_secret
COINBASE_API_KEY=your_coinbase_key
COINBASE_SECRET_KEY=your_coinbase_secret

# Freelance Platforms
UPWORK_API_KEY=your_upwork_key
FIVERR_API_KEY=your_fiverr_key

# Telegram Bot
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_ADMIN_USER_ID=your_user_id

# Payment Gateways
STRIPE_API_KEY=sk_test_your_key
PAYPAL_CLIENT_ID=your_paypal_client
PAYPAL_SECRET=your_paypal_secret

# Database
DATABASE_URL=sqlite:///auto_income.db
REDIS_URL=redis://localhost:6379/0

# Mode
DEBUG_MODE=False
TEST_MODE=True  # Start in test mode!
```

### Running the Agent

```bash
# Test mode (recommended first)
python main.py

# Production mode (set TEST_MODE=False in config.py)
python main.py
```

### Dashboard Access

Once running, access the web dashboard at:
```
http://localhost:8000/dashboard
```

## 💰 Revenue Streams

### 1. Crypto Trading (Automated)
- Executes small trades based on technical indicators (RSI, MA, Bollinger Bands)
- Supports 100+ exchanges via CCXT
- Profit split: 40% reserve, 60% reinvested
- Safety: Max $100/trade without approval, 5% daily drawdown limit

### 2. Freelance Automation
- Auto-bids on Upwork, Fiverr, Freelancer
- Services: Writing, design, VA, data entry, AI editing
- AI-generated proposals
- Max 20 bids/day to avoid spam

### 3. Content Creation (Optional)
- YouTube Shorts (faceless)
- TikTok/Instagram Reels
- Medium articles
- Pinterest affiliate posts

### 4. Lead Generation
- Immigration consulting leads (your specialty)
- Europe job visa inquiries
- WhatsApp/Telegram community building
- Affiliate partnerships

## 🛡️ Safety Mechanisms

### Trading Safety
| Rule | Limit | Action |
|------|-------|--------|
| Max Trade Size | $100 | Auto-execute |
| Large Trades | >$500 | Require Telegram approval |
| Consecutive Losses | 3 | Switch to conservative mode |
| Daily Drawdown | 5% | Stop trading for the day |
| Emergency Stop | 10% portfolio loss | Halt all operations |

### Self-Healing
After losses, the agent:
1. Reduces trade size by 50%
2. Switches to conservative strategy
3. Increases confidence threshold for trades
4. After 3 generations, requests termination

### Self-Termination Sequence
If revenue < $10/day for 7 consecutive days:
1. Logs critical warning
2. Stops all sub-agents
3. Generates final report
4. Sends Telegram notification
5. Exits process (`os._exit(1)`)

## 📊 Monitoring

### Telegram Commands
- `/status` - Current revenue and agent status
- `/approve` - Approve pending trades
- `/stop` - Emergency stop all agents
- `/withdraw` - Initiate withdrawal
- `/report` - Daily/weekly revenue report

### Dashboard Metrics
- Real-time revenue tracking
- Agent health status
- Active positions/proposals
- Historical performance charts
- Withdrawal history

## ⚖️ Legal Compliance (UAE Specific)

### Required for UAE Residents
1. **Business License**: Free zone license recommended (e.g., DMCC, SHAMS)
2. **Tax Registration**: VAT registration if revenue > AED 375,000/year
3. **Crypto Regulations**: Follow VARA (Virtual Assets Regulatory Authority) guidelines
4. **Payment Gateway**: Use UAE-approved gateways (Stripe UAE, PayTabs, Telr)

### Avoid These (Illegal/Scams)
❌ "Pay first to earn" schemes  
❌ Fake crypto mining apps  
❌ Pyramid/MLM schemes  
❌ Guaranteed trading bots  
❌ Unlicensed investment advice  

## 🔧 Customization

### Adding New Agents
```python
# agents/my_new_agent.py
from agents.base_agent import BaseAgent

class MyNewAgent(BaseAgent):
    async def start(self) -> bool:
        # Your implementation
        pass
    
    async def generate_revenue(self) -> float:
        # Revenue logic
        pass

# Add to config.py
SUB_AGENTS["my_new_agent"] = {"enabled": True}

# Register in main.py
from agents.my_new_agent import MyNewAgent
```

### Custom Trading Strategies
Modify `agents/trading_agent.py`:
```python
async def _analyze_market(self, symbol: str):
    # Add your custom indicators
    # Example: MACD, Stochastic, Ichimoku
    pass
```

## 📈 Expected Performance

### Conservative Estimates (Test Mode)
| Stream | Daily Revenue | Monthly |
|--------|--------------|---------|
| Crypto Trading | $5-20 | $150-600 |
| Freelance | $10-50 | $300-1500 |
| Content/Affiliate | $0-30 | $0-900 |
| **Total** | **$15-100** | **$450-3000** |

**Note**: These are estimates. Actual results vary based on:
- Market conditions
- Your effort in setup
- Capital deployed
- Competition

## 🆘 Troubleshooting

### Common Issues

**Agent won't start:**
```bash
# Check logs
tail -f logs/auto_income_agent.log

# Verify API keys
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('BINANCE_API_KEY'))"
```

**No revenue generated:**
- Ensure TEST_MODE=False for real operations
- Verify API keys have correct permissions
- Check minimum capital requirements
- Review bid/proposal quality

**Trading errors:**
- Start with testnet/sandbox mode
- Reduce trade sizes
- Check exchange rate limits
- Review API key permissions

## 📚 Resources

### Documentation
- [CCXT Exchange List](https://docs.ccxt.com/)
- [OpenAI API Docs](https://platform.openai.com/docs)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Stripe Integration](https://stripe.com/docs)

### Learning
- Technical analysis basics (Investopedia)
- Freelance platform best practices
- UAE business setup guides

## 🤝 Support

For issues, questions, or contributions:
1. Check existing issues in repository
2. Review logs in `logs/` directory
3. Test in sandbox/testnet mode first

## 📝 License

MIT License - Educational purposes only. Use at your own risk.

---

**⚠️ Final Warning**: This system can lose money. Only deploy capital you can afford to lose. Start in test mode. Monitor regularly. Consult legal/tax professionals in your jurisdiction.

**Good luck! 🚀**
