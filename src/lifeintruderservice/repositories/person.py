"""
Defines the Person repository
"""

import ast
from models import rdb
from config import args, logger
from flask import abort, g

from rethinkdb.errors import RqlRuntimeError

class PersonRepository:
    """ The repository for the user model """

    @staticmethod
    def get(guid):
        """ Query a person by the globally unique identifier (GUID)"""

        logger.info('Retreiving indivual informations:"{0}"'.format(guid))

        try:
            cursor = rdb.table(args.rethinkdb_table).filter({args.rethinkdb_primary_key: guid}).run(g.rdb_conn)
            for document in cursor:
                return document
        except RqlRuntimeError as e:
            abort(404, f'Records for globally unique identifier (GUID) "{guid}" were not found. "{e}"')

    @staticmethod
    def create(guid, profile):
        """ Create a new user """

        try:
            if self.get(guid) == None:
                person = ast.literal_eval(profile)
                cursor = rdb.table(args.rethinkdb_table).insert(person).run(g.rdb_conn)
                return cursor
            else:
                abort(409, f'An existing record existing record has been found for GUID {guid}. Use the POST method to udpate it')
        except RqlRuntimeError as e:
            abort(503, f'Record could not be inserted. Message: {e}')

    @staticmethod
    def update(self, guid, profile):
        """ Update a person's profile"""
        
        logger.info(f'Updating individual information:"{guid}"')
        
        if self.get(guid) == None:
            abort(404, f'No existing record existing record has been found for GUID {guid}. Use the PUT method to create it')
        
        try:
            person = ast.literal_eval(profile)
            cursor = rdb.table(args.rethinkdb_table).filter({args.rethinkdb_primary_key: guid}).update(person).run(g.rdb_conn)
            return cursor
        except RqlRuntimeError as e:
            abort(503, f'Record could not be update. Message: {e}')
    
    @staticmethod
    def remove(guid):
        """ Remove a person by its globally unique identifier (GUID)"""

        logger.info('Remove all individual related:"{0}"'.format(guid))

        try:
            rdb.table(args.rethinkdb_table).filter({args.rethinkdb_primary_key: guid}).delete().run(g.rdb_conn)
        except RqlRuntimeError as e:
            abort(404, f'Records for globally unique identifier (GUID) "{guid}" were not found. "{e}"')
