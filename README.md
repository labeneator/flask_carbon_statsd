# Flask-Statsd

Generate and send Flask metrics in [Graphite Carbon Format](https://github.com/influxdata/telegraf/tree/master/plugins/inputs/statsd#influx-statsd) format.


# Install
```bash
pip install flask-carbon-statsd

# Latest Code

pip install git+https://github.com/labeneator/flask_carbon_statsd.git
```


# Usage Example
```python
# myapp.py
from flask import Flask, Blueprint
from flask_carbon_statsd import FlaskCarbonStatsdTimerCounter

flask_statsd = FlaskCarbonStatsdTimerCounter(host='localhost', port=8125)


app = Flask(__name__)
flask_statsd.init_app(app)

# or
flask_statsd = FlaskCarbonStatsd(app=app, host='localhost', port=8125)


@app.route('/app/download')
def app_download():
    return 'OK'

bp = Blueprint('blueprint', __name__)

@bp.route('/device/<device>/stats')
def device_stats(device):
    return 'OK'

app.register_blueprint(bp)
```

* Request `/app/download` `/device/android/stats`

    ```
    flask_statsd.myapp,endpoint=app_download,status_code=200,server=vagrant-ubuntu-trusty-64:0.467062|ms
    flask_statsd.myapp,endpoint=blueprint.device_stats,status_code=200,server=vagrant-ubuntu-trusty-64:0.467062|ms
    ```

* Request `/`

    ```
    flask_statsd.myapp,endpoint=None,status_code=404,server=vagrant-ubuntu-trusty-64:0.467062|ms
    ```
