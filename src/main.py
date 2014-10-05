import sqlite3
import keyring.util.platform_
from .usrcommands import *
from .commandline import PassMan
from .keyring_functions import *
import argparse
from .version import __version__

home_directory = pwd.getpwuid(os.getuid()).pw_dir #/home/user
db_directory = home_directory + "/.passshelter/"
db_in_dir = [userFile for userFile in [f for f in os.listdir(db_directory) if os.path.isfile(db_directory + f)]
             if ".db" in userFile]
db_list = [userFile for userFile in [f for f in os.listdir(db_directory) if os.path.isfile(db_directory + f)]
           if userFile.endswith(".db")]

def check_db():
    """Checks if there are db's in directory, if not, creates a new one"""
    global sqlite_conn

    if not os.path.exists(db_directory):
        os.makedirs(db_directory)

    if db_in_dir:
        print("DB detected: " + ', '.join(db_list))
        if len(db_list) == 1:
            choose_db = db_list[0]
            sqlite_conn = sqlite3.connect(db_directory + choose_db)
        else:
            choose_db = input("Which database do you want to use? ")
            sqlite_conn = sqlite3.connect(db_directory + choose_db)
    else:
        try:
            config_dir = keyring.util.platform_.config_root()

            for cfg_file in os.listdir(config_dir):
                cfg_path = os.path.join(config_dir, cfg_file)
                if os.path.isfile(cfg_path):
                    os.unlink(cfg_path)
        except Exception:
            pass

        print(create_db())
        check_db()

def main_function():
    """Main function. Used when script is called"""
    parser = argparse.ArgumentParser(description="Password Manager in Python.")

    parser.add_argument("-dd","--deldb", help="Deletes current database.", action="store_true")
    parser.add_argument("-v","--version", help="Show program's version.", action="store_true")

    user_args = parser.parse_args()

    if user_args.deldb:
        for database in db_list:
            os.remove(db_directory + database)
    elif user_args.version:
        print(__version__)
    else:
        check_db()

        if not pass_is_set():
            set_password()
            user_cursor = sqlite_conn.cursor()
            try:
                PassMan(user_cursor, sqlite_conn).cmdloop()
            except KeyboardInterrupt:
                pass
        elif pass_is_set():
            access_pass = getpass.getpass("Access password: ")
            if pass_is_correct(access_pass):
                user_cursor = sqlite_conn.cursor()
                try:
                    PassMan(user_cursor, sqlite_conn).cmdloop()
                except KeyboardInterrupt:
                    pass

