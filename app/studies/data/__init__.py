from flask import Blueprint

bp = Blueprint('data', __name__)

from app.studies.data import routes, controller