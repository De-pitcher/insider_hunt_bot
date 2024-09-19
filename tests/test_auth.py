# tests/test_auth.py
import unittest
from src.auth import authenticate_twitter


class TestAuth(unittest.TestCase):
    def test_authentication(self):
        api = authenticate_twitter()
        self.assertIsNotNone(api)
        self.assertTrue(api.verify_credentials())


if __name__ == "__main__":
    unittest.main()
