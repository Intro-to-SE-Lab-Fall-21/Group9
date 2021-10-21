import unittest

//username:admin
//password:admin

class Testgp9(unittest.TestCase):

    def SetUp(self):
        self.username = "admin"
        self.password = "admin"

    def test_login(self):
        self.assertTrue('admin')
