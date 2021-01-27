from models.sqlcommand import SqlCommand
from models.password import Password
from models.user import User


if __name__ == "__main__":

    user = User()
    user.username = "dotchetter"
    user.email = "dotchetter@protonmail.ch"
    user.password = Password("password123")

    user.sql_serialize()

    get_device_id = SqlCommand()
    get_device_id.select = "id"
    get_device_id.select_from = "devices"
    get_device_id.where = {"device_id": "device_id_here"}

    insert_message = SqlCommand()
    insert_message.insert_into = "users"
    insert_message.columns = user.columns
    insert_message.values = user.values

    print(insert_message)