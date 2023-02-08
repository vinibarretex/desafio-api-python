from flask import json, jsonify, request

def health():
    """
    Status da API
    """
    responseBody = {
        "data": "null",
        "success": "true"
    }
    return jsonify(responseBody)
