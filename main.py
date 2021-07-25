import GameScreen
import ModuleScreen
from WindowDark import WindowDark

# Create a root window to hold the game using custom window class
root = WindowDark(480, 700)

# Main Game Loop: Load main menu -> user selects level -> load level -> level closed / compleated -> Load main menu
while True:

    # Keep returning to the menu screen until a module is returned
    module = None
    while not module:
        menu_screen = ModuleScreen.Screen(root)
        module = menu_screen.main_loop()

    # Create a game screen and start its mainloop
    game_screen = GameScreen.Screen(root, module)
    game_screen.main_loop()
