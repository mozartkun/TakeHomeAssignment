#!/usr/bin/env python
# coding: utf-8

# # Question 1: Neo Saves World

# ### Python Version 3.5+

# In[ ]:


#!/usr/bin/env python
#-*- coding:utf-8 -*-
#Python version: 3.5+

from collections import defaultdict
import random
import string
import sys, os, time, datetime
from copy import deepcopy


# In[ ]:


# Define the class of this game
class neo_save_world(object):
    def __init__(self):
        self.num_of_balls = -1 # Initialize the cardinality of balls set: number of balls in this set
        self.balls_set = [] # Initialize the balls set: value is color 0/1
        self.color = [0, 1] # Ball color is either 0 or 1
        self.majority_color = -1 # Initialize majority color in this game: either 0 or 1
        self.num_of_query = -1 # Initialize the number of queries that Neo should ask Viky
        self.same_diff_color = defaultdict(lambda: [set(), set()]) # Neo's memory about queries; 
                                                         # key: each ball index; 
                                                         # value: 1st set() stores same-color balls set, 
                                                         #        2nd set() stores diff-color balls set
        self.neo_guess = -1 # Initialize Neo's guess about which ball index is majority-color 
        self.trantab = str.maketrans({key: None for key in ' ' + string.punctuation}) # Remove punctuations from each inputted value if exists any
    
    def input_line1(self):
        '''This function is used to return formatted inputs from the user.
        
           Outputs:
           1) line1: A list of string values converted from the first line inputs
        '''
        # This block of codes is used to deal with first line of inputs by the user
        print("Line 1: Please input 5 single space separated characters/Integers.")
        print("1st value is an integer N which is the cardinality of the balls set.")
        print("2nd value is 0 indicating that Majority exists.")
        print("3rd value is an integer indicating the number of times Viky might lie (0 in this version of the game).")
        print("4th value is 2 indicating each ball can only have any of the 2 colors.")
        print("5th value is an integer 1 indicating the Viky lies exactly 0 time(ignore this number).")
        input_value1 = input("Please input these 5 values, delimited by single space and end with enter: \n")
        line1 = input_value1.strip().split()
        line1 = [item.translate(self.trantab) for item in line1] # Each splitted input value should remove punctuations if exists any
        
        return line1
        
    def input_line2(self):
        '''This function is used to return formatted inputs from the user.
        
           Outputs:
           1) line2: A string value converted from the second line input.
        '''
        # This block of codes is used to deal with second line of inputs by the user
        print("Line 2: Please input an integer D, indicating D queries that Neo should ask and Viky should answer.")
        input_value2 = input("Please input one integer and end with enter: \n")
        line2 = input_value2.strip()
        
        return line2
    
    def display_introduction(self):
        '''This function is used to display the introduction of this game, and initialize this game.
           Make sure that the first line of values inputted by the user really satisfies the formatted rule.
           If yes, then continue. If not, then repeat until everything is satisfies.
        '''
        print("=====Beginning of A New Game: Local Time {0}=====".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
        time.sleep(1)       
        
        # Make sure whether Line 1 inputted values satisfy the formatted rule
        flag_line1 = False # A flag showing that Line 1 inputs are fine
        while not flag_line1:
            # First line of inputs by the user
            line_1 = self.input_line1()
            
            if len(line_1) != 5:
                print("Warning: You did not input exactly 5 values. Please follow the guidelines.")
            elif not line_1[0].isdigit():
                print("Warning: 1st value you input is not an integer. Please follow the guidelines.")
            elif int(line_1[0]) < 2:
                print("Warning: 1st value you input is lower than 2. Please input a bigger integer and follow the guidelines.")
            elif line_1[1] not in ['0', 0]:
                print("Warning: 2nd value you input is not 0. Please follow the guidelines.")
            elif line_1[2] not in ['0', 0]:
                print("Warning: 3rd value you input is not 0. Please follow the guidelines.")
            elif line_1[3] not in ['2', 2]:
                print("Warning: 4th value you input is not 2. Please follow the guidelines.")
            elif line_1[4] not in ['1', 1]:
                print("Warning: 5th value you input is not 1. Please follow the guidelines.")            
            else:
                print("Your 5 input values of first line are: {0}".format(line_1))
                flag_line1 = True        
        
        time.sleep(1)
        
        # Make sure whether Line 2 inputted value satisfy the formatted rule
        flag_line2 = False # A flag showing that Line 2 input is fine
        while not flag_line2:
            # Second line of inputs by the user
            line_2 = self.input_line2()
            
            if not line_2.isdigit():
                # Repeat Line 2
                print("Warning: This value is not integer. Please follow the guidelines.")
            else:
                print("Your input value of second line is: {0}".format(line_2))
                flag_line2 = True        
        
        time.sleep(1)
        
        # After two lines are correctly inputted, the game is then initialized
        self.num_of_balls = int(line_1[0]) # Cardinality of this balls set
        self.balls_set = [random.choice(self.color) for i in range(self.num_of_balls)] # Now each ball has its color: 0/1
        self.num_of_query = int(line_2) # Number of queries that Neo should ask Viky
        
        # Make sure balls_set has majority-color indeed; If not, then randomly assign color again
        while sum(self.balls_set) == self.num_of_balls / 2:
            self.balls_set = [random.choice(self.color) for i in range(self.num_of_balls)] # Re-assign ball color       
        
        self.majority_color = 1 if sum(self.balls_set) > self.num_of_balls / 2 else 0 # Majority color: 0/1
        
        print("The balls set and their colors are prepared. Let Neo send queries to Viky and then guess.")        
        
    
    def neo_query_viky(self):
        '''This function is used to show what queries is Neo making to ask Viky, and what responses is Viky making to Neo's queries.
           Neo updates memory when making queries.         
        '''
        
        # Brush Neo's memory about same-color balls
        for ball_index in range(self.num_of_balls):
            self.same_diff_color[ball_index][0].add(ball_index)
        
        # Ask queries: 
        for query_id in range(self.num_of_query):
            time.sleep(1)
            
            # Initialize two balls index that Neo ask each time: Sampling without replacement
            first_ball, second_ball = random.sample(range(self.num_of_balls), 2)
            
            # Neo asks and Viky answers
            print("Neo asks {0}: Ball {1} and Ball {2} are same-color?".format(query_id, first_ball, second_ball)) 
            answer = "YES" if self.balls_set[first_ball] == self.balls_set[second_ball] else "NO" # Viky's answer
            print("Viky answers {0}: {1}".format(query_id, answer))
            
            print("Query {0} is: {1}".format(query_id, [first_ball, second_ball, answer]))
            
            # Neo memorizes this query in the brain: Update Neo's memory about same-color balls
            # If balls are same-color, add positive index in the same-color set; If not, add ball index in the diff-color set
            if answer == "YES":
                self.same_diff_color[first_ball][0].add(second_ball)            
                self.same_diff_color[second_ball][0].add(first_ball)
            elif answer == "NO":
                self.same_diff_color[first_ball][1].add(second_ball)            
                self.same_diff_color[second_ball][1].add(first_ball)
     
    def neo_make_guess(self):
        '''This function is used to show how Neo processes memory and makes guess.
           In the end of game, after Neo finishes D queries (D is given in second line input), Neo should make a guess about 
           majority-color ball. Neo should propose a ball index (possibly majority-color or not) based on Neo's judgement on 
           previous queries.         
        '''
        # Since there are only 2 colors, ball A and ball B are either same-color or diff-color
        update_memory = defaultdict(lambda: [set(), set()]) # make a copy and then update and compare
        
        # Neo updates the memory until reaching consistency/statiblity
        print("Neo says: Let me think for a while.")
        while(update_memory != self.same_diff_color):      
            update_memory = deepcopy(self.same_diff_color) # temporary copy
            
            # Then update
            for ball_index in range(self.num_of_balls):
                #ball_same, ball_diff = self.same_diff_color[ball_index]
                for compare_index in range(self.num_of_balls):
                    #compare_same, compare_diff = self.same_diff_color[compare_index]
                    
                    # Case 1. If two same-color ball set share the same ball index, or two diff-color ball set share the same ball index,
                    # then combine same-color ball set
                    if not self.same_diff_color[ball_index][0].isdisjoint(self.same_diff_color[compare_index][0]) or                        not self.same_diff_color[ball_index][1].isdisjoint(self.same_diff_color[compare_index][1]):
                        self.same_diff_color[ball_index][0].update(self.same_diff_color[compare_index][0])
                        self.same_diff_color[ball_index][1].update(self.same_diff_color[compare_index][1])
                        self.same_diff_color[compare_index][0].update(self.same_diff_color[ball_index][0])
                        self.same_diff_color[compare_index][1].update(self.same_diff_color[ball_index][1])
                    
                    # Case 2. If one same-color ball set share the same ball index with another diff-color ball set, 
                    # then combine one same-color ball set with another diff-color ball set
                    if not self.same_diff_color[ball_index][0].isdisjoint(self.same_diff_color[compare_index][1]) or                        not self.same_diff_color[ball_index][1].isdisjoint(self.same_diff_color[compare_index][0]):
                        self.same_diff_color[ball_index][0].update(self.same_diff_color[compare_index][1])
                        self.same_diff_color[ball_index][1].update(self.same_diff_color[compare_index][0])
                        self.same_diff_color[compare_index][0].update(self.same_diff_color[ball_index][1])
                        self.same_diff_color[compare_index][1].update(self.same_diff_color[ball_index][0])               
                   
        print("The same-color diff-color ball memory is: {0}".format(self.same_diff_color))
        
        print("Neo says: Let me guess a number.")
        
        # Select the ball index with longest same-color balls set
        length_same_color_ballset = 0 # Initialize        
        for ball_index in range(self.num_of_balls):
            if len(self.same_diff_color[ball_index][0]) > length_same_color_ballset:
                self.neo_guess = ball_index
                length_same_color_ballset = len(self.same_diff_color[ball_index][0])
            
        print("Neo says: I know which ball index number of majority-color.")
       
    
    def end_game(self):
        '''This function is used to determine whether Neo's guess is correct.
           If Neo's guess is really a majority-color ball, then Neo wins the game and human being is saved.        
        '''   
        if self.balls_set[self.neo_guess] != self.majority_color:
            print("Bad Ending: Neo loses the game. John destroys human being.")
            print("=====Game Over: Local Time {0}=====".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))            
        else:
            print("Happy Ending: Neo wins the game. John reaches truce. Human being is saved.")
            print("=====The End of This Story: Local Time {0}=====".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
            
    
    def main(self):
        '''This function is used to be main function of this guess game.
           First, the screen will display guidelines for the user to input 2 lines of values, in order to initilize this game.
           Second, 
        '''
        
        # Step 1. Display game guidelines. Wait for the user's inputs of first line and second line. Initialize this game.
        self.display_introduction()
        
        # Constraint: If number of queries is lower than half of cardinality of balls set, then quickly game over 
        if self.num_of_query < self.num_of_balls / 2:
            print("Bad Ending: Neo has too few queries and loses the game. John destroys human being.")
            print("=====Game Over: Local Time {0}=====".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))) 
        else:
            time.sleep(1)
        
            # Step 2. Neo makes queries and Viky responses
            self.neo_query_viky()        
            time.sleep(1)
        
            # Step 3. Neo makes guess. Then John shows the game initialization: Balls set, ball color, majority-color
            self.neo_make_guess()
            print("Neo answers: The ball indexed at {0} with color {1} is of the majority".format(self.neo_guess, self.balls_set[self.neo_guess]))
            print("John says: The majority color is: {0}".format(self.majority_color))
            print("John says: The balls index and their colors are: \n{0}".format([(index, color) for index, color in enumerate(self.balls_set)]))
            time.sleep(1)
        
            # Step 4. John decides whether Neo's guess is correct or not. Neo wins if Neo's guess is correct.
            self.end_game()  
            print("Final Output: Neo answers that the ball indexed at {0} is of the majority.".format(self.neo_guess))
                  


# In[ ]:


# Run this game
if __name__ == "__main__":
    new_game = neo_save_world()
    new_game.main()


# In[ ]:




