#!/usr/bin/python3
"""
Cart and Purchases Views module
"""
from flask_restful import Resource
import models
from ..serializers.sales import SoldProductSchema
from marshmallow import ValidationError, EXCLUDE
from flask import request, make_response, jsonify
from utilities.auth_utils import auth_required, get_current_user
from datetime import datetime


sold_product_schema = SoldProductSchema(unknown=EXCLUDE)
sold_products_schema = SoldProductSchema(many=True)


def is_cart_closed(purchases) -> object:
    """check if cart is open or closed
    Args:
        purchases: list of purchases objects
    Return: the open pucharse instance or None
    """
    for purchase in purchases:
        if not purchase.is_closed:
            return purchase


class UserPurchasesList(Resource):
    """Defines get(for all) """
    @auth_required
    def get(self):
        """
        retrieve all purchases related to a praticular user
        from the storage

        Note: A purchase is an open cart is the is_closed attr is false
        """
        user = get_current_user()
        if not user.admin:
            purchases = user.purchases
            return make_response(jsonify(purchases), 200)
        else:
            purchases = models.storage.all(models.Purchase)
            return make_response(jsonify(purchases), 200)

    @auth_required
    def post(self):
        """Create cart if it does not exist
        and add items to the purchase
        """
        user = get_current_user()
        user_id = user.id
        purchases = user.purchases
        purchase = is_cart_closed(purchases=purchases)
        if len(purchases) > 0 and purchase:
            cart = models.Purchase(owner_id=user_id)
            cart.save()
        else:
            cart = purchase
        # add items to cart
        try:
            data = request.get_json()
            data['purchase_id'] = cart.id
            data = sold_product_schema.load(data)
        except ValidationError as e:
            responseobject = {
                "status": "fail",
                "message": e.messages
            }
            return make_response(jsonify(responseobject), 400)
        for pdt in cart.sold_products:
            if pdt.id == data['product_id']:
                responseobject = {
                    'status': 'warning',
                    'message': 'This product already exists on cart,' +
                    'simply adjust its quantities in the cart',
                }
                return make_response(jsonify(responseobject), 200)
        sold_product = models.SoldProduct(**data)
        sold_product.save()
        return (sold_product_schema.dump(sold_product), 201)


class CartProductsSingle(Resource):
    """Retrieves a single sold_product, deletes a sold_product
        and makes changes to an exisiting sold_product
    """
    @auth_required
    def get(self, sold_pdt_id):
        """retrive a single sold_product from the storage
        Arg:
            sold_pdt_id: ID of product on cart/sold_product
        """
        sold_pdt = models.storage.get(models.SoldProduct, id=sold_pdt_id)
        if sold_pdt:
            return (sold_product_schema.dump(sold_pdt), 200)

    @auth_required
    def delete(self, sold_pdt_id):
        """Delete sold_product
        Arg:
            sold_pdt_id: ID of product on cart/sold_product
        """
        sold_pdt = models.storage.get(models.SoldProduct, id=sold_pdt_id)
        product = models.storage.get(models.Product, id=sold_pdt.product_id)
        # take back the sold quantities into hub
        product.quantities += sold_pdt.quantities
        models.storage.save()

        if sold_pdt:
            models.storage.delete(sold_pdt)
            response = {'message': 'resource successfully deleted'}
            return make_response(jsonify(response), 200)

    @auth_required
    def put(self, sold_pdt_id):
        """Make changes to an existing sold_product that is already on cart
        Arg:
            sold_pdt_id: ID of product on cart/sold_product
        """
        sold_pdt = models.storage.get(models.SoldProduct, id=sold_pdt_id)
        product = models.storage.get(models.Product, id=sold_pdt.product_id)
        # take back the sold quantities into hub
        product.quantities += sold_pdt.quantities
        models.storage.save()

        try:
            data = request.get_json()
            data = sold_product_schema.load(data)
        except ValidationError as e:
            responseobject = {
                "status": "Input data invalid",
                "message": e.messages
            }
            return make_response(jsonify(responseobject), 400)
        if sold_pdt:
            for key in data.keys():
                if hasattr(sold_pdt, key):
                    setattr(sold_pdt, key, data[key])
            sold_pdt.updated_at = datetime.now()
            models.storage.save()
            return (sold_product_schema.dump(sold_pdt), 200)


class CartProducts(Resource):
    """Defines get for all products in the cart"""
    def get(self, cart_id):
        """retrieve all products on a cart
        Arg:
            cart_id: ID of the cart to which all the products belong
        """
        cart = models.storage.get(models.Purchase, id=cart_id)
        products = cart.sold_products
        return (sold_products_schema.dump(products), 200)
