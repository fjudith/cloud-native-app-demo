

# db setup; only run once
from . import rdb
from config import args, logger
from rethinkdb.errors import RqlRuntimeError, RqlDriverError

class DatabaseSetup:
    def dbSetup():
        connection = rdb.connect(host=args.rethinkdb_host, port=args.rethinkdb_port)
        try:
            rdb.db_create(args.rethinkdb_database).run(connection)
            logger.info('Database setup completed')
        except RqlRuntimeError:
            logger.info('Database already exists.')
        finally:
            connection.close()
    
    def tblSetup():
        connection = rdb.connect(host=args.rethinkdb_host, port=args.rethinkdb_port)
        try:
            rdb.db(args.rethinkdb_database).table_create(args.rethinkdb_table, primary_key=args.rethinkdb_primary_key).run(connection)
            logger.info('Table setup completed')
        except RqlRuntimeError:
            logger.info('Table already exists.')
        finally:
            connection.close()

    dbSetup()
    tblSetup()