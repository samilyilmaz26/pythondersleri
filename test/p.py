from psychopy import visual, core, event
from datetime import datetime
from math import sqrt
import random
import csv
import numpy as np

def check_for_escape():
    if 'escape' in event.getKeys(keyList=['escape']):
        save_and_quit()


def save_and_quit():
    filename = f"mainexperiement_partial_{session_id}.csv"
    with open(filename, mode='w', newline='') as file:
        fieldnames = ['Session ID', 'Block', 'Trial', 'Taste Intensity', 'Pleasantness Response',
                      'Triangle X', 'Triangle Y', 'Label 1', 'Label 2', 'Label 3']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for response_data in responses:
            writer.writerow(response_data)
    win.close()
    print(f"Partial data saved to {filename}")
    core.quit()


def create_cross_stim(win, pos, size, color='red'):
    """Helper function to create a cross visual stimulus."""
    return visual.ShapeStim(win, vertices=[(pos[0], pos[1] - size/3), (pos[0], pos[1] + size/3), pos,
                                           (pos[0] - size/3, pos[1]), (pos[0] + size/3, pos[1])],
                            lineColor=color, fillColor=color, closeShape=False)

def run_slider_trial(win, block, trial, instruction_text, slider_label_text, slider_pos=(0, -0.2)):

    check_for_escape()
    block_trial_abbrev = visual.TextStim(win, text=f"B{block}:T{trial}", pos=(-0.7, 0.9), height=0.05)

    full_instruction_text = f"{instruction_text}\n\nDrag the marker to indicate your rating and press 'space' to confirm within 5 seconds.\n\n\n\n{slider_label_text}"
    instructions = visual.TextStim(win, text=full_instruction_text, pos=(0, 0.5), wrapWidth=1.8)
    

    # Drawing the scale
    scale_line = visual.Line(win, start=(-0.5, slider_pos[1]), end=(0.5, slider_pos[1]), lineWidth=5, lineColor='White')
    labels = [visual.TextStim(win, text=str(i), pos=(x, slider_pos[1] - 0.1), height=0.05, color='White') for i, x in zip([1, 9], [-0.5, 0.5])]
    marker = visual.Rect(win, width=0.02, height=0.1, fillColor='red', lineColor='red', pos=(slider_pos[0], slider_pos[1]))

    mouse = event.Mouse(visible=True, win=win)
    rating_confirmed = False

    while not rating_confirmed:
        check_for_escape()
        block_trial_abbrev.draw()

        instructions.draw()
        scale_line.draw()
        for label in labels:
            label.draw()
        marker.draw()

        win.flip()

        keys = event.getKeys()
        if 'space' in keys:
            rating_confirmed = True
            break
        
        if mouse.getPressed()[0]:
            check_for_escape()
            mouse_pos = mouse.getPos()
            if -0.5 <= mouse_pos[0] <= 0.5 and abs(mouse_pos[1] - slider_pos[1]) < 0.1:
                marker.setPos((mouse_pos[0], slider_pos[1]))
            check_for_escape()

        for key in event.getKeys():
            if key == 'escape':
                core.quit()
    rating = round(((marker.pos[0] + 0.5) * 8) / 1.0) + 1
    return rating


def run_triangle_trial(win, trial_num, block_num, scale_factor=3):
    check_for_escape()
    block_trial_abbrev = visual.TextStim(win, text=f"B{block_num}:T{trial_num}", pos=(-0.7, 0.9), height=0.05)

    pix = 100 * scale_factor
    # Triangle vertices in pixels
    a, b, c = (1*pix, -0.8660254037844386*pix), (-1*pix, -0.8660254037844386*pix), (0, 0.8660254037844386*pix)

    # Calculate centroid of the triangle
    centroid_x = (a[0] + b[0] + c[0]) / 3
    centroid_y = (a[1] + b[1] + c[1]) / 3

    # Draw the triangle
    vertices_centered = [a, b, c]
    triangle = visual.ShapeStim(win, vertices=vertices_centered, lineColor='white', fillColor=None, closeShape=True, lineWidth=3, units='pix')

    # Draw a dot at the centroid
    centroid_dot = visual.Circle(win, radius=4,  # radius in pixels, adjust as needed for visibility
                                 fillColor='white', lineColor='white',
                                 pos=(centroid_x, centroid_y), units='pix')  # Ensure units match those of the triangle

    # Central cross placed at the centroid

    labels = ["Pure Sweet", "Pure Sour", "Pure Salty"]
    label_positions = [(0, 0.63), (-0.55, -0.58), (0.55, -0.58)]
    
    instruction_text = "Please click inside the triangle to position the cross. Adjust its position if necessary. Confirm your final choice by pressing 'space' within 5 seconds."
    instructions = visual.TextStim(win, text=instruction_text, pos=(0, -0.8), color='white', height=0.07)
    cross = create_cross_stim(win, (0, 0), 0.05, 'red')
    mouse = event.Mouse(win=win)
    cross_placed = False
    confirm = False

    while not confirm:
        check_for_escape()
        triangle.draw()
        block_trial_abbrev.draw()

        centroid_dot.draw()  # Draw the central cross at the centroid of the triangle
        for label, pos in zip(labels, label_positions):
            visual.TextStim(win, text=label, pos=pos, color='white', height=0.07).draw()
        instructions.draw()
        if cross_placed:
            cross.draw()
        

        win.flip()

        if mouse.getPressed()[0]:
            mouse_pos = mouse.getPos()
            if triangle.contains(mouse_pos):
                cross.setPos(mouse_pos)
                cross_placed = True
                while mouse.getPressed()[0]:  # Keep checking for escape while mouse button is pressed
                    check_for_escape()

        keys = event.getKeys()
        if 'space' in keys and cross_placed:
            confirm = True
        elif 'escape' in keys:
            core.quit()

    return (mouse_pos[0], mouse_pos[1], labels[0], labels[1], labels[2])

