import os
import redis
from flask import Flask, request, jsonify

app = Flask(__name__)

db = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=6379,
    decode_responses=True
)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"})


@app.route("/sessions", methods=["POST"])
def add_session():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Invalid JSON"}), 400

    minutes = data.get("minutes")

    if type(minutes) is not int or minutes <= 0:
        return jsonify({"error": "Invalid minutes"}), 400

    with db.pipeline(transaction=True) as pipe:
        pipe.incr("total_sessions")
        pipe.incrby("total_minutes", minutes)
        pipe.execute()

    return jsonify({
        "message": "Session recorded",
        "minutes": minutes
    }), 201


@app.route("/stats", methods=["GET"])
def stats():
    return jsonify({
        "total_sessions": int(db.get("total_sessions") or 0),
        "total_minutes": int(db.get("total_minutes") or 0)
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)