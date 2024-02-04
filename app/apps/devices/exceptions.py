class ObjectNotFound(Exception):
    pass


class DeviceNotOwned(Exception):
    pass


class InvalidForm(Exception):
    def __init__(self, errors, *args):
        super().__init__(args)
        self.errors = errors
