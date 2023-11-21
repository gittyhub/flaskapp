from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__) #setup the application, name is reference the app.py file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' #3 / is a realive path, 4/ is an absolute path
db = SQLAlchemy(app) #initialze the sql database. Database is being initialize with the setting from the app

class Todo(db.Model):  #Creating a model? The class here is Todo. What do you want this class to have, id, content, date that will be
                       #stored in the SQLAlchemy database
  '''If you are having trouble with db creation, try the following'''
  '''from app import app,db'''
  '''app.app_context().push()'''
  '''db.create_all()'''
  '''check the instance folder'''

  id = db.Column(db.Integer, primary_key=True) #just creating columns
  content =db.Column(db.String(200), nullable=False) #content specifies what content is, can not be blank, 
  date_created = db.Column(db.DateTime, default=datetime.utcnow)

  def __repr__(self):  #return string a everytime a new element created
    return '<Fuck_shit %r>' % self.id #the sting is fuck_shit with id that was created


#index route so you dont 404 when you get to the page
#to create a route, you use the @ rout decorator
@app.route('/', methods=['POST', 'GET']) #passing the URL string of your rout.This is our decorator. After rout, we add a method option, so we can do post and get. Send data to database

def index():  #define function for that rout
  if request.method == 'POST':  # if request is post then do this
    task_content = request.form['content']  #the app is referencing the index page with /, the method allowed is post and get. If it gets a post mothod
                                            #from the index.html, which we created in the form with method post, then set the variable to the forms content
                                            #which is the name="content"
    new_task = Todo(content=task_content)   #From the todo model above create this Todo() object assign the content object in the Todo class to task_content
    
    try:
      db.session.add(new_task)             #here we are adding the content of the new_task to our database
      db.session.commit()
      return redirect('/')                    #redirect to the index page 
    except:
      return 'There was an issue adding your task'
  else:
    task = Todo.query.order_by(Todo.date_created).all() # This will look at the database content, order them, and return all
    return render_template('index.html', tasks=task) #no need file name, flask knows to used the template file when using render

#app to delete so we need to set up a new rout
@app.route('/delete/<int:id>')  #this is the id of the content id with primary key
def delete(id):
  task_to_delete = Todo.query.get_or_404(id)

  try:
    db.session.delete(task_to_delete) 
    db.session.commit()
    return redirect('/')
  except:
    return 'There was a problem deleting that task'


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'
    else:
      return render_template('update.html', task=task)

if __name__ == "__main__":
  app.run(debug=True)


