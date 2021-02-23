import unittest
from os import getenv
from dotenv import load_dotenv
from crunchsql import SqlCommand, SqlCondition
from models import User, Device
from models.password import Password
from queries import DeviceEnroller,    \
                    DeviceDisenroller, \
                    DeviceFinder,      \
                    UserFinder,        \
                    UserRegistrator,   \
                    DeviceRegistrator

load_dotenv()


class TestQueriesAgainstDatabase(unittest.TestCase):

    device_finder = DeviceFinder()
    user_finder = UserFinder()
    device_enroller = DeviceEnroller()
    device_disenroller = DeviceDisenroller()

    mock_user = next(user_finder(where=SqlCondition(username="dev@parkomatic.com")))
    mock_device = next(device_finder(where=SqlCondition(device_id="devtest")))

    def test_devicefinder(self):
        for i in TestQueriesAgainstDatabase.device_finder(where=SqlCondition(
                device_id=TestQueriesAgainstDatabase.mock_device.device_id)):
            self.assertIsInstance(i, Device)

    def test_userfinder(self):
        for i in TestQueriesAgainstDatabase.user_finder(where=SqlCondition(
                user_id=TestQueriesAgainstDatabase.mock_user.user_id)):
            self.assertIsInstance(i, User)

    def test_device_enroller(self):
        self.assertTrue(TestQueriesAgainstDatabase.device_disenroller(
            TestQueriesAgainstDatabase.mock_device))

        self.assertTrue(TestQueriesAgainstDatabase.device_enroller(
            TestQueriesAgainstDatabase.mock_user,
            TestQueriesAgainstDatabase.mock_device))


if __name__ == "__main__":
    unittest.main(verbosity=4)


