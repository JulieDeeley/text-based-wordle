# This version uses functions with guess_the_word() as the main, controlling function.
import sys # allows us to use sys.exit
import os
import random 
WORD_LENGTH = 5 
TOTAL_GUESSES_ALLOWED = 5

def quit_program():
    print("Exiting the program...")
    sys.exit()  # This will stop the program

def pick_a_word():
    # Get the directory automatically from where the current script is located:
    script_dir = os.path.dirname(__file__)
    # Construct the relative path to the word list file
    file_path = os.path.join(script_dir, 'five_letter_words.txt')

    #randomly select a line number from the file, read the whole file into memory first  
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            random_line_number = random.randint(0, len(lines) - 1)
            return lines[random_line_number].strip()
        
    except (FileNotFoundError, IOError):
        print(f'Word list file named five_letter_words.txt not found or could not be read.')
        quit_program()
           
def instructions():
    # clear the screen, instruct the player.
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f'Guess the word in {TOTAL_GUESSES_ALLOWED} tries or less. The word is {WORD_LENGTH} letters long.')
    print('Correct letters in the right place will be in capitals.')
    print('Correct letters in the wrong place will be in lower case and incorrect letters will be a -.')
    print('To quit the game type a single q and press enter.')

def user_guesses(num_guesses):
    # Gets the user input and makes sure the input is valid. Returns the guess 
    # if  it is a valid guess or False if it isn't.
     
    guess = input (f'Guess {num_guesses+1}/{TOTAL_GUESSES_ALLOWED} - Your guess is? ').lower()
    if guess == 'q':
        quit_program()

    # guess must be letters and must be 5 letters long
    elif guess.isalpha() and len(guess) == WORD_LENGTH:
        
        return list(guess)
    else:
        print('Please use exactly 5 letters.')
        return False
        

def check_guess(answer, guess):
    # This function checks the guess letter by letter against the answer
    # and returns feedback to the user as a list.
    #  remaining_letters holds a copy of the answer and for each correct letter whether the correct letter
    # is in the right place or not that indices will have a 0 replace the answer letter
    # to keep track of the letters remaining unguessed.
     
    feedback = [''] * WORD_LENGTH
    remaining_letters = list(answer) # IMPORTANT! a list changed here will change in the main function
    # so use a new list instead! You can also copy the list for a local copy with answer=list(answer)
    
    # First pass to handle correct letters in the correct place which will be added to feedback as upper case
    for i in range (len(guess)):
        if guess[i] == answer[i]:
            feedback[i] = guess[i].upper() 
            remaining_letters[i] = None # replace the letter in  remaining_letters with None. 
        
    # Second pass to handle incorrect positions and absent letters.
    # Correct guesses in incorrect positions will be added to feedback as small letters
    # Incorrect letters in the guess will result in a - added in feedback
    
    for j in range(len(guess)):
        if guess[j] in  remaining_letters and feedback[j] == '': #if there is a matching letter left in the word and the spot in feedback is empty, add the lowercase letter
            feedback[j] = guess[j] # turn the empty slot into a lowercase letter            
            remaining_letters[ remaining_letters.index(guess[j])] = None # find the letter in  remaining_letters
            #and replace it with None
               
        elif feedback[j] == '': # if the feedback is still empty add a -
            feedback[j] = '-'     
    return feedback

def play_again_question():
    play_again = input('Do you want to play again? y to play again, any other key to quit: ').lower()
    if play_again == 'y':
        return True
    elif play_again != 'y':
        print('Thanks for playing!')
        return False


def guess_the_word():
    # controls the program
    while True: 
        instructions() 
        answer = list(pick_a_word())
        print(f' DEBUG Word is {answer}')
        num_guesses = 0
        playing = True
        
        while playing and num_guesses < TOTAL_GUESSES_ALLOWED:
            # user guess gets the user's guess and checks if it is valid input
            guess = user_guesses(num_guesses)
            
            # if the input is not valid a guess is used up and the loop starts over
            if guess== False:
                continue
            
            # if the user correctly guesses the word, feedback and end program
            if guess == answer:
                print(f'You guessed {"".join(guess)}.')
                print('Right!')
                playing = False
                if not play_again_question():
                    return
                
            # if the input was valid, the guess is checked and feedback provided for the next guess         
            feedback = check_guess(answer, guess)
            print("".join(feedback))
            num_guesses += 1 # increment after valid guess
            
            # If the guesses are used up, the game ends and the answer is revealed        
            if num_guesses == TOTAL_GUESSES_ALLOWED:
                print(f'You ran out of guesses! The answer was: {"".join(answer)}')
                playing = False
                if not play_again_question():
                    return


# Optional: Set a random seed for reproducibility during testing. Turns random to the seed value.
#random.seed(42)
if __name__ == '__main__':
    guess_the_word() 

