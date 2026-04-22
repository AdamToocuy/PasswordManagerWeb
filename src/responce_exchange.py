import requests
from datetime import datetime

def get_rate():
    user_input = input("Введите дату (ДД.ММ.ГГГГ): ")
    
    try:
        # Парсим дату
        dt = datetime.strptime(user_input, "%d.%m.%Y")
        
        # Разбиваем URL на части, чтобы ничего не слиплось
        base_url = "https://cbr-xml-daily.ru"
        path = f"/archive/{dt.year}/{dt.month:02d}/{dt.day:02d}/daily_json.js"
        full_url = base_url + path
        
        print(f"Запрос к: {full_url}") # Это поможет вам увидеть итоговый URL
        
        response = requests.get(full_url)
        
        if response.status_code == 404:
            print("Ошибка 404: Данных на эту дату нет в архиве (попробуйте будний день).")
            return
            
        data = response.json()
        usd_val = data['Valute']['USD']['Value']
        print(f"Курс доллара на {user_input}: {usd_val} руб.")
        
    except ValueError:
        print("Ошибка: Неверный формат даты.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

get_rate()
