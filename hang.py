import tkinter as tk
from tkinter import messagebox
import random
import nltk
from nltk.corpus import words

# Загрузка словаря NLTK
nltk.download('words')
english_words = set(words.words())

# Список слов для игры "Виселица"
HANGMAN_WORDS = ["python", "tkinter", "hangman", "development", "interface", "programming"]
# Список слов для игры "Слова из слова"
WORDS_FROM_WORD = ["development", "programming", "interface"]

class WordGamesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Игры со словами")

        self.main_menu()

    def main_menu(self):
        self.clear_screen()

        self.label = tk.Label(self.root, text="Выберите игру:")
        self.label.pack(pady=10)

        self.hangman_button = tk.Button(self.root, text="Виселица", command=self.start_hangman)
        self.hangman_button.pack(pady=5)

        self.words_from_word_button = tk.Button(self.root, text="Слова из слова", command=self.start_words_from_word)
        self.words_from_word_button.pack(pady=5)

        self.word_on_last_letter_button = tk.Button(self.root, text="Слово на последнюю букву", command=self.start_word_on_last_letter)
        self.word_on_last_letter_button.pack(pady=5)

    def start_hangman(self):
        self.clear_screen()
        self.hangman_game = HangmanGame(self.root, self.main_menu)

    def start_words_from_word(self):
        self.clear_screen()
        self.words_from_word_game = WordsFromWordGame(self.root, self.main_menu)

    def start_word_on_last_letter(self):
        self.clear_screen()
        self.word_on_last_letter_game = WordOnLastLetterGame(self.root, self.main_menu)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()


class HangmanGame:
    def __init__(self, root, back_callback):
        self.root = root
        self.back_callback = back_callback

        self.word = random.choice(HANGMAN_WORDS)
        self.guesses = []
        self.mistakes = 0

        self.create_widgets()
        self.update_display()

    def create_widgets(self):
        self.canvas = tk.Canvas(self.root, width=400, height=400)
        self.canvas.pack()

        self.label = tk.Label(self.root, text="Угадайте слово:")
        self.label.pack()

        self.word_display = tk.Label(self.root, font=('Consolas', 24))
        self.word_display.pack()

        self.entry = tk.Entry(self.root)
        self.entry.pack()
        self.entry.bind('<Return>', self.process_guess)

        self.guess_button = tk.Button(self.root, text="Угадать", command=self.process_guess)
        self.guess_button.pack()

        self.mistakes_label = tk.Label(self.root, text="Ошибки: 0")
        self.mistakes_label.pack()

        self.restart_button = tk.Button(self.root, text="Начать заново", command=self.restart_game)
        self.restart_button.pack()

        self.back_button = tk.Button(self.root, text="Назад", command=self.back_callback)
        self.back_button.pack()

    def update_display(self):
        display_word = " ".join([letter if letter in self.guesses else "_" for letter in self.word])
        self.word_display.config(text=display_word)

        self.canvas.delete("all")
        self.draw_hangman()

        if "_" not in display_word:
            messagebox.showinfo("Поздравляем!", "Вы угадали слово!")
            self.restart_game()

        if self.mistakes >= 6:
            messagebox.showinfo("Игра окончена", f"Вы проиграли! Загаданное слово было: {self.word}")
            self.restart_game()

    def process_guess(self, event=None):
        guess = self.entry.get().lower()
        self.entry.delete(0, tk.END)

        if len(guess) != 1 or not guess.isalpha():
            messagebox.showwarning("Неверный ввод", "Пожалуйста, введите одну букву.")
            return

        if guess in self.guesses:
            messagebox.showwarning("Уже угадано", "Вы уже угадали эту букву.")
            return

        self.guesses.append(guess)

        if guess not in self.word:
            self.mistakes += 1

        self.mistakes_label.config(text=f"Ошибки: {self.mistakes}")
        self.update_display()

    def draw_hangman(self):
        if self.mistakes > 0:
            self.canvas.create_line(50, 350, 150, 350)
        if self.mistakes > 1:
            self.canvas.create_line(100, 350, 100, 50)
        if self.mistakes > 2:
            self.canvas.create_line(100, 50, 250, 50)
        if self.mistakes > 3:
            self.canvas.create_line(250, 50, 250, 100)
        if self.mistakes > 4:
            self.canvas.create_oval(225, 100, 275, 150)
        if self.mistakes > 5:
            self.canvas.create_line(250, 150, 250, 250)
        if self.mistakes > 6:
            self.canvas.create_line(250, 200, 225, 225)
            self.canvas.create_line(250, 200, 275, 225)
            self.canvas.create_line(250, 250, 225, 275)
            self.canvas.create_line(250, 250, 275, 275)

    def restart_game(self):
        self.word = random.choice(HANGMAN_WORDS)
        self.guesses = []
        self.mistakes = 0
        self.mistakes_label.config(text="Ошибки: 0")
        self.update_display()


