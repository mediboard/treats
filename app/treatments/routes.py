from app.treatments import bp


@bp.route('/')
def main():
	return "Hello World"