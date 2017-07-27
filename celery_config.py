from celery.schedules import crontab
from datetime import timedelta
from app.worker import server_monitor_worker

class CeleryConfig:

	CELERY_TIMEZONE='Asia/Shanghai'
	CELERY_BROKER_URL = 'redis://:123456@localhost:6379/0'
	CELERY_RESULT_BACKEND = 'redis://:123456@localhost:6379/0'
	# CELERY_ACCEPT_CONTENT = ['json']
	# CELERY_ACCEPT_CONTENT = ['application/json']
	# CELERY_TASK_SERIALIZER = 'json'
	# CELERY_EVENT_SERIALIZER = 'json'
	# CELERY_RESULT_SERIALIZER = 'json'
	CELERYBEAT_SCHEDULE = {
	    # Executes every 3s
	    'cpu': {
	        'task': 'server_monitor_worker.cpu',
	        # 'schedule': crontab()
	        'schedule': timedelta(seconds=3)
	    },
		'memory': {
			'task': 'server_monitor_worker.memory',
			# 'schedule': crontab('*/3')
			'schedule': timedelta(seconds=3)
		},
		'disks': {
			'task': 'server_monitor_worker.disks',
			# 'schedule': crontab('*/2')
			'schedule': timedelta(seconds=3)
		},
		'network': {
			'task': 'server_monitor_worker.network',
			# 'schedule': crontab('*/2')
			'schedule': timedelta(seconds=3)
		},
		'sensors': {
			'task': 'server_monitor_worker.sensors',
			# 'schedule': crontab('*/2')
			'schedule': timedelta(seconds=3)
		},
	}