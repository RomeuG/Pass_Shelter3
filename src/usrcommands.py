import os
import pwd

home_dir = pwd.getpwuid(os.getuid()).pw_dir # /home/user
db_dir = home_dir + "/.passshelter/"

def create_db():
    """Create db file"""
    db_name = input("Database name: ")
    open(db_dir + db_name + ".db", 'a').close()
    os.utime(db_dir + db_name + ".db", None)
    return "DB created."

def add_directory(db_cursor, table_name):
    """Adds a new dir in DB"""
    check_table_existence = """PRAGMA table_info(%s)""" % table_name
    db_cursor.execute(check_table_existence)
    data = db_cursor.fetchone()

    if type(data) is list or type(data) is tuple:
        print("Database already exists!")
    else:
        db_query = """create table if not exists %s (Id INTEGER primary Key, Username TEXT, Password TEXT)""" % \
                  table_name
        db_cursor.execute(db_query)

def add_to_dir(db_cursor, db_conn, dir_name, user_name, user_pass):
    """Adds user_name and pass to selected dir in db"""
    add_query = """INSERT INTO %s(Username, Password) VALUES('%s', '%s')""" % (dir_name, user_name, user_pass)
    db_cursor.execute(add_query)
    db_conn.commit()

def check_dir_names(db_cursor):
    """Returns all table names"""
    table_nr = """SELECT name FROM sqlite_master"""
    db_cursor.execute(table_nr)
    return db_cursor.fetchall()

def check_dir(db_cursor, table_name):
    """Outputs dir data to user"""
    table_info = """SELECT * FROM %s;""" % table_name
    db_cursor.execute(table_info)
    return db_cursor.fetchall()

def delete_dir(db_cursor, db_conn, dir_name):
    """Deletes directory"""
    del_query = """DROP TABLE %s""" % dir_name
    db_cursor.execute(del_query)
    db_conn.commit()

def delete_row(db_cursor, db_conn, dir_name, row_nr):
    """Deletes selected row in directory"""
    row_query = """DELETE FROM %s WHERE Id = %s;""" % (dir_name, row_nr)
    db_cursor.execute(row_query)
    db_conn.commit()

def update_id(db_cursor, db_conn, dir_name, row_nr, new_id):
    """Function to update Id's in tables"""
    update_query = """UPDATE %s SET Id = %s WHERE Id = %s;""" % (dir_name, new_id, row_nr)
    db_cursor.execute(update_query)
    db_conn.commit()
