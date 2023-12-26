from cryptography.fernet import Fernet
import cmd
from rich.console import Console
from rich.table import Table
from art import *
from prompt_toolkit import prompt
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from random import choice
from string import ascii_letters
from drujba.FolderPath import FOLDER_ACCOUNTS_PATH, FOLDER_NOTESBOOKS_PATH, FOLDER_ADDRESSBOOKS_PATH, create_folders, create_base_json_files
import os
from drujba.Style import positive_action, command_message
from drujba.Bot import MyCmd
from drujba.Notes_book import NotesBook
from drujba.Address_book import AddressBook
import imaplib

import time


class UserAccount():

    def __init__(self, user_name=None, user_email=None, user_password=None, ):
        self._user_name = user_name
        self._user_password = UserPassword(user_password)
        self._account = None
        self._addres_book = None
        self._Notes_book = None
        self._email = 'None'
        self._email_password = 'None'

    def __str__(self):
        return f'UserName = {self._user_name} UserPassword = {self._user_password._password} \n addresbook = {self._addres_book} \n notesbook = {self._Notes_book} \n Email = {self._email} \n Epasword = {self._email_password} '

    def register_account(self):  # Register Func
        console = Console()
        txt_files = [file for file in os.listdir(
            FOLDER_ACCOUNTS_PATH) if file.endswith(".txt")]
        names = []
        for txt_file in txt_files:
            names.append(txt_file.replace('_account.txt', ''))
        self._user_password = UserPassword(None)
        login = input('Input Login:')
        if login == '':
            return
        if login in names:
            console.rule(
                title=f"[red]The username'{login}' is already taken.[/red]", style="bright_magenta")
            return self.register_account()
        self._user_name = login

        self._account = os.path.join(
            FOLDER_ACCOUNTS_PATH, f'{self._user_name}_account.txt')
        self._user_password.pass_ok()
        self._addres_book = os.path.join(
            FOLDER_ADDRESSBOOKS_PATH, f'{self._user_name}_AddressBook.json')
        self._Notes_book = os.path.join(
            FOLDER_NOTESBOOKS_PATH, f'{self._user_name}_NotesBook.json')
        self.create_AdressBook()
        self.create_notesbook()

        self.encryptor(self._user_name, self._user_password._password)
        console.rule(
            title=f"[green]Account'{self._user_name}' successfully created.[/green]", style="bright_magenta")

    def encryptor(self, login, password):
        key = Fernet.generate_key()  # encrypt Key Genaration
        chipers = Fernet(key)
        encrypt_login = chipers.encrypt(login.encode())  # encrypt Login
        encrypt_password = chipers.encrypt(password.encode())  # encrypt Pass
        encrypt_address_book = chipers.encrypt(self._addres_book.encode())
        encrypt_notes_book = chipers.encrypt(self._Notes_book.encode())
        encript_email = chipers.encrypt(self._email.encode())
        encript_email_password = chipers.encrypt(self._email_password.encode())

        with open(self._account, 'wb') as file:  # Save Info
            file.write(key + b'\n')
            file.write(encrypt_login + b'\n')
            file.write(encrypt_password + b'\n')
            file.write(encrypt_address_book + b'\n')
            file.write(encrypt_notes_book + b'\n')
            file.write(encript_email + b'\n')
            file.write(encript_email_password)

    def descriptor(self, login, password):
        path = os.path.join(FOLDER_ACCOUNTS_PATH,
                            f'{login}_account.txt')  # Open Account Data
        if os.path.exists(path):
            with open(path, 'r') as file:
                data = file.readlines()

            key = data[0].strip()  # get cipheres Key
            ciphered_login = data[1].strip()  # get cipheres Login
            ciphered_password = data[2].strip()  # get cipheres pass
            ciphered_adr_file = data[3].strip()  # get adressbook path
            ciphered_note_file = data[4].strip()  # get notebook path
            ciphered_email = data[5].strip()
            ciphered_emailpassword = data[6].strip()

            ciphers = Fernet(key)
            self._user_name = ciphers.decrypt(
                ciphered_login).decode()  # decrypt login
            self._user_password._password = ciphers.decrypt(
                ciphered_password).decode()  # decryt Password
            self._addres_book = ciphers.decrypt(ciphered_adr_file).decode()
            self._Notes_book = ciphers.decrypt(ciphered_note_file).decode()
            self._email = ciphers.decrypt(ciphered_email).decode()
            self._email_password = ciphers.decrypt(
                ciphered_emailpassword).decode()

            return self
        else:

            return False

    def create_AdressBook(self):
        with open(self._addres_book, 'w') as file:
            return

    def create_notesbook(self):
        with open(self._Notes_book, 'w') as file:
            return

    def generate_file_names(self):
        letters = ascii_letters
        filename = ''.join(choice(letters) for _ in range(20)) + '.json'
        return filename

    def login(self):
        """
        Функція login файл account.py
        Відповідає за процесс входу в обліковий запис
        Parameters:
        Немає параметрів.
        Returns:
        якщо логування пройшло, поверне UserAccount.\n
        якщо логування не пройшло поверне False.
        """
        console = Console()
        login = input('Input Login:')
        password = input('Input Password:')
        user_acc = self.descriptor(login, password)

        if user_acc == False or login != user_acc._user_name or password != user_acc._user_password._password:
            console.rule(
                title=f"[red]Invalid Login or Password. Try Again![/red]", style="bright_magenta")
            return False
        else:
            console.rule(
                title=f"[green]{user_acc._user_name}, Welcome Back![/green]", style="bright_magenta")
            time.sleep(3)
            return user_acc

    def add_email(self, email, password):
        """
        Функція add_email(Параметри: email: str, password: str )).
        Приймає емейл та пароль для Підключення google акаунта до бота
        Returns:
        Немає повернення.
        """
        self._email = email
        self._email_password = password

        self.encryptor(self._user_name, self._user_password._password)

    def testLogin(self):
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        console = Console()
        try:

            mail.login(self._email, self._email_password)
            console.rule(title=f"[green]Login successful! The password and email are correct.[/green]",
                         style="bright_magenta")
            return True
        except imaplib.IMAP4.error as e:

            console.rule(
                title=f"[red]Error logging into the account![/red]", style="bright_magenta")
            return False
        finally:
            mail.logout()


