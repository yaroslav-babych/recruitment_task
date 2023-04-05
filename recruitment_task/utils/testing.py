from django.test import TestCase

class AnyValue:
    def __init__(self, class_):
        self.class_ = class_

    def __eq__(self, other):
        self.class_(other)
        return True

    def __ne__(self, other):
        self.class_(other)
        return False


class BaseTestCase(TestCase):
    pass
