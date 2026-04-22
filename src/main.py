from flask import Flask, render_template

app = Flask(__name__, template_folder="../templates")


@app.route('/')
def index():
    items = ['Яблоко', 'Банан', 'Апельсин', 'Груша']
    return render_template('index.html', items=items) 

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')