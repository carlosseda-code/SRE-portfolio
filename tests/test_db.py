# test_db.py

import unittest
from peewee import *

from app import TimelinePost

MODELS = [TimelinePost]

test_db = SqliteDatabase(':memory:')

class TestTimelinePost(unittest.TestCase):
    def setUp(self):
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)
        test_db.connect()
        test_db.create_tables(MODELS)

    def tearDown(self):
        test_db.drop_tables(MODELS)
        test_db.close()

    def test_timeline_post(self):
        first_post = TimelinePost.create(name="John Doe", email="john@example.com", content="Hello World\nI\'m John")
        assert first_post.id == 1
        second_post = TimelinePost.create(name="Jane Doe", email="jane@example.com", content="Hello World\nI\'m Jane")
        assert second_post.id == 2

        posts = TimelinePost.select().order_by(TimelinePost.created_at.desc())
        assert posts.count() == 2

        for post in posts:
            if post.id == 1:
                assert post.name == "John Doe"
                assert post.email == "john@example.com"
                assert post.content == "Hello World\nI\'m John"
            elif post.id == 2:
                assert post.name == "Jane Doe"
                assert post.email == "jane@example.com"
                assert post.content == "Hello World\nI\'m Jane"