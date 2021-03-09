# ----- Prometheus -----
# from prometheus_flask_exporter import PrometheusMetrics
from prometheus_flask_exporter import RESTfulPrometheusMetrics

def start_openmetrics(app, routes):
    # PrometheusMetrics(app=app, path='/metrics')
    RESTfulPrometheusMetrics(app=app, api=routes)