import unittest
from usermanager import UserManager


class TestUserManager(unittest.TestCase):

    def test_create_user(self):
        mock_usermanager = UserManager()

        r = mock_usermanager.new_user(username="username",
                                  email="foo@bar.com",
                                  firstname="firstname",
                                  lastname="lastname")

        self.assertTrue(r)


if __name__ == '__main__':
    unittest.main()
