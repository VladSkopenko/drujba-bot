from abc import ABC,abstractmethod
from datetime import datetime


class Field(ABC):
     @abstractmethod
     def __str__(self):
          pass

class Note_id(Field): # ID нотатки
    def __init__(self,note_id) -> None:
        self._id = None
        self.set_id = note_id
     
    @property
    def get_id(self): #getter повертає данні з поля _id
        return self._id
     #SETTER
    @get_id.setter
    def set_id(self,value): #setter перезаписує данні поля _id (Потреби в зміні id немає воно створюється при додаванні нотатки та є ідентефікатором)
        if type(value) is int:
            self._id = value
        else:
            print('Incrorrect ID')
               

    def __str__(self):
        return f'{self.get_id}'
     

class Title(Field): # Титул
    def __init__(self,title):
        self._title = None
        self.set_title = title
    @property
    def get_title(self): #getter повертає данні з поля _title
        return self._title
    
    @get_title.setter
    def set_title(self,title: str): # Перезаписує данні поля _title
        #Валідація
        if title == None: # Не може бути None 
            raise ValueError('Класс title, Метод set_title, в якості аргумента None -> очікується string: НЕКОРЕКТНІ ДАННІ ') 
        if len(title) < 3 or len(title) > 10: # Може містити від 3 до 10 символів
            raise ValueError('Класс Title, Метод set_title() значення менше 3 або більше 10: НЕКОРЕКТНІ ДАННІ')
        else:
            self._title = title    
    def __str__(self):
        return f'{self.get_title}'



class Note(Field): #Класс Нотатка
    def __init__(self,note):
        self._note = None
        self.set_note = note
    @property 
    def get_note(self): #getter повертає данні поля _note 
        return self._note
    @get_note.setter
    def set_note(self,note): # Перезаписує данні поля _note
        #Валідація
        if note == None: # Не може бути None 
            raise ValueError('Класс Note, Метод set_note, в якості аргумента None: НЕКОРЕКТНІ ДАННІ')     
        elif len(note) < 3: # не може бути менше 3 символів
            raise ValueError('Класс Note, Метод set_note, Нотатка має менше 3 символів: НЕКОРЕКТНІ ДАННІ')
        else:
            self._note = note
    def __str__(self):
        return f'{self.get_note}'
    
class Tag(Field): #Класс тег
    def __init__(self,tag):
        self._tag = None
        self.set_tag = tag
    @property 
    def get_tag(self): # getter повертає данні поля _tag
        return self._tag
    @get_tag.setter #setter перезаписує данні поля _tag
    def set_tag(self,tag: str):
        tag = tag.split()
        if len(tag) == 0 or len(tag) > 1: # один тег не може містити більше 1 слова
            raise ValueError(f'Класс Tag, Метод set_tag, тег складається з {tag} cлів очікується 1 слово: НЕКОРЕКТНІ ДАННІ')
        elif len(tag[0]) < 3 or len(tag[0]) > 10: # не може бути менше 3 і більше 10
            raise ValueError(f'Класс Tag, Метод set_tag, тег {tag[0]} має {len(tag[0])} букв очікується більше 3 і менше 10: НЕКОРЕКТНІ ДАННІ  ')
        else:
            self._tag = tag[0] 
    def __str__(self):
        return f'{self.get_tag}'

class AdditionDate(Field): # Класс дата додавання нотатки
    def __init__(self,date):
        self._date = None
        if date != None:
            self._date = date
        
    @property
    def get_date(self): #getter повертає данні поля _date
        return str(self._date)
    
    @get_date.setter #setter змінює данні поля _date (потреба змінити дату буде тільки при редагуванні нотатки)
    def set_date(self,date):
        self._date = date
    
    def __str__(self):
        return f'{str(self.get_date)}'


class NotesRecord(): # Об'єкт нотатка, використовує всі вище створенні поля та записується в список data класу Notesbook
    
    def __init__(self,id,title=None,note: Note =None,tag = None):
        self.note_id = Note_id(id)
        self.title = Title(title)
        self.note = Note(note)
        self.tag = []
        if tag != None:
            self.tag.append(Tag(tag))
        self.addition_date = AdditionDate(datetime.now().date())

    def __str__(self):
        return f'ID: {str(self.note_id)}\nTitle: {self.title}\nNote: {self.note}\nTags: {" ".join([str(item) for item in self.tag])} \nDate addition: {str(self.addition_date)} '    
#якщо припустити що такий об'єкт є в нашому списку NotesBook.data то ми можем звертатись до його полів за допомогою геттера та сеттера 
#Приклад 
# Notesbook.data[1].title.get_title поверне данні з поля title
# Notesbook.data[1].title.set_title = 'NEW TITLE' змінить поле title якщо воно пройде валідацію
# Аналогічно зі всіма остальними полями  



         


        
     
     
     
               
    

