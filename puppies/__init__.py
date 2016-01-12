from flask import Flask
import pdb

app = Flask(__name__)

app.config.from_pyfile('default_config.py')
app.config.from_envvar('PUPPIES_SETTINGS', silent=True)

from puppies.views import *
# pdb.set_trace()
