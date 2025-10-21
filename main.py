import requests, os, json, random
from google import genai
from google.genai import types
from rules import rules
from datetime import datetime

cookies = {"auth_key":"YxDxc4DVW5P%2BUJ%2Fly137XgxIAx9pKZd2m3Re%2BtspieUjWfPn%2FKcSdRmunFhMCxMU","beget":"begetok","device_id":"0f3714b36a0da8298ec4eac27dfd623f","first_id":"8724","PHPSESSID":"5d250a9f303b6185cfbf1cdd29ff0120"}

session = requests.Session()
session.cookies.update(cookies)

if os.path.exists("db.json"):
    with open("db.json", "r", encoding="utf-8") as f:
        db = json.load(f)
else:
    db = []

def save_db():
    with open("db.json", "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)


def download_image(image_url):

    response = requests.get(image_url)

    with open('image.jpg', 'wb') as file:
        file.write(response.content)

def upload_image (image_url):
    """Загружает изображение на сервер и возвращает URL"""
    download_image(image_url)

    image_path = "image.jpg"

    # URL для загрузки
    url = "https://nolvoprosov.ru/functions/ajaxes/uploads/upload_files.php?method=device&type=image"

    try:
        # Открываем файл для загрузки
        with  open(image_path, 'rb') as file:
            files = {
                'file-0': (os.path.basename(image_path), file, 'image/jpg')
            }
            
            # Отправляем POST запрос
            response = session.post(
                url,
                cookies=cookies,
                files=files
            )
            if response.status_code == 200:
                result = response.json()
           

                if result["3"] is True and 'data' in result:
                    image_data = result['data'][0]
                    return image_data
                else:
                    return image_url
            
            else:
                print(f"HTTP ошибка: {response.status_code}")
                return None

    except Exception as e:
        print(f"Ошибка при загрузке: {e}")
        return None

def main():
    session = requests.Session()
    session.cookies.update(cookies)

    client = genai.Client(api_key="AIzaSyCSHFDlTezabN7YpmPT8JSdQdEdJnzDDP0")

    config = types.GenerateContentConfig(
        system_instruction=rules
    )
    
    def get_news():

        news = requests.get('https://newsapi.org/v2/top-headlines?category=technology&pageSize=100&apiKey=554059aada744635b683ff2c9118e151').json()['articles'][random.randint(0,99)]

        if news["url"] in db:
            return get_news()
        else:
            db.append(news["url"])
            save_db()
            image = upload_image(news["urlToImage"])
            news["urlToImage"] = image
            return news

    news = get_news()
    output = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=f"Новости:{news} НИ В КОЕМ СЛУЧАЕ НЕ ВЫБИРАТЬ КАКОЙ-ТО НОВОСТЬ СВЯЗАННЫЙ С: ",
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

    print(f"✅ Сообщение отправлено успешно в {datetime.now().strftime('%H:%M:%S')}")
    print(f"📰 Получено новостей: {len(news)}")

if __name__ == "__main__":
    main()