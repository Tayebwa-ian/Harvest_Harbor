#!/usr/bin/python3
"""
Core Views module Initiation
"""
from flask import Blueprint
core_bp = Blueprint('core_bp', __name__, url_prefix="/api/core")
