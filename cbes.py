import os
import requests 

from flask import Flask, render_template, request, session, jsonify
from flask_session import Session
from models import *

#from werkzeug.middleware.proxy_fix import ProxyFix
#from cachelib.file import FileSystemCache

#from sqlalchemy import create_engine
#from sqlalchemy.orm import scoped_session, sessionmaker


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] ="postgres://kangmdwnpbhacg:4cef3069b1ef7e56ddf11bc0ff11fab84bdf3072d00363ac87a341d576aad503@ec2-54-228-250-82.eu-west-1.compute.amazonaws.com:5432/dcbv6m7ump5frb"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
#engine = create_engine('postgres://kangmdwnpbhacg:4cef3069b1ef7e56ddf11bc0ff11fab84bdf3072d00363ac87a341d576aad503@ec2-54-228-250-82.eu-west-1.compute.amazonaws.com:5432/dcbv6m7ump5frb')
#db = scoped_session(sessionmaker(bind=engine))
db.init_app(app)





        
@app.route("/registration")
def registration():
    return render_template("Registration.html")

@app.route("/registeruser", methods=['POST'])
def registeruser():
    if request.method == 'POST':
        first_name = request.form['FirstName']
        last_name = request.form['LastName']
        email_id = request.form['EmailID']
        password = request.form['Password']
        user = Registration.query.filter_by(email_id=email_id).count()
        if user == 0:
            user = Registration(first_name=first_name, last_name=last_name, email_id=email_id, password=password)
            db.session.add(user)
            db.session.commit()
            return render_template("Login.html")
        else:
            return render_template("Registration.html" , Message="EMAILID ALREADY REGISTERED!")
        

@app.route("/")
def index():
    if session.get("user_id") is None:
        return render_template('Login.html')
    else:
        user_id = session["user_id"]
        books = Book.query.all()
        return render_template("Index.html", books=books, user_id=user_id)

@app.route("/login")
def login():
    return render_template('Login.html')

@app.route("/logout")
def logout():
    session.clear()
    return render_template('Login.html')


@app.route("/book_review/<int:book_id>", methods=['POST'] )
def book_review(book_id):
    if session.get("user_id") is None:
        return render_template('Login.html')
    else:
        books = Book.query.get(book_id)
        if request.method == 'POST':
            rating = request.form['rating']
            reviewtext = request.form['reviewtext']
            user_id = session.get("user_id")
            review = Review(user_id=user_id, book_id=book_id, reviewtext=reviewtext, rating=rating)
            db.session.add(review)
            db.session.commit()
            return book_info(book_id)
        else:
            return render_template("Bookpage.html", books=books)

@app.route("/book_info/<int:book_id>")
def book_info(book_id):
    key = "eIKtxbPEzxNsBJ4wM4wKQ"
    if session.get("user_id") is None:
        return render_template('Login.html')
    else:
        books = Book.query.get(book_id)
        if books is None:
            return jsonify({"error": "Invalid book_id"}),422
        
        reviews = Review.query.filter(book_id==book_id).all()
        users = Registration.query.all()
        res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": key, "isbns":books.isbn})
        resource = res.json()
        averagerating = resource['books'][0]['average_rating']
        averagerating = 20 * float(averagerating)
        return render_template("Bookpage.html", books=books, reviews=reviews, users=users, resource=resource, averagerating=averagerating)
    
    
@app.route("/api/<isbn>")
def book_api(isbn):
    key = "eIKtxbPEzxNsBJ4wM4wKQ"
    if session.get("user_id") is None:
        return render_template('Login.html')
    else:
        books = Book.query.filter(Book.isbn == isbn).all()
        if books is None:
            return jsonify({"error": "Invalid Isbn Number"}),422
        else:
        
            for book in books:
                title = book.title
                author = book.author
                isbn = book.isbn
                year = book.year


            res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": key, "isbns":isbn})
            if res.status_code != 200:
                raise Exception("Error: API request unsuccessful.")
            resource = res.json()
            return jsonify({
                "title": title,
                "author": author,
                "year": year,
                "isbn": isbn,
                "review_count": resource['books'][0]['ratings_count'],
                "average_score": resource['books'][0]['average_rating']
            })
        
@app.route("/loginuser", methods=['POST'])
def loginuser():
    if request.method == 'POST':
        email_id = request.form['EmailID']
        password = request.form['Password']
        user = Registration.query.filter_by(email_id=email_id, password=password).count()
        if user == 0:
            return render_template("Login.html", Message = "Invalid Email Id or Password!")
        else:
            users = Registration.query.filter_by(email_id=email_id, password=password).all()
            for user in users:
                session["user_id"] = user.id
            return index()
        

@app.route("/search", methods=['POST'])
def search():
    if request.method == 'POST':
        Searchtext = request.form['searchtext']
        books =  Book.query.filter(Book.isbn.like("%"+Searchtext+"%") | Book.title.like("%"+Searchtext+"%") | Book.author.like("%"+Searchtext+"%")).count()
        if books == 0:
            return render_template("error.html", Message = "SEACH DATA NOT FOUND!")
        else:
            books = Book.query.filter(Book.isbn.like("%"+Searchtext+"%") | Book.title.like("%"+Searchtext+"%") | Book.author.like("%"+Searchtext+"%")).all();
            return render_template("search.html", books=books)
    
        
if __name__ == '__main__':
    with app.app_context():
        app.debug = True
        app.run()