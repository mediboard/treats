from flask import Blueprint

bp = Blueprint('studies', __name__)

from app.studies import routes, controller

from app.studies.data import bp as data_bp

bp.register_blueprint(data_bp, url_prefix='/data')
