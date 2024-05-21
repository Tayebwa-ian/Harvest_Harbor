#!/usr/bin/python3
"""
image Views module
"""
from flask_restful import Resource
import models
from ..serializers.images import ImageSchema
from marshmallow import EXCLUDE
from flask import jsonify, make_response
from utilities.auth_utils import auth_required
from utilities.upload_utils import upload_image, delete_image


image_schema = ImageSchema(unknown=EXCLUDE)
images_schema = ImageSchema(many=True)


class ImageHubList(Resource):
    """Defines get(for all) related to a hub
        and post request of images
    """
    def get(self, hub_id):
        """retrieve all images related to a hub"""
        hub = models.storage.get(models.Hub, id=hub_id)
        images = hub.images
        return (images_schema.dump(images), 200)

    @auth_required(roles=['is_farmer', 'is_admin'])
    def post(self, hub_id):
        """Add an image to the storage"""
        return upload_image(hub_id=hub_id)


class ImageProductList(Resource):
    """Defines get(for all) related to a product
        and post request of images
    """
    def get(self, product_id):
        """retrieve all images related to a product
        Arg:
            product_id: ID of the Product related to the image
        """
        product = models.storage.get(models.Product, id=product_id)
        images = product.images
        return (images_schema.dump(images), 200)

    @auth_required(roles=['is_farmer', 'is_admin'])
    def post(self, product_id):
        """Add an image to the storage"""
        return upload_image(product_id=product_id)


class ImageSingle(Resource):
    """Retrieves a single image, deletes a image
    """
    def get(self, image_id):
        """retrive a single image from the storage
        Arg:
            image_id: ID of the image to retrieve
        """
        image = models.storage.get(models.Image, id=image_id)
        if image:
            return (image_schema.dump(image), 200)

    @auth_required(roles=['is_farmer', 'is_admin'])
    def delete(self, image_id):
        """Delete image
        Arg:
            image_id: ID of the image to be deleted
        """
        image = models.storage.get(models.Image, id=image_id)
        if image:
            delete_image(image.link)
            models.storage.delete(image)
            response = {'message': 'Image successfully deleted'}
            return make_response(jsonify(response), 200)
