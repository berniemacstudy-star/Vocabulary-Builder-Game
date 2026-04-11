import random

#Vocabulary Builder Game

#My own word bank
words = { 
    "easy":
        { 
        "rapid": "fast",
        "brief": "short in time",
        "ancient": "very old",
        "scarce": "limited"},
    
    "medium":
        {
        "abundant": "plentiful",
        "fragile": "easily broken",
        "obsolete": "out of style",
        "avert": "prevent"},
        
    "hard":
        {
        "gratuitous": "uncalled for",
        "vivid": "clear and detailed",
        "persistent": "relentless",
        "cynical": "distrustful",
        "candid": "straightforward"}
}

#Prompt difficulty selection, prompts use "input" instead of "print"
while True:
    difficulty = input(f"Choose difficulty (easy/medium/hard): ").lower()
   
   #if user selects VALID option
    if difficulty in words:
        break
        
    #if user selects INVALID option
    else:
        print("Invalid! Enter only easy, medium, hard.")

#Track score
score = 0

#Lives a user will get
lives = 3

#Following is to prevent repeated random words being generated
word_list = list(words[difficulty].keys())
random.shuffle(word_list)

#For loop uses the 'e' word to let python track each word naturally
for i, word in enumerate(word_list, start = 1):
    
    #Below line adds question feedback. Adds a feeling of progression and realism
    print(f"Question {i} of {len(word_list)}")
    
    #Display amount of lives left
    print(f"Lives: {lives}")
    
    #Actual question
    print(f"What does '{word}' mean?\n")
    
    #Build Multiple Choices - 1 correct word & 3 wrong words
    correct = words[difficulty][word]
     
    #Takes account of all wrong answers possible in each difficulty chosen
    wrong_answers = list(words[difficulty].values())
    wrong_answers.remove(correct)
    
    #Choose up to 3 answers safely
    num_choices = min(3, len(wrong_answers))
    choices = random.sample(wrong_answers, num_choices)
    
    choices.append(correct)
    random.shuffle(choices)
    
    #Show options as in A to D
    options = ["A", "B", "C", "D"]
    
    for j in range(len(choices)):
        print(f"{options[j]}. {choices[j]}")
        
    #Get user's input
    #Check answer by checking their choice
    #Error handling against wrong inputs
    while True:
        user_choice = input("Your answer (A/B/C/D): ").upper()
        
        if user_choice in options[:len(choices)]:
            break
        else:
            print("Invalid input! Enter only (A/B/C/D).")
            
    index = options.index(user_choice)
    
    selected_answer = choices[index]
    
    if selected_answer == correct:
        print("Correct!")
        score += 1
        
    else:
        print(f"Wrong! The correct answer is: {correct}")
        lives -= 1
        print(f"Lives remaining: {lives}")
        
        if lives == 0:
            print("\nGame over. You ran out of lives!")
            break
        
    print("-" * 30)

print(f"\nFinal score: {score} / {len(word_list)}")

#Personal feedback 4 user after score is done
if score == len(word_list):
    print("Perfect! Your Vocabulary is strong.")
    
elif score >= 4:
    print("Good! You vocabulary is decent.")
    
else:
    print("Keep training your vocabulary.You'll get there!")

#Date 05/04. Basic vocab questions logic
#Date 06/04. Multiple choice added to make it easier for user to guess "My" word
#Date 07/04. Error handling for invalid inputs
#Date 08/04. Small additional tweaks
#Date 09/04.  Difficulty levels 
#Date 10/04. Fix bugs and add more words
#Date 11/04. Add a lives system