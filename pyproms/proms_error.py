class PromsDataModelError(Exception):
    def __init__(self, arg):
        # Set some exception information
        self.msg = arg