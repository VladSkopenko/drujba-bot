from drujba.Address_book import AddressBook
from drujba.Record import Record
from drujba.Style import command_message, error_message, positive_action
from drujba.Notes_book import NotesBook
from drujba.sort_files import sort_by_type
import cmd
from rich.console import Console
from rich.table import Table
from art import *
from prompt_toolkit import prompt
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from drujba.FolderPath import create_base_json_files , CONTACTS,NOTES


class MyCmd(cmd.Cmd):
    create_base_json_files()
    book = AddressBook(CONTACTS)
    notes_book = NotesBook(NOTES)
    console = Console()
    # випадаючі команди
    word_completer = WordCompleter(
        ['help',
         "exit",
         'make_note',
         'make_tag',
         'find_note',
         'find_tag',
         'edit_note',
         'edit_title',
         "del_note",
         "show_notes",
         "sort_by_type",
         "show_rec",
         "make_rec",
         "find_rec",
         "del_rec",
         "edit_ph_rec",
         "remove_phone_rec",
         "add_phone_rec",
         "cong_rec",
         "exp_tag",
         "import",
         "company_rec",
         "comment_rec",
         "adress_rec",
         "edit_tag_rec",
         "add_tag_rec",
         "remove_tag_rec",
         "add_birthday_rec",
         "remove_birthday_rec",
         "add_email_rec",
         "remove_email_rec",
         "edit_name_rec",
         "authorize_gmail",
         "send_email"
         ])
    intro = tprint("designed  by  DRUJBA  team")

    def cmdloop(self, intro=None):
        self.preloop()
        if self.intro:
            self.console.print(self.intro)
            self.do_help()
        stop = None
        while not stop:
            try:
                session = PromptSession()
                user_input = session.prompt(
                    "Enter command>>> ", completer=self.word_completer)
                stop = self.onecmd(user_input)
            except KeyboardInterrupt:
                print("^C")
        self.postloop()

    def do_hello(self, *args):
        "Say hello"
        print(command_message("How can I help you?"))

    def do_exit(self, *args):
        "Exit from bot"
        print(positive_action("Good bye!"))
        return True

    # таблиця help
    def do_help(self, *args):
        table = Table()
        table.add_column("COMMAND", style="bright_magenta")
        table.add_column("DESCRIPTION", style="bright_blue", no_wrap=True)
        table.add_row("help",
                      "Shows a description of the commands")
        table.add_row("exit",
                      "To exit the session")
        table.add_row("----",
                      "-----------------------------------")
        table.add_row("make_note",
                      "Make a note")
        table.add_row("make_tag",
                      "Make a tag")
        table.add_row("find_note",
                      "Search by title and notes")
        table.add_row("find_tag",
                      "Search by tags")
        table.add_row("edit_note",
                      "Edits notes by ID (use search before use)")
        table.add_row("edit_title",
                      "Edits titles to note by ID (use search before use)")
        table.add_row("del_note",
                      "Deletes note by ID (use search before use)")
        table.add_row("show_notes",
                      "Shows all notes")
        table.add_row("----",
                      "-----------------------------------")
        table.add_row("show_rec",
                      "Shows all book records")
        table.add_row("make_rec",
                      "Make a record to addressbook")
        table.add_row("find_rec",
                      "Search in addressbook")
        table.add_row("del_rec",
                      "Deletes record in addressbook by name (use search before use)")
        table.add_row("edit_ph_rec",
                      "Edites phone to record in addressbook by name (use search before use)")
        table.add_row("remove_phone_rec",
                      "Remove phone from a record in the address book by name (use search before use)")
        table.add_row("add_phone_rec",
                      "Add phone to a record in the address book by name (use search before use)")
        table.add_row("cong_rec",
                      "Search contacts by days to birthday")
        table.add_row("import",
                      "Import file in contacts")
        table.add_row("company_rec",
                      "Add a company to a record in the address book by name (enter <SPACE> to remove)")
        table.add_row("comment_rec",
                      "Add a comment to a record in the address book by name (enter <SPACE> to remove)")
        table.add_row("adress_rec",
                      "Add a address to a record in the address book by name (enter <SPACE> to remove)")
        table.add_row("exp_tag",
                      "Exports contacts by tag to a JSON file (use search before use)")
        table.add_row("edit_tag_rec",
                      "Edites tag to record in addressbook by name (use search before use)")
        table.add_row("add_tag_rec",
                      "Add tag to a record in the address book by name")
        table.add_row("remove_tag_rec",
                      "Remove tag from a record in the address book by name")
        table.add_row("add_birthday_rec",
                      "Add birthday to a record in the address book by name 'YYYY-MM-DD'")
        table.add_row("remove_birthday_rec",
                      "Remove birthday of the record in the address book by name")
        table.add_row("add_email_rec",
                      "Add email to a record in the address book by name")
        table.add_row("remove_email_rec",
                      "Remove email of the record in the address book by name")
        table.add_row("edit_name_rec",
                      "Edites name to record in addressbook by name (use search before use)")
        table.add_row("----",
                      "-----------------------------------")
        table.add_row("sort_by_type",
                      "Sorts files by type (images, videos, documents, music, archives)")
        table.add_row("authorize_gmail",
                      "Authorizes a Google account")
        table.add_row("send_email",
                      "Sends messages to email by tags")

        self.console.print(table)

    ### ------------ NotesBook part-------------###

    def do_make_note(self, *args):
        "Make a note"
        title = input(command_message("Enter title>>> "))
        note = input(command_message("Enter note>>> "))
        if title != "" and note != "" and 3 <= len(title) <= 10:
            self.notes_book.add_note(title, note)
            question = input(command_message(
                "Do you want to enter a tag? (yes/no)>>> "))
            if question.lower() == 'yes':
                tag = input(command_message("Enter tag>>> "))
                if tag != "" and 3 <= len(tag) <= 10:
                    self.notes_book.add_tag(tag)
                else:
                    print(error_message(
                        "Tag is not correct (from 3 to 10 characters)"))
            self.notes_book.save_note()
            print(positive_action("Note added"))
        else:
            print(error_message("The title and note must be entered"))

    def do_make_tag(self, *args):
        "Make a tag"
        inp_id = input(command_message(
            "Enter ID of the record that changes>>> "))
        if len(self.notes_book.find_note_id(inp_id)) >= 1:
            tag = input(command_message("Enter tag>>> "))
            if tag != "" and 3 <= len(tag) <= 10:
                self.notes_book.add_tag(tag, inp_id)
                self.notes_book.save_note()
                print(positive_action("Tag added"))
            else:
                print(error_message("Tag is not correct (from 3 to 10 characters)"))
        else:
            print(error_message("Did not find ID"))

    def do_find_note(self, *args):
        "Search by title and notes"
        question = input(command_message("Enter your request>>> "))
        if question != "":
            table = Table()
            table.add_column("ID", style="bright_magenta")
            table.add_column("Date", style="magenta")
            table.add_column("Tag", style="cyan")
            table.add_column("Title", style="bright_cyan")
            table.add_column("Note", style="blue")
            if len(self.notes_book.find_note(question)) > 0:
                for sh in self.notes_book.find_note(question):
                    if isinstance(sh.tag, list):
                        table.add_row(
                            f"{sh.note_id.get_id}", f"{sh.addition_date.get_date}",
                            f"{' '.join([str(item) for item in sh.tag])}", f"{sh.title.get_title}", f"{sh.note.get_note}")
                self.console.print(table)
            else:
                print(error_message("No notes found."))

    def do_find_tag(self, *args):
        "Search by tags"
        question = input(command_message("Enter your request>>> "))
        if question != "":
            table = Table()
            table.add_column("ID", style="bright_magenta", no_wrap=True)
            table.add_column("Date", style="magenta")
            table.add_column("Tag", style="cyan")
            table.add_column("Title", style="bright_cyan")
            table.add_column("Note", style="blue")
            if len(self.notes_book.find_tag(question)) > 0:
                for sh in self.notes_book.find_tag(question):
                    if isinstance(sh.tag, list):
                        table.add_row(
                            f"{sh.note_id.get_id}", f"{sh.addition_date.get_date}",
                            f"{' '.join([str(item) for item in sh.tag])}", f"{sh.title.get_title}", f"{sh.note.get_note}")

                self.console.print(table)
            else:
                print(error_message("No notes found."))

    def do_edit_note(self, *args):
        "Edits notes"
        inp_id = input(command_message(
            "Enter ID of the record that changes>>> "))
        if len(self.notes_book.find_note_id(inp_id)) >= 1:
            note = input(command_message("Enter new note>>> "))
            if note != "":
                self.notes_book.edit_note(inp_id, note)
                self.notes_book.save_note()
                print(positive_action("Note has been edited"))
            else:
                print(error_message("Note is empty"))
        else:
            print(error_message("Did not find ID"))

    def do_edit_title(self, *args):
        "Edits titles"
        inp_id = input(command_message(
            "Enter ID of the record that changes>>> "))
        if len(self.notes_book.find_note_id(inp_id)) >= 1:
            title = input(command_message("Enter new title>>> "))
            if title != "" and 3 < len(title) < 10:
                self.notes_book.edit_title(inp_id, title)
                self.notes_book.save_note()
                print(positive_action("Title has been edited"))
            else:
                print(error_message("Title is not correct"))
        else:
            print(error_message("Did not find ID"))

    def do_del_note(self, *args):
        "Deletes note"
        inp_id = input(command_message(
            "Enter ID of the record that delete>>> "))
        if len(self.notes_book.find_note_id(inp_id)) >= 1:
            self.notes_book.delete_note(inp_id)
            self.notes_book.save_note()
            print(positive_action("Record deleted successfully"))
        else:
            print(error_message("Did not find ID"))

    def do_show_notes(self, *args):
        "Shows all notes records"
        table = Table()
        table.add_column("ID", style="bright_magenta")
        table.add_column("Date", style="magenta")
        table.add_column("Tag", style="cyan")
        table.add_column("Title", style="bright_cyan")
        table.add_column("Note", style="blue")
        for sh in self.notes_book:
            if isinstance(sh.tag, list):
                table.add_row(f"{sh.note_id.get_id}", f"{sh.addition_date.get_date}",
                              f"{' '.join([str(item) for item in sh.tag])}", f"{sh.title.get_title}",
                              f"{sh.note.get_note}")
        self.console.print(table)

    ### ------------ Sort_by_type part-------------###

    def do_sort_by_type(self, *args):
        "Sorts files by type (images, videos, documents, music, archives)"
        input_path = input(command_message(
            "Enter full path to the folder>>> "))
        if input_path != "":
            sort_by_type(input_path)
        else:
            print(error_message("File path not found"))

    ### ------------ Addressbook part-------------###

    def do_show_rec(self, *args):
        "Shows all book records"
        table = Table()
        table.add_column("ID", style="bright_magenta")
        table.add_column("Tag", style="magenta")
        table.add_column("Name", style="cyan")
        table.add_column("Phone", style="bright_cyan")
        table.add_column("Email", style="blue")
        table.add_column("Address", style="magenta")
        table.add_column("Birthday", style="cyan")
        table.add_column("Company", style="bright_cyan")
        table.add_column("Comment", style="blue")
        for sh in self.book:
            table.add_row(f"{sh.id.get_id}",
                          f"{' '.join([str(item) for item in sh.tags])}",
                          f"{sh.name.get_name}",
                          f"{' '.join([str(item) for item in sh.phones])}",
                          f"{sh.email.get_email}",
                          f"{sh.address.get_address}",
                          f"{sh.birthday.get_birthday}",
                          f"{sh.company.get_company}",
                          f"{sh.comment.get_comment}",
                          )
        self.console.print(table)

    def do_make_rec(self, *args):
        "Make a record to addressbook"
        input_name = input("Enter name>>> ")
        print(self.book.add_full_record(input_name))

    def do_find_rec(self, *args):
        "Search in addressbook"
        question = input(command_message("Enter your request>>> "))
        if question != "":
            table = Table()
            table.add_column("ID", style="bright_magenta")
            table.add_column("Tag", style="magenta")
            table.add_column("Name", style="cyan")
            table.add_column("Phone", style="bright_cyan")
            table.add_column("Email", style="blue")
            table.add_column("Address", style="magenta")
            table.add_column("Birthday", style="cyan")
            table.add_column("Company", style="bright_cyan")
            table.add_column("Comment", style="blue")
            if len(self.book.find(question)) > 0:
                for sh in self.book.find(question):
                    table.add_row(f"{sh.id.get_id}",
                                  f"{' '.join([str(item) for item in sh.tags])}",
                                  f"{sh.name.get_name}",
                                  f"{' '.join([str(item) for item in sh.phones])}",
                                  f"{sh.email.get_email}",
                                  f"{sh.address.get_address}",
                                  f"{sh.birthday.get_birthday}",
                                  f"{sh.company.get_company}",
                                  f"{sh.comment.get_comment}",
                                  )
                self.console.print(table)
            else:
                print(error_message("No record found."))

    def do_del_rec(self, *args):
        "Deletes record in addressbook"
        question = input(command_message("Enter name to detete>>> "))
        print(self.book.remove_record(question))

    # заміна номера телефона (не консольна)
    def edit_phone(self, record_to_edit: Record, exit_record=None):

        if isinstance(record_to_edit, Record):
            edit_old_ph = input(command_message(
                "Enter the old phone number>>> "))
            edit_new_ph = input(command_message(
                "Enter the new phone number>>> "))
            if edit_old_ph and edit_new_ph:
                if exit_record is not None:
                    
                    exiting_record_str = exit_record
                    
                    try:
                        if self.book.edit_phone(record_to_edit, exiting_record_str, edit_old_ph, edit_new_ph):
                            print(positive_action("Phone edit successful"))
                        else:
                            print(error_message("Phone not found"))
                    except Exception as ve:
                        print(error_message("No changes made to the phone number."))
                else:
                    
                    try:
                        exiting_record_str = self.book.find_exiting_record(
                            record_to_edit.name.get_name)
                        if self.book.edit_phone(
                                record_to_edit, exiting_record_str, edit_old_ph, edit_new_ph):
                            print(positive_action("Phone edit successful"))
                        else:
                            print(error_message("Phone not found"))
                    except Exception as ve:
                        print(error_message("No changes made to the phone number."))
            else:
                print(error_message("No changes made to the phone number."))

    # заміна номера телефона (працює разом з <<<def edit_phone>>>)
    def do_edit_ph_rec(self,*args):
        "Edites phone to record in addressbook by name"
        
        question_name = input(command_message(
            "Enter the name to edit phone>>> ")) 
        if question_name != "":
            record_to_edit = self.book.find_record(question_name)
            if isinstance(record_to_edit, Record):

                self.edit_phone(record_to_edit)

            elif isinstance(record_to_edit, list):

                table = Table()
                table.add_column("ID", style="bright_magenta")
                table.add_column("Tag", style="magenta")
                table.add_column("Name", style="cyan")
                table.add_column("Phone", style="bright_cyan")
                table.add_column("Email", style="blue")
                table.add_column("Address", style="magenta")
                table.add_column("Birthday", style="cyan")
                table.add_column("Company", style="bright_cyan")
                table.add_column("Comment", style="blue")

                for sh in record_to_edit:
                    table.add_row(f"{sh.id.get_id}",
                                  f"{' '.join([str(item) for item in sh.tags])}",
                                  f"{sh.name.get_name}",
                                  f"{' '.join([str(item) for item in sh.phones])}",
                                  f"{sh.email.get_email}",
                                  f"{sh.address.get_address}",
                                  f"{sh.birthday.get_birthday}",
                                  f"{sh.company.get_company}",
                                  f"{sh.comment.get_comment}",
                                  )
                self.console.print(table)

                input_id = input(command_message(
                    "Enter ID>>> "))
                if input_id != "":
                    
                    self.edit_phone(self.book.find_record_id(int(input_id)),self.book.find_exititng_record_id(int(input_id)))
            else:
                print(error_message(
                    f"No record found with the name: {question_name}"))

    #############################################################

    ###################### заміна тегу телефона #################
    # не консольна
    def edit_tag(self, record_to_edit: Record, exit_record=None):

        if isinstance(record_to_edit, Record):
            edit_old_ph = input(command_message("Enter the old tag>>> "))
            edit_new_ph = input(command_message("Enter the new tag>>> "))
            if edit_old_ph and edit_new_ph:
                if exit_record is not None:

                    exiting_record_str = exit_record

                    try:
                        if self.book.edit_teg(record_to_edit, exiting_record_str, edit_old_ph, edit_new_ph):
                            print(positive_action("Tag edit successful"))
                        else:
                            print(error_message("Tag not found"))
                    except Exception as ve:
                        print(error_message("No changes made to tag"))
                else:

                    try:
                        exiting_record_str = self.book.find_exiting_record(
                            record_to_edit.name.get_name)
                        if self.book.edit_teg(
                                record_to_edit, exiting_record_str, edit_old_ph, edit_new_ph):
                            print(positive_action("Tag edit successful"))
                        else:
                            print(error_message("Tag not found"))
                    except Exception as ve:
                        print(error_message("No changes made to the tag"))
            else:
                print(error_message("No changes made to the tag"))

    # зміна тегу (працює разом з <<<def edit_tag>>>)
    def do_edit_tag_rec(self, *args):
        "Edites phone to record in addressbook by name"

        question_name = input(command_message(
            "Enter the name to edit phone>>> "))
        if question_name != "":
            record_to_edit = self.book.find_record(question_name)
            if isinstance(record_to_edit, Record):

                self.edit_tag(record_to_edit)

            elif isinstance(record_to_edit, list):

                table = Table()
                table.add_column("ID", style="bright_magenta")
                table.add_column("Tag", style="magenta")
                table.add_column("Name", style="cyan")
                table.add_column("Phone", style="bright_cyan")
                table.add_column("Email", style="blue")
                table.add_column("Address", style="magenta")
                table.add_column("Birthday", style="cyan")
                table.add_column("Company", style="bright_cyan")
                table.add_column("Comment", style="blue")

                for sh in record_to_edit:
                    table.add_row(f"{sh.id.get_id}",
                                  f"{' '.join([str(item) for item in sh.tags])}",
                                  f"{sh.name.get_name}",
                                  f"{' '.join([str(item) for item in sh.phones])}",
                                  f"{sh.email.get_email}",
                                  f"{sh.address.get_address}",
                                  f"{sh.birthday.get_birthday}",
                                  f"{sh.company.get_company}",
                                  f"{sh.comment.get_comment}",
                                  )
                self.console.print(table)

                input_id = input(command_message(
                    "Enter ID>>> "))
                if input_id != "":

                    self.edit_tag(self.book.find_record_id(
                        int(input_id)), self.book.find_exititng_record_id(int(input_id)))
            else:
                print(error_message(
                    f"No record found with the name: {question_name}"))

    #######################################################################

    def do_cong_rec(self, *args):
        "Search contacts by birthday"
        question = input(command_message("Enter days to birthday>>> "))
        if question != "":
            table = Table()
            table.add_column("ID", style="bright_magenta")
            table.add_column("Tag", style="magenta")
            table.add_column("Name", style="cyan")
            table.add_column("Phone", style="bright_cyan")
            table.add_column("Email", style="blue")
            table.add_column("Address", style="magenta")
            table.add_column("Birthday", style="cyan")
            table.add_column("Company", style="bright_cyan")
            table.add_column("Comment", style="blue")
            if len(self.book.congratulation(question)) > 0:
                for sh in self.book.congratulation(question):
                    table.add_row(f"{sh.id.get_id}",
                                  f"{' '.join([str(item) for item in sh.tags])}",
                                  f"{sh.name.get_name}",
                                  f"{' '.join([str(item) for item in sh.phones])}",
                                  f"{sh.email.get_email}",
                                  f"{sh.address.get_address}",
                                  f"{sh.birthday.get_birthday}",
                                  f"{sh.company.get_company}",
                                  f"{sh.comment.get_comment}",
                                  )
                self.console.print(table)
            else:
                print(error_message("No record found."))

    def do_import(self, *args):
        "Import file in contacts"
        file = input(command_message("Enter filename>>> "))

        self.book.import_files(file)

    # Підключає пошту для відправки повідомлень

    def do_authorize_gmail(self, *args):
        self.book.set_up_email()
        self.book.user_info.testLogin()

    # Знаходить контакти за тегом та відправляє клієнтам
    def do_send_email(self, *args):
        self.book.send_message()

    def do_exp_tag(self, *args):
        "Exports contacts by tag to a JSON file"
        tag_to_export = input(command_message(
            "Enter the tag to export contacts: "))

        if tag_to_export != "":
            self.book.export_contacts_by_tag(tag_to_export)
        else:
            print(error_message("Tag cannot be empty."))

    #     else:
    #         print(error_message("Tag cannot be empty."))

    ############## внесення компанії ###########################
    # не консольна
    def add_comp(self, record_to_edit: Record):
        if isinstance(record_to_edit, Record):
            in_data = input(command_message(
                "Enter the company (enter <SPACE> to remove)>>> "))
            if in_data != "":
                try:
                    exiting_record_str = self.book.find_exiting_record(
                        record_to_edit.name.get_name)
                    print(self.book.add_company(
                        record_to_edit, exiting_record_str, in_data))
                except Exception as ve:
                    print(error_message("No changes made to the company"))
            else:
                print(error_message("No added the company"))

    # працює разом з <<<def add_comp>>>
    def do_company_rec(self, *args):
        "Adds a company to a record in the address book by name"
        question_name = input(command_message(
            "Enter the name of the record to edit>>> "))
        if question_name != "":
            record_to_edit = self.book.find_record(question_name)
            if isinstance(record_to_edit, Record):

                self.add_comp(record_to_edit)

            elif isinstance(record_to_edit, list):

                table = Table()
                table.add_column("ID", style="bright_magenta")
                table.add_column("Tag", style="magenta")
                table.add_column("Name", style="cyan")
                table.add_column("Phone", style="bright_cyan")
                table.add_column("Email", style="blue")
                table.add_column("Address", style="magenta")
                table.add_column("Birthday", style="cyan")
                table.add_column("Company", style="bright_cyan")
                table.add_column("Comment", style="blue")

                for sh in record_to_edit:
                    table.add_row(f"{sh.id.get_id}",
                                  f"{' '.join([str(item) for item in sh.tags])}",
                                  f"{sh.name.get_name}",
                                  f"{' '.join([str(item) for item in sh.phones])}",
                                  f"{sh.email.get_email}",
                                  f"{sh.address.get_address}",
                                  f"{sh.birthday.get_birthday}",
                                  f"{sh.company.get_company}",
                                  f"{sh.comment.get_comment}",
                                  )
                self.console.print(table)

                input_id = input(command_message(
                    "Enter ID>>> "))
                if input_id != "":
                    self.add_comp(self.book.find_record_id(int(input_id)))
            else:
                print(error_message(
                    f"No record found with the name: {question_name}"))

    ############################################################

    ############## внесення коментаря ##########################
    # не консольна
    def add_comm(self, record_to_edit: Record):
        if isinstance(record_to_edit, Record):
            in_data = input(command_message(
                "Enter the comment (enter <SPACE> to remove)>>> "))
            if in_data != "":
                try:
                    exiting_record_str = self.book.find_exiting_record(
                        record_to_edit.name.get_name)
                    print(self.book.add_comment(
                        record_to_edit, exiting_record_str, in_data))
                except Exception as ve:
                    print(error_message("No changes made to the comment"))
            else:
                print(error_message("No added the comment"))

    # працює разом з <<<def add_comm>>>
    def do_comment_rec(self, *args):
        "Adds a comment to a record in the address book by name"
        question_name = input(command_message(
            "Enter the name of the record to edit>>> "))
        if question_name != "":
            record_to_edit = self.book.find_record(question_name)
            if isinstance(record_to_edit, Record):

                self.add_comm(record_to_edit)

            elif isinstance(record_to_edit, list):

                table = Table()
                table.add_column("ID", style="bright_magenta")
                table.add_column("Tag", style="magenta")
                table.add_column("Name", style="cyan")
                table.add_column("Phone", style="bright_cyan")
                table.add_column("Email", style="blue")
                table.add_column("Address", style="magenta")
                table.add_column("Birthday", style="cyan")
                table.add_column("Company", style="bright_cyan")
                table.add_column("Comment", style="blue")

                for sh in record_to_edit:
                    table.add_row(f"{sh.id.get_id}",
                                  f"{' '.join([str(item) for item in sh.tags])}",
                                  f"{sh.name.get_name}",
                                  f"{' '.join([str(item) for item in sh.phones])}",
                                  f"{sh.email.get_email}",
                                  f"{sh.address.get_address}",
                                  f"{sh.birthday.get_birthday}",
                                  f"{sh.company.get_company}",
                                  f"{sh.comment.get_comment}",
                                  )
                self.console.print(table)

                input_id = input(command_message(
                    "Enter ID>>> "))
                if input_id != "":
                    self.add_comm(self.book.find_record_id(int(input_id)))
            else:
                print(error_message(
                    f"No record found with the name: {question_name}"))

    ############################################################

    ############## внесення адреси ##########################
    # не консольна
    def add_addr(self, record_to_edit: Record):
        if isinstance(record_to_edit, Record):
            in_data = input(command_message(
                "Enter the address (enter <SPACE> to remove)>>> "))
            if in_data != "":
                try:
                    exiting_record_str = self.book.find_exiting_record(
                        record_to_edit.name.get_name)
                    print(self.book.add_address(
                        record_to_edit, exiting_record_str, in_data))
                except Exception as ve:
                    print(error_message("No changes made to the address"))
            else:
                print(error_message("No added the address"))

    # працює разом з <<<def add_addr>>>
    def do_adress_rec(self, *args):
        "Adds a address to a record in the address book by name"
        question_name = input(command_message(
            "Enter the name of the record to edit>>> "))
        if question_name != "":
            record_to_edit = self.book.find_record(question_name)
            if isinstance(record_to_edit, Record):

                self.add_addr(record_to_edit)

            elif isinstance(record_to_edit, list):

                table = Table()
                table.add_column("ID", style="bright_magenta")
                table.add_column("Tag", style="magenta")
                table.add_column("Name", style="cyan")
                table.add_column("Phone", style="bright_cyan")
                table.add_column("Email", style="blue")
                table.add_column("Address", style="magenta")
                table.add_column("Birthday", style="cyan")
                table.add_column("Company", style="bright_cyan")
                table.add_column("Comment", style="blue")

                for sh in record_to_edit:
                    table.add_row(f"{sh.id.get_id}",
                                  f"{' '.join([str(item) for item in sh.tags])}",
                                  f"{sh.name.get_name}",
                                  f"{' '.join([str(item) for item in sh.phones])}",
                                  f"{sh.email.get_email}",
                                  f"{sh.address.get_address}",
                                  f"{sh.birthday.get_birthday}",
                                  f"{sh.company.get_company}",
                                  f"{sh.comment.get_comment}",
                                  )
                self.console.print(table)

                input_id = input(command_message(
                    "Enter ID>>> "))
                if input_id != "":
                    self.add_addr(self.book.find_record_id(int(input_id)))
            else:
                print(error_message(
                    f"No record found with the name: {question_name}"))

    ############################################################

    ############## внесення тегу ##########################
    # не консольна
    def add_tag(self, record_to_edit: Record, exit_record=None):

        if isinstance(record_to_edit, Record):
            new_tag = input(command_message("Enter the tag>>> "))
            if new_tag != "":
                if exit_record is not None:

                    exiting_record_str = exit_record

                    try:
                        if self.book.add_teg(record_to_edit, exiting_record_str, new_tag):
                            print(positive_action("Tag edded successful"))
                        else:
                            print(error_message("Tag not found"))
                    except Exception as ve:
                        print(error_message("No changes made to tag"))
                else:

                    try:
                        exiting_record_str = self.book.find_exiting_record(
                            record_to_edit.name.get_name)
                        if self.book.add_teg(record_to_edit, exiting_record_str, new_tag):
                            print(positive_action("Tag added successful"))
                        else:
                            print(error_message("Tag not found"))
                    except Exception as ve:
                        print(error_message("No changes made to the tag"))
            else:
                print(error_message("No changes made to the tag"))

    # зміна тегу (працює разом з <<<def add_tag>>>)
    def do_add_tag_rec(self, *args):
        "Edites phone to record in addressbook by name"

        question_name = input(command_message(
            "Enter the name to edit phone>>> "))
        if question_name != "":
            record_to_edit = self.book.find_record(question_name)
            if isinstance(record_to_edit, Record):

                self.add_tag(record_to_edit)

            elif isinstance(record_to_edit, list):

                table = Table()
                table.add_column("ID", style="bright_magenta")
                table.add_column("Tag", style="magenta")
                table.add_column("Name", style="cyan")
                table.add_column("Phone", style="bright_cyan")
                table.add_column("Email", style="blue")
                table.add_column("Address", style="magenta")
                table.add_column("Birthday", style="cyan")
                table.add_column("Company", style="bright_cyan")
                table.add_column("Comment", style="blue")

                for sh in record_to_edit:
                    table.add_row(f"{sh.id.get_id}",
                                  f"{' '.join([str(item) for item in sh.tags])}",
                                  f"{sh.name.get_name}",
                                  f"{' '.join([str(item) for item in sh.phones])}",
                                  f"{sh.email.get_email}",
                                  f"{sh.address.get_address}",
                                  f"{sh.birthday.get_birthday}",
                                  f"{sh.company.get_company}",
                                  f"{sh.comment.get_comment}",
                                  )
                self.console.print(table)

                input_id = input(command_message(
                    "Enter ID>>> "))
                if input_id != "":

                    self.add_tag(self.book.find_record_id(
                        int(input_id)), self.book.find_exititng_record_id(int(input_id)))
            else:
                print(error_message(
                    f"No record found with the name: {question_name}"))

    ############################################################

    ############## видалення тегу ##########################
    # не консольна

    def rem_tag(self, record_to_edit: Record):
        if isinstance(record_to_edit, Record):
            in_data = input(command_message("Enter the tag>>> "))
            if in_data != "":
                try:
                    exiting_record_str = self.book.find_exiting_record(
                        record_to_edit.name.get_name)
                    self.book.remove_teg(
                        record_to_edit, exiting_record_str, in_data)
                    print(positive_action("Removed successfully"))
                except Exception as ve:
                    print(error_message("No changes made to the tag"))
            else:
                print(error_message("No added the tag"))

    # працює разом з <<<def rem_tag>>>
    def do_remove_tag_rec(self, *args):
        "Remove a tag from a record in the address book by name"
        question_name = input(command_message(
            "Enter the name of the record to edit>>> "))
        if question_name != "":
            record_to_edit = self.book.find_record(question_name)
            if isinstance(record_to_edit, Record):

                self.rem_tag(record_to_edit)

            elif isinstance(record_to_edit, list):

                table = Table()
                table.add_column("ID", style="bright_magenta")
                table.add_column("Tag", style="magenta")
                table.add_column("Name", style="cyan")
                table.add_column("Phone", style="bright_cyan")
                table.add_column("Email", style="blue")
                table.add_column("Address", style="magenta")
                table.add_column("Birthday", style="cyan")
                table.add_column("Company", style="bright_cyan")
                table.add_column("Comment", style="blue")

                for sh in record_to_edit:
                    table.add_row(f"{sh.id.get_id}",
                                  f"{' '.join([str(item) for item in sh.tags])}",
                                  f"{sh.name.get_name}",
                                  f"{' '.join([str(item) for item in sh.phones])}",
                                  f"{sh.email.get_email}",
                                  f"{sh.address.get_address}",
                                  f"{sh.birthday.get_birthday}",
                                  f"{sh.company.get_company}",
                                  f"{sh.comment.get_comment}",
                                  )
                self.console.print(table)

                input_id = input(command_message(
                    "Enter ID>>> "))
                if input_id != "":
                    self.rem_tag(self.book.find_record_id(int(input_id)))
            else:
                print(error_message(
                    f"No record found with the name: {question_name}"))

    ############################################################

    ############## внесення дня народження #####################
    # не консольна
    def add_birth(self, record_to_edit: Record):
        if isinstance(record_to_edit, Record):
            in_data = input(command_message(
                "Enter the birthday 'YYYY-MM-DD'>>> "))
            if in_data != "":
                try:
                    exiting_record_str = self.book.find_exiting_record(
                        record_to_edit.name.get_name)
                    print(self.book.add_birthday(
                        record_to_edit, exiting_record_str, in_data))
                except Exception as ve:
                    print(error_message("No changes made to the birthday"))
            else:
                print(error_message("No added the birthday"))

    # працює разом з <<<def add_birth>>>
    def do_add_birthday_rec(self, *args):
        "Adds a birthday to a record in the address book by name"
        question_name = input(command_message(
            "Enter the name of the record to edit>>> "))
        if question_name != "":
            record_to_edit = self.book.find_record(question_name)
            if isinstance(record_to_edit, Record):

                self.add_birth(record_to_edit)

            elif isinstance(record_to_edit, list):

                table = Table()
                table.add_column("ID", style="bright_magenta")
                table.add_column("Tag", style="magenta")
                table.add_column("Name", style="cyan")
                table.add_column("Phone", style="bright_cyan")
                table.add_column("Email", style="blue")
                table.add_column("Address", style="magenta")
                table.add_column("Birthday", style="cyan")
                table.add_column("Company", style="bright_cyan")
                table.add_column("Comment", style="blue")

                for sh in record_to_edit:
                    table.add_row(f"{sh.id.get_id}",
                                  f"{' '.join([str(item) for item in sh.tags])}",
                                  f"{sh.name.get_name}",
                                  f"{' '.join([str(item) for item in sh.phones])}",
                                  f"{sh.email.get_email}",
                                  f"{sh.address.get_address}",
                                  f"{sh.birthday.get_birthday}",
                                  f"{sh.company.get_company}",
                                  f"{sh.comment.get_comment}",
                                  )
                self.console.print(table)

                input_id = input(command_message(
                    "Enter ID>>> "))
                if input_id != "":
                    self.add_birth(self.book.find_record_id(int(input_id)))
            else:
                print(error_message(
                    f"No record found with the name: {question_name}"))

    ############################################################

    ############## видалення дня народження #####################
    # не консольна
    def rem_birth(self, record_to_edit: Record):
        if isinstance(record_to_edit, Record):
            try:
                exiting_record_str = self.book.find_exiting_record(
                    record_to_edit.name.get_name)
                print(self.book.remove_birthday(
                    record_to_edit, exiting_record_str))
            except Exception as ve:
                print(error_message("No changes made to the birthday"))
        else:
            print(error_message("No added the birthday"))

    # працює разом з <<<def rem_birth>>>
    def do_remove_birthday_rec(self, *args):
        "Remove a birthday of the record in the address book by name"
        question_name = input(command_message(
            "Enter the name of the record to edit>>> "))
        if question_name != "":
            record_to_edit = self.book.find_record(question_name)
            if isinstance(record_to_edit, Record):

                self.rem_birth(record_to_edit)

            elif isinstance(record_to_edit, list):

                table = Table()
                table.add_column("ID", style="bright_magenta")
                table.add_column("Tag", style="magenta")
                table.add_column("Name", style="cyan")
                table.add_column("Phone", style="bright_cyan")
                table.add_column("Email", style="blue")
                table.add_column("Address", style="magenta")
                table.add_column("Birthday", style="cyan")
                table.add_column("Company", style="bright_cyan")
                table.add_column("Comment", style="blue")

                for sh in record_to_edit:
                    table.add_row(f"{sh.id.get_id}",
                                  f"{' '.join([str(item) for item in sh.tags])}",
                                  f"{sh.name.get_name}",
                                  f"{' '.join([str(item) for item in sh.phones])}",
                                  f"{sh.email.get_email}",
                                  f"{sh.address.get_address}",
                                  f"{sh.birthday.get_birthday}",
                                  f"{sh.company.get_company}",
                                  f"{sh.comment.get_comment}",
                                  )
                self.console.print(table)

                input_id = input(command_message(
                    "Enter ID>>> "))
                if input_id != "":
                    self.rem_birth(self.book.find_record_id(int(input_id)))
            else:
                print(error_message(
                    f"No record found with the name: {question_name}"))

    ############################################################

    ############## внесення imail #####################
    # не консольна
    def add_eml(self, record_to_edit: Record):
        if isinstance(record_to_edit, Record):
            in_data = input(command_message(
                "Enter the email>>> "))
            if in_data != "":
                try:
                    exiting_record_str = self.book.find_exiting_record(
                        record_to_edit.name.get_name)
                    print(self.book.add_email(
                        record_to_edit, exiting_record_str, in_data))
                except Exception as ve:
                    print(error_message("No changes made to the email"))
            else:
                print(error_message("No added the email"))

    # працює разом з <<<def add_birth>>>
    def do_add_email_rec(self, *args):
        "Adds a email to a record in the address book by name"
        question_name = input(command_message(
            "Enter the name of the record to edit>>> "))
        if question_name != "":
            record_to_edit = self.book.find_record(question_name)
            if isinstance(record_to_edit, Record):

                self.add_eml(record_to_edit)

            elif isinstance(record_to_edit, list):

                table = Table()
                table.add_column("ID", style="bright_magenta")
                table.add_column("Tag", style="magenta")
                table.add_column("Name", style="cyan")
                table.add_column("Phone", style="bright_cyan")
                table.add_column("Email", style="blue")
                table.add_column("Address", style="magenta")
                table.add_column("Birthday", style="cyan")
                table.add_column("Company", style="bright_cyan")
                table.add_column("Comment", style="blue")

                for sh in record_to_edit:
                    table.add_row(f"{sh.id.get_id}",
                                  f"{' '.join([str(item) for item in sh.tags])}",
                                  f"{sh.name.get_name}",
                                  f"{' '.join([str(item) for item in sh.phones])}",
                                  f"{sh.email.get_email}",
                                  f"{sh.address.get_address}",
                                  f"{sh.birthday.get_birthday}",
                                  f"{sh.company.get_company}",
                                  f"{sh.comment.get_comment}",
                                  )
                self.console.print(table)

                input_id = input(command_message(
                    "Enter ID>>> "))
                if input_id != "":
                    self.add_eml(self.book.find_record_id(int(input_id)))
            else:
                print(error_message(
                    f"No record found with the name: {question_name}"))

    ############################################################

    ############## видалення imail #####################
    # не консольна
    def rem_eml(self, record_to_edit: Record):
        if isinstance(record_to_edit, Record):
            try:
                exiting_record_str = self.book.find_exiting_record(
                    record_to_edit.name.get_name)
                print(self.book.remove_email(
                    record_to_edit, exiting_record_str))
            except Exception as ve:
                print(error_message("No changes made to the email"))
        else:
            print(error_message("No removed the email"))

    # працює разом з <<<def rem_eml>>>
    def do_remove_email_rec(self, *args):
        "Remove email of the record in the address book by name"
        question_name = input(command_message(
            "Enter the name of the record to edit>>> "))
        if question_name != "":
            record_to_edit = self.book.find_record(question_name)
            if isinstance(record_to_edit, Record):

                self.rem_eml(record_to_edit)

            elif isinstance(record_to_edit, list):

                table = Table()
                table.add_column("ID", style="bright_magenta")
                table.add_column("Tag", style="magenta")
                table.add_column("Name", style="cyan")
                table.add_column("Phone", style="bright_cyan")
                table.add_column("Email", style="blue")
                table.add_column("Address", style="magenta")
                table.add_column("Birthday", style="cyan")
                table.add_column("Company", style="bright_cyan")
                table.add_column("Comment", style="blue")

                for sh in record_to_edit:
                    table.add_row(f"{sh.id.get_id}",
                                  f"{' '.join([str(item) for item in sh.tags])}",
                                  f"{sh.name.get_name}",
                                  f"{' '.join([str(item) for item in sh.phones])}",
                                  f"{sh.email.get_email}",
                                  f"{sh.address.get_address}",
                                  f"{sh.birthday.get_birthday}",
                                  f"{sh.company.get_company}",
                                  f"{sh.comment.get_comment}",
                                  )
                self.console.print(table)

                input_id = input(command_message(
                    "Enter ID>>> "))
                if input_id != "":
                    self.rem_eml(self.book.find_record_id(int(input_id)))
            else:
                print(error_message(
                    f"No record found with the name: {question_name}"))

    ############################################################

    ############## внесення номера ##########################
    # не консольна
    def add_ph(self, record_to_edit: Record):
        if isinstance(record_to_edit, Record):
            in_data = input(command_message("Enter the phone>>> "))
            if in_data != "":
                try:
                    exiting_record_str = self.book.find_exiting_record(
                        record_to_edit.name.get_name)
                    print(self.book.add_phone(
                        record_to_edit, exiting_record_str, in_data))
                except Exception as ve:
                    print(error_message("No changes made to the phone"))
            else:
                print(error_message("No added the phone"))

    # працює разом з <<<def add_ph>>>
    def do_add_phone_rec(self, *args):
        "Adds phone to a record in the address book by name"
        question_name = input(command_message(
            "Enter the name of the record to edit>>> "))
        if question_name != "":
            record_to_edit = self.book.find_record(question_name)
            if isinstance(record_to_edit, Record):

                self.add_ph(record_to_edit)

            elif isinstance(record_to_edit, list):

                table = Table()
                table.add_column("ID", style="bright_magenta")
                table.add_column("Tag", style="magenta")
                table.add_column("Name", style="cyan")
                table.add_column("Phone", style="bright_cyan")
                table.add_column("Email", style="blue")
                table.add_column("Address", style="magenta")
                table.add_column("Birthday", style="cyan")
                table.add_column("Company", style="bright_cyan")
                table.add_column("Comment", style="blue")

                for sh in record_to_edit:
                    table.add_row(f"{sh.id.get_id}",
                                  f"{' '.join([str(item) for item in sh.tags])}",
                                  f"{sh.name.get_name}",
                                  f"{' '.join([str(item) for item in sh.phones])}",
                                  f"{sh.email.get_email}",
                                  f"{sh.address.get_address}",
                                  f"{sh.birthday.get_birthday}",
                                  f"{sh.company.get_company}",
                                  f"{sh.comment.get_comment}",
                                  )
                self.console.print(table)

                input_id = input(command_message(
                    "Enter ID>>> "))
                if input_id != "":
                    self.add_ph(self.book.find_record_id(int(input_id)))
            else:
                print(error_message(
                    f"No record found with the name: {question_name}"))

    ############################################################

    ############## видалення номера ##########################
    # не консольна
    def rem_ph(self, record_to_edit: Record):
        if isinstance(record_to_edit, Record):
            in_data = input(command_message("Enter the phone>>> "))
            if in_data != "":
                try:
                    exiting_record_str = self.book.find_exiting_record(
                        record_to_edit.name.get_name)
                    self.book.remove_phone(
                        record_to_edit, exiting_record_str, in_data)
                    print(positive_action("Removed successfully"))
                except Exception as ve:
                    print(error_message("No changes made to the phone"))
            else:
                print(error_message("No added the phone"))

    # працює разом з <<<def rem_ph>>>
    def do_remove_phone_rec(self, *args):
        "Remove phone from a record in the address book by name"
        question_name = input(command_message(
            "Enter the name of the record to edit>>> "))
        if question_name != "":
            record_to_edit = self.book.find_record(question_name)
            if isinstance(record_to_edit, Record):

                self.rem_ph(record_to_edit)

            elif isinstance(record_to_edit, list):

                table = Table()
                table.add_column("ID", style="bright_magenta")
                table.add_column("Tag", style="magenta")
                table.add_column("Name", style="cyan")
                table.add_column("Phone", style="bright_cyan")
                table.add_column("Email", style="blue")
                table.add_column("Address", style="magenta")
                table.add_column("Birthday", style="cyan")
                table.add_column("Company", style="bright_cyan")
                table.add_column("Comment", style="blue")

                for sh in record_to_edit:
                    table.add_row(f"{sh.id.get_id}",
                                  f"{' '.join([str(item) for item in sh.tags])}",
                                  f"{sh.name.get_name}",
                                  f"{' '.join([str(item) for item in sh.phones])}",
                                  f"{sh.email.get_email}",
                                  f"{sh.address.get_address}",
                                  f"{sh.birthday.get_birthday}",
                                  f"{sh.company.get_company}",
                                  f"{sh.comment.get_comment}",
                                  )
                self.console.print(table)

                input_id = input(command_message(
                    "Enter ID>>> "))
                if input_id != "":
                    self.rem_ph(self.book.find_record_id(int(input_id)))
            else:
                print(error_message(
                    f"No record found with the name: {question_name}"))

    ############################################################

    ############## зміна імені ##########################
    # не консольна
    def edit_name(self, record_to_edit: Record):
        if isinstance(record_to_edit, Record):
            in_data = input(command_message("Enter the name>>> "))
            if in_data != "":
                try:
                    exiting_record_str = self.book.find_exiting_record(
                        record_to_edit.name.get_name)
                    print(self.book.rename(
                        record_to_edit, exiting_record_str, in_data))
                    # print(positive_action("Name changed successfully"))
                except Exception as ve:
                    print(error_message("No changes made to the phone"))
            else:
                print(error_message("No added the phone"))

    # працює разом з <<<def rem_ph>>>
    def do_edit_name_rec(self, *args):
        "Edites name to record in addressbook by name (use search before use)"
        question_name = input(command_message(
            "Enter the name of the record to edit>>> "))
        if question_name != "":
            record_to_edit = self.book.find_record(question_name)
            if isinstance(record_to_edit, Record):

                self.edit_name(record_to_edit)

            elif isinstance(record_to_edit, list):

                table = Table()
                table.add_column("ID", style="bright_magenta")
                table.add_column("Tag", style="magenta")
                table.add_column("Name", style="cyan")
                table.add_column("Phone", style="bright_cyan")
                table.add_column("Email", style="blue")
                table.add_column("Address", style="magenta")
                table.add_column("Birthday", style="cyan")
                table.add_column("Company", style="bright_cyan")
                table.add_column("Comment", style="blue")

                for sh in record_to_edit:
                    table.add_row(f"{sh.id.get_id}",
                                  f"{' '.join([str(item) for item in sh.tags])}",
                                  f"{sh.name.get_name}",
                                  f"{' '.join([str(item) for item in sh.phones])}",
                                  f"{sh.email.get_email}",
                                  f"{sh.address.get_address}",
                                  f"{sh.birthday.get_birthday}",
                                  f"{sh.company.get_company}",
                                  f"{sh.comment.get_comment}",
                                  )
                self.console.print(table)

                input_id = input(command_message(
                    "Enter ID>>> "))
                if input_id != "":
                    self.edit_name(self.book.find_record_id(int(input_id)))
            else:
                print(error_message(
                    f"No record found with the name: {question_name}"))

    ############################################################


if __name__ == "__main__":
    my_cmd = MyCmd()
    my_cmd.do_help()
    my_cmd.cmdloop()
