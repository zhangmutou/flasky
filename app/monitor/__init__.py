from flask import Blueprint

mointor = Blueprint('mointor', __name__)

from . import views