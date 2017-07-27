from .. import celery
from .. import db
from .. import celery_task_logger
from ..models import ServerMonitor
from datetime import datetime
import psutil
import json

logger = celery_task_logger

@celery.task(bind=True)
def server_monitor(self):
	cpu_info = cpu()
	memory_info = memory()
	disks_info = disks()
	network_info = network()
	sensors_info = sensors()

	server_monitor = ServerMonitor(
									cpu_info=json.dumps(cpu_info),
									memory_info=json.dumps(memory_info),
									disks_info=json.dumps(disks_info),
									network_info=json.dumps(network_info),
									sensors_info=json.dumps(sensors_info)
									# moniter_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
									)
	db.session.add(server_monitor)
	logger.info('{}: done!'.format(self.request))

def cpu():
	cpu = psutil.cpu_times()
	cpu_usage = cpu.user / cpu.system
	# print('%.2f%%' %(cpu_usage))
	cpu_info = {
		'user': cpu.user,
		# 'nice': cpu.nice,
		'system': cpu.system,
		'idle': cpu.idle,
		'iowait ': cpu.iowait,
		'irq': cpu.irq,
		'softirq': cpu.softirq,
		'steal': cpu.steal,
		'guest': cpu.guest,
		'guest_nice': cpu.guest_nice,
		# 'interrupt': cpu.interrupt,
		# 'dpc': cpu.dpc
	}
	return cpu_info
	# print(cpu_info)

def memory():
	memory = psutil.virtual_memory()
	memory_info = {
		'total': memory.total,
		 'available': memory.available,
		 'percent': memory.percent,
		 'used': memory.used,
		 'free': memory.free,
		 'active': memory.active,
		 'inactive': memory.inactive,
		 'buffers': memory.buffers,
		 'cached': memory.cached,
		 'shared': memory.shared
	}
	return memory_info

def disks():
	disk_usage = psutil.disk_usage('/')
	disk_io_counters = psutil.disk_io_counters()
	disk_usage_info = {
		'total': disk_usage.total,
		'used': disk_usage.used,
		'free': disk_usage.free,
		'percent': disk_usage.percent
	}
	disk_io_counters_info = {
		'read_count': disk_io_counters.read_count,
		'write_count': disk_io_counters.write_count,
		'read_bytes': disk_io_counters.read_bytes,
		'write_bytes': disk_io_counters.write_bytes,
		'read_time': disk_io_counters.read_time,
		'write_time': disk_io_counters.write_time,
		'read_merged_count': disk_io_counters.read_merged_count,
		'write_merged_count': disk_io_counters.write_merged_count,
		'busy_time': disk_io_counters.busy_time
	}
	# print(disk_usage_info)
	# print(disk_io_counters_info)
	return {'disk_usage_info': disk_usage_info, 'disk_io_counters_info': disk_io_counters_info}

def network():
	net_io_counters = psutil.net_io_counters()
	net_io_counters_info = {
		'bytes_sent': net_io_counters.bytes_sent,
		'bytes_recv': net_io_counters.bytes_recv,
		'packets_sent': net_io_counters.packets_sent,
		'packets_recv': net_io_counters.packets_recv,
		'errin': net_io_counters.errin,
		'errout': net_io_counters.errout,
		'dropin': net_io_counters.dropin,
		'dropout': net_io_counters.dropout,
	}
	# print(net_io_counters_info)
	return net_io_counters_info

def sensors():
	pass
