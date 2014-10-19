import os
import unittest


class TestBase(unittest.TestCase):
    RESOURCE_DIR = os.path.abspath('./test/rsrc')
    
    def setUp(self):
        pass
