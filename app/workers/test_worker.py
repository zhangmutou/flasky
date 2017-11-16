from .. import celery
from datetime import datetime
from flask_login import current_user
from flask import current_app


@celery.task
def test_worker(user):
	app = current_app._get_current_object()
	print(app.config['FLASKY_MAIL_SUBJECT_PREFIX'])
	with app.app_context():
		print(id(app))
		print(user)