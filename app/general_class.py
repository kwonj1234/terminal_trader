import sqlite3

class General:
    tablename = ""
    dbpath = "data/teller.db"
    fields = []

    def save(self):
        if self.pk is None:
            self._insert()
        else:
            self._update()
    
    def _insert(self):
        with sqlite3.connect(self.dbpath) as conn:
            c = conn.cursor()
            field_string = ', '.join(self.fields)
            q_marks = ', '.join(['?' for _ in self.fields])

            sql = f'''INSERT INTO {self.tablename} ({field_string}) 
                    VALUES ({q_marks});'''
            values = [getattr(self, field) for field in self.fields]

            c.execute(sql, values)

    def _update(self):
        with sqlite3.connect(self.dbpath) as conn:
            curs = conn.cursor()
            assignments = ", ".join([f"{field} = ?" for field in self.fields])

            sql = f'''UPDATE {self.tablename} SET {assignments} WHERE pk = ?;'''
            values = [getattr(self, field) for field in self.fields]
            values.append(self.pk)

            curs.execute(sql, values)

    def delete(self):
        if not self.pk:
            raise KeyError(f"{self.pk} does not exist in the database")

        with sqlite3.connect(self.dbpath) as conn:
            c = conn.cursor()

            sql = f'''DELETE FROM {self.tablename} WHERE pk = ?'''
            c.execute(sql, (self.pk,))
    
    @classmethod
    def select_one(cls, where_clause = '', values = tuple()):
        with sqlite3.connect(cls.dbpath) as conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()

            sql = f'''SELECT * FROM {cls.tablename} WHERE {where_clause};'''
            c.execute(sql, values)
            result = c.fetchone()

            if not result:
                return False
            return cls(**result)

    @classmethod
    def select_all_where(cls, where_clause = "", values = tuple()):
        with sqlite3.connect(cls.dbpath) as conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()

            sql = f'''SELECT * FROM {cls.tablename} WHERE {where_clause};'''
            c.execute(sql, values)
            result = c.fetchall()

            return [cls(**row) for row in result]