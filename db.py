from flask import abort
class Database:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()

    def getAll(self, table):
        self.cursor.execute("SELECT * from {}".format(table))
        return [dict(zip(self.cursor.column_names, i)) for i in self.cursor.fetchall()]

    def getOne(self, table, idd):
        self.cursor.execute("SELECT * FROM {table} WHERE id={id}".format(table=table, id=idd))
        res = self.cursor.fetchall()
        print(res)
        if res is not None and res != []:
            return dict(zip(self.cursor.column_names, res[0])) if res else {}
        else:
            abort(404)

    def post(self, data, table):
        new_id = self.getLastId(table) + 1
        values = [data[i] for i in data]
        values.insert(0, str(new_id))
        columnNames = self.getColumnNames(table)
        if len(columnNames) != len(data) + 1 or table == "student_summary":
            abort(422)


        try:
            self.cursor.execute("insert into {table}({columns}) values ({value})".format(table=table,
                                columns=",".join([i for i in columnNames]),
                                value=",".join(['\"' + i + '\"' for i in values])))
        except:
            return None

        self.cursor.fetchone()
        self.conn.commit()
        return new_id

    def put(self, data, table):
        columnNames = self.getColumnNames(table)
        columnNamesRequest = [i for i in data]
        values = [data[i] for i in data]
        if columnNames != columnNamesRequest or table == "student_summary":
            abort(424)
        if None in values:
            abort(422)

        try:
            self.cursor.execute("update {table} set {changes} where id={id}".format(table=table,
                            changes="".join([i[0]+"="+"\'"+str(i[1])+"\',"
                                             for i in (zip(columnNames, values))])[:-1], id=data["id"]))
        except:
            abort(500)

        self.cursor.fetchone()
        self.conn.commit()

    def delete(self, table, idd):
        self.cursor.execute("select exists(select * from {table} where id={idd})".format(table=table, idd=idd))
        if not self.cursor.fetchone()[0]:
            abort(404)
        if table == "student_summary":
            abort(424)

        if table =="students" or table == "assignments":
            self.cursor.execute("DELETE FROM students_assignments WHERE {table}_id = {idd}".format(table=table[:-1],idd=idd))
        elif table == "cohorts" or table == "transport_types" or table == "pets":
            self.cursor.execute("DELETE FROM students WHERE {table}_id = {idd}".format(table=table[:-1], idd=idd))

        self.cursor.execute("delete from {table} where id={idd}".format(table=table,idd=idd))
        return ""

    def getColumnNames(self, table):
        self.cursor.execute(f"SHOW columns FROM {table}")
        res = self.cursor.fetchall()
        return [i[0] for i in res]

    def getLastId(self, table):
        self.cursor.execute('select id from {table} order by id desc limit 1'.format(table=table))
        res = self.cursor.fetchone()
        if res is not None:
            return res[0]
        return 0

#studnets assignments
    def studentsAssignmentsGetAll(self, st_id, ass_id):
        self.cursor.execute("""select * from students_assignments where student_id = {student_id} and 
                            assignment_id = {assignment_id};""".format(student_id= st_id, assignment_id=ass_id))
        return self.cursor.fetchall()

    def studentsAssignmentsDelete(self, st_id, ass_id):
        self.cursor.execute("""delete from students_assignments where student_id = {student_id} 
                        and assignment_id = {assignment_id};""".format(student_id=st_id,
                                                                       assignment_id=ass_id))
        self.conn.commit()