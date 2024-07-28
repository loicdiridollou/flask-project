"""Test application home page."""

from flaskr.application import application


def test_home():
    """Test home page of the application."""
    response = application.test_client().get("/")

    assert response.status_code == 200
