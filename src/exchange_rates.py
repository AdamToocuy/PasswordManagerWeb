from flask import Flask, render_template, request
from get_exchange import process_exchange_dashboard

app = Flask(__name__)

# 1. ОПРЕДЕЛИТЕ СПИСОК ВАЛЮТ (замените на свои, если нужно)
RTL_CURRENCIES = ["AED", "SAR", "KWD", "OMR", "BHD", "QAR"]

@app.route("/exchange_rates.html", methods=["GET"])
def exchange_page():
    # 1. Получаем данные
    context = process_exchange_dashboard()

    # 2. Логика RTL
    is_rtl = (
        context.get("selected_base") in RTL_CURRENCIES or
        request.args.get("rtl") == "1"
    )

    # 3. Генерируем дашборд
    dashboard_data = build_rtl_dashboard(context, is_rtl)

    # 4. ЯВНО добавляем переменные в context
    context["is_rtl"] = is_rtl
    context["dashboard"] = dashboard_data 

    # 5. Вывод для отладки (посмотрите в консоли терминала, что там реально лежит)
    print("DEBUG CONTEXT KEYS:", context.keys())

    return render_template('exchange_rates.html', **context)


def build_rtl_dashboard(context, is_rtl):
    # Создаем список карточек
    cards =[
        {"title": "Текущий курс", "value": context.get("current_rate"), "color": "text-info"},
        {"title": "Максимум", "value": context.get("high_rate"), "color": "text-success"},
        {"title": "Минимум", "value": context.get("low_rate"), "color": "text-danger"},
    ]

    # Если включен RTL, просто разворачиваем порядок карточек
    if is_rtl:
        cards.reverse() 

    return {"cards": cards} # Возвращаем объект, у которого есть свойство cards

if __name__ == "__main__":
    app.run(debug=True)