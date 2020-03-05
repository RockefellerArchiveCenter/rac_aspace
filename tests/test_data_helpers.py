"""
Unit tests for Data Helpers
"""
import unittest

from rac_aspace import data_helpers


class TestDataHelpers(unittest.TestCase):

    def test_helpers(self):
        pass

    def test_strip_html_tags(self):
        input = "<h1>Title</h1><p>This is <i>some</i> text! It is wrapped in a \
                variety of html tags, which should <strong>all</strong> be \
                stripped &amp; not returned.</p>"
        expected = "TitleThis is some text! It is wrapped in a variety of html \
                    tags, which should all be stripped &amp; not returned."
        output = data_helpers.strip_html_tags(input)
        self.assertEqual(
            expected, output,
            "Expected string {} but got {} instead.".format(expected, output))


if __name__ == '__main__':
    unittest.main()
