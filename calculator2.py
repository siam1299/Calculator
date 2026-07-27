from tkinter import Tk, Entry, Button, StringVar, PhotoImage
import os

# ---------- Color palette (modern dark theme) ----------
BG_MAIN     = '#1e1e2e'   # window background
BG_DISPLAY  = '#181825'   # entry background
FG_DISPLAY  = '#ffffff'   # entry text
BG_NUMBER   = '#313244'   # number buttons
FG_NUMBER   = '#ffffff'
BG_OPERATOR = '#f38ba8'   # + - x / (pink/red accent)
FG_OPERATOR = '#1e1e2e'
BG_UTILITY  = '#585b70'   # ( ) %
FG_UTILITY  = '#ffffff'
BG_CLEAR    = '#eba0ac'   # C
FG_CLEAR    = '#1e1e2e'
BG_EQUAL    = '#a6e3a1'   # =
FG_EQUAL    = '#1e1e2e'

FONT_DISPLAY = ('Segoe UI', 26)
FONT_BUTTON  = ('Segoe UI', 14, 'bold')


class Calculator:
    def __init__(self, master):
        master.title("Calculator")
        master.geometry('360x520')
        master.config(bg=BG_MAIN)
        master.resizable(False, False)

        self.equation = StringVar()
        self.entry_value = ''

        # ---------- Display ----------
        entry = Entry(
            master,
            textvariable=self.equation,
            font=FONT_DISPLAY,
            bg=BG_DISPLAY,
            fg=FG_DISPLAY,
            insertbackground=FG_DISPLAY,
            relief='flat',
            justify='right',
            bd=0,
        )
        entry.grid(row=0, column=0, columnspan=4, sticky='nsew', padx=12, pady=(20, 15), ipady=25)

        # ---------- Button layout ----------
        # (label, row, col, bg, fg, command)
        buttons = [
            ('C', 1, 0, BG_CLEAR, FG_CLEAR, self.clear),
            ('(', 1, 1, BG_UTILITY, FG_UTILITY, lambda: self.show('(')),
            (')', 1, 2, BG_UTILITY, FG_UTILITY, lambda: self.show(')')),
            ('%', 1, 3, BG_UTILITY, FG_UTILITY, lambda: self.show('%')),

            ('7', 2, 0, BG_NUMBER, FG_NUMBER, lambda: self.show('7')),
            ('8', 2, 1, BG_NUMBER, FG_NUMBER, lambda: self.show('8')),
            ('9', 2, 2, BG_NUMBER, FG_NUMBER, lambda: self.show('9')),
            ('/', 2, 3, BG_OPERATOR, FG_OPERATOR, lambda: self.show('/')),

            ('4', 3, 0, BG_NUMBER, FG_NUMBER, lambda: self.show('4')),
            ('5', 3, 1, BG_NUMBER, FG_NUMBER, lambda: self.show('5')),
            ('6', 3, 2, BG_NUMBER, FG_NUMBER, lambda: self.show('6')),
            ('x', 3, 3, BG_OPERATOR, FG_OPERATOR, lambda: self.show('x')),

            ('1', 4, 0, BG_NUMBER, FG_NUMBER, lambda: self.show('1')),
            ('2', 4, 1, BG_NUMBER, FG_NUMBER, lambda: self.show('2')),
            ('3', 4, 2, BG_NUMBER, FG_NUMBER, lambda: self.show('3')),
            ('-', 4, 3, BG_OPERATOR, FG_OPERATOR, lambda: self.show('-')),

            ('0', 5, 0, BG_NUMBER, FG_NUMBER, lambda: self.show('0')),
            ('.', 5, 1, BG_NUMBER, FG_NUMBER, lambda: self.show('.')),
            ('=', 5, 2, BG_EQUAL, FG_EQUAL, self.solve),
            ('+', 5, 3, BG_OPERATOR, FG_OPERATOR, lambda: self.show('+')),
        ]

        self.widgets = {}
        for (text, row, col, bg, fg, cmd) in buttons:
            btn = Button(
                master,
                text=text,
                font=FONT_BUTTON,
                bg=bg,
                fg=fg,
                relief='flat',
                bd=0,
                activebackground=self._darken(bg),
                activeforeground=fg,
                cursor='hand2',
                command=cmd,
            )
            btn.grid(row=row, column=col, sticky='nsew', padx=6, pady=6, ipady=18)
            # simple hover effect
            btn.bind('<Enter>', lambda e, b=btn, c=bg: b.config(bg=self._darken(c)))
            btn.bind('<Leave>', lambda e, b=btn, c=bg: b.config(bg=c))

        # ---------- Grid resizing ----------
        for i in range(6):
            master.grid_rowconfigure(i, weight=1)
        for i in range(4):
            master.grid_columnconfigure(i, weight=1)

    @staticmethod
    def _darken(hex_color, factor=0.85):
        """Return a slightly darker shade of hex_color for hover/active states."""
        hex_color = hex_color.lstrip('#')
        r, g, b = (int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
        r, g, b = (max(0, int(c * factor)) for c in (r, g, b))
        return f'#{r:02x}{g:02x}{b:02x}'

    # Method to show values
    def show(self, value):
        self.entry_value += str(value)
        self.equation.set(self.entry_value)

    # Method to clear the entry
    def clear(self):
        self.entry_value = ''
        self.equation.set(self.entry_value)

    # Method to solve the equation
    def solve(self):
        try:
            self.entry_value = self.entry_value.replace('x', '*')  # Replace 'x' with '*' for multiplication
            result = str(eval(self.entry_value))
            self.equation.set(result)
            self.entry_value = result  # Allow for further calculations with the result
        except Exception:
            self.equation.set('error')
            self.entry_value = ''


if __name__ == '__main__':
    root = Tk()

    icon_path = "cal.png"
    if os.path.exists(icon_path):
        image_icon = PhotoImage(file=icon_path)
        root.iconphoto(False, image_icon)

    Calculator(root)
    root.mainloop()