import unittest

#username:admin & user
#password:admin & user

class Testgp9(unittest.TestCase):

    def SetUp(self):
        self.username = "admin"
        self.password = "admin"
        self.username2 = "user"
        self.password2 = "user"
        self.emailcontent = "I am sending this email to test the system"
        self.sender = "admin"
        self.receiver = "user"
        self.title = "test this message"

    def test_login(self):
        self.assertEqual(username, "admin")
        self.assertEqual(password, "admin")

        self.assertEqual(username2, "user")
        self.assertEqual(password2, "user")

    def test_emailsent:
        self.assertTrue

    if __name__ == '__main__':
        unittest.main()
