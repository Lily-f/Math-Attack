#Mike Fahey
#18/9/2017

####### IMPORTS, SETUP AND CONFIG #######

from tkinter import *
from tkinter import ttk
import random
import time

root = Tk()
root.title("Math Attack")

# Change red window close button to soft closes
def _quit():
    root.destroy()
root.protocol('WM_DELETE_WINDOW', _quit)

### Sets up menu GUI to get username and difficulty
# Also gives instructions and creates a button to continue to the game
class User:

    # Creates the canvas for the menu gui to be placed on and runs functions to populate it
    def __init__(self):

        # Makes menu_canvas global so it can be used in other functions
        global menu_canvas

        # Makes str_username_entry global so it can be used in other functions
        global str_username_entry
        
        # Create canvas that all menu GUI widgets will be placed on
        menu_canvas = Canvas(root,width = 800, height = 500, bg='orange')
        menu_canvas.pack()

        # Run the username function to get the User's username. This will be used in score gui
        str_username_entry = User.username()

        # Runs functions within class      
        User.difficulty(self)
        User.instructions()
        User.play_button(self)
        
    # Create a Username entry to get the user's username, then create a greeting display with it
    def username():

        # Makes sure the username cannot be longer than 20 characters (so its not to big)
        # Then set the username variable to the greeting text plus the username entry (for use in greeting label)
        def text_changed(*args):

            # Sets the username entry to the first 20 characters to limit name length
            str_username_entry_length = str_username_entry.get()[0:20]
            str_username_entry.set(str_username_entry_length)

            # Puts the new length-checked username onto the welcome
            str_username.set("Welcome to Math Attack\n" + str_username_entry.get())
            return str_username

        # Create variable to store username and greeting text
        str_username = StringVar()
        str_username.set("Welcome to Math Attack\n")

        # Set Str_username_entry and check if it is updated. If so then run function textchanged
        str_username_entry = StringVar()
        str_username_entry.set("Enter username here")   
        str_username_entry.trace('w', text_changed)

        # Create username entry for str_username_entry variable
        username_entry = ttk.Entry(menu_canvas, textvariable = str_username_entry,
                                   justify="center", width = 23)

        # Make entry clear when user clicks on it
        def clear(event):
            str_username_entry.set("")
        username_entry.bind('<Button-1>', clear)

        # Place the entry field onto the menu gui
        username_entry.pack()
        menu_canvas.create_window(400, 200, window=username_entry)

        # Create 'welcome to math attack username' on canvas
        greet_label = ttk.Label(menu_canvas,textvariable = str_username, width = 30, justify = "center",
                                anchor ="center", background="orange", font=('Impact', 30))
        greet_label.pack()
        menu_canvas.create_window(400, 100, window=greet_label)

        # returns the username entry so that itcan be used in other functions
        return str_username_entry

    # Creates difficulty entry
    def difficulty(self):

        # makes difficulty_entry global so it can be called in menu_close function
        # to create the obj_numbers
        global str_difficulty_default
        
        # Creates a list of possible game difficulties for combobox
        list_difficulty = ["Short", "Medium", "Long"]

        # Creates varaible for default value of difficulty combobox
        self.str_difficulty_default = StringVar()
        self.str_difficulty_default.set("Set Game Length Here")

        # Creates combobox for user to entry in the difficulty of game
        difficulty_entry = ttk.Combobox(menu_canvas, textvariable=self.str_difficulty_default,
                                        justify="center")
        difficulty_entry['values'] = list_difficulty
        difficulty_entry.pack()
        menu_canvas.create_window(400, 250, window=difficulty_entry)

        # Make entry clear when user clicks on it
        def clear(event):
            self.str_difficulty_default.set("")
        difficulty_entry.bind('<Button-1>', clear)

    # Creates instructions text for user
    def instructions():
        menu_canvas.create_text(400, 320, font=('Impact', -25), fill="black", text="""
            Math Attack is a number clicking game
            Click the right numbers to gain points
            or the wrong numbers to lose them""", justify="center")

    # Creates play button to close menu GUI and run the menu_close function
    def play_button(self):
        # Create menu close button
        menu_close_btn = Button(menu_canvas, text="PLAY", command=self.menu_close)
        menu_canvas.create_window(700, 400, window=menu_close_btn)

    # Uses the difficulty input to get number of obj_number instances to create
    # and runs game_setup with that variable. Gives user an error if no difficulty chosen
    def menu_close(self):
        
        #use the game length to set the number of numbers in game, then close menu_canvas GUI
        int_difficulty = 0
        if self.str_difficulty_default.get() == "Short":
            int_difficulty = 10
            menu_canvas.destroy()

            # Function for setting up game gui and obj_number instances with int_difficulty
            game_setup(int_difficulty)
            
        elif self.str_difficulty_default.get() == "Medium":
            int_difficulty = 20
            menu_canvas.destroy()

            # Function for setting up game gui and obj_number instances with int_difficulty
            game_setup(int_difficulty)
            
        elif self.str_difficulty_default.get() == "Long":
            int_difficulty = 30
            menu_canvas.destroy()

            # Function for setting up game gui and obj_number instances with int_difficulty
            game_setup(int_difficulty)
            
        else: # not one of the 3 options. sends user error message and they can't progress
            menu_canvas.create_text(420, 450, font=('Impact', 30), fill="black",
                                    text="You need to select one of the Game Lengths")

