from flask import request, _app_ctx_stack as stack
from .metric_base import MetricBase

class FlaskCarbonStatsdBase(MetricBase):

    def __init__(self, app=None, host='localhost', port=8125, environment="dev"):
        super(FlaskCarbonStatsd, self).__init__(host, port, environment)
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        if not self.measurement:
            self.measurement = 'flask.carbon.statsd.%s.%s' %(
                self.environment, self.app.name.strip('.')
        )

        try:
            self.connection = self.connect()
            self.app.before_request(self.before_request)
            self.app.after_request(self.after_request)
        except Exception as e:
            print("Unable to initalise metrics client: %s" % e)

    def before_request(self):
        ctx = stack.top
        ctx._flask_statsd_request_begin_at = time.time()

    def after_request(self, resp):
        ctx = stack.top
        elapsed = (time.time() - ctx._flask_statsd_request_begin_at) * 1000

        status_code = resp.status_code
        endpoint = request.endpoint

        self.send_flask_metrics(
            self.measurement, elapsed, self.hostname, endpoint, status_code)

        return resp


class FlaskCarbonStatsdTimer(FlaskCarbonStatsdBase):
    def send_flask_metrics(measurement, elapsed, hostname, endpoint, status_code):
        with self.connection.pipeline() as pipe:
            metric = self.mk_metric(measurement, elapsed, hostname, endpoint, status_code)
            pipe.timing(metric, elapsed)


class FlaskCarbonStatsdTimerCounter(FlaskCarbonStatsdBase):
    def send_flask_metrics(measurement, elapsed, hostname, endpoint, status_code):
        with self.connection.pipeline() as pipe:
            metric = self.mk_metric(measurement, elapsed, hostname, endpoint, status_code)
            pipe.timing(metric, elapsed)
            pipe.incr(metric, 1)
