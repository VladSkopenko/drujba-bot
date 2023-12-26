# drujba
<h1>Description</h1>

This is a console application developed by the DRUJBA team to manage an address book and notes. The application provides a set of commands for performing various operations such as adding notes, tags, searching, editing, and deleting records.

<h1>Features</h1>

<b>Address Book</b>: Manage contact information in the address book.

<b>Notes Book</b>: Keep track of notes with optional tags.

<h1>Available Commands</h1>

## Notes

| Command    | Description                                      |
|------------|--------------------------------------------------|
| help       | Shows a description of the commands               |
| exit       | To exit the session                               |
| make_note  | Make a note                                       |
| make_tag   | Make a tag                                        |
| find_note  | Search by title and notes                         |
| find_tag   | Search by tags                                    |
| edit_note  | Edits notes by ID (use search before use)         |
| edit_title | Edits titles to note by ID (use search before use)|
| del_note   | Deletes note by ID (use search before use)        |
| show_notes | Shows all notes                                   |

## Address Book

| Command        | Description                                         |
|----------------|-----------------------------------------------------|
| show_rec       | Shows all book records                              |
| make_rec       | Make a record to addressbook                        |
| find_rec       | Search in addressbook                               |
| del_rec        | Deletes record in addressbook by name (use search before use) |
| edit_ph_rec    | Edits phone to record in addressbook by name (use search before use) |
| remove_phone_rec| Remove phone from a record in the address book by name (use search before use) |
| add_phone_rec  | Add phone to a record in the address book by name (use search before use) |
| cong_rec       | Search contacts by days to birthday                 |
| import         | Import file in contacts                             |
| company_rec    | Add a company to a record in the address book by name (enter <SPACE> to remove) |
| comment_rec    | Add a comment to a record in the address book by name (enter <SPACE> to remove) |
| address_rec    | Add an address to a record in the address book by name (enter <SPACE> to remove) |
| exp_tag        | Exports contacts by tag to a JSON file (use search before use) |
| edit_tag_rec   | Edits tag to record in addressbook by name (use search before use) |
| add_tag_rec    | Add tag to a record in the address book by name   |
| remove_tag_rec | Remove tag from a record in the address book by name |
| add_birthday_rec| Add birthday to a record in the address book by name 'YYYY-MM-DD' |
| remove_birthday_rec| Remove birthday of the record in the address book by name |
| add_email_rec  | Add email to a record in the address book by name |
| remove_email_rec| Remove email of the record in the address book by name |
| edit_name_rec  | Edits name to record in addressbook by name (use search before use) |

## File Management

| Command        | Description                                            |
|----------------|--------------------------------------------------------|
| sort_by_type   | Sorts files by type (images, videos, documents, music, archives) |
| import         | Import file in contacts                                |
| exp_tag        | Exports contacts by tag to a JSON file (use search before use) |

## Email Operations

| Command        | Description                                            |
|----------------|--------------------------------------------------------|
| authorize_gmail| Authorizes a Google account                             |
| send_email     | Sends messages to email by tags                         |






<h1>Example</h1>

```python
Enter the command>>> make_note
Input title>>> My Note Title
Input note>>> This is the content of my note.
Do you want to enter a tag?>> yes
Input tag>>> Important
Note added
```
