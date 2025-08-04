import bcrypt
from sqlalchemy.ext.mutable import Mutable


class PasswordHash(Mutable):
    def __init__(self, hash_: str, rounds: int = 12):
        self.hash = str(hash_)
        self.rounds = rounds

    def __repr__(self):
        """Simple object representation."""
        return "<{}>".format(type(self).__name__)

    @classmethod
    def coerce(cls, key: str, value):
        """Ensure that loaded values are PasswordHashes."""
        if isinstance(value, PasswordHash):
            return value
        return super(PasswordHash, cls).coerce(key, value)

    @classmethod
    def new(cls, password: str, rounds: int | None = None):
        """Returns a new PasswordHash object for the given password and rounds."""
        return cls(cls._new(password, rounds))

    @staticmethod
    def _new(password: str, rounds: int | None = None):
        """Returns a new crypt hash for the given password and rounds."""
        salt = bcrypt.gensalt(rounds)
        hashed = bcrypt.hashpw(password.encode(), salt)
        return hashed.decode()

    def _rehash(self, password: str):
        """Recreates the internal hash and marks the object as changed."""
        self.hash = self._new(password, self.rounds)
        self.changed()
