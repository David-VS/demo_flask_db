import sqlite3
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True)

conn = sqlite3.connect('database.db')
print("Opened database successfully")

conn.execute('CREATE TABLE IF NOT EXISTS students (nm TEXT, addr TEXT, city TEXT, zip TEXT)')
print("Table created successfully")
conn.close()

@app.route('/enternew')
def new_student():
    return render_template('student.html')


@app.route('/addrec', methods=['POST', 'GET'])
def addrec():
    if request.method == 'POST':
        try:
            nm = request.form['nm']
            addr = request.form['add']
            city = request.form['city']
            zip = request.form['zip']

            with sqlite3.connect("database.db") as con:
                cur = con.cursor()

                cur.execute("INSERT INTO students (nm,addr,city,zip) VALUES(?, ?, ?, ?)",(nm,addr,city,zip) )

                con.commit()
                msg = "Record successfully added"
        except:
            con.rollback()
            msg = "error in insert operation"

        finally:
            con.close()
            return render_template("result.html", msg=msg)

@app.route('/delete/<string:entry>')
def delete(entry):
    try:
        with sqlite3.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("DELETE FROM students WHERE nm = ?", (entry,))
            con.commit()
            msg = "Record successfully deleted"
    except:
        con.rollback()
        msg = "error in delete operation"

    finally:
        con.close()
        return render_template("result.html", msg=msg)

@app.route('/list')
def list():
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("SELECT * FROM students")

    rows = cur.fetchall()
    data = []
    for row in rows:
        data.append([x for x in row])
    return jsonify(data)
