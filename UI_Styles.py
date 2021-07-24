import pyglet
pyglet.font.add_file("assets/lmmath-regular.otf")


class DarkTheme:
    def __init__(self):
        # Colours for background elements
        self.bg_1 = '#221f22'
        self.bg_2 = '#221f22'
        self.bg_3 = '#2d2a2e'
        self.bg_4 = '#272822'

        # Colours for foreground elements
        self.fg_1 = '#797979'
        self.fg_2 = '#d6d6d6'

        self.fg_err = '#221f22'
        self.fg_cor = '#221f22'

        self.bg_err = '#ff6188'
        self.bg_cor = '#a9dc76'

        # Colours for text elements
        self.txt_1 = '#FFFFFF'
        self.txt_2 = '#AAAAAA'

        # Default Fonts
        self.font_math = ('Latin Modern Math', 12)
        self.font_text = 'Corbel 11'
        self.font_title = 'Corbel 16 bold'
        self.font_button = 'Corbel 14 bold'


class DarkThem_:
    def __init__(self):
        # Colours for background elements
        self.bg_1 = '#1e2124'
        self.bg_2 = '#282b30'
        self.bg_3 = '#36393e'
        self.bg_4 = '#424549'

        # Colours for foreground elements
        self.fg_1 = '#7289da'
        self.fg_2 = '#ff904c  '

        self.fg_err = '#221f22'
        self.fg_cor = '#221f22'

        self.bg_err = '#ff6188'
        self.bg_cor = '#a9dc76'

        # Colours for text elements
        self.txt_1 = '#FFFFFF'
        self.txt_2 = '#AAAAAA'

        # # Default Fonts
        self.font_math = 'Corbel 11'
        self.font_text = 'Corbel 11'
        self.font_title = 'Corbel 16 bold'
        self.font_button = 'Corbel 14 bold'
