from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import pandas as pd

app = Flask(__name__)

# /// = relative path, //// = absolute path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)


db.create_all()


@app.get("/")
def home():
    # todo_list = Todo.query.all()
    todo_list = db.session.query(Todo).all()
    return render_template("base.html", todo_list=todo_list)


# @app.route("/add", methods=["POST"])
@app.post("/add")
def add():
    title = request.form.get("title")
    gender = request.form.get("gender_select")

    if gender == 'Male':
        gender = False
    else:
        gender = True
    
    new_todo = Todo(title=title, complete=gender)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("home"))


@app.get("/update/<int:todo_id>")
def update(todo_id):
    # todo = Todo.query.filter_by(id=todo_id).first()
    todo = db.session.query(Todo).filter(Todo.id == todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("home"))


@app.get("/delete/<int:todo_id>")
def delete(todo_id):
    # todo = Todo.query.filter_by(id=todo_id).first()
    todo = db.session.query(Todo).filter(Todo.id == todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home"))

@app.get("/search_names")
def search_names():

    return render_template("search_names.html")

@app.post("/show_table")
def show_table():
    decade = request.form.get("decade_select")
    
    if decade == '00s':
         
        decade_description = 'Top 200 Names from the 20{}'.format(decade)
        url = 'https://www.ssa.gov/oact/babynames/decades/names20{}.html'.format(decade)
    elif decade == '10s':
            
        decade_description = 'Top 200 Names from the 20{}'.format(decade)
        url = 'https://www.ssa.gov/oact/babynames/decades/names20{}.html'.format(decade)
    else:
            
        decade_description = 'Top 200 Names from the 19{}'.format(decade)
        url = 'https://www.ssa.gov/oact/babynames/decades/names19{}.html'.format(decade)
    
    # create dataframe
    df = pd.read_html(url, skiprows=1, header=0)[0]
    df = df.dropna()
    df = df.drop(df.columns[[2,4]], axis=1)
    df = df.rename(columns={'Name': 'Male Names', 'Name.1': 'Female Names'}) 
    df2 = df.to_html(index=False) 
    return render_template("search_names.html", tables=[df2], titles=df.columns.values, decade_description=decade_description)

#if __name__ == '__main__':
#    app.run(host='0.0.0.0')
