import datetime
from enum import Enum
import re
import unittest


class Action(Enum):
    add = 1
    modi = 2
    mark = 3
    copy = 4


class DSCComment:
    __comment_mark = "//"
    __max_char_of_line = 100
    __history_list = "xxx.json"
    __keep_max_history = 10

    @property
    def MAX_CHAR_OF_LINE(self):
        return self.__max_char_of_line

    @property
    def ds_mark(self):
        return self.__ds_mark

    @property
    def staff(self):
        return self.__staff

    @staff.setter
    def staff(self, value):
        self.__staff = value

    @property
    def confirmation(self):
        return self.__confirmation

    @confirmation.setter
    def confirmation(self, value):
        self.__confirmation = value

    @property
    def date(self):
        return self.__date

    def __init__(self, ds_mark, staff, confirmation, date=""):
        self.__ds_mark = ds_mark
        self.__date = date if date != "" else datetime.datetime.today().strftime("%Y/%m/%d")
        self.__staff = staff
        self.__confirmation = confirmation

    def get_comment(self, act, block=False, blank=""):
        result = "{} {} {} by {} for {}".format(
            self.__ds_mark, self.__date, Action(act).name if Action(act) != Action.copy else "Copy PKG(%S)",
            self.staff, self.__confirmation
        )
        if block:
            result = "{0}{comment} ↓↓↓\r\n{0}{comment} ↑↑↑\r\n".format(blank, comment=result)
        return result

    def do_line_comment(self, act, s):
        if s.strip("\r\n") == "":
            return "\r\n"
        elif Action(act) == Action.mark:
            space = self.__get_space_of_line(s)
            if (len(s) + 3) <= self.MAX_CHAR_OF_LINE:
                s = "{}// {}".format(space, s.strip("\r\n").strip())
                return "{} {}\r\n".format(s, self.get_comment(act))
            else:
                return self.do_block_comment(act, s)
        else:
            if len(s.strip("\r\n")) <= self.MAX_CHAR_OF_LINE:
                comment_in_line = self.__find_comment(s)
                return "{} {}\r\n".format(s.strip("\r\n"), self.get_comment(act))
            else:
                return self.do_block_comment(act, s)

    def do_block_comment(self, act, s):
        blank = self.__get_min_space_of_lines(s)
        comment = self.get_comment(act, True, blank).splitlines()
        i = 1
        empty_lines = True
        for l in s.splitlines():
            if Action(act) == Action.mark:
                comment.insert(i, "{}{}{}".format(blank, self.__add_comment_mark(l), l[len(blank):]))
            else:
                comment.insert(i, l)
            if empty_lines:
                empty_lines = (l.strip("\r\n") == "")
            i += 1
        result = ""
        if not empty_lines:
            for c in comment:
                result += c + "\r\n"

        return result

    def __get_space_of_line(self, line):
        if re.search("\w", line):
            return line[:re.search("\w", line).start()]
        else:
            return line.strip("\r\n")

    def __get_min_space_of_lines(self, s):
        lines = s.splitlines()
        num_of_line = len(lines)
        i = 0
        result = self.__get_space_of_line(lines[i])
        while i < num_of_line:
            space = self.__get_space_of_line(lines[i])
            if len(result) > len(space):
                result = space
            i += 1

        return result

    def __add_comment_mark(self, line):
        if line.strip("\r\n") == "":
            return "//"
        else:
            return "// "

    def __find_comment(self, line):
        re.search(r"//", line, )


class DSCCommentTest(unittest.TestCase):

    def setUp(self):
        self.ds_mark = "//^_^"
        self.time = "2017/02/26"
        self.staff = "07079"
        self.cmf = "abc_efg"

        self.comment = DSCComment(self.ds_mark, self.staff, self.cmf, self.time)

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
