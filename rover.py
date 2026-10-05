#Ethan Swann
#ENGT-102_Project 1

rover_state = {
    "current_x": 0,
    "current_y": 0,
    "current_depth": 2.0,
    "energy_remaining": 100.0,
    "hull_integrity": 100.0,
    "clue_points": 0,
    "total_time": 0.0,
    "searched_locations": [],
    "time_history": [0.0],
    "energy_history": [100.0],
    "hull_history": [100.0]
}
#Above is the rover state in a dictionary format for ease of use

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
