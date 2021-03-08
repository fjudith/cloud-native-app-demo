"""
Defines the blueprint for the persons
"""
from flask import Blueprint
from flask_restful import Api

from resources import PersonResource

PERSON_BLUEPRINT = Blueprint("person", __name__)
Api(PERSON_BLUEPRINT).add_resource(
    PersonResource, "/person/v1/<string:guid>"
)