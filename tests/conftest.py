import pytest

from app import create_app, db


@pytest.fixture
def app():
    """テスト用のアプリ。データベースはメモリ上に作り、本番のファイルは触らない"""
    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        }
    )
    yield app
    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()
