import json
import os
import datetime

NOTES_FILE = "notes.json"


class Note:
    def __init__(self, note_id, title, body, created_at, updated_at):
        self.id = note_id
        self.title = title
        self.body = body
        self.created_at = created_at
        self.updated_at = updated_at


class NoteModel:
    def __init__(self):
        self.notes = []

    def load_notes(self):
        if os.path.exists(NOTES_FILE):
            with open(NOTES_FILE, "r") as file:
                try:
                    notes_data = json.load(file)
                    self.notes = [
                        Note(note_data["id"], note_data["title"], note_data["body"], note_data["created_at"],
                             note_data["updated_at"])
                        for note_data in notes_data
                    ]
                except json.JSONDecodeError:
                    pass

    def save_notes(self):
        notes_data = [
            {
                "id": note.id,
                "title": note.title,
                "body": note.body,
                "created_at": note.created_at,
                "updated_at": note.updated_at,
            }
            for note in self.notes
        ]
        with open(NOTES_FILE, "w") as file:
            json.dump(notes_data, file)


class NotePresenter:
    def __init__(self, model):
        self.model = model

    def show_notes(self):
        if not self.model.notes:
            print("Нет заметок.")
        else:
            for note in self.model.notes:
                print(f"[{note.id}] {note.title}: {note.body}")
                print(f"Дата создания: {note.created_at}")
                print(f"Последнее изменение: {note.updated_at}")
                print()

    def add_note(self, title, body):
        note_id = len(self.model.notes) + 1
        created_at = datetime.datetime.now().isoformat()
        updated_at = created_at
        note = Note(note_id, title, body, created_at, updated_at)
        self.model.notes.append(note)
        self.model.save_notes()
        print("Заметка добавлена.")

    def edit_note(self, note_id, title, body):
        for note in self.model.notes:
            if note.id == note_id:
                note.title = title
                note.body = body
                note.updated_at = datetime.datetime.now().isoformat()
                self.model.save_notes()
                print("Заметка отредактирована.")
                return
        print("Заметка не найдена.")

    def delete_note(self, note_id):
        for note in self.model.notes:
            if note.id == note_id:
                self.model.notes.remove(note)
                self.model.save_notes()
                print("Заметка удалена.")
                return
        print("Заметка не найдена.")


class NoteView:
    def __init__(self, presenter):
        self.presenter = presenter

    def display_menu(self):
        print("===== Заметки =====")
        print("1. Показать заметки")
        print("2. Добавить заметку")
        print("3. Редактировать заметку")
        print("4. Удалить заметку")
        print("5. Выход")

    def get_user_choice(self):
        choice = input("Выберите действие (1-5): ")
        return choice.strip()

    def show_notes(self):
        self.presenter.show_notes()

    def add_note(self):
        title = input("Введите заголовок заметки: ")
        body = input("Введите текст заметки: ")
        self.presenter.add_note(title, body)

    def edit_note(self):
        note_id = int(input("Введите ID заметки для редактирования: "))
        title = input("Введите новый заголовок заметки: ")
        body = input("Введите новый текст заметки: ")
        self.presenter.edit_note(note_id, title, body)

    def delete_note(self):
        note_id = int(input("Введите ID заметки для удаления: "))
        self.presenter.delete_note(note_id)

    def show_message(self, message):
        print(message)


def main():
    model = NoteModel()
    model.load_notes()
    presenter = NotePresenter(model)
    view = NoteView(presenter)

    while True:
        view.display_menu()
        choice = view.get_user_choice()

        if choice == "1":
            view.show_notes()
        elif choice == "2":
            view.add_note()
        elif choice == "3":
            view.edit_note()
        elif choice == "4":
            view.delete_note()
        elif choice == "5":
            break
        else:
            view.show_message("Некорректный выбор. Попробуйте еще раз.")

        print()


if __name__ == "__main__":
    main()
