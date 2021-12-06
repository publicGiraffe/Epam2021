from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:admin@localhost/epam_db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import Place, Category, Special
