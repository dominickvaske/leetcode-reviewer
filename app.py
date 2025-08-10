from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html',
                            problems_count=15,
                            review_count = 3)

@app.route('/problems')
def problems():
    return render_template('problems.html')


if __name__ == '__main__':
    app.run(debug=True)