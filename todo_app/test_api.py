import unittest

import flask_sqlalchemy

# app.py 는 MySQL 주소를 쓰고, import 되는 순간 데이터베이스가 그 주소로 묶입니다.
# 그 뒤에 주소를 바꿔도 소용이 없어서, 테스트의 drop_all() 이 진짜 DB 를 지울 수 있습니다.
# 그래서 app.py 를 import 하기 전에, 주소를 메모리 SQLite 로 바꿔 둡니다. (app.py 는 건드리지 않습니다)
_original_init_app = flask_sqlalchemy.SQLAlchemy.init_app


def _init_app_in_memory(self, app):
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    _original_init_app(self, app)


flask_sqlalchemy.SQLAlchemy.init_app = _init_app_in_memory

import app as todo_app          # 2차시에 친 app.py 를 가져온다

flask_sqlalchemy.SQLAlchemy.init_app = _original_init_app


class TodoApiTest(unittest.TestCase):

    def setUp(self):            # 테스트 하나마다 먼저 돈다
        todo_app.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        todo_app.app.config["TESTING"] = True
        self.client = todo_app.app.test_client()
        self.ctx = todo_app.app.app_context()
        self.ctx.push()
        todo_app.db.drop_all()
        todo_app.db.create_all()

    def tearDown(self):         # 끝날 때마다 돈다
        todo_app.db.session.remove()
        self.ctx.pop()
