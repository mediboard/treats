from flask import Blueprint

bp = Blueprint('measures', __name__)

from app.measures import routes, controller