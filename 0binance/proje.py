import hmac
import hashlib
import time
import requests
from urllib.parse import urlencode

# ==============================================================================
# CONFIGURATION
# ==============================================================================
# The Base URL for the Binance Spot Testnet
BASE_URL = 'https://testnet.binance.vision'

# TODO: Replace these with your actual Binance Testnet API keys.
# IMPORTANT: Do NOT use your real Binance mainnet keys here!
API_KEY =  'WjOcPlGiZ5wlB6G8Y7KdoA3B2q5xGPngsqrFp1pj5i8nxHvIH7Ck78cXyAaFeipT'
SECRET_KEY = 'nkL3lgVubOov3VDc3Nc5A7G8xmeh9EfNLXmR5qCMYHPMPkoGdIVSgN0z3y2367ym'

# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================

def generate_signature(query_string, secret_key):
    """
    Generates an HMAC SHA256 signature required by Binance for private endpoints.
    """
    return hmac.new(
        secret_key.encode('utf-8'),
        query_string.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

def send_signed_request(http_method, endpoint, payload=None):
    """
    Constructs and sends a signed HTTP request to the Binance API.
    """
    if payload is None:
        payload = {}
        
    # Binance requires a timestamp in milliseconds for all secure requests
    payload['timestamp'] = int(time.time() * 1000)
    
    # URL encode the payload parameters
    query_string = urlencode(payload)
    
    # Generate the cryptographic signature
    signature = generate_signature(query_string, SECRET_KEY)
    
    # Append the signature to the query string
    url = f"{BASE_URL}{endpoint}?{query_string}&signature={signature}"
    
    # The API Key must be sent in the HTTP headers
    headers = {
        'X-MBX-APIKEY': API_KEY
    }
    
    print(f"Sending {http_method} request to {endpoint}...")
    
    # Execute the HTTP request
    try:
        if http_method == 'GET':
            response = requests.get(url, headers=headers)
        elif http_method == 'POST':
            response = requests.post(url, headers=headers)
        elif http_method == 'DELETE':
            response = requests.delete(url, headers=headers)
        else:
            raise ValueError("Unsupported HTTP method")
            
        response.raise_for_status() # Raise an exception for bad status codes
        return response.json()
        
    except requests.exceptions.RequestException as e:
        print(f"HTTP Request failed: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response content: {e.response.text}")
        return None

def send_public_request(endpoint, payload=None):
    """
    Sends an unsigned request for public data (e.g., current prices, order book).
    """
    url = f"{BASE_URL}{endpoint}"
    if payload:
        query_string = urlencode(payload)
        url = f"{url}?{query_string}"
        
    print(f"Sending public GET request to {endpoint}...")
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"HTTP Request failed: {e}")
        return None

# ==============================================================================
# MAIN EXECUTION
# ==============================================================================

def run_tests():
    """
    Runs a series of tests to verify connectivity and API functionality.
    """
    print("--- Starting Binance Testnet Script ---")
    
    # 1. Test Connectivity (Public)
    print("\n1. Pinging Server...")
    ping_result = send_public_request('/api/v3/ping')
    if ping_result == {}:
        print("Success! Connected to Binance Testnet.")

    # 2. Get Current Price of Bitcoin (Public)
    print("\n2. Fetching BTC/USDT Price...")
    ticker_result = send_public_request('/api/v3/ticker/price', {'symbol': 'BTCUSDT'})
    if ticker_result:
        print(f"Current Price: {ticker_result['price']} USDT")

    # If the user hasn't set up keys, stop here before trying private endpoints
    if API_KEY == 'YOUR_TESTNET_API_KEY_HERE':
        print("\n[!] API Keys not configured. Skipping private endpoint tests (Balances & Orders).")
        print("Please replace API_KEY and SECRET_KEY to test trading capabilities.")
        return

    # 3. Get Account Balance (Private)
    # print("\n3. Fetching Account Balances...")
    # account_info = send_signed_request('GET', '/api/v3/account')
    # if account_info:
    #     # Filter and show only balances greater than 0
    #     balances = [b for b in account_info.get('balances', []) if float(b['free']) > 0 or float(b['locked']) > 0]
    #     print("Your Non-Zero Balances:")
    #     for balance in balances:
    #         print(f"  {balance['asset']}: Free = {balance['free']}, Locked = {balance['locked']}")

    # 4. Place a Dummy Limit Order (Private)
    # WARNING: Even on testnet, ensure you understand what order you are placing.
    print("\n4. Placing a Test Limit Order (Buy BTC)...")
    order_payload = {
        'symbol': 'BTCUSDT',
        'side': 'BUY',
        'type': 'LIMIT',
        'timeInForce': 'GTC', # Good Till Cancelled
        'quantity': 0.01,     # Amount of BTC to buy
        'price': 15000.00     # Price you are willing to pay (set intentionally low so it doesn't fill immediately)
    }
    
    order_result = send_signed_request('POST', '/api/v3/order', payload=order_payload)
    if order_result:
        print("Order placed successfully!")
        print(f"Order ID: {order_result.get('orderId')}")
        print(f"Status: {order_result.get('status')}")

if __name__ == "__main__":
    run_tests()