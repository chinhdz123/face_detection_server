import os
import sqlite3
PATH_ALALYTIC_DB = "face.db"

class AlalyticDatabase():
    def get_data(self,query, type = "all"):
        conn = sqlite3.connect(os.path.join(os.getcwd(), PATH_ALALYTIC_DB), check_same_thread=False)
        cursor = conn.cursor()
        if type == "all":
            data = cursor.execute(query).fetchall()
        else:
            data = cursor.execute(query).fetchone()
        conn.close()
        return data
    
    def create(self, datas):
        conn = sqlite3.connect(os.path.join(os.getcwd(), PATH_ALALYTIC_DB), check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO faces (name, encoding, image)
            VALUES (?, ?,?)
        ''', datas)
        conn.commit()
        conn.close()

    
    def get_all_datas(self):
        query = f"SELECT name, encoding,image FROM faces ;"
        datas = self.get_data(query, type = "all")
        return datas
    
    
db = AlalyticDatabase()