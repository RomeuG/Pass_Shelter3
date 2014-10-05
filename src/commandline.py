import cmd
import keyring
from .usrcommands import *
from .encryption import aes_encryption

class PassMan(cmd.Cmd):
    """Class handles the cmd loop and its commands"""
    def __init__(self, sqlite_cursor, db_connection):
        cmd.Cmd.__init__(self)
        self.prompt = "->> "
        self.intro = "Welcome!"
        self.sqlite_cursor = sqlite_cursor
        self.db_connection = db_connection

    def do_shell(self, usr_command):
        """shell [command]
            Execute shell command"""
        if usr_command:
            os.system(usr_command)
        else:
            print("Bad command.")

    def do_add(self, args):
        """add [directory] [username] [password]
            Add username and password to selected directory"""
        db_directory, user_name, user_pass = args.split()
        if db_directory and user_name and user_pass:
            encrypted_pass = aes_encryption.aes_encrypt(user_pass, keyring.get_password("system", "passman-cipher")).decode('utf-8')
            print(encrypted_pass)
            add_to_dir(self.sqlite_cursor, self.db_connection, db_directory, user_name, encrypted_pass)
            print("%s:%s added to directory `%s` !" % (user_name, user_pass, db_directory))
        else:
            print("Bad command.")

    def do_newdir(self, dir_name):
        """newdir [directory]
            Creates new directory"""
        if dir_name:
            add_directory(self.sqlite_cursor, dir_name)
        else:
            print("Bad command.")

    def do_check(self, dir_name):
        """check [directory]
            Outputs usernames and passwords included in selected directory"""
        if dir_name:
            table_rows = check_dir(self.sqlite_cursor, dir_name)
            for i, row in enumerate(table_rows):
                update_id(self.sqlite_cursor, self.db_connection, dir_name, row[0], i)
                print("[%s] - Username: %s | Password: %s - Hash: %s" % (i, row[1],
                        aes_encryption.aes_decrypt(row[2], keyring.get_password("system", "passman-cipher")), row[2]))
        else:
            print("Bad command.")

    def do_checkdirs(self, *args):
        """checkdirs
            Outputs directory names"""
        dir_names = check_dir_names(self.sqlite_cursor)
        for dirs in dir_names:
            print(str(dirs[0]))

    def do_deldir(self, dir_name):
        """deldir [directory]
            Deletes selected directory"""
        if dir_name:
            delete_dir(self.sqlite_cursor, self.db_connection, dir_name)

    def do_delentry(self, args):
        """delentry [direcotyr] [row number]
            Deletes username/password combination"""
        row_dir, row_nr = args.split()
        if row_dir and row_nr:
            delete_row(self.sqlite_cursor, self.db_connection, row_dir, row_nr)

    def do_help(self, args):
        """help
            Outputs commands"""
        cmd.Cmd.do_help(self, args)

    @staticmethod
    def do_exit(self, *args):
        """exit
            Exits the progam"""
        return True

    def postloop(self):
        cmd.Cmd.postloop(self)
        print("Exiting...")
