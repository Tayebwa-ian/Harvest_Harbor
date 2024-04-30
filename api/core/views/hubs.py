#!/usr/bin/python3
"""
hubs Views module
"""
from flask_restful import Resource
from models import storage, Hub
from ..serializers.hubs import HubSchema
from marshmallow import ValidationError, EXCLUDE
from flask import request, abort
import json


hub_schema = HubSchema(unknown=EXCLUDE)
hubs_schema = HubSchema(many=True)

class HubList(Resource):
    """Defines get(for all) for hubs"""
    def get(self):
        """retrieve all categories from the storage"""
        hubs = storage.all(Hub)
        return (hubs_schema.dump(hubs), 200)

    def post(self):
        """Add a hub to the storage"""
        try:
            data = hub_schema.load(request.get_json())
        except ValidationError as e:
            abort(400, "invalid input data")
        new_hub = Hub(**data)
        new_hub.save()
        return (hub_schema.dump(new_hub), 201)

class HubSingle(Resource):
    """Retrieves a single hub
    Arg:
        hub_name: name of the hub to retrieve
    """
    def get(self, hub_name):
        """retrive a single hub from the storage"""
        hub = storage.get(Hub, name=hub_name)
        if hub:
            return (hub_schema.dump(hub), 200)

    def delete(self, hub_name):
        """Delete hub
        Arg:
            hub_name: name of the hub to retrieve
        """
        hub = storage.get(Hub, name=hub_name)
        if hub:
            storage.delete(hub)
            response = {'message': 'resource successfully deleted'}
            return (json.dumps(response), 204)

    def put(self, hub_name):
        """Make changes to an existing hub
        Arg:
            hub_name: name of the hub to retrieve
        """
        try:
            data = hub_schema.load(request.get_json())
        except ValidationError as e:
            abort(400, "invalid input data")
        hub = storage.get(Hub, name=hub_name)
        if hub:
            for key in data.keys():
                if hasattr(hub, key):
                    setattr(hub, data[key])
            storage.save()
            return (hub_schema.dump(hub), 200)
