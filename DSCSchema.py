import unittest
import re

class DSField(object):
    def __init__(self, field, cht_name, data_type, data_length, comment):
        self.field = field
        self.cht_name = cht_name
        self.data_type = data_type
        self.data_length = data_length
        self.comment = comment

    def __str__(self):
        return "{: <6}{: <10}{: <15}{}".format(
            self.field, self.cht_name, "{}({})".format(self.data_type, self.data_length), self.comment)


class DSTable(object):

    def __init__(self, table_id, cht_name, pk, fields):
        self.table_id = table_id
        self.cht_name = cht_name
        self.pk = pk
        if fields:
            self.fields = fields
        else:
            self.fields = {}

    def get_field_by_name(self, name):
        return self.fields[name]

    def __str__(self):
        return "Table: {}\r\n"\
            "Name: {}\r\n"\
            "Primary Key: {} \r\n"\
            "{:=<120}\r\n"\
            "{: <6}{: <10}{: <15}{}\r\n"\
            "{:=<120}\r\n"\
            "{}".format(self.table_id, self.cht_name, "+".join(self.pk), "", "ID", "Name", "Type(Length)",
                        "Comment", "", "")

class DSCSchema(object):
    _t_id_ex = re.compile("(檔案代碼:)(.*)")
    _t_name_ex = re.compile("(檔案名稱 *:)(.*)")
    _t_key_ex = re.compile("(PRIMARY *:)(.*)")
    _t_split_ex = re.compile("^=+", flags=re.MULTILINE)
    _t_col_ex = re.compile("(\d{4})( +)([A-Z]{2}\d{3})( +)(.*?)( +)([A-Z])( +)(\d+(\.?\d?))(.*)")

    def __init__(self, file_content):
        self.file_content = file_content
        self.tables = {}

    @property
    def tables(self):
        return self.tables

    def get_a_table(self, table_id):
        return self.tables[table_id]

    def parse(self):
        all_content = self._remove_dirty_content()
        items = list(self._t_id_ex.finditer(all_content))
        for index, item in enumerate(items):
            if index + 1 < len(items):
                content = all_content[item.start():items[index + 1].start() - 1]
            else:
                content = all_content[item.start():len(all_content)]

            splitters = list(self._t_split_ex.finditer(content))

            self._tables.update({item.group(2): DSTable(
                item.group(2), self._t_name_ex.search(content).group(2),
                self._t_key_ex.search(content).group(2).split("+"), self._get_fields(content[splitters[1].end() + 1:])
            )})

    def _remove_dirty_content(self):
        content = self.file_content
        content = re.sub("^\f", "", content, flags=re.MULTILINE)

        content = re.sub("^/.*", "", content, flags=re.MULTILINE)

        content = re.sub("^ ?\r?\n", "", content, flags=re.MULTILINE)

        return content

    def _get_fields(self, body):
        result = {}
        for line in body.splitlines():
            detail = self._t_col_ex.search(line)
            result.update({detail.group(3): DSField(
                detail.group(3), detail.group(5), detail.group(7), float(detail.group(9)), detail.group(11)
            )})
        return result


class DSCSchemaTest(unittest.TestCase):
    pass

if __name__ == '__main__':
    unittest.main()