"""
Define the REST verbs relative to the persons
"""

import json
from flasgger import swag_from
from flask.json import jsonify
from flask_restful import Resource
from flask_restful.reqparse import Argument

from repositories import PersonRepository
from util import parse_params
from server import request


class PersonResource(Resource):
    """ Verbs relative to the persons """
    
    @staticmethod
    @swag_from("../swagger/person/GET.yaml")
    def get(guid):
        """ Return a person key information based on his globally unique identifier (GUID) """
        person = PersonRepository.get(guid=guid)
        return jsonify(person)
    
    @staticmethod
    @parse_params(
        Argument("profile", location="json", required=True, help="The profile of a person.")
    )
    @swag_from("../swagger/person/POST.yaml")
    def post(guid, profile):
        """ Update a person based on the sent information """
        repository = PersonRepository()
        person = repository.update(guid=guid, profile=profile)
        return jsonify(person)


    @staticmethod
    @parse_params(
        Argument("profile", location="json", required=True, help="The profile of a person.")
    )
    @swag_from("../swagger/person/PUT.yaml")
    def put(guid, profile):
        """ Create a person based on the sent information """
        person = PersonRepository.create(
            guid=guid, profile=profile
        )
        return jsonify(person)
    
    @staticmethod
    @swag_from("../swagger/person/DELETE.yaml")
    def get(guid):
        """ Delete all data related to a person key information based on his globally unique identifier (GUID) """
        person = PersonRepository.remove(guid=guid)
        return jsonify(person)
