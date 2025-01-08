from game import Game

game = Game()
#game.manual_loop()
wins_in_a_row = 0
rounds = 0
while True:
    game.setup()
    rounds += 1 # update attempts
    print(f"Now running round number {rounds}") 
    word = game.get_random_word() # get word
    success, attempts = game.bot_mode(word)
    
    if success:
        print(f"Word found in {attempts} attempts\n")
        continue
    else:
        print(f"Bot has failed after {attempts} attempts")
        break
