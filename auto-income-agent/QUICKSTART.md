# Auto-Income AI Agent - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Install Dependencies

```bash
cd /workspace/auto-income-agent

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

### Step 2: Configure Environment

```bash
# Copy the template
cp .env.example .env

# Edit with your keys (use nano, vim, or any editor)
nano .env
```

**Minimum Required Keys to Start:**
- `TELEGRAM_BOT_TOKEN` - For notifications
- `TELEGRAM_ADMIN_USER_ID` - Your Telegram ID
- Keep `TEST_MODE=True` for safe testing

### Step 3: Create Telegram Bot

1. Open Telegram and search for `@BotFather`
2. Send `/newbot` command
3. Follow instructions to create bot
4. Copy the token to `.env` as `TELEGRAM_BOT_TOKEN`
5. Search for `@userinfobot` to get your User ID
6. Add it to `.env` as `TELEGRAM_ADMIN_USER_ID`

### Step 4: Run in Test Mode

```bash
# Make sure you're in the virtual environment
source venv/bin/activate

# Run the agent
python main.py
```

You should see output like:
```
══════════════════════════════════════
Starting AutoIncome-Agent-v1
══════════════════════════════════════
[INFO] Initializing orchestrator...
[INFO] Trading agent initialized
[INFO] Freelance agent initialized
[INFO] Orchestrator initialized with 2 agents
[INFO] Starting all agents...
[INFO] All agents started successfully
[INFO] AutoIncome-Agent-v1 is now running 24/7...
[INFO] Minimum daily revenue target: $10.0
[INFO] Termination grace period: 7 days
```

### Step 5: Monitor Dashboard

Open another terminal and check status:

```bash
# View logs
tail -f logs/auto_income_agent.log

# Or check if process is running
ps aux | grep main.py
```

## 📱 Telegram Commands

Once running, message your bot:

- `/start` - Initialize bot
- `/status` - Check revenue and agent status
- `/help` - Show available commands

## ⚙️ Basic Configuration

Edit `config.py` to customize:

```python
# Change minimum revenue threshold
MIN_DAILY_REVENUE_USD = 10.0  # Your target

# Change grace period
TERMINATION_GRACE_PERIOD_DAYS = 7  # Days before self-terminate

# Enable/disable specific agents
SUB_AGENTS = {
    "trading_agent": {"enabled": True},   # Crypto trading
    "freelance_agent": {"enabled": True}, # Upwork/Fiverr
    "content_agent": {"enabled": False},  # YouTube/TikTok
    "lead_gen_agent": {"enabled": True}   # Immigration leads
}
```

## 💡 First Steps for Revenue

### Option 1: Freelance Automation (Recommended for Beginners)

1. Get Upwork API key from https://www.upwork.com/developers
2. Add to `.env`:
   ```
   UPWORK_API_KEY=your_key
   UPWORK_API_SECRET=your_secret
   ```
3. Agent will start auto-bidding on relevant jobs

### Option 2: Crypto Trading (Requires Capital)

**⚠️ Start with testnet only!**

1. Create Binance testnet account: https://testnet.binance.vision
2. Get API keys
3. Add to `.env`:
   ```
   BINANCE_API_KEY=your_testnet_key
   BINANCE_SECRET_KEY=your_testnet_secret
   ```
4. Agent will trade with fake money first

### Option 3: Lead Generation (Your Specialty)

Since you do immigration consulting:

1. Set up WhatsApp Business API
2. Create lead capture form
3. Agent qualifies leads automatically
4. Book seminars via AI

## 🔒 Safety Checklist

Before going live:

- [ ] Running in TEST_MODE initially
- [ ] Using testnet/sandbox for exchanges
- [ ] Set conservative trade limits ($100 max)
- [ ] Telegram alerts working
- [ ] Emergency stop tested
- [ ] Reviewed legal requirements for UAE

## 🛑 Stopping the Agent

```bash
# Graceful shutdown
# Press Ctrl+C in the terminal running main.py

# Or send SIGTERM
kill <PID>

# Check it stopped
ps aux | grep main.py
```

## 📊 Checking Performance

```python
# Python script to check stats
import sqlite3
conn = sqlite3.connect('auto_income.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM revenue_log ORDER BY timestamp DESC LIMIT 10")
for row in cursor.fetchall():
    print(row)
conn.close()
```

## 🆘 Troubleshooting

### "Module not found" errors
```bash
pip install -r requirements.txt --upgrade
```

### "API key invalid"
- Double-check keys in `.env`
- Ensure no extra spaces
- Verify API keys have correct permissions

### Agent won't start
```bash
# Check Python version (need 3.9+)
python --version

# Check logs
cat logs/auto_income_agent.log | tail -50
```

### No revenue showing
- Ensure TEST_MODE=False for real operations
- Verify API credentials
- Check that services are actually running
- Review bid/proposal quality

## 📈 Next Steps

1. **Week 1**: Run in test mode, monitor behavior
2. **Week 2**: Add real freelance platform APIs
3. **Week 3**: Start small crypto trades (testnet → real)
4. **Week 4**: Scale up, add more revenue streams

## 🎯 Success Metrics

Track these weekly:

| Metric | Target | Actual |
|--------|--------|--------|
| Daily Revenue | >$10 | $___ |
| Active Proposals | >20 | ___ |
| Win Rate | >10% | ___% |
| Trading PnL | Positive | $___ |
| Uptime | 99% | ___% |

## 📞 Getting Help

1. Check README.md for detailed docs
2. Review logs in `logs/` directory
3. Test in sandbox mode first
4. Consult UAE business regulations

---

**Remember**: Start small, test thoroughly, scale gradually! 🚀
