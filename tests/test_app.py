import unittest
import warnings

warnings.filterwarnings("ignore")
warnings.simplefilter("ignore", ResourceWarning)


class TestApp(unittest.TestCase):
    def test_app(self):
        from app import app

        print("Successfully imported app")
