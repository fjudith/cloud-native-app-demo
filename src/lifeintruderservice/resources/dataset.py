"""
Define the REST verbs relative to the datasets
"""

from flasgger import swag_from
from flask.json import jsonify
from flask_restful import Resource
from flask_restful.reqparse import Argument

from repositories import DatasetRepository
from util import parse_params

class DatasetResource(Resource):
    """ Verbs relative to the datasets """

    @staticmethod
    @parse_params(
        Argument("url", location="json", required=True, help="The url of the dataset.")
    )
    @swag_from("../swagger/dataset/POST.yaml")
    def post(url):
        """ Import data based on the dataset sent url """
        person = DatasetRepository.create(
            url=url
        )
        return jsonify(person)
