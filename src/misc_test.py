from unittest import main, TestCase

from src.misc import multiline


class MiscMultiline(TestCase):
    def test_it_dedents(self):
        self.assertEqual("i like\n  potatoes", multiline("""
            i like
              potatoes
        """))

    def test_it_trims_whitespace(self):
        self.assertEqual("", multiline("""
        """))

        self.assertEqual("", multiline("""
        
        """))


if __name__ == '__main__':
    main()
