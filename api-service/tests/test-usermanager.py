import unittest
from dotenv import load_dotenv

from crunchsql import SqlCondition
from models import User, Device
from models.password import Password
from queries import DeviceEnroller,    \
                    DeviceDisenroller, \
                    DeviceFinder,      \
                    UserFinder,        \
                    UserRegistrator,   \
                    DeviceRegistrator


class TestQueries(unittest.TestCase):

    device_finder = DeviceFinder()
    user_finder = UserFinder()
    device_enroller = DeviceEnroller()
    device_disenroller = DeviceDisenroller()

    mock_user = next(user_finder(where=SqlCondition(username="dev@parkomatic.com")))
    mock_device = next(device_finder(where=SqlCondition(device_id="devtest")))

    def test_devicefinder(self):
        for i in TestQueries.device_finder():
            self.assertIsInstance(i, Device)

    def test_userfinder(self):
        for i in TestQueries.user_finder():
            self.assertIsInstance(i, User)

    def test_device_enroller(self):
        self.assertTrue(TestQueries.device_disenroller(TestQueries.mock_user))
        self.assertTrue(TestQueries.device_enroller(TestQueries.mock_user))

load_dotenv()

user_registrator = UserRegistrator()
device_registrator = DeviceRegistrator()
device_registrator(Device(device_id="devtest"))
user = User(username="dev@parkomatic.com",
            password=Password("password"))


# print(user_registrator(user))

#unittest.main(verbosity=2)

"""
    enroller = DeviceEnroller()
    disenroller = DeviceDisenroller()
    
    mock_user = User()
    mock_device = Device(device_id="2ce2fa33-4abc-4a77-bc3e-aa50b3e2ec88")

    my_user = User()
    my_user.username = "dotchetter@protonmail.ch"

    my_device = Device()
    my_device.device_id = "55b076a9-3efc-4593-9975-25f8048fa56e"



    antons_device = Device()
    antons_device.device_id = "2ce2fa33-4abc-4a77-bc3e-aa50b3e2ec88"

    user_where = SqlConditon()
    user_where["user_id"] = my_user.user_id

    delete_user_cmd = SqlCommand()
    delete_user_cmd.delete_from = getenv("UsersTable")
    delete_user_cmd.where = SqlConditon()
    delete_user_cmd.where["email"] = my_user.email

    print(delete_user_cmd)

    update_device_owner_cmd = SqlCommand()
    update_device_owner_cmd.update = getenv("DevicesTable")
    update_device_owner_cmd.set = SqlConditon()
    update_device_owner_cmd.set["user_id"] = SqlCommand(select="id",
                                                        select_from=getenv("UsersTable"),
                                                        where=user_where)
    update_device_owner_cmd.where = SqlConditon()
    update_device_owner_cmd.where["device_id"] = my_device.device_id

    print(update_device_owner_cmd)

    db = DbManager(getenv("SqlConnectionString"))
    """


