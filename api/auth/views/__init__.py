#!/usr/bin/python3
"""
Auth Views module Initiation
"""
from flask import Blueprint
auth_bp = Blueprint('auth_bp', __name__, url_prefix="/api/auth")
