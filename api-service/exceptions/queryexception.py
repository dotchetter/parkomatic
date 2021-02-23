
class DeviceAlreadyEnrolledException(Exception):
    """
    Throwable for scenarios where a request is
    parsed which aims to enroll a device which
    is already enrolled with another user.
    """
    pass


class UsernameTakenException(Exception):
    """
    Throwable for when a username is already
    taken in a database.
    """
    pass


class DeviceAlreadyExistsException(Exception):
    """
    Throwable for when a device already
    exists in the database that shares
    the device_id.
    """
    pass
