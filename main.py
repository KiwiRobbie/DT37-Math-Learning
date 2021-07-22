import GameScreen
import ModuleScreen
from WindowDark import WindowDark

root = WindowDark(480, 700)

while True:
    menu_screen = ModuleScreen.Screen(root)
    course = menu_screen.main_loop()

    game_screen = GameScreen.Screen(root, course)  # menu_screen.game_screen
    game_screen.main_loop()