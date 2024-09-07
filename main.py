# Constants
CURRENT_GUESS_LENGTH = 5
FIXED_PART = ["_", "_", "I", "L", "_"]
REMAINING_LETTERS = ["Q","I","L","H","J","Z","X","C","B","M"]
KNOWN_LETTERS = ["H", "C"]

# Find which slots are blank
temp_word = FIXED_PART
temp_lets = KNOWN_LETTERS

def get_blanks(word):
    return [index for index, value in enumerate(word) if value == "_"]

def generate_combos(blank_list, temp_lets):
    for start_index in range(len(temp_lets)):
        rotated_temp_lets = temp_lets[start_index:] + temp_lets[:start_index]

        for blank, letter in zip(blank_list, rotated_temp_lets):
            temp_word[blank] = letter

        # Find the last unused blank (if any)
        used_blanks = set(blank_list[:len(rotated_temp_lets)])
        remaining_blanks = [blank for blank in blank_list if blank not in used_blanks]

        # Now fill the last unused blank with each letter from REMAINING_LETTERS
        if remaining_blanks:
            last_blank = remaining_blanks[0]  # Assuming only one last blank to fill
            for letter in REMAINING_LETTERS:
                temp_word[last_blank] = letter
                printable = ''.join(temp_word).lower()
                print(printable)

def rotate_and_track(blanks):
    original = blanks[:]  # Make a copy of the original list
    rotated = blanks[:]  # Start with the original list
    rotations = [rotated[:]]  # Track all rotations, starting with the initial list

    while True:
        # Rotate the list
        rotated = rotated[1:] + rotated[:1]

        if rotated == original:
            break

        rotations.append(rotated[:])

    return rotations

# runs the code
blank_list = get_blanks(temp_word)
rotations = rotate_and_track(blank_list) # gets all possible combinations of blanks [0,3,4] -> [3,4,0] (these are indices)

for i, rotation in enumerate(rotations):
    generate_combos(rotation, temp_lets)