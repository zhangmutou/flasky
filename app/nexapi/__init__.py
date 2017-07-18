from flask import Blueprint

nexapi = Blueprint('nexapi', __name__)

from . import views
