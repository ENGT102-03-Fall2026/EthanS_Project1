#Ethan Swann
#ENGT-102_Project 1

current_x=int()
current_y=int()
current_depth=float()
energy_remaining=float()
hull_integrity=float()
clue_points=int()
total_time=float()
searched_locations=[]
time_history=[]
energy_history=[]
hull_history=[]

def get_direction():
    Possible_directions=["forward", "backward","left","right"]
    
    while True:
        direction =input(
        "enter direction (forward, backward, left, right):").lower()
        
        if direction in Possible_directions:
            return direction
        else:
            print("Invalid Direction. Enter New Direction")
#get_direction is a function that has a list of all movement directions and prompts the user to enter
#a direction; if the direction is mistyped or an invalid direction is entered, the program returns an
#error message. This function does not yet account for whether or not the movement is possible on the
#supplied map. 

print("Entered direction",get_direction())
