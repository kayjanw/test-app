import unittest
import warnings

warnings.filterwarnings("ignore")
warnings.simplefilter("ignore", ResourceWarning)


class TestImport(unittest.TestCase):
    def test_import(self):
        import nltk
        from nltk.corpus import stopwords, wordnet

        stopwords.words("english")
        try:
            wordnet.ensure_loaded()
        except AttributeError:
            wordnet.ensure_loaded()
        print("Successfully imported nltk")
