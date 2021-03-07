"""
Defines the Person repository
"""

import csv
import requests
from contextlib import closing

from models import rdb
from config import args, logger
from flask import abort, g

from rethinkdb.errors import RqlRuntimeError, RqlDriverError

class DatasetRepository:
    """ The repository for the dataset model """

    # download and import the dataset in rethinkdb
    @staticmethod
    def create(url):
        """ Import a dataset from a download url """

        logger.info('Download dataset URL:"{0}"'.format(url))
        
        # Output
        output = {
            'deleted': 0,
            'errors': 0,
            'inserted': 0,
            'replaced': 0,
            'skipped': 0,
            'unchanged': 0,
            'zrejected': []
        }

        # check that dataset exists
        try:
            request_response = requests.head(url)
        except Exception as e:
            logger.error('Could not find: "{0}", response: {1}'.format(url, e))
            abort(500)

        # check that dataset exists
        request_response = requests.head(url)
        if not request_response.status_code == 200:
            logger.error('Could not find: "{0}", response: {1}'.format(url, request_response))
            abort(request_response.status_code)

        # proceed the online dataset line by line
        with closing(requests.get(url, stream=True)) as r:
            f = (line.decode('utf-8') for line in r.iter_lines())
            reader = csv.DictReader(f)
            for data in reader:
                try:
                    cursor = rdb.table(args.rethinkdb_table).insert(data).run(g.rdb_conn)
                    
                    if cursor['errors'] >= 1:
                        output['zrejected'].append(cursor['first_error'])

                    # incrementation based on query result
                    output['deleted'] += cursor['deleted']
                    output['errors'] += cursor['errors']
                    output['inserted'] += cursor['inserted']
                    output['replaced'] += cursor['replaced']
                    output['skipped'] += cursor['skipped']
                    output['unchanged'] += cursor['unchanged']
                except RqlRuntimeError as e:
                    abort(503, f'Record could not be inserted. Message: {e}')
            
            return output        