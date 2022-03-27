def create_notfound_error(message):
	body = {'Not Found': message}
	return create_error(body), 404


def create_error(body):
	return {
		'Message': 'The server encountered an error',
		'Error': body
	}
