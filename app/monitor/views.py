from . import mointor
from .. import db
from ..models import ServerMonitor
from ..decorators import admin_required, permission_required
from flask_login import login_required
from flask import jsonify
from datetime import datetime
import json


@mointor.route('/all', methods=['GET', 'POST'])
@login_required
@admin_required
def all():
	time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	mointor_info = ServerMonitor.query.filter(ServerMonitor.moniter_time<time)
	x_categories = []
	cpu = {'name': 'CPU', 'data':[]}
	memory = {'name': '内存', 'data': []}
	series = []
	if mointor_info.count() > 0:
		for m in mointor_info:
			x_categories.append(m.moniter_time.strftime("%H:%M:%S"))
			print(json.loads(m.cpu_info))
			cpu['data'].append(json.loads(m.cpu_info)['percent'])
			memory['data'].append(json.loads(m.memory_info)['percent'])

	
	series.append(memory)
	series.append(cpu)
	print(series)

	return jsonify({'x_categories':x_categories, 'series':series})
