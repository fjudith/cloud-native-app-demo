"""
Defines the blueprint for the datasets
"""
from flask import Blueprint
from flask_restful import Api

from resources import DatasetResource

DATASET_BLUEPRINT = Blueprint("dataset", __name__)
Api(DATASET_BLUEPRINT).add_resource(
    DatasetResource, "/dataset/v1"
)