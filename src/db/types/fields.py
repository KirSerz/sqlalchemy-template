import json

from sqlalchemy.types import TypeDecorator, Text, String

from crypto.password import PasswordHash


class JSONEncodedDict(TypeDecorator):

    impl = Text

    def process_bind_param(self, value, dialect):
        if isinstance(value, dict | list | tuple):
            return json.dumps(value, separators=(",", ":"))
        elif isinstance(value, str):
            json.loads(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value


class Password(TypeDecorator):
    """Allows storing and retrieving password hashes using PasswordHash."""

    impl = String

    def __init__(self, rounds=12, **kwds):
        self.rounds = rounds
        super(Password, self).__init__(**kwds)

    def process_bind_param(self, value, dialect):
        """Ensure the value is a PasswordHash and then return its hash."""
        if value is not None:
            return self._convert(value).hash
        return None

    def process_result_value(self, value, dialect):
        """Convert the hash to a PasswordHash, if it's non-NULL."""
        if value is not None:
            return PasswordHash(value, rounds=self.rounds)
        return None

    def validator(self, password):
        """Provides a validator/converter for @validates usage."""
        return self._convert(password)

    def _convert(self, value):
        """Returns a PasswordHash from the given string.

        PasswordHash instances or None values will return unchanged.
        Strings will be hashed and the resulting PasswordHash returned.
        Any other input will result in a TypeError.
        """
        if isinstance(value, PasswordHash):
            return value
        elif isinstance(value, str):
            return PasswordHash.new(value, self.rounds)
        elif value is not None:
            raise TypeError("Cannot convert {} to a PasswordHash".format(type(value)))
        return None
