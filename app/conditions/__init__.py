from flask import Blueprint

bp = Blueprint('conditions', __name__)

from app.conditions import routes, controller