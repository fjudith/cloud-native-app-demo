import argparse
import os
import logging

# ===============================================
# Python Script arguments and
# environment variables declaration
# ===============================================
parser = argparse.ArgumentParser()
parser.parse_known_args()
# applicaiton config
parser.add_argument('--appname', help='Specifies the application name.', default=os.environ.get('APPNAME', 'fakenames'))
parser.add_argument('--listen-address', help='Specifies the application listen address.', default=os.environ.get('LISTEN', 'localhost'))
parser.add_argument('--listen-port', help='Specifies the application listen port.', default=os.environ.get('PORT', '3000'))
parser.add_argument('--service-root', help='Specifies the web service root path.', default=os.environ.get('SERVICE_ROOT', '/apis'))
# rethinkdb config
parser.add_argument('--rethinkdb-host', help='Specifies the remote RethinkDB server host.', default=os.environ.get('RDB_HOST', 'localhost'))
parser.add_argument('--rethinkdb-port', help='Specifies the remote RethinkDB server port.', default=os.environ.get('RDB_PORT', 28015))
parser.add_argument('--rethinkdb-database', help='Specifies the RethinkDB database name.', default=os.environ.get('RDB_DB', 'fakenames'))
parser.add_argument('--rethinkdb-table', help='Specifies the RethinkDB table name.', default=os.environ.get('RDB_TBL', 'fakenames'))
parser.add_argument('--rethinkdb-primary-key', help='Specifies the RethinkDB table primary key.', default=os.environ.get('RDB_PKEY', 'GUID'))
# open policy agent config
parser.add_argument('-u', '--opa-url', help='Specifies the OPA proxy server URL.', default=os.environ.get('OPA_URL', 'http://localhost:8181'))

parser.add_argument('-d', '--debug', help="Enable debug logging", action="store_true")
args = parser.parse_args()

# logging config
logger = logging.getLogger('server')
ch = logging.StreamHandler()
if args.debug:
    logger.setLevel(logging.DEBUG)
    ch.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)
    ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
