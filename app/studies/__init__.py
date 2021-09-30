from flask import Blueprint

bp = Blueprint('studies', __name__)

from app.studies import routes, controller