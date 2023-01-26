import random
rock = '''
    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)
'''

paper = '''
    _______
---'   ____)____
          ______)
          _______)
         _______)
---.__________)
'''

scissors = '''
    _______
---'   ____)____
          ______)
       __________)
      (____)
---.__(___)
'''

#Write your code below this line 👇
user_score = 0
computer_score = 0

print("Welcome to rock paper scissors")
print("best of 3")

for i in range(0,3) :

   

  input_user_choice = input("Enter 0 for rock, 1 for paper, 2 for scissors\n")
  RPS = [rock, paper, scissors]
  computer_choice = random.choice(RPS)

  if input_user_choice == 0 :
       user_choice = rock
  elif input_user_choice == 1 :
       user_choice = paper
  else :
       user_choice = scissors


  print("Your Choice")
  print(user_choice)
  print("Computer Choice")
  print(computer_choice)

  if  user_choice == rock and computer_choice == rock :
       print("Draw")
       user_score += 1
       computer_score += 1
  elif user_choice == rock and computer_choice == paper :
       print("Computer wins")
       computer_score += 1
  elif user_choice == rock and computer_choice == scissors :
       print("user wins")
       user_score += 1
  elif user_choice == paper and computer_choice == rock :
       print("computer wins")
       computer_score += 1
  elif user_choice == paper and computer_choice == paper :
       print("Draw")
       user_score += 1
       computer_score += 1
  elif user_choice == paper and computer_choice == scissors :
       print("computer wins")
       computer_score += 1
  elif user_choice == scissors and computer_choice == rock :
       print("computer wins")
       computer_score += 1
  elif user_choice == scissors and computer_choice == paper :
       print("user wins")
       user_score += 1
  else :
       print("Draw")
       computer_score += 1
       user_score += 1

if user_score > computer_score :
  print("User wins the b03")
else :
  print("Computer wins b03 ur trash")

        
    
      
   

     
       




