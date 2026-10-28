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


search_effects = {
    "Low Hazard": (-5, -5, 0),
    "Medium Hazard": (-10, -5, 0),
    "High Hazard": (-15, -10, 0),
    "Low Value Clue": (-5, -5, 1),
    "Strong Clue": (-2, -5, 2),
    "High Value Clue": (-2, -2, 3),
    "None": (-2, -5, 0)
}
#Above is the search effects dictionary 


import matplotlib.pyplot as plt
import csv

def load_mission(filename):

    mission = {}

    with open(filename, newline="") as file:

        reader = csv.reader(file)

        for row in reader:

            x = int(row[0])
            y = int(row[1])

            mission[(x, y)] = {
                "at_location": row[2],
                "description": row[3],
                "depth_m": float(row[4]),
                "distance_m": float(row[5]),
                "time_min": float(row[6])
            }

    return mission
#The above line loads the csv and determines the full size of the grid


def get_grid_size(mission):
    max_y=max(cord[1] for cord in mission.keys())+1
    max_x=max(cord[0] for cord in mission.keys())+1
    
    return max_x,max_y
#Above is the function to define the bounds for the game based on the csv
    
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
#error message. This function doesnt account for if the new direction is possible yet


def get_new_position(rover_state, direction):

    current_x = rover_state["current_x"]
    current_y = rover_state["current_y"]

    if direction == "forward":
        return current_x, current_y + 1
    elif direction == "backward":
        return current_x, current_y - 1
    elif direction == "right":
        return current_x + 1, current_y
    elif direction == "left":
        return current_x - 1, current_y


def is_valid_position(x, y, max_x, max_y):

    if 0 <= x < max_x and 0 <= y < max_y:
        return True

    return False
#The above functin defines the bounds of movement between (0,0) and the max (x,y) specified in the csv file


def display_status(rover_state):

    print("\n--- Rover Status ---")
    print(
        f"Position: ({rover_state['current_x']}, "
        f"{rover_state['current_y']})"
    )

    print(f"Depth: {rover_state['current_depth']:.1f} m")
    print(f"Energy: {rover_state['energy_remaining']:.1f}%")
    print(f"Hull: {rover_state['hull_integrity']:.1f}%")
    print(f"Clue Points: {rover_state['clue_points']}")
    print(f"Time: {rover_state['total_time']:.1f} min")
#The above function is used to display the rover stats to the shell for user veiwing
    
    
def apply_movement_cost(rover_state, destination):
    previous_depth = rover_state["current_depth"]
    new_depth = destination["depth_m"]
    distance = destination["distance_m"]
    time = destination["time_min"]
    
    hull_loss = abs(new_depth - previous_depth) * 0.8 * time
    energy_loss = (abs(new_depth - previous_depth) * 0.5 + (distance / time) * 1.2)

    rover_state["hull_integrity"] -= hull_loss
    rover_state["energy_remaining"] -= energy_loss
    rover_state["total_time"] += time
    rover_state["current_depth"] = new_depth
    rover_state["time_history"].append(rover_state["total_time"])
    rover_state["energy_history"].append(rover_state["energy_remaining"])
    rover_state["hull_history"].append(rover_state["hull_integrity"])
    return hull_loss, energy_loss
#The above function updates the rover status after a move to new values in accordance with the type of space being filled

def get_search_choice():
    while True:
        choice = input("Search location? (yes/no): ").lower()
        if choice in ["yes", "y"]:
            return True
        if choice in ["no", "n"]:
            return False
        print("Invalid input. Try again.")
#The above function prompts the user to search or not 


def search_location(rover_state, location):
    current_position = (rover_state["current_x"],rover_state["current_y"])
    if current_position in rover_state["searched_locations"]:
        print("Location already searched.")
        return None
    rover_state["searched_locations"].append(current_position)
    category = location["at_location"]
    
    print("\nLocation Found:")
    print("Category:", category)
    print("Description:", location["description"])
    
    if category == "Treasure":
        return "TREASURE"
    hull_change, energy_change, clue_change = (search_effects[category])
    rover_state["hull_integrity"] += hull_change
    rover_state["energy_remaining"] += energy_change
    rover_state["clue_points"] += clue_change
    rover_state["energy_history"][-1] = (rover_state["energy_remaining"])
    rover_state["hull_history"][-1] = (rover_state["hull_integrity"])
#The above function contains all of the possible effects for searching a give spot and updates the rover state accordingly
    

def check_failure(rover_state):
    return (
        rover_state["energy_remaining"] <= 10
        or
        rover_state["hull_integrity"] <= 10)
#The above function checks for faliure conditions


def check_clue_success(rover_state):
    return ( rover_state["clue_points"] >= 6
        and rover_state["energy_remaining"] > 10
        and rover_state["hull_integrity"] > 10)
#The above function determines if the max number of clue points have been met and if the rover has not failed


def update_plot(rover_state):
    plt.figure(figsize=(8, 5))
    ax1 = plt.gca()
    ax1.plot(rover_state["time_history"],rover_state["energy_history"],color="blue",label="Energy")
    
    ax1.set_xlabel("Mission Time (min)")
    ax1.set_ylabel("Energy (%)")
    
    ax2 = ax1.twinx()
    ax2.plot(rover_state["time_history"],rover_state["hull_history"],color="red",label="Hull Integrity")

    ax2.set_ylabel("Hull Integrity (%)")
    plt.title("Mission Status")

    plt.savefig("mission_plot.png")
    plt.close()



def main():

    mission = load_mission("mission_training.csv")
    max_x, max_y = get_grid_size(mission)

    print("\nCaptain Flint Recovery Mission")
    print("Starting Position: (0,0)")
    print("Energy: 100%")
    print("Hull Integrity: 100%")
    print("Clue Target: 6")

    mission_active = True

    while mission_active:
        direction = get_direction()
        new_x, new_y = get_new_position(rover_state,direction)
        if not is_valid_position(new_x,new_y,max_x,max_y):
            print("Out of bounds. Select another direction.")

            continue

        destination = mission[(new_x, new_y)]

        hull_loss, energy_loss = (apply_movement_cost(rover_state,destination))
        rover_state["current_x"] = new_x
        rover_state["current_y"] = new_y

        print("\nMove Successful")
        print(f"Hull Loss: {hull_loss:.2f}")
        print(f"Energy Loss: {energy_loss:.2f}")

        display_status(rover_state)
        update_plot(rover_state)

        if check_failure(rover_state):
            print("\nMISSION FAILED")
            break

        if get_search_choice():
            result = search_location(rover_state,destination)
            update_plot(rover_state)
            if result == "TREASURE":
                print("\nTREASURE FOUND!")
                print("MISSION SUCCESS!")

                break
            if check_failure(rover_state):
                print("\nMISSION FAILED")
                
                break
            if check_clue_success(
                rover_state):
                print("\nEnough clue points collected!")
                print("MISSION SUCCESS!")
                break

        display_status(rover_state)
    print("\n----- FINAL SUMMARY -----")
    print(
        f"Final Position: "
        f"({rover_state['current_x']}, "
        f"{rover_state['current_y']})")
    print(
        f"Total Time: "
        f"{rover_state['total_time']:.2f}")
    print(
        f"Energy Remaining: "
        f"{rover_state['energy_remaining']:.2f}%")
    print(
        f"Hull Remaining: "
        f"{rover_state['hull_integrity']:.2f}%")
    print(
        f"Clue Points: "
        f"{rover_state['clue_points']}")
    print(
        f"Searched Locations: "
        f"{len(rover_state['searched_locations'])}")

if __name__ == "__main__":
    main()
    
#The above is the entire gameplay loop 