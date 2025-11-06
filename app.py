from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import timedelta
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

app.config["JWT_SECRET_KEY"] = "1234567898ytrew"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=1)
jwt = JWTManager(app)

# Import BEFORE route definition
import model
import route

@app.route('/')
def home():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(debug=True)