class UserPassword():
    def __init__(self, password=None) -> None:
        self._password = password

    def pass_ok(self):
        """Функція для перевірки корекстності вводу паролю використовується в функції register_account

        Returns:
            _type_: _description_

        """
        console = Console()
        password = input('Input Password:')
        repeat_password = input('Repeate The Password:')
        if password != repeat_password:
            console.rule(
                title=f"[red]Passwords do not match. Please try again.[/red]", style="bright_magenta")
            return self.pass_ok()
        elif password == repeat_password:
            self._password = password

    def __str__(self) -> str:
        return f'{self._password}'


class LoginCMD(cmd.Cmd):
    userAccount = UserAccount()

    word_completer = WordCompleter(['login', 'register', "exit"])

    # intro = tprint("designed  by  DRUJBA  team")

    def cmdloop(self, intro=None):
        self.preloop()
        if self.intro:
            self.console.print(self.intro)
        stop = None
        while not stop:
            try:
                session = PromptSession()
                user_input = session.prompt(
                    "Input command>>> ", completer=self.word_completer)
                stop = self.onecmd(user_input)
            except KeyboardInterrupt:
                print("^C")
        self.postloop()

    def do_login(self, *args):

        if self.userAccount.login():
            botcmd = MyCmd()
            botcmd.adr = str(self.userAccount._addres_book)
            botcmd.notes_book = NotesBook(self.userAccount._Notes_book)
            botcmd.book = AddressBook(self.userAccount._addres_book)

            botcmd.book.user_info = self.userAccount
            botcmd.book.user_info._account = os.path.join(FOLDER_ACCOUNTS_PATH,
                                                          f'{botcmd.book.user_info._user_name}_account.txt')

            botcmd.do_help()
            botcmd.cmdloop()

    def do_register(self, *args):
        self.userAccount.register_account()

    def do_exit(self, *args):
        "Exit from bot"

        return True


def start():
    console = Console()
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Welcome To Help Assistant", style="bright_magenta", width=100, vertical='middle',
                     justify='center')
    create_folders()
    create_base_json_files()
    table.add_row("login    ---> Log in to the application")
    table.add_row("register ---> Register an account", )

    console.print(table, width=100, style="bold magenta")
    logcmd = LoginCMD()
    logcmd.cmdloop()


if __name__ == '__main__':
    start()
