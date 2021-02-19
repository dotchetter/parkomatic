from datetime import datetime
import secrets
import hashlib
import hmac


class Password:
    """
    Represent a password for a user.
    The Password object is responsible in
    itself to hash the plain text password
    that is being assigned to it in CTOR or
    by methods, thus the plain text password
    is never stored in this object(!).
    """

    HASH_NUM_ITER = 1000000

    def __init__(self, plaintext_password=str(),
                 hashed_password=str(),
                 salt_hex=str()):

        self._hashed_password = hashed_password
        self._salt = bytes().fromhex(salt_hex) if salt_hex else bytes()
        self._created_at: datetime = datetime.now()

        if plaintext_password:
            self.__hash_password(plaintext_password)

    def __repr__(self):
        return self._hashed_password

    def __eq__(self, compare: str):
        """
        Verifies the validity of a provided plain
        text string against the hashed value of the
        contents in self.
        :param compare: Plain text password for assertion
        :return: bool, password matched
        """
        compare_hash_hex = hashlib.pbkdf2_hmac("sha3-512",
                                               compare.encode(),
                                               self._salt,
                                               Password.HASH_NUM_ITER).hex()

        return hmac.compare_digest(self._hashed_password, compare_hash_hex)

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def hashed_password(self) -> str:
        return self._hashed_password

    @property
    def salt(self) -> str:
        return self._salt.hex() if self._salt else bytes().hex()

    @salt.setter
    def salt(self, value: str):
        self._salt = bytes().fromhex(value)

    def __hash_password(self, plaintext_password: str) -> None:
        self._salt = secrets.token_bytes(32)
        dk = hashlib.pbkdf2_hmac("sha3-512",
                                 plaintext_password.encode("utf-8"),
                                 self._salt,
                                 Password.HASH_NUM_ITER)
        self._hashed_password = dk.hex()
