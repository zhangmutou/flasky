from .. import mail
from .. import celery
from flask import current_app, render_template
from flask_mail import Message

@celery.task
def send_email(to, subject, template, **kwargs):
	print(to,subject,template)
	app = current_app._get_current_object()
	msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
	# msg.body = render_template(template + '.txt', **kwargs)
	msg.body = 'test'
	# msg.html = render_template(template + '.html', **kwargs)

	with app.app_context():
		mail.send(msg)