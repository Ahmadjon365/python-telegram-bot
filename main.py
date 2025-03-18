# Tasvirnoma: Bu oddiy telegram bot uchun skript.
import requests

teken = "YOUR_BOT_TOKEN"
method = "sendMessage"
response = requests.get(
    f'https://api.telegram.org/bot{teken}/{method}',
    {'chat_id': 00000000, 'text': 'Assalomu aleykum va rohmatullohi va barokatuh, Ahmadjon qondesan?'}
)

print(response)
