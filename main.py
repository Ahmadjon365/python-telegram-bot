# Tasvirnoma: Bu oddiy telegram bot uchun skript.
import requests

teken = "7688427772:AAEQTKMp3DqIEizhN5fvqBbsGd7oPI8Jjmg"
method = "sendMessage"
response = requests.get(
    f'https://api.telegram.org/bot{teken}/{method}',
    {'chat_id': 92091371, 'text': 'Assalomu aleykum va rohmatullohi va barokatuh, Ahmadjon qondesan?'}
)

print(response)
