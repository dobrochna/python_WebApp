from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import statistics


app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data1.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'True'

db = SQLAlchemy(app)

class data1(db.Model):
    __tablename__ = 'data1'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    nazwa_statku = db.Column(db.String)
    bandera = db.Column(db.String)
    port_macierzysty = db.Column(db.String)
    typ_statku = db.Column(db.String)
    ocena = db.Column(db.Integer)



    def __init__(self, nazwa_statku, bandera, port_macierzysty, typ_statku, ocena):

        self.nazwa_statku = nazwa_statku
        self.bandera = bandera
        self.port_macierzysty = port_macierzysty
        self.typ_statku = typ_statku
        self.ocena = ocena


db.create_all()


@app.route("/")
def welcome():
    return render_template('welcome.html')

@app.route("/form")
def show_form():
    return render_template('form.html')

@app.route("/raw")
def show_raw():
    fd = db.session.query(data1).all()
    return render_template('raw.html', data1=fd)


@app.route("/result")
def show_result():
    fd_list = db.session.query(data1).all()

    # Some simple statistics for sample questions
    mean_ocena = []

    for el in fd_list:
        mean_ocena.append(int(el.ocena))
    if len(mean_ocena)> 0:
        mean_sat1 = statistics.mean(mean_ocena)
    else:
        mean_sat1 = 0

    # Prepare data for google charts
    data = ['Pole1', mean_sat1]

    return render_template('result.html', data=data)


@app.route("/save", methods=['POST'])
def save():
    # Get data from FORM
    nazwa_statku = request.form['nazwa_statku']
    bandera = request.form['bandera']
    port_macierzysty = request.form['port_macierzysty']
    typ_statku = request.form['typ_statku']
    ocena = request.form['ocena']

    # Save the data
    fd = data1(nazwa_statku, bandera, port_macierzysty, typ_statku, ocena)
    db.session.add(fd)
    db.session.commit()

    return redirect('/')


if __name__ == "__main__":
    app.debug = True
    app.run()