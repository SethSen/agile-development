import pytest
from myapp import app, db, Locations, RequestLocation


# Sets up a client for testing, with a clean database
@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False
    client = app.test_client()

    with app.app_context():
        db.create_all()

    yield client


# Test that the home page returns a successful response.
def test_home_page(client):
    rv = client.get('/')
    assert rv.status_code == 200


# Test that the request location page returns a successful response.
def test_request_location_page(client):
    rv = client.get('/request-location')
    assert rv.status_code == 200


# Test submitting a form to request a location.
def test_post_request_location(client):
    rv = client.post('/request-location', data={
        'name': 'test',
        'city': 'testcity',
        'address': 'testaddress',
        'hours': 'testhours',
        'link': 'testlink',
        'phone': 'testphone',
        'location_type': 'testtype'
    }, follow_redirects=True)
    assert rv.status_code == 200

    with app.app_context():
        location = RequestLocation.query.filter_by(name='test').first()
        assert location is not None


# Test accessing the admin page without being logged in; should redirect to login.
def test_admin_page_without_login(client):
    rv = client.get('/admin')
    assert rv.status_code == 302  # should redirect to login page


# Test accessing the admin page without being logged in; should redirect to login.
def test_admin_page_with_login(client):
    with client.session_transaction() as sess:
        sess['admin'] = 'admin'
    rv = client.get('/admin')
    assert rv.status_code == 200
