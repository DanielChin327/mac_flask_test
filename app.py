from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)

# Database Configuration for MariaDB (XAMPP on port 3306)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mariadb+pymysql://root:@localhost:3306/mac_flask_test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Extensions
db = SQLAlchemy(app)
CORS(app)

# -------------------------------------------
# Database Model: Represents the 'quotes' table
# -------------------------------------------
class Quote(db.Model):
    quote_id = db.Column(db.Integer, primary_key=True)
    person = db.Column(db.String(100), nullable=False)
    quote = db.Column(db.String(255), nullable=False)

# -------------------------------------------
# Initialize Database (NEW FIX FOR FLASK 2.3+)
# -------------------------------------------
with app.app_context():
    db.create_all()  # Ensure tables are created before running the app

# -------------------------------------------
# Root Route: Basic Test
# -------------------------------------------
@app.route('/')
def testing():
    return "The app is working!"

# -------------------------------------------
# Add a Quote (POST Request)
# -------------------------------------------
@app.route('/quotes', methods=['POST'])
def add_quote():
    data = request.json
    person = data.get('person')
    quote = data.get('quote')

    if not person or not quote:
        return jsonify({"error": "Both 'person' and 'quote' are required."}), 400

    new_quote = Quote(person=person, quote=quote)
    db.session.add(new_quote)
    db.session.commit()
    return jsonify({"message": "Quote added successfully!"}), 201

# -------------------------------------------
# Get All Quotes (GET Request)
# -------------------------------------------
@app.route('/quotes', methods=['GET'])
def get_quotes():
    quotes = Quote.query.all()
    quote_list = [{"quote_id": q.quote_id, "person": q.person, "quote": q.quote} for q in quotes]
    return jsonify(quote_list)

# -------------------------------------------
# Run the Flask App
# -------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)