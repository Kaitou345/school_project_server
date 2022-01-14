import sqlite3
import numpy as np
import io
from uuid import uuid4

def uuid64():
  return uuid4().hex

class person_db:

  def __init__(self, db) -> None:
    self.con = sqlite3.connect(db, detect_types=sqlite3.PARSE_DECLTYPES)
    self.cur = self.con.cursor()
    self.table_name = "person_db"
    self.cur.execute(f"""CREATE TABLE IF NOT EXISTS {self.table_name} (
                    id TEXT NOT NULL,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    address TEXT NOT NULL,
                    contact_number TEXT NOT NULL,
                    age INT NOT NULL,
                    PRIMARY KEY(id)
                    );""")

  def disconnect(self):
    self.cur.close()
    self.con.close()


  def insert_person(self, name, email="Not Available", address="Not Available", contact_number="Not Available",  age=0):
    id = uuid64()
    self.cur.execute(f"""INSERT INTO {self.table_name} (id, name, email, address, contact_number, age)
                      VALUES(?,?,?,?,?,?);
                    """,(id, name, email, address, contact_number, age))
    
    self.con.commit()

    return id
  

  def get_ids(self):

    self.cur.execute(f"SELECT id FROM {self.table_name};")
    data = self.cur.fetchall()
    data = [x[0] for x in data]
    return data

  def get_info(self, id):
    self.cur.execute(f"""SELECT * FROM {self.table_name} WHERE id = "{id}";""")

    desc = self.cur.description
    column_names = [col[0] for col in desc]
    data = [dict(zip(column_names, row)) for row in self.cur.fetchall()]
    
    return data[0]


  def get_all_info(self):
    self.cur.execute(f"""SELECT * FROM {self.table_name};""")

    desc = self.cur.description
    column_names = [col[0] for col in desc]
    data = [dict(zip(column_names, row)) for row in self.cur.fetchall()]
    
    return data


  def delete_person(self, id):

    self.cur.execute(f"""DELETE FROM {self.table_name} WHERE id = "{id}";""")
    self.con.commit()





def adapt_array(arr):
    """
    http://stackoverflow.com/a/31312102/190597 (SoulNibbler)
    """
    out = io.BytesIO()
    np.save(out, arr)
    out.seek(0)
    return sqlite3.Binary(out.read())

def convert_array(text):
    out = io.BytesIO(text)
    out.seek(0)
    return np.load(out)

class encoding_db:
  def __init__(self, db):

    # Registers numpy array type in sqlite3
    sqlite3.register_adapter(np.ndarray, adapt_array)
    sqlite3.register_converter("ARRAY", convert_array)
    self.con = sqlite3.connect(db, detect_types=sqlite3.PARSE_DECLTYPES)
    self.cur = self.con.cursor()
    self.table_name = "encoding_db"
    self.cur.execute(f"""CREATE TABLE IF NOT EXISTS {self.table_name} (
                    person_id TEXT NOT NULL,
                    encoding ARRAY,
                    FOREIGN KEY (person_id) REFERENCES person_db(id)
                    );""")
  
  def disconnect(self):
    self.cur.close()
    self.con.close()


  def insert_encodings(self, id, image_encodings):
    """
    Inserts image encodings and ID into table
    """
    for encoding in image_encodings:
      self.cur.execute(f"""INSERT INTO {self.table_name} (person_id, encoding) 
                    VALUES(?,?)
                    ;""", (id, encoding,))
    self.con.commit()

  def get_encodings(self, id):
    """
    Gets all the encodings for the id
    """
    self.cur.execute(f"""SELECT encoding FROM {self.table_name} WHERE person_id = "{id}" ;""")

    data = self.cur.fetchall()
    data = [x[0] for x in data]
    return data


  def delete_person(self, id):

    self.cur.execute(f"""DELETE FROM {self.table_name} WHERE person_id = "{id}";""")
    self.con.commit()