# Creates game_canvas and populates it with widgets for the user
# These will be changed in Number class as game goes on
def game_setup(int_difficulty):

    # Create game_canvas that widgets will appear on
    global game_canvas
    game_canvas = Canvas(root,width = 800, height = 500, bg='orange')
    game_canvas.pack()

    ### Widgets for game_canvas

    # Creates scoring variables and labels for the user to see. (These are updated in score_change function)
    def score():

        # Make variables global so they can be used in function score_change in Number class
        global int_score
        global score_label
        global str_score

        # Creates variable that will hold user's score
        int_score = IntVar()
        int_score.set(0)
        
        # Creates label to display the score of the user
        str_score = StringVar()
        str_score.set("This is your score: " + str(int_score.get()))
        score_label = Label(game_canvas, textvariable = str_score,
                            background = "orange", font=('Impact', 18))
        score_label.pack()
        game_canvas.create_window(110, 20, window=score_label)

    # Create variable and label telling user how many numbers left. (These are updated in the score_change function)
    def obj_number_tally(int_difficulty):

        # make variables global so that they can change as obj_numbers are deleted in score_change function
        global obj_left_label
        global int_number_obj_numbers
        global str_obj_left
        
        # Create variable to know how many obj_numbers have been deleted
        int_number_obj_numbers = IntVar()
        int_number_obj_numbers.set(int_difficulty)

        # Create label to display how many are left
        str_obj_left = StringVar()
        str_obj_left.set(str(int_number_obj_numbers.get()) + " Numbers left")
        obj_left_label = Label(game_canvas, textvariable = str_obj_left,
                            background = "orange", font=('Impact', 18))
        obj_left_label.pack()
        game_canvas.create_window(100, 480, window=obj_left_label)
        
    # Creates list of possible statements and pick one to show the user (This determins what numbers to click)
    def statement():
        
        # Makes str_statment global so can be used in number class for determining a change in score
        global str_statement
        
        # Create list holding statements on what numbers to click on, and pick a statement at random
        list_statement = ["Click every odd number",
                          "Click every number evenly divisable by 3",
                          "Click every even number"]
        str_statement = StringVar()
        str_statement.set(random.choice(list_statement))

        # Create label That tells the user the statement
        statement_label = Label(game_canvas, textvariable=str_statement,
                                background="orange", font=('Impact', 22))
        statement_label.pack()
        game_canvas.create_window(560, 25, window=statement_label)    
        
    #### Run functions to fill canvas
    score()
    statement()
    obj_number_tally(int_difficulty)
    
    # Allows loop to run as a variable needs to be set (Value irrelevant)
    _obj_number = 0

    # Creates instances of obj_number, amount proportional to int_difficulty
    def obj_create(int_difficulty, _obj_number):
        if int_difficulty > 0:
            _obj_number = Number()
            int_difficulty -= 1
            root.after(500, obj_create, int_difficulty, _obj_number)        
    obj_create(int_difficulty, _obj_number)  
    
