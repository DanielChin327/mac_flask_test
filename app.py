from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

# MySQL Database Connection Configuration for XAMPP
app.config['SQLALCHEMY_DATABASE_URI'] = 'mariadb+pymysql://root:@localhost:3306/mac_test_flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Database Model
class Quote(db.Model):
    quote_id = db.Column(db.Integer, primary_key=True)
    person = db.Column(db.String(50))
    quote = db.Column(db.String(255))

# Initialize the Database (Run only once to create the tables)
with app.app_context():
    db.create_all()

# Home Route - Display tasks
@app.route('/')
def testing():
    return "Flask Routes are Working. "

@app.route('/quotes', methods=['GET'])
def get_quotes():
    quotes = Quote.query.all()
    #converts to json format
    quotes_list = [{"quote_id": q.quote_id, "person": q.person, "quote": q.quote} for q in quotes]
    return jsonify(quotes_list)


if __name__ == "__main__":
    app.run(debug=True)