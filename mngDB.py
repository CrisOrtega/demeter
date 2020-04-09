import sqlite3

class mngdb:
    def __init__(self,namedb):
        self.conn = sqlite3.connect(namedb)
        self.cursor = self.conn.cursor()
        self.error=0
        print("Opened database successfully")

    def execute(self,query):
        try:
            self.cursor.execute(query)
            data=self.cursor.fetchall()
            self.error=0
            if not data:
                self.conn.commit()
            return data
        except sqlite3.Error as e:
            print("/*ERROR*/ %s" % query)
            print("Database error: %s" % e)
            self.error=1
        except Exception as e:
            print("Exception in query: %s" % e)

    def insert_dict(self,table,dictionary):
        insert_query="insert into "+table+" "
        field_list="("
        values="("
        comma=""
        for field in dictionary.items():
            field_list=field_list+comma+str(field[0])
            values=values+comma+"'"+str(field[1]).replace("'","''")+"'"
            comma=","
        field_list=field_list+")"
        values=values+")"
        insert_query=insert_query+field_list+" values "+values
        try:
            self.cursor.execute(insert_query)
            self.error = 0
            self.conn.commit()
        except sqlite3.Error as e:
            print("/*ERROR*/ %s" % insert_query)
            print("Database error: %s" % e)
            self.error = 1
        except Exception as e:
            print("Exception in query: %s" % e)

    def close(self):
        self.conn.close()
