from collections import UserList
from Notes import NotesRecord, Tag
import json
import re
from decorators import input_error


class NotesBook(UserList):
    def __init__(self, file_name):
        self.data = []
        self.exiting_data = []
        self.json_file_name = file_name
        self.last_id = 0
        self.load_notes()

    # генерація ID
    def set_id(self):
        if len(self.exiting_data) == 0:
            id = 1
            return id
        else:
            id_values = []
            for item in self.exiting_data:
                id_values.append(item['ID'])
            max_id = max(id_values)

            for id in range(1, max_id):
                if id in id_values:
                    continue
                else:
                    return id
        return max_id + 1

    # серіалізація
    def serialize_to_json(self, notes: NotesRecord):
        serialize_note_records = {
            'ID': notes.note_id.get_id,
            'Title': notes.title.get_title,
            'Note': notes.note.get_note,
            'Tags': [item.get_tag for item in notes.tag],
            'Addition Date': notes.addition_date.get_date,
        }
        self.exiting_data.append(serialize_note_records)

    # збереження в файл
    def save(self):
        with open(self.json_file_name, 'w') as fh:
            json.dump(self.exiting_data, fh, indent=1)

    # десеріалізація
    def deserialize(self, dict) -> NotesRecord:
        Notes_record = NotesRecord(
            id=dict['ID'], title=dict['Title'], note=dict['Note'],)
        [Notes_record.tag.append(Tag(item)) for item in dict['Tags']]
        return Notes_record

    # завантаження з файлу
    def load_notes(self):
        with open(self.json_file_name, 'a+') as fh:
            try:
                self.exiting_data = json.load(fh)
            except json.JSONDecodeError:
                return
            for item in self.exiting_data:
                self.data.append(self.deserialize(item))

    # введення нотатки
    @input_error
    def add_note(self,  input_title: str, input_note: str):
        calc_id = self.set_id()
        rec_note = NotesRecord(
            id=calc_id, note=input_note, title=input_title)
        self.last_id = calc_id
        self.data.insert(calc_id-1, rec_note)
        self.serialize_to_json(rec_note)

    # додавання тегів
    @input_error
    def add_tag(self, input_tag: str, find_to_id=None):
        find_to_id = self.last_id if find_to_id == None else int(find_to_id)
        self.data[find_to_id-1].tag.append(Tag(input_tag))

    # зберігання нотатків
    def save_note(self):
        self.exiting_data = []
        for s in self.data:
            self.serialize_to_json(s)
        self.save()

    # пошук по нотатці та заголовку
    def find_note(self, input_string: str):
        find_list = []
        if input_string != '':
            for rec in self.data:
                if isinstance(rec.title.get_title, str) and re.search(input_string.lower(), rec.title.get_title.lower()):
                    find_list.append(rec) if not id(rec) in [
                        id(p) for p in find_list] else None
                if isinstance(rec.note.get_note, str) and re.search(input_string.lower(), rec.note.get_note.lower()):
                    find_list.append(rec) if not id(rec) in [
                        id(p) for p in find_list] else None
                if isinstance(rec.addition_date.get_date, str) and re.search(input_string.lower(), rec.addition_date.get_date.lower()):
                    find_list.append(rec) if not id(rec) in [
                        id(p) for p in find_list] else None
        return find_list

    # пошук по тегу
    def find_tag(self, input_tag: str):
        find_list = []
        if input_tag != '':
            for rec in self.data:
                if isinstance(rec.tag, list):
                    for f in [p.get_tag for p in rec.tag]:
                        if re.search(input_tag.lower(), f.lower()):
                            find_list.append(rec) if not id(rec) in [
                                id(p) for p in find_list] else None
        return find_list

    # пошук нотатки по ідентифікатору
    def find_note_id(self, input_id: str):
        find_list = []
        if input_id != '':
            for rec in self.data:
                if isinstance(rec.note_id.get_id, int) and re.search(input_id.lower(), str(rec.note_id.get_id).lower()):
                    find_list.append(rec) if not id(rec) in [
                        id(p) for p in find_list] else None
        return find_list

    # редагування нотатки
    def edit_note(self, input_id: str, input_string: str):
        if input_id != '':
            for index, item in enumerate(self.data):
                if item.note_id.get_id == int(input_id):
                    # print(index)
                    self.data[index].note.set_note = input_string

    # видалення нотатки
    def delete_note(self, input_id: str):
        if input_id != '':
            for index, item in enumerate(self.data):
                if item.note_id.get_id == int(input_id):
                    # print(index)
                    self.data.pop(index)

    # редагування заголовку
    @input_error
    def edit_title(self, input_id: str, input_string: str):
        if input_id != '':
            for index, item in enumerate(self.data):
                if item.note_id.get_id == int(input_id):
                    # print(index)
                    self.data[index].title.set_title = input_string
