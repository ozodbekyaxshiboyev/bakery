from enum import Enum


class Status(Enum):
    new = 'new'
    confirmed = 'confirmed'
    cancelled = 'cancelled'
    success = 'success'

    @classmethod
    def choices(cls):
        return ((i.name, i.value) for i in cls)

