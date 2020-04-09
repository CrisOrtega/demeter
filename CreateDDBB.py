import sqlite3

conn = sqlite3.connect('demeter.sqlite')
cursor = conn.cursor()
print("Opened database successfully")

# https://medium.com/analytics-vidhya/programming-with-databases-in-python-using-sqlite-4cecbef51ab9
try:
    cursor.execute('''drop TABLE if exists customers;''')
except sqlite3.Error as e:
    print("Database error: %s" % e)
except Exception as e:
    print("Exception in query: %s" % e)
try:
    cursor.execute('''CREATE TABLE customers
         (IDCUSTOMER CHAR(25)    PRIMARY KEY      NOT NULL,
         REGION                  CHAR(25)         NOT NULL,
         DATABASE                CHAR(25)         NOT NULL,
         BUCKET                  TEXT             NOT NULL,
         PATH                    CHAR(256)        NOT NULL,
         PROFILE_NAME            CHAR(50)         NOT NULL,
         BRAND                   CHAR(256));''')
except sqlite3.Error as e:
    print("Database error: %s" % e)
except Exception as e:
    print("Exception in query: %s" % e)

try:
    cursor.execute('''drop TABLE if exists checks;''')
except sqlite3.Error as e:
    print("Database error: %s" % e)
except Exception as e:
    print("Exception in query: %s" % e)
try:
    cursor.execute('''CREATE TABLE checks
         (IDCHECK          INT         NOT NULL,
         QUERY            TEXT        NOT NULL,
         WARNING          TEXT        ,
         HEADER           TEXT        ,
         LEGEND           TEXT        ,
         MESSAGE          TEXT        ,
         APPLYTO          TEXT        NOT NULL,
         NOTAPPLYTO       TEXT,
         PRIMARY KEY (IDCHECK)
         );''')
except sqlite3.Error as e:
    print("Database error: %s" % e)
except Exception as e:
    print("Exception in query: %s" % e)

cursor.close()

