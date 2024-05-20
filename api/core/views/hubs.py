#!/usr/bin/python3
"""
Hub Views module
"""
from flask_restful import Resource
import models
from ..serializers.hubs import HubSchema
from marshmallow import ValidationError, EXCLUDE
from flask import request, jsonify, make_response
from utilities.auth_utils import auth_required, get_current_user
from datetime import datetime


hub_schema = HubSchema(unknown=EXCLUDE)
hubs_schema = HubSchema(many=True)


class HubList(Resource):
    """Defines get(for all) related to a user
        and post request of hubs
    """
    def get(self):
        """retrieve all hubs related to a user"""
        user = get_current_user()
        if user and user.is_farmer:
            hubs = user.hubs
            return (hubs_schema.dump(hubs), 200)
        else:
            hubs = models.storage.all(models.Hub)
            return (hubs_schema.dump(hubs), 200)

    @auth_required(roles=['is_farmer'])
    def post(self):
        """Add a Hub to the storage"""
        user = get_current_user()
        user_id = user.id
        try:
            data = request.get_json()
            data['owner_id'] = user_id
            data = hub_schema.load(data)
        except ValidationError as e:
            responseobject = {
                "status": "fail",
                "message": e.messages
            }
            return make_response(jsonify(responseobject))
        new_Hub = models.Hub(**data)
        new_Hub.save()
        return (hub_schema.dump(new_Hub), 201)


class HubSingle(Resource):
    """Retrieves a single Hub, deletes a Hub
        and makes changes to an exisiting Hub
    """
    def get(self, hub_id):
        """retrive a single Hub from the storage
        Arg:
            hub_id: ID of the Hub to retrieve
        """
        hub = models.storage.get(models.Hub, id=hub_id)
        if hub:
            return (hub_schema.dump(hub), 200)

    @auth_required(roles=['is_farmer', 'is_admin'])
    def delete(self, hub_id):
        """Delete Hub
        Arg:
            hub_id: ID of the Hub to be deleted
        """
        user = get_current_user()
        hub = models.storage.get(models.Hub, id=hub_id)
        if user.id == hub.owner_id or user.is_admin:
            models.storage.delete(hub)
            response = {'message': 'resource successfully deleted'}
            return make_response(jsonify(response), 200)

    @auth_required(roles=['is_farmer', 'is_admin'])
    def put(self, hub_id):
        """Make changes to an existing Hub
        Arg:
            hub_id: ID of the Hub to be changed
        """
        user = get_current_user()
        hub = models.storage.get(models.Hub, id=hub_id)
        if hub.owner_id == user.id or user.is_admin:
            try:
                data = request.get_json()
                data["owner_id"] = user.id
                data = hub_schema.load(data)
            except ValidationError as e:
                responseobject = {
                    "status": "Input data invalid",
                    "message": e.messages
                }
                return make_response(jsonify(responseobject), 400)
            if hub and user.id == hub.owner_id:
                for key in data.keys():
                    if hasattr(hub, key):
                        setattr(hub, key, data[key])
                hub.updated_at = datetime.now()
                models.storage.save()
                return (hub_schema.dump(hub), 200)
