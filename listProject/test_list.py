import pytest
from listProject import app, db
from listProject.models import Item, User


class TestCase:
    def setup_class(self):
        app.config.update(
            TESTING=True
        )

        self.client = app.test_client()
        self.runner = app.test_cli_runner()
        print('go!!')

    def teardown_class(self):
        print('over!!')

    def teardown(self):
        self.logout()

    def test_app_exist(self):
        assert app

    # 测试程序是否处于测试模式
    def test_app_is_testing(self):
        assert app.config['TESTING']

    def test_404_page(self):
        response = self.client.get('/nothing')  # 传入目标 URL
        data = response.get_data(as_text=True)
        assert 'Page Not Found - 404' in data
        assert 'Go Back' in data
        assert response.status_code == 404

    def test_index_page(self):
        response = self.client.get('/')
        data = response.get_data(as_text=True)
        assert 'DiuDiu', 'pytest' in data
        assert response.status_code == 200

    @pytest.fixture()
    def login(self):
        self.client.post('/login', data=dict(
            username='DiuDiu',
            password='123123'
        ), follow_redirects=True)

    def logout(self):
        self.client.get('/logout')

    def test_before_login_movie(self):
        response = self.client.get('/movie')  # 传入目标 URL
        data = response.get_data(as_text=True)
        assert 'Add' not in data
        assert 'Login' in data
        assert 'Logout', 'Settings' not in data

    def test_after_login_movie(self, login):
        response = self.client.get('/movie')  # 传入目标 URL
        data = response.get_data(as_text=True)
        assert 'Logout', 'Settings' in data
        assert 'Add' and 'Edit' and 'Delete' in data
        assert 'Login' not in data

    def test_before_login_book(self):
        response = self.client.get('/book')  # 传入目标 URL
        data = response.get_data(as_text=True)
        assert 'Add' not in data
        assert 'Login' in data
        assert 'Logout', 'Settings' not in data

    def test_after_login_book(self, login):
        response = self.client.get('/book')
        data = response.get_data(as_text=True)
        assert 'Logout', 'Settings' in data
        assert 'Add' and 'Edit' and 'Delete' in data
        assert 'Login' not in data

    def test_before_login_store(self):
        response = self.client.get('/store')  # 传入目标 URL
        data = response.get_data(as_text=True)
        assert 'Add' not in data
        assert 'Login' in data
        assert 'Logout', 'Settings' not in data

    def test_after_login_store(self, login):
        response = self.client.get('/store')
        data = response.get_data(as_text=True)
        assert 'Logout', 'Settings' in data
        assert 'Add' and 'Edit' and 'Delete' in data
        assert 'Login' not in data

    def test_before_login_place(self):
        response = self.client.get('/place')  # 传入目标 URL
        data = response.get_data(as_text=True)
        assert 'Add' not in data
        assert 'Login' in data
        assert 'Logout', 'Settings' not in data

    def test_after_login_place(self, login):
        response = self.client.get('/place')
        data = response.get_data(as_text=True)
        assert 'Logout', 'Settings' in data
        assert 'Add' and 'Edit' and 'Delete' in data
        assert 'Login' not in data
