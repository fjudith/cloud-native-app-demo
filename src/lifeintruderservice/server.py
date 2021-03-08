import json
import requests
from flasgger import Swagger
from flask import Flask, request, abort, g
from flask.blueprints import Blueprint

from config import args, logger
import routes
from models import rdb

from rethinkdb.errors import RqlDriverError

server = Flask(__name__)

# open connection before each request
@server.before_request
def before_request():
    # Open Policy Agent request filtering
    def check_authorization():
        try:
            input_request = json.dumps({
                            "method": request.method,
                            "path": request.path.strip().split("/")[1:],
                            "user": get_authentication(request),
            }, indent=2)
            url = args.opa_url
            server.logger.debug("OPA query: %s. Body: %s", url, input_request)
            response = requests.post(url, data=input_request)
        except Exception as e:
            server.logger.exception("Unexpected error querying OPA.")
            abort(500)

        if response.status_code != 200:
            server.logger.error("OPA status code: %s. Body: %s",
                            response.status_code, response.json())
            abort(500)

        allowed = response.json()
        server.logger.debug("OPA result: %s", allowed)
        if not allowed:
            abort(403)

    def get_authentication(request):
        return request.headers.get("Authorization", "")
    
    # RethinkDB data persistence
    def connect_database():
        logger.debug('Connecing to database host:"{0}"'.format(args.rethinkdb_host))
        try:
            g.rdb_conn = rdb.connect(host=args.rethinkdb_host, port=args.rethinkdb_port, db=args.rethinkdb_database)
        except RqlDriverError:
            abort(503, "Database connection could be established.")
    
    check_authorization()
    connect_database()

# close the connection after each request
@server.teardown_request
def teardown_request(exception):
    logger.debug('Disconnecting from database host:"{0}"'.format(args.rethinkdb_host))
    try:
        g.rdb_conn.close()
    except AttributeError:
        pass


# config your API specs
# you can define multiple specs in the case your api has multiple versions
# ommit configs to get the default (all views exposed in /spec url)
# rule_filter is a callable that receives "Rule" object and
#   returns a boolean to filter in only desired views

server.config["SWAGGER"] = {
    "swagger_version": "2.0",
    "title": "Application",
    "specs": [
        {
            "version": "0.0.1",
            "title": "Application",
            "endpoint": "spec",
            "route": "/apis/spec",
            "rule_filter": lambda rule: True,  # all in
        }
    ],
    "static_url_path": "/apidocs",
}

Swagger(server)

for blueprint in vars(routes).values():
    if isinstance(blueprint, Blueprint):
        server.register_blueprint(blueprint, url_prefix=args.service_root)


if __name__ == "__main__":
    server.run( host=args.listen_address,
                port=args.listen_port
              )