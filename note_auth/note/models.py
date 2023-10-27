# models are the schema of the table of the database

# from this folder/package import db
from . import db
# this is a custom class
from flask_login import UserMixin
# func wil allow us to determine the date and time when the user add the note
from sqlalchemy.sql import func


# UserMixin is used to get all the information of the current_user in the flask_login module
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    firstName = db.Column(db.String(150))
    
    # this field will make a list of all the user notes and we always refere the other class with the capital letter Note
    notes = db.relationship('Note')
    
    def __repr__(self):
        return f"User('{self.firstName}', '{self.email}', '{self.id}')"


   
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    
    # user_id = owner which is a foreign key for User class and we always specify it with lower letter to refere to its 'user.id' = User.id
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __repr__(self):
        return f"User('{self.content}', '{self.id}')"