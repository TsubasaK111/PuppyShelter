from flask import Flask
import pprint
import pdb

app = Flask(__name__)

app.config.from_pyfile('default_config.py')
app.config.from_envvar('PUPPIES_SETTINGS', silent=True)

# pdb.set_trace()

import puppies.views
