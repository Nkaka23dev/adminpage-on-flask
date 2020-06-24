from flask import Flask,url_for
from flask_sqlalchemy import SQLAlchemy 
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app=Flask(__name__)
db=SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///base.db'
app.config['SQALCHEMY_ECHO']=True
app.config['SECRET_KEY']='7b62433dacaa52ad1bdefcc79b19c935c31ac6d9089c9ef47f4f129162da0ee0'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True

class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50))
    password=db.Column(db.Unicode(100))
    units=db.Column(db.String(3))
    workout=db.relationship('Workout',backref='user',lazy='dynamic')

    def __repr__(self):
        return f"User={self.name},{self.password},{self.units})"

class Workout(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    date=db.Column(db.DateTime())
    notes=db.Column(db.Text)
    bodyweight=db.Column(db.Numeric)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    exercice=db.relationship('Exercice',backref='workout',lazy='dynamic')

    def __repr__(self):
        return f"Workout={self.date},{self.notes},{self.bodyweight}"

class Exercices(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50))
    exercice=db.relationship('Exercice',backref='exercices',lazy='dynamic')

    def __repr__(self):
        return f"Exercice={self.name}"


class Exercice(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    workout_id=db.Column(db.Integer,db.ForeignKey('workout.id'),primary_key=True)
    order=db.Column(db.Integer,primary_key=True)
    exercices_id=db.Column(db.Integer,db.ForeignKey('exercices.id'))
    sets=db.relationship('Set',backref='exercice',lazy='dynamic')

    def __repr__(self):
        return f"User={self.order}"

class ExerciceView(ModelView):
    form_columns=['id','workout','order','exercices']  


class Set(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    order=db.Column(db.Integer,primary_key=True)
    weight=db.Column(db.Numeric)
    reps=db.Column(db.Integer)
    exercice_id=db.Column(db.Integer,db.ForeignKey('exercice.id'))

    def __repr__(self):
        return f"User={self.order},{self.reps}"

class SetView(ModelView):
    form_columns=['id','order','weight','reps','exercice']
    
admin=Admin(app,template_mode='bootstrap3')  
admin.add_view(ModelView(User,db.session))
admin.add_view(ModelView(Workout,db.session)) 
admin.add_view(ModelView(Exercices,db.session)) 
admin.add_view(ExerciceView(Exercice,db.session)) 
admin.add_view(SetView(Set,db.session)) 


if __name__=='__main__':
    app.run(debug=True)