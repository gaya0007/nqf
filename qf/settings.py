from decimal import Decimal
import os


ENVIRONMENTS = { 
    "streaming": {
        "real": "stream-fxtrade.oanda.com",
        "practice": "stream-fxpractice.oanda.com",
        "sandbox": "stream-sandbox.oanda.com"
    },
    "api": {
        "real": "api-fxtrade.oanda.com",
        "practice": "api-fxpractice.oanda.com",
        "sandbox": "api-sandbox.oanda.com"
    }
}

DATA_DIR = os.environ.get('QF_DATA_DIR', None)
OUTPUT_RESULTS_DIR = os.environ.get('QF_OUTPUT_RESULTS_DIR', None)

DOMAIN = "practice"
STREAM_DOMAIN = ENVIRONMENTS["streaming"][DOMAIN]
API_DOMAIN = ENVIRONMENTS["api"][DOMAIN]
ACCESS_TOKEN = os.environ.get('API_ACCESS_TOKEN', None)
ACCOUNT_ID = os.environ.get('API_ACCOUNT_ID', None)


BASE_CURRENCY = "USD"
EQUITY = Decimal("100000.00")
