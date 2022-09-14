from flask import Blueprint

bp = Blueprint('blogs', __name__)

from app.blogs import routes