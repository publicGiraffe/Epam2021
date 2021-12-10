from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restx import Api

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:admin@localhost/epam_db'
bluePrint = Blueprint('api', __name__, url_prefix='/api')
api = Api(bluePrint, title='Sample Flask-Restx Application')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import Place, Category, Special
from views import PlaceResource, PlaceListResource, CategoryResource, CategoryListResource


app.register_blueprint(bluePrint)

if __name__ == '__main__':
    app.run()
