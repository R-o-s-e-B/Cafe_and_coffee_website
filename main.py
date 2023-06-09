from flask import Flask, redirect, render_template, url_for, jsonify, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL1', "sqlite:///cafes.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

Bootstrap(app)

class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        dictionary = {column.name: getattr(self, column.name) for column in self.__table__.columns}
        return dictionary

class CafeForm(FlaskForm):
        name = StringField('Cafe name', validators=[DataRequired()])
        location = StringField('Location')
        map_url = StringField('Cafe location on Google maps', validators=[DataRequired()])
        img_url = StringField("Image url", validators=[DataRequired()])
        has_sockets = BooleanField('Sockets available?', validators=[DataRequired()])
        has_toilet = BooleanField('Toilets available?', validators=[DataRequired()])
        has_wifi = BooleanField('Wifi', validators=[DataRequired()])
        can_take_calls = BooleanField('Can take calls', validators=[DataRequired()])
        seats = StringField('Seats', validators=[DataRequired()])
        coffee_price = StringField('Coffee price', validators=[DataRequired()])
        submit = SubmitField('Submit')



@app.route('/all')
def get_all():

    cafes = db.session.query(Cafe).all()
    cafe_jsons = jsonify(cafes=[cafe.to_dict() for cafe in cafes])
    return cafe_jsons

@app.route('/')
def home():
    all_cafes = db.session.query(Cafe).all()
    return render_template('index.html', all_cafes=all_cafes)

@app.route('/add', methods=['POST', 'GET'])
def add():
    form = CafeForm()

    if request.method == 'POST':
        new_cafe = Cafe(
            name=request.form.get("name"),
            map_url=request.form.get("map_url"),
            img_url=request.form.get("img_url"),
            location=request.form.get("location"),
            has_sockets=bool(request.form.get("has_sockets")),
            has_toilet=bool(request.form.get("has_toilet")),
            has_wifi=bool(request.form.get("has_wifi")),
            can_take_calls=bool(request.form.get("can_take_calls")),
            seats=request.form.get("seats"),
            coffee_price=request.form.get("coffee_price"),
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("add.html", form=form)

@app.route('/delete')
def delete():
    cafe_id = request.args.get('id')
    cafe = db.session.query(Cafe).get(cafe_id)
    if app.secret_key == "secret_key":
        db.session.delete(cafe)
        db.session.commit()
        return redirect(url_for("home"))
    else:
        return redirect(url_for("home"))

@app.route('/view')
def view():
    cafe_id = request.args.get('id')
    cafe = db.session.query(Cafe).get(cafe_id)
    return render_template("view.html", cafe=cafe)


if __name__ == '__main__':
    app.run(debug=True)


