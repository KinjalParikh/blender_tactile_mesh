import pygame
import pygame_gui
import data_generator
from datetime import datetime
import json

# load randomized test trials
anchor_point = 4
level_num = 7
repeat_num = 10
shuffle = True
trial_num = level_num * repeat_num
user_responses = []

trials = data_generator.generate_data(anchor_point, level_num, repeat_num, shuffle)
print(trials)
current_trial = 0
is_started = False

# Initialize pygame
pygame.init()

# Constants for window size
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Create the window
window_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Set up the GUI manager
manager = pygame_gui.UIManager((WINDOW_WIDTH, WINDOW_HEIGHT), 'theme.json')

# Create GUI elements
left_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((150, 250), (100, 50)),
                                           text='Left',
                                           manager=manager)

right_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((550, 250), (100, 50)),
                                            text='Right',
                                            manager=manager)

start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 450), (100, 50)),
                                            text='Start',
                                            manager=manager)

export_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((650, 550), (100, 50)),
                                            text='Export',
                                            manager=manager)

left_text_box = pygame_gui.elements.UITextBox(html_text='1',
                                              relative_rect=pygame.Rect((150, 100), (100, 100)),
                                              manager=manager)

right_text_box = pygame_gui.elements.UITextBox(html_text='3',
                                               relative_rect=pygame.Rect((550, 100), (100, 100)),
                                               manager=manager)

trials_text_box = pygame_gui.elements.UITextBox(html_text=f'# of trials: 0/{trial_num}',
                                                relative_rect=pygame.Rect((200, 550), (400, 50)),
                                                manager=manager)

def start_function():
    global is_started, current_trial
    print("Start button clicked")
    if not is_started and current_trial < trial_num:
        is_started = True
        # start the trials
        left_number, right_number = trials[current_trial]
        left_text_box.set_text(str(left_number))
        right_text_box.set_text(str(right_number))
        current_trial += 1
        trials_text_box.set_text(f"# of trials: {current_trial}/{trial_num}")
        print(f"Start trial {current_trial}/{trial_num}")

def left_button_clicked():
    global is_started
    print("Left button clicked")
    if is_started:
        # record the response
        is_started = False
        left_button.disable()
        right_button.disable()
        user_responses.append(0)
        left_button.enable()
        right_button.enable()

def right_button_clicked():
    global is_started
    print("Right button clicked")
    if is_started:
        # record the response
        is_started = False
        left_button.disable()
        right_button.disable()
        user_responses.append(1)
        left_button.enable()
        right_button.enable()

def export_button_clicked():
    print("Export button clicked")
    # export the responses
    file_name = f"results/responses_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"
    with open(file_name, "w") as f:
        for i in range(len(user_responses)):
            data = {
                "trial": trials[i].tolist(),
                "response": user_responses[i]
            }
            f.write(json.dumps(data) + "\n")
    print(f"Exported the responses to {file_name}")

# Main loop
clock = pygame.time.Clock()
is_running = True

while is_running:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == start_button:
                    start_function()
                elif event.ui_element == left_button:
                    left_button_clicked()
                elif event.ui_element == right_button:
                    right_button_clicked()
                elif event.ui_element == export_button:
                    export_button_clicked()

        manager.process_events(event)
    
    manager.update(time_delta)
    # Clear the window surface to some background color
    window_surface.fill(pygame.Color('#FFFFFF'))

    # Draw the UI elements
    manager.draw_ui(window_surface)

    # Update the full display surface to the screen
    pygame.display.update()

# Quit pygame
pygame.quit()
