import requests

url = "https://solana-gateway.moralis.io/nft/mainnet/8RDo11QJ6CL5EfQeitLCRToC8xWafFKuu8HDzP2rCLWm%2F/metadata"

headers = {"accept": "application/json"}

response = requests.get(url, headers=headers)

print(response.text)