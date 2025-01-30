import pytest
from app.server import app, db, User

from werkzeug.security import generate_password_hash


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['WTF_CSRF_ENABLED'] = False

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            user = User(username="testuser", password=generate_password_hash("password"))
            db.session.add(user)
            db.session.commit()
        yield client
        with app.app_context():
            db.drop_all()


def test_register(client):
    """Test user registration."""
    response = client.post('/register', data={'username': 'newuser', 'password': 'newpass'}, follow_redirects=True)
    assert b'Username is taken' not in response.data
    assert response.status_code == 200


def test_login(client):
    """Test login with valid credentials."""
    response = client.post('/login', data={'username': 'testuser', 'password': 'password'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Invalid credentials' not in response.data


def test_login_invalid(client):
    """Test login with invalid credentials."""
    response = client.post('/login', data={'username': 'testuser', 'password': 'wrongpassword'}, follow_redirects=True)
    assert b'Invalid credentials' in response.data


def test_protected_route(client):
    """Ensure home route requires login."""
    response = client.get('/home', follow_redirects=True)
    assert b'Login' in response.data


def test_add_food(client):
    """Test adding food."""
    client.post('/login', data={'username': 'testuser', 'password': 'password'}, follow_redirects=True)
    response = client.post('/add', data={
        'name': 'Apple',
        'meal': 'True',
        'price': '1.5',
        'calories': '95',
        'proteins': '0.5',
        'fats': '0.3',
        'time': '2025-01-30'
    }, follow_redirects=True)
    assert b'Food added successfully!' in response.data


def test_logout(client):
    """Test logout."""
    client.post('/login', data={'username': 'testuser', 'password': 'password'}, follow_redirects=True)
    response = client.get('/logout', follow_redirects=True)
    assert b'Login' in response.data
