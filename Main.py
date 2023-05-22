from EA import *
from visualizer import *
import pygame
import turtle
import pygame_gui

pygame.init()


screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))

# Create a Pygame GUI manager
gui_manager = pygame_gui.UIManager((screen_width, screen_height))

show_label_rect = pygame.Rect(10, 50, 200, 20)
show_label = pygame_gui.elements.UILabel(
    relative_rect=show_label_rect,
    text="Choose Initial Population",
    manager=gui_manager
)

show_label_rect_2 = pygame.Rect(10, 100, 200, 20)
show_label_2 = pygame_gui.elements.UILabel(
    relative_rect=show_label_rect_2,
    text="Choose no of Substitutions",
    manager=gui_manager
)

show_label_rect_a = pygame.Rect(10, 150, 200, 20)
show_label_a = pygame_gui.elements.UILabel(
    relative_rect=show_label_rect_a,
    text="Positive phototropism",
    manager=gui_manager
)

show_label_rect_b = pygame.Rect(10, 200, 200, 20)
show_label_b = pygame_gui.elements.UILabel(
    relative_rect=show_label_rect_b,
    text="Bilateral Symmetry",
    manager=gui_manager
)


show_label_rect_d = pygame.Rect(10, 250, 200, 20)
show_label_d = pygame_gui.elements.UILabel(
    relative_rect=show_label_rect_d,
    text="Structural Stability",
    manager=gui_manager
)

show_label_rect_e = pygame.Rect(10, 300, 230, 20)
show_label_e = pygame_gui.elements.UILabel(
    relative_rect=show_label_rect_e,
    text="Branching point proportion",
    manager=gui_manager
)


# Create a slider for no.of Trees
slider_rect = pygame.Rect(220, 50, 200, 20)
slider_range = (20, 60)
slider_start_value = 40
slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=slider_rect,
    start_value=slider_start_value,
    value_range=slider_range,
    manager=gui_manager
)

# Create a slider for no.of substitutions
slider2_rect = pygame.Rect(220, 100, 200, 20)
slider2_range = (1, 6)
slider2_start_value = 3
slider2 = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=slider2_rect,
    start_value=slider2_start_value,
    value_range=slider2_range,
    manager=gui_manager
)

# SLIDERS FOR FITNESS FUNCTION WEIGHTAGE.
slider3_rect = pygame.Rect(220, 150, 200, 20)
slider3_range = (10, 100)
slider3_start_value = 100
slider3 = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=slider3_rect,
    start_value=slider3_start_value,
    value_range=slider3_range,
    manager=gui_manager
)

sliderb_rect = pygame.Rect(220, 200, 200, 20)
sliderb_range = (10, 100)
sliderb_start_value = 90
sliderb = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=sliderb_rect,
    start_value=sliderb_start_value,
    value_range=sliderb_range,
    manager=gui_manager
)


sliderd_rect = pygame.Rect(220, 250, 200, 20)
sliderd_range = (10, 100)
sliderd_start_value = 40
sliderd = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=sliderd_rect,
    start_value=sliderd_start_value,
    value_range=sliderd_range,
    manager=gui_manager
)

slidere_rect = pygame.Rect(240, 300, 200, 20)
slidere_range = (10, 100)
slidere_start_value = 80
slidere = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=slidere_rect,
    start_value=slidere_start_value,
    value_range=slidere_range,
    manager=gui_manager
)

InitialTrees = slider_start_value
substitue_order = slider2_start_value
wa = slider3_start_value
wb = sliderb_start_value
#wc = sliderc_start_value
wd = sliderd_start_value
we = slidere_start_value

# Create a label to display the current value of the slider
label_rect = pygame.Rect(450, 50, 50, 20)
label = pygame_gui.elements.UILabel(
    relative_rect=label_rect,
    text=str(slider.get_current_value()),
    manager=gui_manager
)

label2_rect = pygame.Rect(450, 100, 50, 20)
label2 = pygame_gui.elements.UILabel(
    relative_rect=label2_rect,
    text=str(slider2.get_current_value()),
    manager=gui_manager
)

label3_rect = pygame.Rect(450, 150, 50, 20)
label3 = pygame_gui.elements.UILabel(
    relative_rect=label3_rect,
    text=str(slider3.get_current_value()),
    manager=gui_manager
)

label4_rect = pygame.Rect(450, 200, 50, 20)
label4 = pygame_gui.elements.UILabel(
    relative_rect=label4_rect,
    text=str(sliderb.get_current_value()),
    manager=gui_manager
)

label6_rect = pygame.Rect(450, 250, 50, 20)
label6 = pygame_gui.elements.UILabel(
    relative_rect=label6_rect,
    text=str(sliderd.get_current_value()),
    manager=gui_manager
)
label7_rect = pygame.Rect(450, 300, 50, 20)
label7 = pygame_gui.elements.UILabel(
    relative_rect=label7_rect,
    text=str(slidere.get_current_value()),
    manager=gui_manager
)

# Creating the button
button_rect = pygame.Rect(150, 400, 300, 30)
done_button = pygame_gui.elements.UIButton(
    relative_rect=button_rect,
    text="Optimize to get the best Tree:",
    manager=gui_manager
)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Pass events to the GUI manager
        gui_manager.process_events(event)

        label.set_text(str(slider.get_current_value()))
        label2.set_text(str(slider2.get_current_value()))
        label3.set_text(str(slider3.get_current_value()))
        label4.set_text(str(sliderb.get_current_value()))
        # label5.set_text(str(sliderc.get_current_value()))
        label6.set_text(str(sliderd.get_current_value()))
        label7.set_text(str(slidere.get_current_value()))

        # Handle button clicks
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == done_button:
                    # Get the final values of both sliders
                    InitialTrees = slider.get_current_value()
                    substitue_order = slider2.get_current_value()
                    wa = slider3.get_current_value()
                    wb = sliderb.get_current_value()
                    wc = 60
                    #wc = sliderc.get_current_value()
                    wd = sliderd.get_current_value()
                    we = slidere.get_current_value()

                    # VALUES DECIDED BY US.
                    generations = 40
                    mutationrate = 0.3
                    offsprings = int(0.6*InitialTrees)

                    system = GeneticAlgorithm(
                        InitialTrees, generations, mutationrate, offsprings, substitue_order, False, wa, wb, wc, wd, we)
                    print(system.population)
                    result = system.Optimization()
                    max_sublist = max(result, key=lambda x: x[0])
                    # print(system.population)
                    running = False

                    s = lSysGenerate(max_sublist[1], 4)
                    visualize(s)

    # Update the GUI manager
    gui_manager.update(pygame.time.get_ticks() / 1000)

    # Draw the GUI manager to the screen
    screen.fill((255, 255, 255))
    gui_manager.draw_ui(screen)
    pygame.display.update()


pygame.quit()