class WordsFromWordGame:
    def __init__(self, root, back_callback):
        self.root = root
        self.back_callback = back_callback

        self.words = set(words.words())
        self.used_words = set()
        self.words_found = 0

        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self.root, text="Составьте слова из слова:")
        self.label.pack()

        self.entry = tk.Entry(self.root)
        self.entry.pack()
        self.entry.bind('<Return>', self.process_word)

        self.submit_button = tk.Button(self.root, text="Отправить", command=self.process_word)
        self.submit_button.pack()

        self.words_label = tk.Label(self.root, text="Найденные слова:")
        self.words_label.pack()

        self.words_display = tk.Label(self.root, text="", font=('Consolas', 14))
        self.words_display.pack()

        self.back_button = tk.Button(self.root, text="Назад", command=self.back_callback)
        self.back_button.pack()

    def process_word(self, event=None):
        word = self.entry.get().lower()
        self.entry.delete(0, tk.END)

        if len(word) < 2:
            messagebox.showwarning("Слишком короткое слово", "Слово должно содержать не менее 2 букв.")
            return

        if word in self.used_words:
            messagebox.showwarning("Уже использовано", "Вы уже использовали это слово.")
            return

        if word in self.words and all(word.count(letter) <= self.word.count(letter) for letter in word):
            self.used_words.add(word)
            self.words_found += 1
            self.update_display()
            if self.words_found >= 5:
                messagebox.showinfo("Поздравляем!", "Вы нашли 5 слов!")
                self.back_callback()
        else:
            messagebox.showwarning("Неправильное слово", "Это слово не может быть составлено из предложенного или его нет в словаре.")

    def update_display(self):
        words_text = "\n".join(sorted(self.used_words))
        self.words_display.config(text=words_text)


class WordOnLastLetterGame:
    def __init__(self, root, back_callback):
        self.root = root
        self.back_callback = back_callback

        self.words = set(words.words())
        self.used_words = set()
        self.words_found = 0
        self.last_letter = random.choice(list('abcdefghijklmnopqrstuvwxyz'))

        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self.root, text=f"Слова на букву '{self.last_letter}':")
        self.label.pack()

        self.entry = tk.Entry(self.root)
        self.entry.pack()
        self.entry.bind('<Return>', self.process_word)

        self.submit_button = tk.Button(self.root, text="Отправить", command=self.process_word)
        self.submit_button.pack()

        self.words_label = tk.Label(self.root, text="Найденные слова:")
        self.words_label.pack()

        self.words_display = tk.Label(self.root, text="", font=('Consolas', 14))
        self.words_display.pack()

        self.back_button = tk.Button(self.root, text="Назад", command=self.back_callback)
        self.back_button.pack()

    def process_word(self, event=None):
        word = self.entry.get().lower()
        self.entry.delete(0, tk.END)

        if len(word) < 2:
            messagebox.showwarning("Слишком короткое слово", "Слово должно содержать не менее 2 букв.")
            return

        if word[0] != self.last_letter:
            messagebox.showwarning("Неправильная буква", f"Слово должно начинаться с буквы '{self.last_letter}'.")
            return

        if word in self.used_words:
            messagebox.showwarning("Уже использовано", "Вы уже использовали это слово.")
            return

        if word in self.words:
            self.used_words.add(word)
            self.words_found += 1
            self.update_display()
            if self.words_found >= 10:
                messagebox.showinfo("Поздравляем!", "Вы нашли 10 слов!")
                self.back_callback()
        else:
            messagebox.showwarning("Неправильное слово", "Это слово отсутствует в словаре.")

    def update_display(self):
        words_text = "\n".join(sorted(self.used_words))
        self.words_display.config(text=words_text)


if __name__ == "__main__":
    root = tk.Tk()
    app = WordGamesApp(root)
    root.mainloop()

