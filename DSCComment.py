import datetime
from enum import Enum
import re


class Action(Enum):
    add = 1
    modi = 2
    mark = 3
    copy = 4


class DSCComment(object):
    __comment_mark = "//"
    __max_char_of_line = 100
    __keep_max_history = 10

    def __init__(self, confirmation, date=""):
        self.ds_mark = ""
        self.staff = ""

        self.__date = date if date != "" else datetime.datetime.today().strftime("%Y/%m/%d")
        self.__confirmation = confirmation
        self.load_setting("config.json")
        self.load_history("config.json")

    def load_setting(self, json_file):
        self.ds_mark = "//^_^"
        self.staff = "07079"
        pass

    def load_history(self, file):
        pass

    @property
    def MAX_CHAR_OF_LINE(self):
        return self.__max_char_of_line

    @property
    def confirmation(self):
        return self.__confirmation

    @confirmation.setter
    def confirmation(self, value):
        self.__confirmation = value

    @property
    def date(self):
        return self.__date

    def get_comment(self, act, block=False, blank=""):
        result = "{} {} {} by {} for {}".format(
            self.ds_mark, self.__date, Action(act).name if Action(act) != Action.copy else "Copy PKG(%S)",
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
