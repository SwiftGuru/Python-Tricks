import pyodbc


def existinDB(id, cursor):
    cursor.execute("SELECT top 1 * from results where recordid = ?",  id)
    result = cursor.fetchall()
    return(len(result)>0)

def lastrecordid(cursor):
    cursor.execute('Select max recordid from results')
    return cursor.fetchall()[0].recordid

cnxn = pyodbc.connect('DRIVER={SQL Server Native Client 10.0};SERVER=agnlasql2;DATABASE=MLMS1;Trusted_Connection=yes')
cursor = cnxn.cursor()
cnxn2 = pyodbc.connect('DRIVER={SQL Server Native Client 10.0};SERVER=agngis2\sqlexpress;DATABASE=SOILLAB;Trusted_Connection=yes')
cursor2 = cnxn2.cursor()
cursor.execute("SELECT * FROM MLMS1.dbo.results where order_number BETWEEN 2017000000 AND 2018000000")
rows = cursor.fetchall()
cursor2.execute("SELECT * FROM SOILLAB.dbo.results where order_number BETWEEN 2017000000 AND 2018000000")
target = cursor2.fetchall()

for row in rows:
   # if not lastrecordid(cursor2):
    #    cursor2.execute("insert into SOILLAB.dbo.results values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",row)
    #    cnxn2.commit()
    if not existinDB(row.recordid, cursor2):
        cursor2.execute("insert into SOILLAB.dbo.results values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",row)
        cnxn2.commit()
    else:
      print('already in DB')
