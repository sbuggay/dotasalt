from flask import Flask

app = Flask(__name__)

import dotasalt.dotasalt
import dotasalt.views
import dotasalt.api