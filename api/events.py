from flask.ext import restful
from authenticate import authenticate
from flask import request, abort
import time

from models import Event

class Events(restful.Resource):
    method_decorators=[authenticate]
    def get(self):
        # Get events since last poll
        return Event.fetch('1','montreal', 1424558599)

