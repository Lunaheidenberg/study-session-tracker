import sys
from pathlib import Path
from unittest.mock import patch


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from main import app


def test_health():
    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "healthy"}

def test_add_session():
    client = app.test_client()

    with patch("main.db") as mock_redis:
        response = client.post(
            "/sessions",
            json={"minutes": 45}
        )

        assert response.status_code == 201
        assert response.get_json() == {
            "message": "Session recorded",
            "minutes": 45
        }

        mock_pipeline = (
            mock_redis.pipeline.return_value
            .__enter__.return_value
        )

        mock_redis.pipeline.assert_called_once_with(
            transaction=True
        )

        mock_pipeline.incr.assert_called_once_with(
            "total_sessions"
        )

        mock_pipeline.incrby.assert_called_once_with(
            "total_minutes", 45
        )

        mock_pipeline.execute.assert_called_once()

def test_invalid_session():
    client = app.test_client()

    response = client.post(
        "/sessions",
        json={"minutes": -10}
    )

    assert response.status_code == 400
    assert response.get_json() == {
        "error": "Invalid minutes"
    }