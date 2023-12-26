from drujba.Record import Record, Phone, Tag
from collections import UserList
from datetime import datetime, date
from drujba.Style import positive_action, command_message, book_style, error_message
from drujba.decorators import input_error
import json
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class AddressBook(UserList):
    def __init__(self, file_name):
        self.data = []
        self.exiting_data = []
        self.json_file_name = file_name
        self.user_info = None
        self.load_contacts()

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

    @input_error
    def add_full_record(self, name):
        record = Record(name, int(self.set_id()))
        record.phones.append(Phone(input(command_message('Enter Phone: '))))
        record.birthday.set_birthday = input(
            command_message('Enter Birthday YYYY-MM-DD: '))
        record.email.set_email = input(command_message('Enter Email: '))
        record.comment.set_comment = input(command_message('Enter comment: '))
        record.address.set_address = input(command_message('Enter address: '))
        record.company.set_company = input(command_message('Enter company: '))
        record.tags.append(Tag(input(command_message('Enter Tag: '))))
        self.data.append(record)
        self.serialize_to_json(record)
        self.save_contacts()
        return (positive_action(f'{record.name.get_name} added'))

    @input_error
    def add_record(self, name):

        record = Record(name, int(self.set_id()))
        self.data.append(record)
        self.serialize_to_json(record)
        self.save_contacts()
        return (positive_action(f'{record.name.get_name} added'))

    @input_error
    def remove_record(self, name):
        record = self.find_record(name)
        ex_record = self.find_exiting_record(name)
        self.data.remove(record)
        self.exiting_data.remove(ex_record)
        self.save_contacts()
        return positive_action(f'{record.name.get_name} removed.')

    def export_contacts_by_tag(self, target_tag: str):
        filtered_records = []
        for cont in self.data:
            for element in cont.tags:
                if element == Tag(target_tag):
                    filtered_records.append(cont)

        if filtered_records:
            tag_file_name = f'Contacts_{target_tag.lower()}.json'

            tag_data = []
            for record in filtered_records:
                serialize_record = {'Name': record.name.get_name,
                                    'ID': record.id.get_id,
                                    'Phones': [item.get_phone for item in record.phones],
                                    'Birthday': record.birthday.get_birthday.strftime('%Y-%m-%d') if isinstance(
                                        record.birthday.get_birthday, date) else None,
                                    'Email': record.email.get_email,
                                    'Comment': record.comment.get_comment,
                                    'Address': record.address.get_address,
                                    'Company': record.company.get_company,
                                    'Tags': [item.get_tag for item in record.tags],
                                    }
                tag_data.append(serialize_record)

            with open(tag_file_name, 'w') as tag_fh:
                json.dump(tag_data, tag_fh, indent=1)
                print("Success")
        else:
            print("Noooooo")

    # @input_error
    def import_files(self, file):
        script_directory = os.path.dirname(os.path.abspath(__file__))
        source_filepath = os.path.join(script_directory, self.json_file_name)
        import_file_path = os.path.join(script_directory, file)

        # Load source file
        with open(source_filepath, 'r') as source_file:
            source_content = source_file.read()
            source_data = json.loads(
                source_content) if source_content.strip() else []

        # Load import file and check if exist
        if not os.path.exists(import_file_path):
            print('Такого файлу не існує')
            return

        with open(import_file_path, 'r') as import_file:
            import_content = import_file.read()
            if not import_content.strip():  # check is empty
                print(f'Файл пустий')
                return
            import_file.seek(0)
            import_data = json.load(import_file)

        numbers1 = set(str(phone)
                       for obj in source_data for phone in obj.get("Phones") or [])
        import_data = [obj for obj in import_data if
                       not any(str(phone) in numbers1 for phone in obj.get("Phones") or [])]

        new_json = source_data + import_data
        count = 1

        for item in new_json:
            item['ID'] = count
            count += 1

        # Write data into source file
        with open(self.json_file_name, 'w') as destination_file:
            json.dump(new_json, destination_file, indent=2)

        print(f"Дані імпортовано у {self.json_file_name}")

    def serialize_to_json(self, record: Record):
        serialize_record = {'Name': record.name.get_name,
                            'ID': record.id.get_id,
                            'Phones': [item.get_phone for item in record.phones],
                            'Birthday': record.birthday.get_birthday.strftime('%Y-%m-%d') if isinstance(
                                record.birthday.get_birthday, date) else None,
                            'Email': record.email.get_email,
                            'Comment': record.comment.get_comment,
                            'Address': record.address.get_address,
                            'Company': record.company.get_company,
                            'Tags': [item.get_tag for item in record.tags],
                            }
        self.exiting_data.append(serialize_record)
    def find_exititng_record_id(self,id):
        #print(f'Type {type(id)} Value {id}')
        for item in self.exiting_data:
            if item['ID'] == id:
                return item
            
    @input_error
    def deserialize(self, dict) -> Record:
        record = Record(dict['Name'], dict['ID'])

        record.birthday.set_birthday = dict['Birthday']
        [record.phones.append(Phone(item))
         for item in dict['Phones'] if item is not None]
        record.email.set_email = dict['Email']
        if "Comment" in dict:
            record.comment.set_comment = dict['Comment']
        if 'Address' in dict:
            record.address.set_address = dict['Address']
        if "Company" in dict:
            record.company.set_company = dict['Company']
        if 'Tags' in dict:
            record.tags.extend([Tag(item) for item in dict['Tags']])

        return record

    @input_error
    def add_company(self, record: Record, serialize_record, company):
        record.company.set_company = company
        serialize_record['Company'] = company
        self.save_contacts()
        return f"{positive_action('Company')} {book_style(record.company.get_company)} {positive_action('added')}"

    @input_error
    def remove_company(self, record: Record, serialize_record, company):
        record.company.set_company = None
        serialize_record['Company'] = None
        self.save_contacts()
        return f"{positive_action('Company')} {book_style(record.company.get_company)} {positive_action('removed')}"

    @input_error
    # Додавання або зміна все існуючого коментаря
    def add_comment(self, record: Record, serialize_record, comment):
        record.comment.set_comment = comment
        serialize_record['Comment'] = comment
        self.save_contacts()
        return f'{positive_action("Comment")} {book_style(record.comment.get_comment)} {positive_action("added.")}'

    @input_error
    def remove_comment(self, record: Record, serialize_record):  # Видалення
        record.comment.set_comment = None
        serialize_record['Comment'] = None
        self.save_contacts()
        # Виправив помилку
        return f'{positive_action("Comment")} {book_style(record.comment.get_comment)} {positive_action("removed.")}'

    @input_error
    # Додавання або зміна вже існуючого адреса
    def add_address(self, record: Record, serialize_record, address):
        record.address.set_address = address
        serialize_record['Address'] = address
        self.save_contacts()
        return f'{positive_action("Address")} {book_style(record.address.get_address)} {positive_action("added.")}'

    @input_error
    def remove_address(self, record: Record, serialize_record):  # видалення адреси
        record.address.set_address = None
        serialize_record['Address'] = None
        self.save_contacts()
        return f'{positive_action("Address")} {book_style(record.address.get_address)} {positive_action("removed")}'

    @input_error
    def add_teg(self, record: Record, serialize_record, tag):
        record.tags.append(Tag(tag))
        serialize_record['Tags'].append(tag)
        self.save_contacts()
        return f"{positive_action(f'Tags:')} {book_style(f'{tag}')} {positive_action('added')}"

    @input_error
    def edit_teg(self, record: Record, serialize_record, old_tag, new_tag):
        for item in record.tags:
            if item.get_tag == old_tag:
                item.set_tag = new_tag
                break
            elif old_tag == "":
                item.set_tag = new_tag
                break

        for index, item in enumerate(serialize_record['Tags']):
            if item == old_tag:
                serialize_record['Tags'][index] = new_tag
                self.save_contacts()
                return True
            elif item == "":
                serialize_record['Tags'][index] = new_tag
                self.save_contacts()
                return True

    @input_error
    def remove_teg(self, record: Record, serialize_record, tag):
        removed_tags = [item for item in record.tags if item.get_tag == tag]

        if removed_tags:
            for removed_tag in removed_tags:
                record.tags.remove(removed_tag)

            serialize_record['Tags'] = [
                item for item in serialize_record['Tags'] if item != tag]
            self.save_contacts()
        else:
            raise ValueError("Tags is not found.")

    @input_error
    def add_phone(self, record: Record, serialize_record, phone) -> str:

        record.phones.append(Phone(phone))
        serialize_record['Phones'].append(phone)
        self.save_contacts()
        return f'{positive_action(f"Phone:")} {book_style(f"{phone}")} {positive_action("added.")}'

    def edit_phone(self, record: Record, serialize_record: {}, old_phone: str, new_phone: str) -> Record:
        
        print()
        for item in record.phones:
            if item.get_phone == old_phone:
                item.set_phone = new_phone
                break
        for index, item in enumerate(serialize_record['Phones']):
            if item == old_phone:
                
                serialize_record['Phones'][index] = new_phone
                self.save_contacts()                
                return True
        

    @input_error
    def remove_phone(self, record: Record, serialize_record, phone):
        if not record.phones:
            return error_message('Phone is None!')
        removed_phones = [
            item for item in record.phones if item.get_phone == phone]
        if removed_phones:
            for removed_phone in removed_phones:
                record.phones.remove(removed_phone)
            serialize_record['Phones'] = [
                item for item in serialize_record['Phones'] if item != phone]
            self.save_contacts()
            return f'{positive_action("Phone number")} {phone} {positive_action("successfully removed.")}'
        else:
            raise ValueError('ValueError: Phone number not found.')

    @input_error
    def add_birthday(self, record: Record, serialize_record, birthday):
        record.birthday.set_birthday = birthday
        serialize_record['Birthday'] = str(record.birthday.get_birthday)
        self.save_contacts()
        return f'{positive_action("Birthday ")} {book_style(record.birthday.get_birthday)} {positive_action("successfully added.")}'

    @input_error
    def remove_birthday(self, record: Record, serialize_record):
        if not record.birthday.set_birthday:
            return error_message('Birthday is None!')
        record.birthday.set_birthday = None
        serialize_record['Birthday'] = None
        self.save_contacts()
        return f'{positive_action("The Birthday of ")}{book_style(record.name.get_name)} {positive_action("was successfully deleted.")}'

    @input_error
    def add_email(self, record: Record, serialize_record, email):
        record.email.set_email = email
        serialize_record['Email'] = email
        self.save_contacts()
        return f'{positive_action("Email")} {book_style(record.email.get_email)} {positive_action("added.")}'

    @input_error
    def remove_email(self, record: Record, serialize_record):
        if not record.email.set_email:
            return error_message('Email is None!')
        old_email = record.email.set_email
        record.email.set_email = None
        serialize_record['Email'] = None
        self.save_contacts()
        return f'{positive_action("Email")} {book_style(old_email)} {positive_action("removed.")}'

    @input_error
    def rename(self, record: Record, serialize_record, name):
        old_name = str(record.name.get_name)
        record.name.set_name = name.capitalize()
        serialize_record['Name'] = name.capitalize()
        self.save_contacts()

        return f'{book_style(old_name)} {positive_action("changed")} {book_style(record.name.get_name)}.'

    @input_error
    def find_record(self, name) -> Record:
        records = []
        for item in self.data:
            if item.name.get_name == name.capitalize():
                records.append(item)
        if len(records) > 1:
            return records
        elif len(records) == 0:
            raise ValueError(f'{name} Not found!')
        else:
            return records[0]

    def find_record_id(self, id) -> Record:
        for item in self.data:
            if item.id.get_id == id:
                return item

    def find_exiting_record(self, name):
        for item in self.exiting_data:
            if item['Name'] == name.capitalize():
                return item

    @input_error
    def show_records(self, name=None):
        page = 1
        if name == None:

            for item in self.iterator(50):
                print(positive_action(
                    f'Page: {page} ------------------------------------------------'))
                print(item)
                page += 1

            # for item in self.data:
            #     print(item)
        elif isinstance(name, list):
            [print(item) for item in name]
        else:
            record = self.find_record(name)
            print(record)

    def load_contacts(self):
        if os.path.exists(self.json_file_name):

            with open(self.json_file_name, 'r') as fh:
                try:
                    self.exiting_data = json.load(fh)
                except json.JSONDecodeError:
                    return
                for item in self.exiting_data:
                    self.data.append(self.deserialize(item))
        else:
            print(f'{self.json_file_name} Not Found!')

    def save_contacts(self):
        with open(self.json_file_name, 'w') as fh:
            json.dump(self.exiting_data, fh, indent=1)

    def iterator(self, item_number):
        counter = 0
        result = ''
        for item in self.data:
            result += f'{item}\n'
            counter += 1
            if counter >= item_number:
                yield result
                counter = 0
                result = ''
        if result != '':
            yield result

    def find(self, search_string):
        find_contacts = []
        for item in self.data:
            name = item.name.get_name
            phone_numbers = [phone.get_phone for phone in item.phones]
            birthday = str(item.birthday.get_birthday)
            email = item.email.get_email
            tags = [tag.get_tag for tag in item.tags]
            if tags:
                for tag in tags:
                    if tag is not None and search_string.lower() in tag.lower():
                        find_contacts.append(item)
                        continue

            if name != None and search_string.lower() in name.lower():
                find_contacts.append(item)
                continue

            if len(phone_numbers) > 0:
                for phone in phone_numbers:
                    if search_string in phone:
                        find_contacts.append(item)
                        continue
            if birthday != None and search_string in birthday:
                find_contacts.append(item)
                continue
            if email != None and search_string in email:
                find_contacts.append(item)
                continue

        return find_contacts

    @input_error
    def congratulation(self, days_to_happy: str):
        happy_list = []
        current_date = datetime.today().date()
        if 0 <= int(days_to_happy) <= 365:
            for record in self.data:
                if record.birthday.get_birthday:
                    next_birthday = record.birthday.get_birthday.replace(
                        year=current_date.year)
                    if next_birthday < current_date:
                        next_birthday = record.birthday.get_birthday.replace(
                            year=current_date.year + 1)

                    if int(days_to_happy) == (next_birthday - current_date).days:
                        happy_list.append(record)
        return happy_list

    def set_up_email(self):
        email = input(command_message('Enter Email:'))
        password = input(command_message('Enter Password:'))
        self.user_info._email = email
        self.user_info._email_password = password
        self.user_info.encryptor(
            self.user_info._user_name, self.user_info._user_password._password)

        # console.rule(title=f"[green]Autho[/green]", style="bright_magenta")

    def get_contacts_by_tags(self, search_tag):

        contacts = []
        for item in self.data:

            if search_tag in [tag.get_tag for tag in item.tags]:
                contacts.append(item)
        return contacts

    def send_message(self):
        tag = input('Enter Tag:')
        self.message_sender(self.get_contacts_by_tags(tag))

    def message_sender(self, list_contacts: list[Record]):
        if self.user_info.testLogin():
            if self.user_info is not None:
                email = self.user_info._email
                password = self.user_info._email_password
                if email != 'None' and password != 'None':

                    receiver_email = [
                        item.email.get_email for item in list_contacts if item.email.get_email is not None]
                    title = input(command_message('Enter Message Title'))
                    message_body = input(command_message('Enter Message'))

                    smtp_server = 'smtp.gmail.com'
                    port = 587

                    for r_email in receiver_email:

                        message = MIMEMultipart()
                        message['From'] = email

                        message['To'] = r_email
                        message['Subject'] = title

                        message.attach(MIMEText(message_body, 'plain'))

                        with smtplib.SMTP(smtp_server, port) as server:
                            server.starttls()
                            server.login(email, password)
                            text = message.as_string()

                            server.sendmail(email, r_email, text)
                            print('Лист успішно відправлено!')
                else:
                    print("Для відправки повідомлень треба підключити гугл аккаунт")

                    if input('Підключити? y/n') == 'y':
                        email = input('Enter Email:')
                        password = input('Enter Password')
                        self.user_info.add_email(email, password)
            else:
                print('Для відправки повідомлень потрібно залогінитись')
