#!/usr/bin/python3
"""
Hub Views module
"""
from flask_restful import Resource
import models
from ..serializers.hubs import HubSchema
from marshmallow import ValidationError, EXCLUDE
from flask import request, jsonify
from utilities.auth_utils import auth_required
from datetime import datetime


hub_schema = HubSchema(unknown=EXCLUDE)
hubs_schema = HubSchema(many=True)


class HubList(Resource):
    """Defines get(for all) related to a user
        and post request of hubs
    """
    @auth_required(roles=['is_farmer', 'is_admin'])
    def get(self, user_id):
        """retrieve all hubs related to a user"""
        user = models.storage.get(models.User, id=user_id)
        hubs = user.hubs
        return (jsonify(hubs), 200)

    @auth_required(roles=['is_farmer'])
    def post(self, user_id):
        """Add a Hub to the storage"""
        try:
            data = request.get_json()
            hub_schema.load(data)
        except ValidationError as e:
            responseobject = {
                "status": "fail",
                "message": e.messages
            }
            return jsonify(responseobject)
        data['owner_id'] = user_id
        new_Hub = models.Hub(**data)
        new_Hub.save()
        return (hub_schema.dump(new_Hub), 201)


class HubSingle(Resource):
    """Retrieves a single Hub, deletes a Hub
        and makes changes to an exisiting Hub
    Arg:
        hub_id: ID of the Hub to retrieve
    """
    @auth_required(roles=['is_farmer', 'is_admin'])
    def get(self, hub_id):
        """retrive a single Hub from the storage"""
        Hub = models.storage.get(models.Hub, id=hub_id)
        if Hub:
            return (hub_schema.dump(Hub), 200)

    @auth_required(roles=['is_farmer', 'is_admin'])
    def delete(self, hub_id):
        """Delete Hub
        Arg:
            hub_id: ID of the Hub to be deleted
        """
        Hub = models.storage.get(models.Hub, id=hub_id)
        if Hub:
            models.storage.delete(Hub)
            response = {'message': 'resource successfully deleted'}
            return (jsonify(response))

    @auth_required(roles=['is_farmer', 'is_admin'])
    def put(self, hub_id):
        """Make changes to an existing Hub
        Arg:
            hub_id: ID of the Hub to be changed
        """
        try:
            data = request.get_json()
            hub_schema.load(data)
        except ValidationError as e:
            responseobject = {
                "status": "Input data invalid",
                "message": e.messages
            }
            return jsonify(responseobject)
        Hub = models.storage.get(models.Hub, id=hub_id)
        if Hub:
            for key in data.keys():
                if hasattr(Hub, key):
                    setattr(Hub, key, data[key])
            Hub.updated_at = datetime.now()
            models.storage.save()
            return (hub_schema.dump(Hub), 200)


class HubAll(Resource):
    """Defines get(for all) hubs
    Admin user can retrieve all hubs
    """
    @auth_required(roles=['is_admin'])
    def get(self):
        """retrieve all hubs"""
        hubs = models.storage.get(models.Hub)
        return (hubs_schema.dump(hubs), 200)
