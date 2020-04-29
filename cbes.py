from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = ''
    
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://tklkvrkxsgwyxr:ab086afcf8bb885d414f0d381eaba3254a21a6ecd9640636798c670a1881e0cd@ec2-54-217-204-34.eu-west-1.compute.amazonaws.com:5432/dbk8u87rgr937q'
    

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route("/")
def registration():
    return render_template("Registration.html")

@app.route("/registrationdata", methods=['POST'])
def registrationdata():
    if request.method == 'POST':
        FirstName = request.form['FirstName']
        LastName = request.form['LastName']
        EmailID = request.form['EmailID']
        Password = request.form['Password']
        if FirstName == '' or EmailID == '' or Password == '':
            return render_template ("Registration.html", Message = 'Please Enter Required Fields')
        return render_template("Login.html")


if __name__ == '__main__':
    
    app.run()