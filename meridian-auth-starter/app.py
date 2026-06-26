"""Meridian Labs - tiny demo API (starter). Auth lives in auth.py."""
from flask import Flask, request, jsonify
import auth

app = Flask(__name__)


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(force=True)
    token = auth.login(data.get("email"), data.get("password"))
    if not token:
        return jsonify({"error": "invalid credentials"}), 401
    return jsonify({"token": token})


@app.route("/me", methods=["GET"])
def me():
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    user = auth.verify(token)
    if not user:
        return jsonify({"error": "unauthorized"}), 401
    return jsonify({"user": user})


if __name__ == "__main__":
    app.run(port=5000, debug=True)
