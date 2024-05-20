#!/usr/bin/python3
"""
location Views module
"""
from flask_restful import Resource
import models
from ..serializers.locations import LocationSchema
from marshmallow import ValidationError, EXCLUDE
from flask import request, jsonify, make_response
from utilities.auth_utils import auth_required, get_current_user
from datetime import datetime


location_schema = LocationSchema(unknown=EXCLUDE)
locations_schema = LocationSchema(many=True)


def add_location(hub_id=None, user_id=None):
    """helper function to add location instance to the storage
    Args:
        hub_id: the hub to which location belong to
        user_id: the user to ehich the locations belong to
    """
    try:
        data = request.get_json()
        if hub_id:
            data['hub_id'] = hub_id
        if user_id:
            data['owner_id'] = user_id
        data = location_schema.load(data)
    except ValidationError as e:
        responseobject = {
            "status": "fail",
            "message": e.messages
        }
        return make_response(jsonify(responseobject), 400)
    new_location = models.Location(**data)
    new_location.save()
    return (location_schema.dump(new_location), 201)


class LocationHubList(Resource):
    """Defines get(for all) and post request of locations
    related to a particular hub
    """
    @auth_required
    def get(self, hub_id):
        """retrieve all locations from the storage
        Arg:
            hub_id: the hub to which location belong to
        """
        hub = models.storage.get(models.Hub, id=hub_id)
        locations = hub.locations
        return (locations_schema.dump(locations), 200)

    @auth_required
    def post(self, hub_id):
        """Add a location to the storage
        Arg:
            hub_id: the hub to which location belong to
        """
        add_location(hub_id=hub_id)


class LocationSingle(Resource):
    """Retrieves a single location, deletes a location
        and makes changes to an exisiting location
    """
    @auth_required
    def get(self, location_id):
        """retrive a single location from the storage
        Arg:
            location_id: ID of the location to retrieve
        """
        location = models.storage.get(models.Location, id=location_id)
        if location:
            return (location_schema.dump(location), 200)

    @auth_required
    def delete(self, location_id):
        """Delete location
        Arg:
            location_id: ID of the location to be deleted
        """
        user = get_current_user()
        location = models.storage.get(models.Location, id=location_id)
        if location.owner_id == user.id:
            if location:
                models.storage.delete(location)
                response = {'message': 'resource successfully deleted'}
                return make_response(jsonify(response), 200)

    @auth_required
    def put(self, location_id):
        """Make changes to an existing location
        Arg:
            location_id: ID of the location to be changed
        """
        try:
            data = request.get_json()
            data = location_schema.load(data)
        except ValidationError as e:
            responseobject = {
                "status": "Input data invalid",
                "message": e.messages
            }
            return make_response(jsonify(responseobject), 400)
        location = models.storage.get(models.Location, id=location_id)
        if location:
            for key in data.keys():
                if hasattr(location, key):
                    setattr(location, key, data[key])
            location.updated_at = datetime.now()
            models.storage.save()
            return (location_schema.dump(location), 200)


class LocationUserList(Resource):
    """Defines get(for all) and post request of locations
    related to a particular user
    """
    @auth_required
    def get(self):
        """retrieve all locations from the storage
        """
        user = get_current_user()
        user_id = user.id
        if not user.admin:
            user = models.storage.get(models.User, id=user_id)
            locations = user.locations
            return (locations_schema.dump(locations), 200)
        else:
            locations = models.storage.all(models.Location)
            return (locations_schema.dump(locations), 200)

    @auth_required
    def post(self):
        """Add a location to the storage
        """
        user = get_current_user()
        user_id = user.id
        add_location(user_id=user_id)
