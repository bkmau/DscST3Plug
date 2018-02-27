import unittest


class Keyword:
    # DDL(data definition language)
    DDL = ("CREATE", "ALTER", "DROP")
    
    # DML(data manipulation language)
    DML = ("INSERT", "UPDATE", "DELETE")
    
    # DQL(data query language)
    DQL = tuple("SELECT")
    
    # DCL(data control language)
    DCL = ("GRANT", "REVOKE", "COMMIT", "ROLLBACK", "TRANSACTION")


class DSCSQL:

    def __init__(self, uppercase=True, indent):
        self._sql = ""
        self._ddl = False
        self._dml = False
        self._dql = False
        self._dcl = False
        self._uppercase_keyword = uppercase

    @property
    def sql(self):
        return self._sql

    @sql.setter
    def sql(self, value):
        self._sql = value

    def prettify(self):
        pass

    def replace_parms(self):
        pass



class DSCSQLTest(unittest.TestCase):
    def setUp(self):
        sql = DSCSQL()


if __name__ == '__main__':
    unittest.main()