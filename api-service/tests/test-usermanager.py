import unittest
from usermanager import UserManager


class TestUserManager(unittest.TestCase):

    def test_create_user(self):
        mock_usermanager = UserManager()

        r = mock_usermanager.new_user(username="username",
                                      email="foo@bar.com",
                                      firstname="firstname",
                                      lastname="lastname",
                                      password_plaintext="password")

        self.assertTrue(r)

    def test_delete_user(self):
        mock_usermanager = UserManager()
        mock_usermanager.new_user(username="username",
                                  email="foo@bar.com",
                                  firstname="firstname",
                                  lastname="lastname",
                                  password_plaintext="password")

        r = mock_usermanager.delete_user("username")
        self.assertTrue(r)


if __name__ == '__main__':
    unittest.main()