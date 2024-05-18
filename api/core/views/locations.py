#!/usr/bin/python3
"""
location Views module
"""
from flask_restful import Resource
import models
from ..serializers.locations import LocationSchema
from marshmallow import ValidationError, EXCLUDE
from flask import request
from flask import jsonify
from utilities.auth_utils import auth_required
from datetime import datetime


location_schema = LocationSchema(unknown=EXCLUDE)
locations_schema = LocationSchema(many=True)


class locationList(Resource):
    """Defines get(for all) and post request of locations"""
    @auth_required
    def get(self):
        """retrieve all locations from the storage"""
        locations = models.storage.all(models.Location)
        return (locations_schema.dump(locations), 200)

    @auth_required
    def post(self):
        """Add a location to the storage"""
        try:
            data = request.get_json()
            location_schema.load(data)
        except ValidationError as e:
            responseobject = {
                "status": "fail",
                "message": e.messages
            }
            return jsonify(responseobject)
        new_location = models.Location(**data)
        new_location.save()
        return (location_schema.dump(new_location), 201)


class locationSingle(Resource):
    """Retrieves a single location, deletes a location
        and makes changes to an exisiting location
    Arg:
        location_id: ID of the location to retrieve
    """
    @auth_required
    def get(self, location_id):
        """retrive a single location from the storage"""
        location = models.storage.get(models.Location, id=location_id)
        if location:
            return (location_schema.dump(location), 200)

    @auth_required
    def delete(self, location_id):
        """Delete location
        Arg:
            location_id: ID of the location to be deleted
        """
        location = models.storage.get(models.Location, id=location_id)
        if location:
            models.storage.delete(location)
            response = {'message': 'resource successfully deleted'}
            return (jsonify(response))

    @auth_required
    def put(self, location_id):
        """Make changes to an existing location
        Arg:
            location_id: ID of the location to be changed
        """
        try:
            data = request.get_json()
            location_schema.load(data)
        except ValidationError as e:
            responseobject = {
                "status": "Input data invalid",
                "message": e.messages
            }
            return jsonify(responseobject)
        location = models.storage.get(models.Location, id=location_id)
        if location:
            for key in data.keys():
                if hasattr(location, key):
                    setattr(location, key, data[key])
            location.updated_at = datetime.now()
            models.storage.save()
            return (location_schema.dump(location), 200)
