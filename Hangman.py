import curses
import random

class Game:
    def __init__(self):
        #Curses vars (display only)
        self.screen = curses.initscr()
        self.screen.clear()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)
        self.correct_letter_color = curses.color_pair(3)
        self.incorrect_letter_color = curses.color_pair(2)
        self.man_color = curses.color_pair(1)
        self.underscore_color = curses.color_pair(4)
        #Game vars
        self.words = ["giraffe", "mosquito", "octogon", "xylophone", "nebula", "freezer", "highway", "trombone"]
        self.word = ""
        self.wrong_guesses = 0
        self.guessed_letters = []
        self.game_over = False

    def draw_gallows(self):
        line1 = " ___"
        line2 = "|   |"
        line3 = "|"
        line4 = "|"  
        line5 = "|"  
        line6 = "|"
        line7 = "|_______"
        lines = [line1, line2, line3, line4, line5, line6, line7]
        for line in range(0, len(lines)):
            self.screen.addstr(line, 1, lines[line])
        #Display hanged man
        for guess in range(self.wrong_guesses+1):
            if guess == 1:
                self.screen.addstr(2, 5, "O", self.man_color) #Head
            if guess == 2:
                self.screen.addstr(3, 5, "|", self.man_color) #Body
            if guess == 3:
                self.screen.addstr(4, 4, "/", self.man_color) #Left Leg
            if guess == 4:
                self.screen.addstr(4, 6, "\\", self.man_color) #Right Leg
            if guess == 5:
                self.screen.addstr(3, 4, "/", self.man_color) #Left Arm
            if guess == 6:
                self.screen.addstr(3, 6, "\\", self.man_color) #Right Arm
        self.show_guesses()
        self.show_word()

    def show_guesses(self):
        x = 1
        y = 8
        color = ""
        self.screen.addstr(7, 1, "Guessed Letters:")
        for letter in range(len(self.guessed_letters)):
            if self.guessed_letters[letter] in self.word:
                color = self.correct_letter_color #Displays as green if correct guess
            else:
                color = self.incorrect_letter_color #Displays as red if incorrect guess
            self.screen.addstr(y, x, self.guessed_letters[letter], color)
            x+=2
        self.screen.refresh()

    def show_word(self):
        for letter in range(len(self.word)):
            display = "*" #Displays one for each letter in the selected word
            color = self.underscore_color
            if self.word[letter] in self.guessed_letters:
                display = self.word[letter] #If the player has guessed this letter, it will display instead
                color = self.correct_letter_color
            self.screen.addstr(4, 10+letter, display, color)

    def get_user_guess(self):
        loop = True
        #only letters allowed
        allowed_chars = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l",
                         "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
        while loop == True:
            self.screen.move(9, 1)
            self.screen.clrtoeol()
            self.screen.move(10, 1)
            self.screen.clrtoeol()
            self.screen.addstr(9, 1, "Guess a letter in the word:")
            response = self.screen.getstr(10, 1).decode('utf-8')
            response = response.lower()
            if response not in self.guessed_letters and len(response) == 1 and response in allowed_chars:
                self.guessed_letters.append(response) #Add letter to the list of guessed letters
                if response not in self.word:
                    self.wrong_guesses += 1 #If not a correct guess, increase the wrong guess count
                loop = False

    def check_for_game_over(self):
        if self.wrong_guesses >= 6: #Displays full hanged man
            self.game_over = True
        word_len = len(self.word)
        correct_guesses = 0
        for letter in range(len(self.word)):
            if self.word[letter] in self.guessed_letters:
                correct_guesses += 1
        if correct_guesses == word_len: #Correctly guessed each letter
            self.game_over = True


    def play_again(self):
        loop = True
        while loop == True:
            self.screen.move(9, 1)
            self.screen.clrtoeol()
            self.screen.move(10, 1)
            self.screen.clrtoeol()
            self.screen.addstr(9, 1, "Play again? (Y/N)")
            response = self.screen.getstr(10, 1).decode('utf-8')
            response = response.upper()
            if response == "Y":
                loop = False
                self.restart_game()
            elif response == "N":
                loop = False
                self.screen.addstr(11, 1, "Thanks for playing!")
                response = self.screen.getstr(12, 1).decode('utf-8')

    def restart_game(self):
        #Resets game vars
        self.game_over = False
        self.wrong_guesses = 0
        self.guessed_letters = []
        self.screen.clear()
        self.game()

    def game(self):
        #Randomly select a word from self.words
        rand = random.randint(0, len(self.words)-1)
        self.word = self.words[rand]
        #Initialize screen
        self.draw_gallows()
        #PLAY!
        while self.game_over == False:
            self.get_user_guess()
            self.draw_gallows()
            self.check_for_game_over()
        self.play_again()

game = Game()
game.game()