# Functions on the numbers that appear on the game screen, controling how they are interacted with and affect points. 
class Number:
        
    # deletes obj_number upon click and sends score change
    def number_click(self, event, obj_number, int_number):         
        ### Check to see if number clicked will increase or decrease score
        # Good number was clicked
        if str_statement.get() == "Click every odd number" and int_number.get() % 2 == 1:
            str_score_change = "Positive"

        # Good number was clicked 
        elif str_statement.get() == "Click every number evenly divisable by 3" and int_number.get() % 3 == 0:
                str_score_change = "Positive"

        # Good number was clicked  
        elif str_statement.get() == "Click every even number" and int_number.get() % 2 == 0:
            str_score_change = "Positive"

            # Bad number was clicked
        else:
            str_score_change = "Negative"

        # Runs the score_change function and passes how the score changes
        self.score_change(str_score_change, obj_number)
            
    # Calculates the change in score when obj_number instances get deleted. Updates obj_number instances left (and label)
    def score_change(self, str_score_change, obj_number):
        ### Gets whether the change should be positive or negative and updates label
        # Score goes up and label is updated
        if str_score_change == "Positive":
            int_score.set(int_score.get() + 5)
            str_score.set("This is your score: " + str(int_score.get()))
            score_label.config(textvariable = str_score)

        # Score only goes up by 1 for not clicking anumber that shouldn't be clicked
        elif str_score_change == "Neutral":
            int_score.set(int_score.get() + 1)
            str_score.set("This is your score: " + str(int_score.get()))
            score_label.config(textvariable = str_score)

        # Score goes down, label is updated
        else:
            int_score.set(int_score.get() - 3)
            str_score.set("This is your score: " + str(int_score.get()))
            score_label.config(textvariable = str_score)

        # Destroys the obj_number as it either popped or was clicked on
        obj_number.destroy()

        # Counts how many obj_number's have been deleted
        int_number_obj_numbers.set(int_number_obj_numbers.get() - 1)

        # update the label that tells the user how many nubers are left
        str_obj_left.set(str(int_number_obj_numbers.get()) + " Numbers left")
        obj_left_label.config(textvariable = str_obj_left)

        # If there are no instances of obj-number left then wait and go to score screen
        if int_number_obj_numbers.get() == 0:
            root.after(500, score_screen)
        
    # Creates the instance and it's properties. Holds placement function to display obj_number instances
    def __init__(self):
        #Set default valuefor the font size
        int_font_size = 8

        # Set coord variables to 0 
        int_x_coord = 0
        int_y_coord = 0

        # Set coords to random point on screen
        int_x_coord = random.randrange(20, 780)
        int_y_coord = random.randrange(70, 450)
        
        # Places obj_number randemly on canvas
        def placement(int_font_size, obj_number, int_number):

            # Check to see if the obj_number hasn't already been clicked on.
            if obj_number.winfo_exists() == 0:
                pass
            else: # Number not clicked so go ahead as normal
                #Increase the size of the font
                int_font_size += 1
                obj_number.config(font=('Impact', int_font_size))

                # Check if number is big enough to be deleted
                if int_font_size > 40:
                    ### Check to see in number should have been clicked for score
                    # Should have been clicked but wasn't
                    if str_statement.get() == "Click every odd number" and int_number.get() % 2 == 1:
                        str_score_change = "Negative"

                    # Should have been clicked but wasn't   
                    elif str_statement.get() == "Click every number evenly divisable by 3" and int_number.get() % 3 == 0:
                        str_score_change = "Negative"

                    # Should have been clicked but wasn't   
                    elif str_statement.get() == "Click every even number" and int_number.get() % 2 == 0:
                        str_score_change = "Negative"

                    # Shouldn't have been clicked and wasn't
                    else:
                        str_score_change = "Neutral"

                    # Runs the score_change function and passes how the score changes
                    self.score_change(str_score_change, obj_number)

                # If number not big enough yet, grow it    
                else:
                    root.after(200, placement, int_font_size, obj_number, int_number)

        # Create value for number to click on
        int_number = IntVar()
        int_number.set(random.randrange(1, 10))

        # Create obj_number label on screen for user to interact with
        obj_number = Label(game_canvas, textvariable = int_number,
                            background = "orange", font=('Impact', int_font_size))

        # Binds the obj_number to the left mouse button to call the number_click function
        obj_number.bind("<Button-1>", lambda event: self.number_click(event, obj_number, int_number))
        
        obj_number.pack()
        game_canvas.create_window(int_x_coord, int_y_coord, window = obj_number)
        
        # Run the embeded function to place labels and pass int_number so user sees number value
        placement(int_font_size, obj_number, int_number)

### Create score screen after the game has finished
def score_screen():
    game_canvas.destroy()

    # Create score_canvas that widgets will appear on
    global score_canvas
    score_canvas = Canvas(root,width = 800, height = 500, bg='orange')
    score_canvas.pack()

    # Create button to move user back to the main menu
    menu_return_btn = Button(score_canvas, text="RETURN TO MENU", command= menu_open)
    score_canvas.create_window(400, 400, window = menu_return_btn)

    # Create label congratulating user on their score
    str_congratulations = StringVar()

    ### Check how well user did to change game response
    # User got negative score, so give encouragement
    if int_score.get() < 0:
        str_congratulations.set("You can do better next time\n" + str_username_entry.get()
                                + "\nYou Scored " + str(int_score.get()))
    # User got between 0 and 20 so say well done
    elif int_score.get() > 0 and int_score.get() < 20:
        str_congratulations.set("Well Done\n" + str_username_entry.get()
                                + "\nYou Scored " + str(int_score.get()))    
    # User got a score over 20 so say congrats
    else:
        str_congratulations.set("Congratulations\n" + str_username_entry.get()
                                + "\nYou Scored " + str(int_score.get()))
        
    congratulations_label = Label(score_canvas, textvariable = str_congratulations,
                                  background = "orange", font=('Impact', 30))
    congratulations_label.pack()
    score_canvas.create_window(400,200, window = congratulations_label)

# Create a new instance of User class to play the game again
def menu_open():
    score_canvas.destroy()
    run_game_again = User()

########### Create instance for User class, makes game run ############
run_game = User()

#### LOOP PROGRAM ####
# Make canvas non-resizable and loop
root.resizable(width=False, height=False)
root.mainloop()

# COPYRIGHT FLOW COMPUTING
