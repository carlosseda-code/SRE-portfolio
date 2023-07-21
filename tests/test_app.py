# test_app.py

import unittest
import os
os.environ["TESTING"] = "true"

from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home(self):
        response = self.client.get('/')
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<title>Carlos Seda's Portfolio</title>" in html
        assert "<h1>Hi, I'm Carlos Seda from Monterrey, Nuevo Leon</h1>"
        assert "About Me" in html
        assert "My Experience" in html
        assert "My Projects" in html

    def test_timeline(self):
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 0

        response1 = self.client.post("/api/timeline_post", data={
            'name': 'John Doe',
            'email': 'john@example.com',
            "content": "Hello World\nI\'m John"
        })
        assert response1.status_code == 200

        response2 = self.client.post("/api/timeline_post", data={
            "name": "Jane Doe",
            "email": "jane@example.com",
            "content": "Hello World\nI\'m Jane"
        })
        assert response2.status_code == 200

        response3 = self.client.get("/api/timeline_post")
        assert response3.status_code == 200
        assert response3.is_json

        json = response3.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 2

        posts = json["timeline_posts"]
        assert posts[0]["name"] == "Jane Doe"
        assert posts[1]["name"] == "John Doe"

        response4 = self.client.get("/timeline")
        assert response4.status_code == 200

    def test_malformed_timeline_post(self):

        response = self.client.post("/api/timeline_post", data={
            "name": "",
            "email": "john@example.com",
            "content": "Hello World, I'm John"
        })
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid name" in html

        response1 = self.client.post("/api/timeline_post", data={
            "name": "John Doe",
            "email": "john@example.com",
            "content": ""
        })
        assert response1.status_code == 400
        html = response1.get_data(as_text=True)
        assert "Invalid content" in html

        response2 = self.client.post("/api/timeline_post", data={
            "name": "John Doe",
            "email": "not-an-email",
            "content": "Hello World, I'm John"
        })
        assert response2.status_code == 400
        html = response2.get_data(as_text=True)
        assert "Invalid email" in html
