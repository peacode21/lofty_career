from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#from flask_wtf.csrf import CSRFProtect

app = Flask(__name__,instance_relative_config=True)

app.config.from_pyfile('config.py', silent=False)

db = SQLAlchemy(app)

from lofty_career import adminroute,userroute,companyroute