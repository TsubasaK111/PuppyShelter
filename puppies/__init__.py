from flask import Flask

import pdb
import logging

app = Flask(__name__)

app.config.from_pyfile('default_config.py')
app.config.from_envvar('PUPPIES_SETTINGS', silent=True)

logging.basicConfig(filename='log.log',level=logging.DEBUG)

from puppies.views import *
# pdb.set_trace()
