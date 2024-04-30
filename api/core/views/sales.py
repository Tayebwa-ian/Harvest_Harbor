#!/usr/bin/python3
"""
sales Views module
"""
from flask_restful import Resource
from models import storage, Sale
from ..serializers.sales import SaleSchema
from marshmallow import ValidationError, EXCLUDE
from flask import request, abort
import json


sale_schema = SaleSchema(unknown=EXCLUDE)
sales_schema = SaleSchema(many=True)

class SalesList(Resource):
    """Defines get(for all) for sales"""
    def get(self):
        """retrieve all sales details from the storage"""
        sales = storage.all(Sale)
        return (sales_schema.dump(sales), 200)
    
    def post(self):
        """Add sales details to the storage"""
        try:
            data = sale_schema.load(request.get_json())
        except ValidationError as e:
            abort(400, "invalid input data")
        new_sales = Sale(**data)
        new_sales.save()
        return (sale_schema.dump(new_sales), 201)

class SaleSingle(Resource):
    """Retrieves a sale details for a single owner
    Arg:
        hub_name: name of the hub to retrieve
    """
    def get(self, owner_id):
        """retrive sales details from the storage"""
        sales = storage.get(Sale, owner_id=owner_id)
        if sales:
            return (sales_schema.dump(sales), 200)

    """todo: get sales detail for a particular product from a particular user"""
    """todo: delete a particular product from sales"""
