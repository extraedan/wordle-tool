import string

class Game:
    def __init__(self):
        self.letters = list(string.ascii_lowercase)
        self.positions = {"First": 1, "Second": 2, "Third": 3, "Fourth": 4, "Fifth": 5}
        self.letter_status = None
        
        
    def setup(self):
        self.letter_status = self.reset_letters()
    
    
    
    def game_loop(self):
        print ("Hello, welcome to the Wordl assistant.\nFirst, input your guess, and then tell me the results.")
        print("If your letter is present and in the correct place, put a '+' before it.\n If it is present and not in the right place, add a '-'.\n")
        
        
        # process each of the five letters
        for position in self.positions:
            self.process_letter(position)
            
        self.print_status()
            
            
    def process_letter(self, position):
        # get the letter
        letter_guess = input(f"{position} letter: ").lower()
        # handle empty input
        if not letter_guess: 
            print("Please enter a letter.")
            return self.process_letter(position)
        
        actual_letter = letter_guess[1] if len(letter_guess) > 1 else letter_guess
        first_character = letter_guess[0]
        
        # check if input is valid, else try again
        if actual_letter not in self.letters or self.letter_status[actual_letter]["status"] == "absent":
            print("That's not a valid letter, try again.")
            self.process_letter(position)

        # for each position, update the letter
        self.update_letter(position, actual_letter, first_character)
        
        
    def update_letter(self, position, letter, first_character):
        if first_character == "-":
            self.letter_status[letter]["status"] = "present"
        
        elif first_character == "+":
            self.letter_status[letter]["status"] = "correct"
            self.letter_status[letter]["position"] = self.positions[position]
        else:
            self.letter_status[letter]["status"] = "absent"
        
        
        
        
        
        
        
        
        
        
        
        
        
    def reset_letters(self):
        letter_status = {
        letter: {
            'status': 'unused',
            'position': None
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