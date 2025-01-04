from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)

# Database Model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)

# Initialize Database
with app.app_context():
    db.create_all()

# Home Route - Display tasks
@app.route("/")
def home():
    tasks = Task.query.all()
    return render_template("index.html", tasks=tasks)

# Add New Task
@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    new_task = Task(title=title, complete=False)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for("home"))

# Toggle Task Completion
@app.route("/update/<int:task_id>")
def update(task_id):
    task = Task.query.get(task_id)
    task.complete = not task.complete
    db.session.commit()
    return redirect(url_for("home"))

# Delete Task
@app.route("/delete/<int:task_id>")
def delete(task_id):
    task = Task.query.get(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)