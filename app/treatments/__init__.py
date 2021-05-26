from flask import Blueprint

bp = Blueprint('treatments', __name__)

from app.treatments import routes