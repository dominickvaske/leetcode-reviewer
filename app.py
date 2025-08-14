from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#create server app
app = Flask(__name__)

#configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///leetcode_reviewer.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#initialize the database
db = SQLAlchemy(app)

#now define the Problem model for database table
class Problem(db.Model):
    id = db.Column(db.Integer, primary_key=True) #update id automatically
    number = db.Column(db.String(20), nullable=False) #string number for problem
    title = db.Column(db.String(200), nullable=False) #title of problem
    description = db.Column(db.Text) #description of problem can be very long
    difficulty = db.Column(db.Integer, nullable=False) #will be 1-5 scale
    last_reviewed = db.Column(db.Date, default=datetime.utcnow)
    times_seen = db.Column(db.Integer, default = 0)
    tags = db.Column(db.String(500)) #will hold different tags for the problem, comma separated

    def __repr__(self):
        return f'<Problem {self.number}: {self.title}>'

#here we route to homepage
@app.route('/')
def home():
    #count problems in database
    problems_count = Problem.query.count()

    #count problems that are ready for review
    review_count = 3

    return render_template('home.html',
                            problems_count=problems_count,
                            review_count = review_count)

#here we can see list of problems
@app.route('/problems')
def problems():
    #get all problems from database
    all_problems = Problem.query.all()
    return render_template('problems.html', problems=all_problems)

#adding a test problem to the database
@app.route('/add-test-data')
def add_test_data():
    #check if it already exists
    existing = Problem.query.filter_by(number="1").first()
    if existing:
        return "Problem already exists! <a href='/'>Go home</a>"

    # Create a test problem
    test_problem = Problem(
        number="1",
        title="Two Sum",
        description="Given an array of integers, return indices of two numbers that add up to target.",
        difficulty=2,
        tags="array, hash table"
    )
    
    db.session.add(test_problem)
    db.session.commit()
    
    return "Test data added! <a href='/'>Go home</a>"

#route to delete a problem from the database
@app.route('/delete_problem/<int:problem_id>')
def delete_problem(problem_id):
    problem_to_delete = Problem.query.filter_by(id=problem_id).first()
    if problem_to_delete:
        db.session.delete(problem_to_delete)
        db.session.commit()
        return "Problem deleted! <a href='/problems'>Back to problems</a>"
    else:
        return "Problem does not exist!"

#Route for showing the add_problem template
@app.route('/add_problem', methods=['GET'])
def show_add_problem():
    return render_template('add_problem.html')

#this route will process the form submission
@app.route('/add_problem', methods=['POST'])
def add_problem(): 
    #get data from form to create problem
    number = request.form['number']
    title = request.form['title']
    description = request.form['description']
    difficulty = int(request.form['difficulty'])
    tags = request.form['tags']

    new_problem = Problem (
        number = number,
        title = title,
        description = description,
        difficulty = difficulty,
        tags = tags,
        times_seen = 1 #first time seeing problem
    )

    #save new problem to database
    db.session.add(new_problem)
    db.session.commit()

    #return to problems list
    return redirect(url_for('problems'))


#now create the database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)