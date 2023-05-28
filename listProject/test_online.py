import pytest
from listProject import app


class TestCase:
    def setup_class(self):
        self.client = app.test_client()
        # self.runner = app.test_cli_runner()
        print('Ready!')

    def test_app_exist(self):
        assert app

    def test_index(self):
        response = self.client.get('/')
        data = response.get_data(as_text=True)
        assert 'DiuDiu', 'pytest' in data
        assert response.status_code == 200

    def test_movie_page(self):
        response = self.client.get('/movie')
        data = response.get_data(as_text=True)
        assert 'Add' or 'Edit' or 'Delete' not in data
        assert 'Login' and 'Movies' in data
        assert 'Logout' or 'Settings' not in data

    def test_book_page(self):
        response = self.client.get('/book')
        data = response.get_data(as_text=True)
        assert 'Add' or 'Edit' or 'Delete' not in data
        assert 'Login' and 'Books' in data
        assert 'Logout' or 'Settings' not in data

    def test_movie_store(self):
        response = self.client.get('/store')
        data = response.get_data(as_text=True)
        assert 'Add' or 'Edit' or 'Delete' not in data
        assert 'Login' and 'Stores' in data
        assert 'Logout' or 'Settings' not in data

    def test_movie_place(self):
        response = self.client.get('/place')
        data = response.get_data(as_text=True)
        assert 'Add' or 'Edit' or 'Delete' not in data
        assert 'Login' and 'Places' in data
        assert 'Logout' or 'Settings' not in data
