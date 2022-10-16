import requests

url = "https://solana-gateway.moralis.io/nft/mainnet/Ek64ZYUJ8oaDwSAhumzP8VzXyaE1ZW2xfcaufDXHyCY4/metadata"

headers = {
    "accept": "application/json",
    "X-API-Key": "F5GCxxgXhLDTENlIDl8RHLBva7jXUC0SQuyrIV8jL1LJ8H9ZznttU81G50Rrhwqq"
}

response = requests.get(url, headers=headers)
payload = response.json()
uri = payload["symbol"]
print(response.text)
print(uri)