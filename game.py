import string
import random

class Game:
    def __init__(self):
        self.letters = list(string.ascii_lowercase)
        self.positions = {"First": 1, "Second": 2, "Third": 3, "Fourth": 4, "Fifth": 5}
        self.letter_status = None
        self.words_list = self.load_words("potential_words.txt")
        
    def setup(self):
        self.letter_status = self.reset_letters()
        self.word_bank = self.words_list
        
    
    def manual_loop(self):
        self.setup()
        print ("Hello, welcome to the Wordl assistant.\nFirst, input your guess, and then tell me the results.")
        print("If your letter is present and in the correct place, put a '+' before it.\n If it is present and not in the right place, add a '-'.\n")
        
        for i in range(5):
            print(f"Starting round {i+1}")
            # process each of the five letters
            for position in self.positions:
                self.process_letter(position)
            
            self.update_wordbank()
            
            for word in self.word_bank:
                print(word)
    
        print("Alright buddy, it's on you now, choose the right one.")
        
    
    def bot_mode(self, target_word):
        print(f"The target word is {target_word}")
        
        self.setup()
        for i in range(6):
            guess = self.get_random_word()
            print(f"We are guessing {guess}")
            results = self.validate_guess(guess, target_word)
            
            # use position names properly
            for pos_name, result in zip(self.positions.keys(), results):
                letter = result[-1]
                first_char = result[0] if len(result) > 1 else ''
                self.update_letter(pos_name, letter, first_char)
                
            self.update_wordbank()
            if guess == target_word:
                return True, i+1
        return False, 6
        
        
    def validate_guess(self, guess, target_word):
        result = []
        for i, letter in enumerate(guess):
            if letter == target_word[i]:
                result.append(f"+{letter}")
            elif letter in target_word:
                result.append(f"-{letter}")
            else:
                result.append(letter)
        return result
        
    
    def manual_process_letter(self, position):
        while True:
            # get the letter
            letter_guess = input(f"{position} letter: ").lower()
            # handle empty input
            if not letter_guess: 
                print("Please enter a letter.")
                continue
            
            actual_letter = letter_guess[1] if len(letter_guess) > 1 else letter_guess
            first_character = letter_guess[0]

            # for each position, update the letter
            self.update_letter(position, actual_letter, first_character)
            break
        
        
    def update_letter(self, position, letter, first_character):
        if first_character == "-":
            self.letter_status[letter]["status"] = "present"
            self.letter_status[letter]["wrong_positions"].append(self.positions[position])
        
        elif first_character == "+":
            self.letter_status[letter]["status"] = "correct"
            self.letter_status[letter]["position"] = self.positions[position]
        else:
            if self.letter_status[letter]["status"] != "present":
                self.letter_status[letter]["status"] = "absent"
    
    
    
    
    def update_wordbank(self):
        updated_bank = []
        
        #iterate through each word
        for word in self.word_bank:
            if self.is_valid(word):
                updated_bank.append(word)
                
        self.word_bank = updated_bank
    
    
    def is_valid(self, word):
        """Returns true if word passes all checks to be valid"""
        letters_in_word = list(word)
        # check each letter in word
        for index, letter in enumerate(letters_in_word):
            if self.is_letter_absent(letter):
                return False
            elif self.is_wrong_position(letter,index+1):
                return False
            elif self.is_wrong_present_position(letter,index+1):
                return False
            
        if not self.contains_all_present_letters(word):
            return False
        
        return True
    
    def is_wrong_present_position(self,focus_letter,current_position):
        # look up the letter we're focusing on
        # if it's present
        # is our current position in it's wrong position tab?
        # if so, True
        
        try:
            if self.letter_status[focus_letter]["status"] == "present":
                if current_position in self.letter_status[focus_letter]["wrong_positions"]:
                    return True
        except KeyError:
            print(f"Invalid letter encountered: {focus_letter}")
            return True 
        
        return False
        
        
    def contains_all_present_letters(self, word):  
        present_letters = [letter for letter, info in self.letter_status.items() if info["status"] == "present"]
        for letter in present_letters:
            if letter not in word:  
                return False
        return True
        
    def is_letter_absent(self, letter):
        try:
            if self.letter_status[letter]["status"] == "absent":
                return True
        except KeyError:
            return True  
    
    def is_wrong_position(self, letter_in_focus, current_position):
        """Returns true if the letter in focus does not match the letter in a correct position"""
        try:
            for letter, info in self.letter_status.items():
                if info["position"] is not None:  
                    if info["position"] == current_position:  
                        if letter_in_focus != letter:  
                            return True
            return False
        
        except KeyError:
            return True
            
        
        
        
    def reset_letters(self):
        letter_status = {
        letter: {
            'status': 'unused',
            'position': None,
            'wrong_positions': []
        } for letter in self.letters
    }
        return letter_status


    def print_status(self):
        print("\nFinal letter statuses:")
        for letter, info in self.letter_status.items():
            if info['status'] != 'unused':
                print(f"{letter}: {info['status']}", end='')
                if info['position']:
                    print(f" at position {info['position']}")
                else:
                    print()
                    
                    
    def load_words(self,filename):
        with open(filename, 'r') as file:
            # strip() removes whitespace, [] and eventual commas
            text = file.read().strip('[]')
            # split on commas and clean up each word
            words = [word.strip().strip('"') for word in text.split(',')]
        return words
    
    def get_random_word(self):
        return random.choice(self.word_bank)