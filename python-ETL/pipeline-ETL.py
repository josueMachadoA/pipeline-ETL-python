import pandas as pd
import requests
import json
import openai


df = pd.read_csv('SDW2023.csv')
user_ids = df['UserID'].tolist()

print("Usuários extraídos:\n")

for user_id in user_ids:
    print(f"Usuário: {user_id}")

sdw2023_api_url = 'https://sdw-2023-prd.up.railway.app'

def get_user(id):
    response = requests.get(f'{sdw2023_api_url}/users/{id}')
    return response.json() if response.status_code == 200 else None

users = [user for id in user_ids if (user := get_user(id)) is not None]
print(json.dumps(users, indent=2))

openai_api_key = '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'
openai.api_key = openai_api_key

def generate_ai_news(user):
    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "Você é um especialista em investimentos"
            },
            {
                "role": "user",
                "content": f"Crie uma mensagem para {user['name']} sobre a forma mais assertiva de investir tendo um patrimônio acima de 5000 reais (máximo de 100 caracteres)"
            }
        ]
    )
    return completion.choices[0].message.content.strip('\"')


for user in users:
    user['news'] = []

for user in users:
    news = generate_ai_news(user)
    print(news)
    user['news'].append({
        "icon": "https://digitalinnovationone.github.io/santander-dev-week-2023-api/icons/credit.svg",
        "description": news
    })
    print ("\n")
def update_user(user):
  response = requests.put(f"{sdw2023_api_url}/users/{user['id']}", json=user)
  return True if response.status_code == 200 else False
for user in users:
  success = update_user(user)
  print(f"\n'O usuário {user['name']} foi atualizado? {success}!")