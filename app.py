from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.now(timezone.utc))

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Task(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "something went wrong"
    else:
        tasks = Task.query.order_by(Task.date_created).all()
        return render_template("index.html", tasks=tasks)
    
@app.route("/delete/<int:id>")
def delete(id):
    item_to_delete = Task.query.get_or_404(id)

    try:
        db.session.delete(item_to_delete)
        db.session.commit()
        return redirect("/")
    except:
        return "a problem occured while deleting the task"
    
@app.route("/update/<int:id>", methods=['GET', 'POST'])
def update(id):
    item_to_update = Task.query.get_or_404(id)

    if request.method == 'POST':

        item_to_update.content = request.form['update']
        db.session.commit()
        return redirect("/")

    else:
        return render_template("update.html", task=item_to_update)


if __name__ == "__main__":
    app.run(debug=True)