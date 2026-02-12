import os
from abc import ABC, abstractmethod

class Book:
    def __init__(self, title, author):
        self._title = title
        self._author = author
        self._status = "доступна"

    def get_title(self):
        return self._title

    def get_author(self):
        return self._author

    def get_status(self):
        return self._status

    def set_status(self, new_status):
        if new_status == "доступна" or new_status == "выдана":
            self._status = new_status

    def info(self):
        return f"{self._title} - {self._author} ({self._status})"


class Person(ABC):
    def __init__(self, name):
        self._name = name

    def get_name(self):
        return self._name

    @abstractmethod
    def info(self):
        pass


class Librarian(Person):
    def info(self):
        return f"Библиотекарь: {self._name}"


class User(Person):
    def __init__(self, name):
        super().__init__(name)
        self._taken_books = []

    def get_taken_books(self):
        taken = []
        for book in self._taken_books:
            taken.append(book)
        return taken

    def take_book(self, book):
        self._taken_books.append(book)
        book.set_status("выдана")

    def return_book(self, book):
        if book in self._taken_books:
            self._taken_books.remove(book)
            book.set_status("доступна")
            return True
        return False

    def info(self):
        if len(self._taken_books) == 0:
            books_str = "нет книг"
        else:
            titles = []
            for b in self._taken_books:
                titles.append(b.get_title())
            books_str = ", ".join(titles)
        return f"Пользователь: {self._name} | Книги: {books_str}"


class Library:
    def __init__(self):
        self._books = []
        self._users = []
        self._librarians = []
        self.load_data()

    def load_data(self):
        if os.path.exists("books.txt"):
            f = open("books.txt", "r", encoding="utf-8")
            for line in f:
                line = line.strip()
                if line == "":
                    continue
                parts = line.split("|")
                if len(parts) == 3:
                    t, a, s = parts
                    book = Book(t, a)
                    book.set_status(s)
                    self._books.append(book)
            f.close()

        if os.path.exists("users.txt"):
            f = open("users.txt", "r", encoding="utf-8")
            for line in f:
                line = line.strip()
                if line == "":
                    continue
                parts = line.split("|")
                name = parts[0]
                user = User(name)
                if len(parts) > 1 and parts[1] != "":
                    titles = parts[1].split(",")
                    for t in titles:
                        book = self.find_book_by_title(t)
                        if book:
                            user.take_book(book)
                self._users.append(user)
            f.close()

        if os.path.exists("librarians.txt"):
            f = open("librarians.txt", "r", encoding="utf-8")
            for line in f:
                name = line.strip()
                if name != "":
                    self._librarians.append(Librarian(name))
            f.close()
        else:
            self._librarians.append(Librarian("Админ"))

    def save_data(self):
        f = open("books.txt", "w", encoding="utf-8")
        for book in self._books:
            f.write(f"{book.get_title()}|{book.get_author()}|{book.get_status()}\n")
        f.close()

        f = open("users.txt", "w", encoding="utf-8")
        for user in self._users:
            taken = user.get_taken_books()
            titles = []
            for b in taken:
                titles.append(b.get_title())
            taken_str = ",".join(titles)
            f.write(f"{user.get_name()}|{taken_str}\n")
        f.close()

        f = open("librarians.txt", "w", encoding="utf-8")
        for lib in self._librarians:
            f.write(f"{lib.get_name()}\n")
        f.close()
        print("Данные сохранены")

    def find_book_by_title(self, title):
        for book in self._books:
            if book.get_title().lower() == title.lower():
                return book
        return None

    def find_user_by_name(self, name):
        for user in self._users:
            if user.get_name().lower() == name.lower():
                return user
        return None

    def find_librarian_by_name(self, name):
        for lib in self._librarians:
            if lib.get_name().lower() == name.lower():
                return lib
        return None

    def add_book(self, title, author):
        book = Book(title, author)
        self._books.append(book)
        print(f"Книга '{title}' добавлена")

    def remove_book(self, title):
        book = self.find_book_by_title(title)
        if book is None:
            print("Книга не найдена")
            return
        for user in self._users:
            if book in user.get_taken_books():
                user.return_book(book)
        self._books.remove(book)
        print(f"Книга '{title}' удалена")

    def register_user(self, name):
        if self.find_user_by_name(name) is not None:
            print("Пользователь уже существует")
            return
        user = User(name)
        self._users.append(user)
        print(f"Пользователь '{name}' зарегистрирован")

    def show_all_users(self):
        if len(self._users) == 0:
            print("Нет пользователей")
            return
        print("Все пользователи:")
        for user in self._users:
            print(user.info())

    def show_all_books(self):
        if len(self._books) == 0:
            print("В библиотеке нет книг")
            return
        print("Все книги:")
        for book in self._books:
            print(book.info())

    def show_available_books(self):
        found = False
        for book in self._books:
            if book.get_status() == "доступна":
                print(book.info())
                found = True
        if not found:
            print("Нет доступных книг")

    def take_book(self, user_name, book_title):
        user = self.find_user_by_name(user_name)
        if user is None:
            print("Пользователь не найден")
            return
        book = self.find_book_by_title(book_title)
        if book is None:
            print("Книга не найдена")
            return
        if book.get_status() == "выдана":
            print("Книга уже выдана")
            return
        user.take_book(book)
        print(f"Книга '{book_title}' выдана {user_name}")


def main():
    lib = Library()

    while True:
        print("\nБИБЛИОТЕКА")
        print("1 - Библиотекарь")
        print("2 - Пользователь")
        print("0 - Выход")

        choice = input("Выберите: ")

        if choice == "0":
            lib.save_data()
            print("До свидания!")
            break

        elif choice == "1":
            name = input("Имя библиотекаря: ")
            librarian = lib.find_librarian_by_name(name)
            if librarian is None:
                print("Доступ запрещён")
                continue

            while True:
                print("\nМЕНЮ БИБЛИОТЕКАРЯ")
                print("1 - Добавить книгу")
                print("2 - Удалить книгу")
                print("3 - Зарегистрировать пользователя")
                print("4 - Список пользователей")
                print("5 - Список книг")
                print("0 - Назад")

                cmd = input("Действие: ")

                if cmd == "0":
                    break
                elif cmd == "1":
                    t = input("Название: ")
                    a = input("Автор: ")
                    lib.add_book(t, a)
                elif cmd == "2":
                    t = input("Название книги для удаления: ")
                    lib.remove_book(t)
                elif cmd == "3":
                    n = input("Имя нового пользователя: ")
                    lib.register_user(n)
                elif cmd == "4":
                    lib.show_all_users()
                elif cmd == "5":
                    lib.show_all_books()
                else:
                    print("Неверный ввод")

        elif choice == "2":
            name = input("Ваше имя: ")
            user = lib.find_user_by_name(name)
            if user is None:
                print("Пользователь не найден. Сначала зарегистрируйтесь.")
                continue

            while True:
                print("\nМЕНЮ ПОЛЬЗОВАТЕЛЯ")
                print("1 - Доступные книги")
                print("2 - Взять книгу")
                print("0 - Назад")

                cmd = input("Действие: ")

                if cmd == "0":
                    break
                elif cmd == "1":
                    lib.show_available_books()
                elif cmd == "2":
                    bt = input("Название книги: ")
                    lib.take_book(user.get_name(), bt)
                else:
                    print("Неверный ввод")

        else:
            print("Неверный выбор")


if __name__ == "__main__":
    main()