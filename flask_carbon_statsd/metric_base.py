import time
import socket
import platform
from statsd import StatsClient

class MetricBase(object):
    def __init__(self, host='localhost', port=8125, environment="dev"):
        self.hostname = platform.node() or socket.gethostname()
        self.statsd_host = host
        self.statsd_port = port
        self.measurement = None
        self.environment = environment

    def connect(self):
        return StatsClient(host=self.statsd_host,
                           port=self.statsd_port)

    def mk_metric(self, metric, **tags):
        return '.'.join([metric] + ['{}'.format(v) for k, v in tags.items()])

