from flask import Flask, jsonify, request, abort, Response, json
import mysql.connector as sql
from db import Database
import os

host = os.environ.get('DB_HOST', 'localhost')
conn = sql.connect(host=host, user='VALERA', password='1111', database='university')
db = Database(conn)
app = Flask(__name__)

# def parse_arg_from_requests(arg, **kwargs):
#     parse = reqparse.RequestParser()
#     parse.add_argument(arg, **kwargs)
#     args = parse.parse_args()
#     return args[arg]

@app.route('/<string:table>', methods=["GET"])
def show_all(table):
    return jsonify(db.getAll(table))


@app.route('/<string:table>/<int:idd>', methods=["GET"])
def show_one(table, idd):
    return jsonify(db.getOne(table, idd))


@app.route('/<string:table>', methods=["POST"])
def make_post(table):
    if table == "student_summary":
        abort(404)
    data = request.get_json(force=True)
    if data is not None:
        new_id = db.post(data, table)
        data["id"] = new_id
        return jsonify(data)
    return None





@app.route('/<string:table>', methods=["PUT"])
def change_data(table):
    if table == "student_summary":
        abort(404)
    data = request.get_json(force=True)
    if data is not None:
        db.put(data, table)
    return jsonify(data)


@app.route('/<string:table>/<int:idd>', methods=["DELETE"])
def delete_data(table, idd):
    if table == "student_summary":
        abort(404)
    db.delete(table, idd)
    return ""


@app.route('/students_assignments/<int:student_id>/<int:assignment_id>', methods=["GET"])
def stundet_assignment_get(student_id, assignment_id):
    res = db.studentsAssignmentsGetAll(student_id, assignment_id)
    if res:
        return jsonify(res)
    abort(404)


@app.route('/students_assignments/<int:student_id>/<int:assignment_id>', methods=["DELETE"])
def stundet_assignment_delete(student_id, assignment_id):
    db.studentsAssignmentsDelete(student_id, assignment_id)


if __name__ == '__main__':
    app.run(debug=True)
