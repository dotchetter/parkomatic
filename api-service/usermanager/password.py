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

    def __init__(self, plaintext_password: str = None):
        self._hashed_password: str
        self._salt: bytes
        self._created_at: datetime = datetime.now()

        if plaintext_password:
            self.__hash_password(plaintext_password)

    def __repr__(self):
        return f"Password(created: {self._created_at}, hash: {self._hashed_password}, " \
               f"salt: {self._salt})"

    def __str__(self):
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
        return self._hashed_password if self._hashed_password else None

    @property
    def salt(self) -> bytes:
        return self._salt if self._salt else None

    @property
    def created_at(self) -> datetime:
        return self._created_at

    def __hash_password(self, plaintext_password: str) -> None:
        self._salt = secrets.token_bytes(16)
        dk = hashlib.pbkdf2_hmac("sha3-512",
                                 plaintext_password.encode("utf-8"),
                                 self._salt,
                                 Password.HASH_NUM_ITER)

        self._hashed_password = dk.hex()
