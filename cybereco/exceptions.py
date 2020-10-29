import re

__all__ = (
    'InvalidID'
)


class InvalidID(Exception):
    def __init__(self, message='You passed an invalid ID'):
        self.message = message

    def __str__(self):
        return self.message
