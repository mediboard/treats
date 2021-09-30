from app.studies import bp
from flask_cors import cross_origin


@bp.route('/')
@cross_origin(supports_credentials=True)
def main():
	return "Hello Studies"


@bp.route('/<string:name>')