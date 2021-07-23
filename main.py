import GameScreen
import ModuleScreen
from WindowDark import WindowDark

# Create a root window to hold the game using custom window class
root = WindowDark(480, 700)

# Main Game Loop: Load main menu -> user selects level -> load level -> level closed / compleated -> Load main menu
while True:
    # Create a menu screen and enter the main loop awaiting the users selection
    menu_screen = ModuleScreen.Screen(root)
    course = menu_screen.main_loop()

    # Create a game screen, specify the selected course
    game_screen = GameScreen.Screen(root, course)  # menu_screen.game_screen
    game_screen.main_loop()