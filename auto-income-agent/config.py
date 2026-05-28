"""
Auto-Income AI Agent - Main Configuration
This agent runs 24/7, makes money through multiple legal channels,
and self-terminates if it fails to generate revenue.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# =============================================================================
# CORE SETTINGS
# =============================================================================

AGENT_NAME = "AutoIncome-Agent-v1"
AGENT_VERSION = "1.0.0"
RUN_MODE = "production"  # development, staging, production

# Revenue threshold: Agent terminates if revenue < this amount after N days
MIN_DAILY_REVENUE_USD = 10.0
TERMINATION_GRACE_PERIOD_DAYS = 7

# =============================================================================
# AI/LLM CONFIGURATION
# =============================================================================

# Primary AI Model (OpenAI)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = "gpt-4-turbo-preview"
OPENAI_TEMPERATURE = 0.7

# Fallback Models
USE_LOCAL_LLM = True  # Use Ollama/Llama2 if OpenAI fails
LOCAL_LLM_ENDPOINT = "http://localhost:11434/api/generate"
LOCAL_LLM_MODEL = "llama2"

# AI Behavior Settings
MAX_TOKENS_PER_RESPONSE = 2000
AI_DECISION_CONFIDENCE_THRESHOLD = 0.75  # Only act if confidence > 75%

# =============================================================================
# CRYPTO TRADING CONFIGURATION
# =============================================================================

ENABLE_CRYPTO_TRADING = True

# Exchange Configuration
SUPPORTED_EXCHANGES = [
    "binance",
    "coinbase",
    "kraken",
    "kucoin",
    "bybit",
    "okx"
]

EXCHANGE_API_KEYS = {
    "binance": {
        "api_key": os.getenv("BINANCE_API_KEY", ""),
        "secret_key": os.getenv("BINANCE_SECRET_KEY", ""),
        "testnet": True  # Start with testnet for safety
    },
    "coinbase": {
        "api_key": os.getenv("COINBASE_API_KEY", ""),
        "secret_key": os.getenv("COINBASE_SECRET_KEY", ""),
        "sandbox": True
    }
}

# Trading Safety Rules
MAX_TRADE_SIZE_USD = 100.0  # Max per trade without approval
REQUIRE_APPROVAL_ABOVE_USD = 500.0  # Require Telegram approval for larger trades
MAX_CONSECUTIVE_LOSSES = 3  # After this, switch to conservative mode
MAX_DAILY_DRAWDOWN_PERCENT = 5.0  # Stop trading if daily loss > 5%
COOLDOWN_AFTER_LOSS_MINUTES = 30  # Wait time after consecutive losses

# Profit Distribution
PROFIT_RESERVE_PERCENT = 40  # 40% to protected reserve
PROFIT_REINVEST_PERCENT = 60  # 60% back into trading pool

# Trading Pairs
DEFAULT_TRADING_PAIRS = [
    "BTC/USDT",
    "ETH/USDT",
    "BNB/USDT",
    "SOL/USDT"
]

# Technical Indicators
TRADING_INDICATORS = {
    "rsi_period": 14,
    "rsi_oversold": 30,
    "rsi_overbought": 70,
    "ma_short_period": 9,
    "ma_long_period": 21,
    "bollinger_period": 20,
    "bollinger_std": 2.0
}

# =============================================================================
# FREELANCE/AUTOMATION CONFIGURATION
# =============================================================================

ENABLE_FREELANCE_AUTOMATION = True

# Platform APIs
UPWORK_API_KEY = os.getenv("UPWORK_API_KEY", "")
FIVERR_API_KEY = os.getenv("FIVERR_API_KEY", "")
FREELANCER_API_KEY = os.getenv("FREELANCER_API_KEY", "")

# Services to Offer Automatically
AUTO_SERVICES = [
    "content_writing",
    "logo_design",
    "data_entry",
    "virtual_assistant",
    "social_media_management",
    "resume_writing",
    "canva_designs",
    "translation",
    "ai_content_editing",
    "voice_over",
    "affiliate_marketing"
]

# Pricing Strategy (USD)
SERVICE_PRICES = {
    "content_writing": {"min": 20, "max": 100, "per": "article"},
    "logo_design": {"min": 50, "max": 300, "per": "design"},
    "data_entry": {"min": 10, "max": 50, "per": "hour"},
    "virtual_assistant": {"min": 15, "max": 75, "per": "hour"},
    "social_media_management": {"min": 200, "max": 1000, "per": "month"},
    "resume_writing": {"min": 30, "max": 150, "per": "resume"},
    "canva_designs": {"min": 15, "max": 100, "per": "post"},
    "translation": {"min": 0.08, "max": 0.20, "per": "word"},
    "ai_content_editing": {"min": 25, "max": 150, "per": "project"},
    "voice_over": {"min": 30, "max": 200, "per": "minute"},
    "affiliate_marketing": {"min": 0, "max": 0, "per": "commission"}
}

# Languages Supported
SUPPORTED_LANGUAGES = ["en", "hi", "ur", "pa", "ar"]

# =============================================================================
# TELEGRAM BOT CONFIGURATION
# =============================================================================

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_ADMIN_USER_ID = os.getenv("TELEGRAM_ADMIN_USER_ID", "")

# Notification Settings
SEND_TRADE_ALERTS = True
SEND_REVENUE_REPORTS = True
SEND_ERROR_ALERTS = True
REQUIRE_TRADE_APPROVAL = True  # For trades above threshold

# =============================================================================
# PAYMENT CONFIGURATION
# =============================================================================

ENABLE_PAYMENTS = True

# Payment Gateways
STRIPE_API_KEY = os.getenv("STRIPE_API_KEY", "")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")
PAYPAL_CLIENT_ID = os.getenv("PAYPAL_CLIENT_ID", "")
PAYPAL_SECRET = os.getenv("PAYPAL_SECRET", "")

# Bank/Wallet Details (for withdrawals)
WITHDRAWAL_WALLET_ADDRESS = os.getenv("WITHDRAWAL_WALLET_ADDRESS", "")
MIN_WITHDRAWAL_AMOUNT_USD = 50.0
AUTO_WITHDRAW_THRESHOLD_USD = 500.0  # Auto-withdraw when balance exceeds this

# =============================================================================
# DATABASE CONFIGURATION
# =============================================================================

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///auto_income.db")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# =============================================================================
# SUB-AGENT CONFIGURATION
# =============================================================================

ENABLE_SUB_AGENTS = True

SUB_AGENTS = {
    "trading_agent": {
        "enabled": True,
        "strategy": "conservative",  # conservative, moderate, aggressive
        "max_positions": 3
    },
    "freelance_agent": {
        "enabled": True,
        "platforms": ["upwork", "fiverr", "freelancer"],
        "auto_bid": True,
        "max_daily_bids": 20
    },
    "content_agent": {
        "enabled": True,
        "platforms": ["youtube", "tiktok", "instagram", "medium"],
        "auto_publish": False,  # Require approval before publishing
        "content_types": ["shorts", "reels", "articles", "posts"]
    },
    "lead_gen_agent": {
        "enabled": True,
        "niches": ["immigration", "europe_jobs", "truck_driver_visa"],
        "channels": ["whatsapp", "telegram", "facebook"]
    },
    "monitoring_agent": {
        "enabled": True,
        "check_interval_seconds": 300,
        "alert_on_anomalies": True
    }
}

# =============================================================================
# SELF-HEALING & SAFETY
# =============================================================================

ENABLE_SELF_HEALING = True

# After losses, agent becomes more conservative
CONSERVATIVE_MODE_MULTIPLIER = 0.5  # Reduce trade size by 50%
MAX_GENERATION_RESTARTS = 3  # Max times to restart with new strategy

# Emergency Controls
EMERGENCY_STOP_LOSS_PERCENT = 10.0  # Stop all operations if portfolio drops 10%
AUTO_EMERGENCY_STOP = True

# =============================================================================
# LOGGING & MONITORING
# =============================================================================

LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FILE = "logs/auto_income_agent.log"
ENABLE_METRICS = True
METRICS_PORT = 9090

# =============================================================================
# SCHEDULING
# =============================================================================

# When to run different tasks
TRADING_ACTIVE_HOURS = "00:00-23:59"  # 24/7 trading
FREELANCE_BIDDING_HOURS = "09:00-18:00"  # Business hours for bidding
CONTENT_PUBLISHING_HOURS = "18:00-22:00"  # Peak engagement hours

# Report Schedule
DAILY_REPORT_TIME = "23:00"
WEEKLY_REPORT_DAY = "Sunday"
WEEKLY_REPORT_TIME = "10:00"

# =============================================================================
# LEGAL & COMPLIANCE
# =============================================================================

COMPLIANCE_MODE = "strict"  # strict, moderate, lenient
AVOID_HIGH_RISK_ACTIVITIES = True
TAX_REPORTING_ENABLED = True
KYC_REQUIRED_FOR_WITHDRAWALS = True

# Terms of Service URLs
TERMS_OF_SERVICE_URL = ""
PRIVACY_POLICY_URL = ""

# =============================================================================
# MISC
# =============================================================================

DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() == "true"
TEST_MODE = True  # Start in test mode, set to False for real operations
MAX_CONCURRENT_TASKS = 10
REQUEST_TIMEOUT_SECONDS = 30
RETRY_ATTEMPTS = 3
RETRY_DELAY_SECONDS = 5
