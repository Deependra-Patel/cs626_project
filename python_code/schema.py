import MySQLdb
from config import *
'''
connect to the database using credentials imported from credentials.py
'''
def connect_db():
    db = MySQLdb.connect(host="localhost",
                         user=mysql_username,
                         passwd=mysql_password,
                         db=mysql_database)
    return db

class table:
    def __init__(self, name):
        self.table_name = name
        self.columns = []

    def print_table(self):
        print self.table_name
        print '==========================='
        for col in self.columns:
            col.print_column()

class column:
    def __init__(self, name, col_type):
        self.column_name = name
        self.column_type = col_type

    def print_column(self):
        print self.column_name, self.column_type

tables = []
db = connect_db()
dbcur = db.cursor()
tablenames = []
dbcur.execute('show tables')
for row in dbcur.fetchall():
    tablenames.append(row[0])

for t in tablenames:
    dbcur.execute("show columns from "+t)
    tb = table(t)
    for row in dbcur.fetchall():
        col = column(row[0], row[1])
        tb.columns.append(col)
    tables.append(tb)

for t in tables:
    t.print_table()



