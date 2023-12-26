from abc import ABC, abstractmethod
import json
import datetime
from drujba.Style import book_style, positive_action
from drujba.decorators import input_error
import re
import calendar


class Field(ABC):
    @abstractmethod
    def __str__(self):
        pass


class Tag(Field):
    def __init__(self, tag):
        self._tag = None
        self.set_tag = tag

    @property
    def get_tag(self):
        return self._tag

    @get_tag.setter
    def set_tag(self, tag: str):
            self._tag = tag

    def __eq__(self, other):
        return isinstance(other, Tag) and self._tag == other._tag

    def __str__(self):
        return f"{self.get_tag}"


class Company(Field):  # Новий клас компания
    def __init__(self, company: str):
        self._company = None
        self.set_company = company

    @property
    def get_company(self):
        return self._company

    @get_company.setter
    def set_company(self, value: str):
        if bool(value) is False:
            self._company = None
        else:
            self._company = value

    def __str__(self):
        return f"{self.get_company}"


class Address(Field):  # Новий класс адреси
    def __init__(self, address: str):
        self._address = None
        self.set_address = address

    @property
    def get_address(self):
        return self._address

    @get_address.setter
    def set_address(self, value: str):
        if bool(value) is None or bool(value) is False:
            self._address = None
        else:
            self._address = value

    def __str__(self):
        return f"{self.get_address}"


class Comment(Field):  # новий клас
    def __init__(self, comment: str):
        self._comment = None
        self.set_comment = comment

    @property
    def get_comment(self):
        return self._comment

    @get_comment.setter
    def set_comment(self, value: str):
        if value is None or bool(value) is False:
            self._comment = None
        elif value.strip():
            self._comment = value

    def __str__(self):
        return f"{self.get_comment}"


class ID(Field):
    def __init__(self, id) -> None:
        self._id = None
        self.set_id = id

    # GETTER
    @property
    def get_id(self):
        return self._id

    # SETTER
    @get_id.setter
    def set_id(self, value):

        if type(value) is int:
            self._id = value
        else:
            print('Incrorrect ID')

    def __str__(self):
        return f'{self.get_id}'


class Name(Field):
    def __init__(self, name) -> None:
        self._name = None
        self.set_name = name.capitalize()

    @property
    def get_name(self):
        return self._name

    @get_name.setter
    def set_name(self, value: str):

        name = value.split()

        chars_count = 0
        for letter in name:
            if letter.isalpha():
                chars_count += len(letter)
            else:
                raise ValueError(
                    'ValueError: The name should consist only of letters and spaces. Minimum length is 3 characters, '
                    'maximum is 20. Please try again.')
        chars_count += len(name)
        if chars_count >= 3 and chars_count <= 20:
            self._name = value
        else:
            raise ValueError(
                'ValueError: The name should consist only of letters and spaces. Minimum length is 3 characters, '
                'maximum is 20. Please try again.')

    def __str__(self):
        return f'{self.get_name}'


class Phone(Field):
    def __init__(self, phone):
        self._phone = None
        self.set_phone = phone

    @property
    def get_phone(self):
        return self._phone

    @get_phone.setter
    def set_phone(self, phone: str):
        if phone.isdigit() and len(phone) == 10:
            self._phone = phone
        elif bool(phone) is False:
            self._phone = None
        else:
            raise ValueError('ValueError: Phone Number must have 10 numbers ex: 0501952343')

    def __str__(self):
        return f'{self.get_phone}'


class Birthday(Field):
    def __init__(self, birthday) -> None:
        self._birthday = None
        self.set_birthday = birthday

    @property
    def get_birthday(self):
        return self._birthday

    @get_birthday.setter
    def set_birthday(self, birthday):

        if isinstance(birthday, str) and birthday != '':
            birthday_date = birthday.split('-')
            if len(birthday_date) != 3:
                raise ValueError(
                    "Invalid birthday date. Please enter the date in 'YYYY-MM-DD' format.")
            year = birthday_date[0]
            mounth = birthday_date[1]
            day = birthday_date[2]
            if not year.isdigit() or len(year) != 4:
                raise ValueError('The year consists only of numbers and has 4 characters.')
            if not mounth.isdigit() or len(mounth) > 2:
                raise ValueError('The month consists only of numbers and contains 2 symbols.')
            if int(mounth) > 12:
                raise ValueError('The month can have values ​​from 1 to 12.')
            if not day.isdigit():
                raise ValueError('The day consists only of numbers.')
            days_in_mounth = calendar.monthrange(int(year), int(mounth))[1]
            if int(day) > days_in_mounth:
                raise ValueError(f'Wrong day, the month has only {days_in_mounth} days.')
            self._birthday = datetime.date(int(year), int(mounth), int(day))

        elif birthday == None:
            self._birthday = None

    def __str__(self):
        return f'{str(self._birthday)}'


class Email(Field):
    def __init__(self, email) -> None:
        self._email = None
        self.set_email = email
        
    def find_all_emails(self, email):
        result = re.findall(r"[a-zA-Z][\w_.]+@\w{2,}\.\w{2,}", email)
        return result

    @property
    def get_email(self):
        return self._email

    @get_email.setter
    def set_email(self, email):
        if email:
            if self.find_all_emails(email):
                self._email = email
            else:
                raise ValueError('Wrong email format.')
        else:
            self._email = None

    def __str__(self):
        return f'{self.get_email}'


class Record:
    def __init__(self, name, id, birthday=None, email=None, comment=None, address=None, company=None):
        self.name = Name(name)
        self.id = ID(int(id))
        self.phones = []
        self.birthday = Birthday(birthday)
        self.email = Email(email)
        self.comment = Comment(comment)
        self.address = Address(address)
        self.company = Company(company)
        self.tags = []

    def __str__(self):
        return (f'{positive_action("ID:")} {book_style(self.id.get_id)} '
                f'{positive_action("Name:")} {book_style(self.name.get_name)} '
                f'{positive_action("Phones:")} {book_style(" ".join([str(item) for item in self.phones]))} '
                f'{positive_action("Birthday:")} {book_style(self.birthday.get_birthday)} '
                f'{positive_action("Email:")} {book_style(self.email.get_email)} '
                f'{positive_action("Comment:")} {book_style(self.comment.get_comment)} '
                f'{positive_action("Address:")} {book_style(self.address.get_address)} '
                f'{positive_action("Company:")} {book_style(self.company.get_company)} '
                f'{positive_action("Tags:")} {book_style(" ".join([str(i) for i in self.tags]))} ')

