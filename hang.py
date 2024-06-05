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
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        self.main_menu()

    def main_menu(self):
        self.clear_screen()

        self.label = tk.Label(self.root, text="Выберите игру:", font=("Arial", 24), bg="#f0f0f0")
        self.label.pack(pady=20)

        self.hangman_button = tk.Button(self.root, text="Виселица", font=("Arial", 18), command=self.start_hangman, bg="#4CAF50", fg="white", width=25)
        self.hangman_button.pack(pady=10)

        self.words_from_word_button = tk.Button(self.root, text="Слова из слова", font=("Arial", 18), command=self.start_words_from_word, bg="#2196F3", fg="white", width=25)
        self.words_from_word_button.pack(pady=10)

        self.word_on_last_letter_button = tk.Button(self.root, text="Слово на последнюю букву", font=("Arial", 18), command=self.start_word_on_last_letter, bg="#FF5722", fg="white", width=25)
        self.word_on_last_letter_button.pack(pady=10)

    def start_hangman(self):
        self.clear_screen()
        self.root.geometry("800x1000")
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
        self.canvas = tk.Canvas(self.root, width=400, height=400, bg="#FFFFFF", bd=2, relief="groove")
        self.canvas.pack(pady=20)

        self.label = tk.Label(self.root, text="Угадайте слово:", font=("Arial", 18), bg="#f0f0f0")
        self.label.pack()

        self.word_display = tk.Label(self.root, font=('Consolas', 28), bg="#f0f0f0")
        self.word_display.pack(pady=10)

        self.entry = tk.Entry(self.root, font=("Arial", 18))
        self.entry.pack(pady=10)
        self.entry.bind('<Return>', self.process_guess)

        self.guess_button = tk.Button(self.root, text="Угадать", font=("Arial", 18), command=self.process_guess, bg="#9C27B0", fg="white", width=12)
        self.guess_button.pack(pady=10)

        self.mistakes_label = tk.Label(self.root, text="Ошибки: 0", font=("Arial", 18), bg="#f0f0f0")
        self.mistakes_label.pack(pady=10)

        self.guesses_label = tk.Label(self.root, text="Названные буквы: ", font=("Arial", 18), bg="#f0f0f0")
        self.guesses_label.pack(pady=10)

        self.restart_button = tk.Button(self.root, text="Начать заново", font=("Arial", 16), command=self.restart_game, bg="#FFC107", fg="black", width=20)
        self.restart_button.pack(pady=5)

        self.back_button = tk.Button(self.root, text="Назад", font=("Arial", 16), command=self.back_callback, bg="#607D8B", fg="white", width=20)
        self.back_button.pack(pady=5)

    def update_display(self):
        display_word = " ".join([letter if letter in self.guesses else "_" for letter in self.word])
        self.word_display.config(text=display_word)

        self.canvas.delete("all")
        self.draw_hangman()

        self.guesses_label.config(text="Названные буквы: " + ", ".join(sorted(self.guesses)))

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
        self.guesses_label.config(text="Названные буквы: ")
        self.update_display()


class WordsFromWordGame:
    def __init__(self, root, back_callback):
        self.root = root
        self.back_callback = back_callback

        self.word = random.choice(WORDS_FROM_WORD)
        self.words = set(words.words())
        self.used_words = set()
        self.words_found = 0

        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self.root, text=f"Составьте слова из слова: {self.word}", font=("Arial", 18), bg="#f0f0f0")
        self.label.pack(pady=10)

        self.entry = tk.Entry(self.root, font=("Arial", 18))
        self.entry.pack(pady=10)
        self.entry.bind('<Return>', self.process_word)

        self.submit_button = tk.Button(self.root, text="Отправить", font=("Arial", 18), command=self.process_word, bg="#9C27B0", fg="white", width=12)
        self.submit_button.pack(pady=10)

        self.words_label = tk.Label(self.root, text="Найденные слова:", font=("Arial", 18), bg="#f0f0f0")
        self.words_label.pack(pady=10)

        self.words_display = tk.Label(self.root, text="", font=('Consolas', 14), bg="#f0f0f0")
        self.words_display.pack(pady=10)

        self.back_button = tk.Button(self.root, text="Назад", font=("Arial", 16), command=self.back_callback, bg="#607D8B", fg="white", width=20)
        self.back_button.pack(pady=10)

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
        self.label = tk.Label(self.root, text=f"Слова на букву '{self.last_letter}':", font=("Arial", 18), bg="#f0f0f0")
        self.label.pack(pady=10)

        self.entry = tk.Entry(self.root, font=("Arial", 18))
        self.entry.pack(pady=10)
        self.entry.bind('<Return>', self.process_word)

        self.submit_button = tk.Button(self.root, text="Отправить", font=("Arial", 18), command=self.process_word, bg="#9C27B0", fg="white", width=12)
        self.submit_button.pack(pady=10)

        self.words_label = tk.Label(self.root, text="Найденные слова:", font=("Arial", 18), bg="#f0f0f0")
        self.words_label.pack(pady=10)

        self.words_display = tk.Label(self.root, text="", font=('Consolas', 14), bg="#f0f0f0")
        self.words_display.pack(pady=10)

        self.back_button = tk.Button(self.root, text="Назад", font=("Arial", 16), command=self.back_callback, bg="#607D8B", fg="white", width=20)
        self.back_button.pack(pady=10)

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
