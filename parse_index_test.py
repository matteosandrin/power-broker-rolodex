import unittest
import parse_index


class TestParseIndex(unittest.TestCase):

    def test_parse_index_line_1(self):
        line = "Swarthe, Leonard, 874 swimming pools, 454, 456-7, 487, 512-13;"
        r = parse_index.parse_index_line(line)
        self.assertEqual(r, {
            "first": "Leonard",
            "last": "Swarthe",
            "parentheses": "",
            "pages": [454, 456, 457, 487, 512, 513, 874]
        })

    def test_parse_index_line_2(self):
        line = "Walker, James J., 321, 324-8, 347, 713; as mayor, 20, 210, 321, 324-8, 332, 333 \"., 336, 338-9, 340, 344, 353, 357, 375, 446, 465, 615, 779; in N.Y.S. Senate, 136-7, 139, 141, 201, 320; playboy habits of, 320-1, 338-9, 397, 605, 799, 996; and Smith, 320-1, 380, 398, 401; and Tammany, 321, 324, 712 n., 787"
        r = parse_index.parse_index_line(line)
        self.assertEqual(r, {
            "first": "James J.",
            "last": "Walker",
            "parentheses": "",
            "pages": [20, 136, 137, 139, 141, 201, 210, 320, 321, 324, 325,
                      326, 327, 328, 332, 333, 336, 338, 339, 340, 344, 347,
                      353, 357, 375, 380, 397, 398, 401, 446, 465, 605, 615,
                      712, 713, 779, 787, 799, 996]
        })

    def test_parse_page_list_default(self):
        pages_str = "1, 5, 7"
        r = parse_index.parse_page_list(pages_str)
        self.assertEqual(r, [
            1, 5, 7
        ])

    def test_parse_page_list_range_1char(self):
        pages_str = "1, 10-12, 20"
        r = parse_index.parse_page_list(pages_str)
        self.assertEqual(r, [
            1, 10, 11, 12, 20
        ])

    def test_parse_page_list_range_2char(self):
        pages_str = "1, 119-22, 130"
        r = parse_index.parse_page_list(pages_str)
        self.assertEqual(r, [
            1, 119, 120, 121, 122, 130
        ])


if __name__ == '__main__':
    unittest.main()
