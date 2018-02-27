import unittest
from DSCComment import DSCComment
from DSCComment import Action


class DSCCommentTest(unittest.TestCase):
    def setUp(self):
        self.ds_mark = "//^_^"
        self.time = "2017/02/26"
        self.staff = "07079"
        self.cmf = "abc_efg"

        self.comment = DSCComment(self.cmf, self.time)

        self.history_file = ""

    def test_get_comment_for_a_line(self):
        expect = "{} {} add by {} for {}".format(self.ds_mark, self.time, self.staff, self.cmf)
        self.assertEqual(self.comment.get_comment(Action.add), expect)
        self.assertEqual(self.comment.get_comment(1), expect)

        expect = "{} {} modi by {} for {}".format(self.ds_mark, self.time, self.staff, self.cmf)
        self.assertEqual(self.comment.get_comment(Action.modi), expect)
        self.assertEqual(self.comment.get_comment(2), expect)

        expect = "{} {} mark by {} for {}".format(self.ds_mark, self.time, self.staff, self.cmf)
        self.assertEqual(self.comment.get_comment(Action.mark), expect)
        self.assertEqual(self.comment.get_comment(3), expect)

        expect = "{} {} Copy PKG(%S) by {} for {}".format(self.ds_mark, self.time, self.staff, self.cmf)
        self.assertEqual(self.comment.get_comment(Action.copy), expect)
        self.assertEqual(self.comment.get_comment(4), expect)

    def test_get_comment_for_lines(self):
        expect = "{} {} add by {} for {}".format(self.ds_mark, self.time, self.staff, self.cmf)
        expect = "{comment} ↓↓↓\r\n{comment} ↑↑↑\r\n".format(comment=expect)
        self.assertEqual(self.comment.get_comment(Action.add, True), expect)
        self.assertEqual(self.comment.get_comment(1, True), expect)

        expect = "{} {} modi by {} for {}".format(self.ds_mark, self.time, self.staff, self.cmf)
        expect = "{comment} ↓↓↓\r\n{comment} ↑↑↑\r\n".format(comment=expect)
        self.assertEqual(self.comment.get_comment(Action.modi, True), expect)
        self.assertEqual(self.comment.get_comment(2, True), expect)

        expect = "{} {} mark by {} for {}".format(self.ds_mark, self.time, self.staff, self.cmf)
        expect = "{comment} ↓↓↓\r\n{comment} ↑↑↑\r\n".format(comment=expect)
        self.assertEqual(self.comment.get_comment(Action.mark, True), expect)
        self.assertEqual(self.comment.get_comment(3, True), expect)

        expect = "{} {} Copy PKG(%S) by {} for {}".format(self.ds_mark, self.time, self.staff, self.cmf)
        expect = "{comment} ↓↓↓\r\n{comment} ↑↑↑\r\n".format(comment=expect)
        self.assertEqual(self.comment.get_comment(Action.copy, True), expect)
        self.assertEqual(self.comment.get_comment(4, True), expect)

    def test_do_line_comment_with_act_is_not_mark_and_char_less_than_or_eq_max_char_per_line_(self):
        s = "".join("a" for _ in range(1, self.comment.MAX_CHAR_OF_LINE - 1))
        expect = "{} {} {} add by {} for {}\r\n".format(s, self.ds_mark, self.time, self.staff, self.cmf)
        self.assertEqual(self.comment.do_line_comment(Action.add, s), expect)

        s = "".join("a" for _ in range(1, self.comment.MAX_CHAR_OF_LINE))
        expect = "{} {} {} add by {} for {}\r\n".format(s, self.ds_mark, self.time, self.staff, self.cmf)
        self.assertEqual(self.comment.do_line_comment(Action.add, s), expect)

        s = "".join("a" for _ in range(1, self.comment.MAX_CHAR_OF_LINE - 1))
        expect = "{} {} {} add by {} for {}\r\n".format(s, self.ds_mark, self.time, self.staff, self.cmf)
        self.assertEqual(self.comment.do_line_comment(Action.add, (s + "\r\n")), expect)

        s = "".join("a" for _ in range(1, self.comment.MAX_CHAR_OF_LINE))
        expect = "{} {} {} add by {} for {}\r\n".format(s, self.ds_mark, self.time, self.staff, self.cmf)
        self.assertEqual(self.comment.do_line_comment(Action.add, (s + "\r\n")), expect)

        s = ""
        expect = "\r\n"
        self.assertEqual(self.comment.do_line_comment(Action.add, s), expect)

    def test_do_line_comment_with_act_is_mark_and_char_less_than_or_eq_max_char_per_line_after_add_comment_mark(self):
        s = "".join("a" for _ in range(1, self.comment.MAX_CHAR_OF_LINE - 10))
        expect = "// {} {} {} mark by {} for {}\r\n".format(s, self.ds_mark, self.time, self.staff, self.cmf)
        self.assertEqual(self.comment.do_line_comment(Action.mark, s), expect)

        s = "".join("a" for _ in range(1, self.comment.MAX_CHAR_OF_LINE - 10))
        s = "   " + s
        expect = "   // {} {} {} mark by {} for {}\r\n".format(s.strip(), self.ds_mark, self.time, self.staff, self.cmf)
        self.assertEqual(self.comment.do_line_comment(Action.mark, s), expect)

        s = "".join("a" for _ in range(1, self.comment.MAX_CHAR_OF_LINE - 3))
        expect = "// {} {} {} mark by {} for {}\r\n".format(s, self.ds_mark, self.time, self.staff, self.cmf)
        self.assertEqual(self.comment.do_line_comment(Action.mark, s), expect)

        s = "".join("a" for _ in range(1, self.comment.MAX_CHAR_OF_LINE - 6))
        s = "   " + s
        expect = "   // {} {} {} mark by {} for {}\r\n".format(s.strip("\r\n").strip(), self.ds_mark, self.time,
                                                               self.staff, self.cmf)
        self.assertEqual(self.comment.do_line_comment(Action.mark, s), expect)

        s = ""
        expect = "\r\n"
        self.assertEqual(self.comment.do_line_comment(Action.mark, s), expect)

    def test_do_block_comment_with_act_is_not_mark_and_aligned_lines(self):
        comment = "{} {} add by {} for {}".format(self.ds_mark, self.time, self.staff, self.cmf)

        s = "\r\n\r\n"
        expect = ""
        self.assertEqual(self.comment.do_block_comment(Action.add, s), expect)

        s = "\r\na\r\n"
        expect = "{comment} ↓↓↓\r\n\r\na\r\n{comment} ↑↑↑\r\n".format(comment=comment)
        self.assertEqual(self.comment.do_block_comment(Action.add, s), expect)

        s = "   \r\n   a\r\n"
        expect = "   {comment} ↓↓↓\r\n   \r\n   a\r\n   {comment} ↑↑↑\r\n".format(comment=comment)
        self.assertEqual(self.comment.do_block_comment(Action.add, s), expect)

    def test_do_block_comment_with_act_is_mark_and_aligned_lines(self):
        comment = "{} {} mark by {} for {}".format(self.ds_mark, self.time, self.staff, self.cmf)

        s = "\r\n\r\n"
        expect = ""
        self.assertEqual(self.comment.do_block_comment(Action.mark, s), expect)

        s = "\r\na\r\n"
        expect = "{comment} ↓↓↓\r\n//\r\n// a\r\n{comment} ↑↑↑\r\n".format(comment=comment)
        self.assertEqual(self.comment.do_block_comment(Action.mark, s), expect)

        s = "   \r\n   a\r\n"
        expect = "   {comment} ↓↓↓\r\n   // \r\n   // a\r\n   {comment} ↑↑↑\r\n".format(comment=comment)
        self.assertEqual(self.comment.do_block_comment(Action.mark, s), expect)

    def test_do_block_comment_with_act_is_not_mark_and_lines_is_not_aligned(self):
        comment = "{} {} add by {} for {}".format(self.ds_mark, self.time, self.staff, self.cmf)

        s = "\r\n     a\r\n"
        expect = "{comment} ↓↓↓\r\n\r\n     a\r\n{comment} ↑↑↑\r\n".format(comment=comment)
        self.assertEqual(self.comment.do_block_comment(Action.add, s), expect)

        s = "     \r\na\r\n"
        expect = "{comment} ↓↓↓\r\n     \r\na\r\n{comment} ↑↑↑\r\n".format(comment=comment)
        self.assertEqual(self.comment.do_block_comment(Action.add, s), expect)

        s = "    \r\n  a\r\n"
        expect = "  {comment} ↓↓↓\r\n    \r\n  a\r\n  {comment} ↑↑↑\r\n".format(comment=comment)
        self.assertEqual(self.comment.do_block_comment(Action.add, s), expect)

    def test_do_block_comment_with_act_is_mark_and_lines_is_not_aligned(self):
        comment = "{} {} mark by {} for {}".format(self.ds_mark, self.time, self.staff, self.cmf)

        s = "\r\n     a\r\n"
        expect = "{comment} ↓↓↓\r\n//\r\n//      a\r\n{comment} ↑↑↑\r\n".format(comment=comment)
        self.assertEqual(self.comment.do_block_comment(Action.mark, s), expect)

        s = "     \r\na\r\n"
        expect = "{comment} ↓↓↓\r\n//      \r\n// a\r\n{comment} ↑↑↑\r\n".format(comment=comment)
        self.assertEqual(self.comment.do_block_comment(Action.mark, s), expect)

        s = "     \r\n   a\r\n"
        expect = "   {comment} ↓↓↓\r\n   //   \r\n   // a\r\n   {comment} ↑↑↑\r\n".format(comment=comment)
        self.assertEqual(self.comment.do_block_comment(Action.mark, s), expect)

    def test_do_line_comment_with_act_is_not_mark_and_char_greater_than_max_char_per_line_(self):
        s = "".join("a" for _ in range(1, self.comment.MAX_CHAR_OF_LINE + 5))
        expect = "{} {} add by {} for {}".format(self.ds_mark, self.time, self.staff, self.cmf)
        expect = "{comment} ↓↓↓\r\n{}\r\n{comment} ↑↑↑\r\n".format(s, comment=expect)
        self.assertEqual(self.comment.do_line_comment(Action.add, s), expect)

    def test_do_line_comment_with_line_contain_comment_mark(self):
        comment = "{} {} add by {} for {}\r\n".format(self.ds_mark, self.time, self.staff, self.cmf)
        s = "aa //abc"
        expect = "aa {} //abc".format(comment)
        self.assertEqual(self.comment.do_line_comment(Action.add, s), expect)


if __name__ == '__main__':
    unittest.main()