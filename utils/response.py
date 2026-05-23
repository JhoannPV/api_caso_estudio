from flask import jsonify


def success_response(data, status=200):
    return jsonify({"ok": True, "data": data}), status


def error_response(message, status=400):
    return jsonify({"ok": False, "error": message}), status
