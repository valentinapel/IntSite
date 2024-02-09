from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Istanziamo l'applicazione da eseguire con le sue variabili di configurazione.
app = Flask(__name__, static_url_path='/static')
app.config['CACHE_TYPE'] = "null" 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True #Per zittire il warning sull'overhead
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from GecoIntSite import routes