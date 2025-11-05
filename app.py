from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import timedelta
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

app.config["JWT_SECRET_KEY"] = "1234567898ytrew"  # put in ENV in production
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=1)
jwt = JWTManager(app)


if __name__ == '__main__':
    import model   # 👈 moved here
    import route   # 👈 moved here
    app.run(debug=True)