# Main experiment setup
win = visual.Window(size=[1440, 900],fullscr=True, color='black')
session_id = datetime.now().strftime("%Y%m%d_%H%M%S")

session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
num_blocks = 4  # Number of blocks in the experiment
trials_per_block = 28  # Number of trials per block

# Display welcome message
welcome_message = visual.TextStim(win, text="Welcome to the experiment.\nPlease press any key when you're ready to start.", pos=(0, 0), height=0.05, wrapWidth=1.8, color='white')
welcome_message.draw()
win.flip()
event.waitKeys()

responses = []

for block in range(1, num_blocks + 1):
    for trial in range(1, trials_per_block + 1):

        # Setup and display fixation, HOLD, and DRINK messages
        fixation = visual.TextStim(win, text="+", pos=(0, 0), color='white')
        fixation.draw()
        win.flip()
        core.wait(3)  # Wait for 4 seconds

        message = visual.TextStim(win, text="CUP", pos=(0, 0), color='white')
        message.draw()
        win.flip()
        core.wait(3)  # Wait for 3 seconds

        message = visual.TextStim(win, text="DRINK", pos=(0, 0), color='white')
        message.draw()
        win.flip()
        core.wait(3)  # Wait for participants to taste the sample

        # Conduct the triangle taste test first
        triangle_response = run_triangle_trial(win, trial, block)

        # Then, gather intensity rating
        intensity_instruction_text = "Please rate the taste intensity."
        intensity_response = run_slider_trial(win, block, trial, intensity_instruction_text, "Taste Intensity")
        # Finally, gather pleasantness rating
        pleasantness_instruction_text = "Rate the taste pleasantness."
        pleasantness_response = run_slider_trial(win, block, trial, pleasantness_instruction_text, "Taste Pleasantness")
        # Insert RINSE prompt here
        rinse_message = visual.TextStim(win, text="RINSE", pos=(0, 0), color='white')
        rinse_message.draw()
        win.flip()
        core.wait(3)  # Display the RINSE message for 3 seconds

        # Append all responses to the response list
        responses.append({'Session ID': session_id, 'Block': block, 'Trial': trial, 
                          'Triangle X': triangle_response[0], 'Triangle Y': triangle_response[1], 
                          'Label 1': triangle_response[2], 'Label 2': triangle_response[3], 
                          'Label 3': triangle_response[4],
                          'Taste Intensity': intensity_response, 
                          'Pleasantness Response': pleasantness_response})

    if block < num_blocks:
        # First part: Inform the participant about the 3-minute break
        break_message_part1 = visual.TextStim(win, text="Break time\n Feel free to take a 3-minute break.",
                                              pos=(0, 0), height=0.05, wrapWidth=1.8)
        break_message_part1.draw()
        win.flip()
        core.wait(180)  # Wait for 180 seconds (3 minutes)
        
        # Second part: Prompt to press any key to continue
        break_message_part2 = visual.TextStim(win, text="Press any key to continue when you're ready.",
                                              pos=(0, 0), height=0.05, wrapWidth=1.8)
        break_message_part2.draw()
        win.flip()
        event.waitKeys()

# Save the experiment data
def save_data():
    global responses, session_id
    filename = f"mainexperiment_data_{session_id}.csv"
    with open(filename, mode='w', newline='') as file:
        fieldnames = ['Session ID', 'Block', 'Trial', 'Taste Intensity', 'Pleasantness Response',
                      'Triangle X', 'Triangle Y', 'Label 1', 'Label 2', 'Label 3']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for response_data in responses:
            writer.writerow(response_data)
    print(f"Data saved to {filename}")
    
    
save_data()
win.close()
core.quit()

