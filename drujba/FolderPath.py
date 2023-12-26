import os
current_directory = os.getcwd()

FOLDER_ACCOUNTS_PATH = os.path.join(current_directory, 'Accounts')
FOLDER_ADDRESSBOOKS_PATH = os.path.join(current_directory, 'AddresBooksFolder')
FOLDER_NOTESBOOKS_PATH = os.path.join(current_directory, 'NotesBooksFolder')


CONTACTS = os.path.join(current_directory, 'Contacts.json')
NOTES = os.path.join(current_directory, 'Notes.json')


def create_folders():
    if not os.path.exists(FOLDER_ACCOUNTS_PATH):
        os.makedirs(FOLDER_ACCOUNTS_PATH)
    if not os.path.exists(FOLDER_ADDRESSBOOKS_PATH):
        os.makedirs(FOLDER_ADDRESSBOOKS_PATH)
    if not os.path.exists(FOLDER_NOTESBOOKS_PATH):
        os.makedirs(FOLDER_NOTESBOOKS_PATH)


CONTACTS = os.path.join(current_directory, 'Contacts.json')
NOTES = os.path.join(current_directory, 'Notes.json')


def create_base_json_files():
    with open(CONTACTS, 'w') as file:
        print('CONTACTS OK')
    with open(NOTES, 'w') as file:
        print('NOTES OK')
    # if not os.path.exists(CONTACTS):
    #     os.makedirs(CONTACTS)
    # if not os.makedirs(NOTES):
    #     os.makedirs(NOTES)

# def create_base_json_files():
#     if not os.path.exists(CONTACTS):
#         os.makedirs(CONTACTS)
#     if not os.makedirs(NOTES):
#         os.makedirs(NOTES)

