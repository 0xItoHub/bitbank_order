import requests
import time
import hashlib
import hmac
import json

# APIキーとシークレットキー
API_KEY = 'あなたのAPIキー'
API_SECRET = 'あなたのシークレットキー'

# URL
BASE_URL = 'https://api.bitbank.cc/v1/'

# ヘッダー作成関数
def create_headers(api_key, api_secret, method, endpoint, params):
    nonce = str(int(time.time() * 1000))
    body = json.dumps(params) if params else ''
    data = nonce + body
    sign = hmac.new(api_secret.encode(), data.encode(), hashlib.sha256).hexdigest()

    headers = {
        'ACCESS-KEY': api_key,
        'ACCESS-NONCE': nonce,
        'ACCESS-SIGNATURE': sign,
        'Content-Type': 'application/json'
    }
    return headers

# 指値注文関数
def place_order(pair, price, amount, side):
    endpoint = 'user/spot/order'
    url = BASE_URL + endpoint
    method = 'POST'
    
    # 注文内容
    params = {
        'pair': pair,        # 通貨ペア（例: 'btc_jpy'）
        'price': str(price), # 指値の価格
        'amount': str(amount),# 注文数量
        'side': side,        # 'buy' か 'sell'
        'type': 'limit'      # 指値注文は 'limit'
    }
    
    headers = create_headers(API_KEY, API_SECRET, method, endpoint, params)
    
    # リクエストを送信
    response = requests.post(url, headers=headers, data=json.dumps(params))
    
    # レスポンスの確認
    if response.status_code == 200:
        return response.json()
    else:
        return response.text

# 指値注文の実行
pair = 'btc_jpy'   # 通貨ペア
price = 3000000    # 指値価格（例: 300万円）
amount = 0.01      # 注文数量
side = 'buy'       # 'buy' か 'sell'

order_result = place_order(pair, price, amount, side)
print(order_result)
