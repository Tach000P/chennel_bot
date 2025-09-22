import requests
from google import genai
from google.genai import types
from rules import rules

cookies = {"auth_key":"YxDxc4DVW5P%2BUJ%2Fly137XgxIAx9pKZd2m3Re%2BtspieUjWfPn%2FKcSdRmunFhMCxMU","beget":"begetok","device_id":"0f3714b36a0da8298ec4eac27dfd623f","first_id":"8724","PHPSESSID":"5d250a9f303b6185cfbf1cdd29ff0120"}

session = requests.Session()
session.cookies.update(cookies)

client = genai.Client(api_key="AIzaSyCSHFDlTezabN7YpmPT8JSdQdEdJnzDDP0")

config = types.GenerateContentConfig(
    system_instruction=rules
)

news = requests.get('https://newsapi.org/v2/top-headlines?category=technology&apiKey=554059aada744635b683ff2c9118e151').json()['articles']

output = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=f"{news}",
                    config=config,
                )

"""Отправляем сообщение"""
url = "https://nolvoprosov.ru/functions/ajaxes/messages/act.php"
payload = {
    "rs[parent_id]": str(332),
    "rs[group]": "message",
    "rs[type]": "group_message",
    "rs[mode]": "add",
    "rs[plan]": "simple",
    "text": f"<p>{output.text}</p>",
}
r = session.post(url, data=payload)
r.raise_for_status()
print(r.text)