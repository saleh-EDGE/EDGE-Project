from tkinter import Tk, Entry, Button, StringVar, PhotoImage

try:
    from PIL import Image, ImageDraw, ImageTk, ImageColor
except ImportError:
    print("Pillow library not found. Please install it: pip install Pillow")
    # You might want to exit or use a fallback here.
    # For now, we'll let it raise an error if Pillow is not found.
    raise


class Calculator:
    def __init__(self, master):
        self.master = master  # Store master for use in methods
        master.title('Calculator')
        master.geometry('357x420+0+0')
        # A slightly muted background
        master.config(bg='#3a3a3a')
        master.resizable(False, False)

        self.equation = StringVar()
        self.entry_value = ''

        # Entry widget with a dark theme
        Entry(width=20, bg='#252525', fg='white', font=('Arial Bold', 28),
              textvariable=self.equation, bd=10, relief='sunken',
              insertbackground='white').place(x=0, y=0)

        # Keep track of PhotoImage objects to prevent garbage collection
        self.button_images = []

        # Button dimensions in pixels (adjust as needed for your display)
        btn_w_px, btn_h_px = 88, 73

        # Define gradient pairs (Top to Bottom) and text colors
        func_grad = ('#EAEAEA', '#C0C0C0')  # Light Grey gradient
        num_grad = ('#808080', '#505050')  # Dark Grey gradient
        op_grad = ('#FFC107', '#FFA000')  # Amber/Orange gradient
        eq_grad = ('#8BC34A', '#689F38')  # Light Green gradient
        c_grad = ('#F44336', '#D32F2F')  # Red gradient

        func_fg = 'black'
        num_fg = 'white'
        op_fg = 'white'
        eq_fg = 'white'
        c_fg = 'white'

        # --- Create and place buttons using gradients ---

        # Row 1
        self.create_gradient_button('(', lambda: self.show('('), 0, 50, btn_w_px, btn_h_px, func_grad, func_fg)
        self.create_gradient_button(')', lambda: self.show(')'), 90, 50, btn_w_px, btn_h_px, func_grad, func_fg)
        self.create_gradient_button('%', lambda: self.show('%'), 180, 50, btn_w_px, btn_h_px, func_grad, func_fg)
        self.create_gradient_button('/', lambda: self.show('/'), 270, 50, btn_w_px, btn_h_px, op_grad, op_fg)

        # Row 2
        self.create_gradient_button('1', lambda: self.show('1'), 0, 125, btn_w_px, btn_h_px, num_grad, num_fg)
        self.create_gradient_button('2', lambda: self.show('2'), 90, 125, btn_w_px, btn_h_px, num_grad, num_fg)
        self.create_gradient_button('3', lambda: self.show('3'), 180, 125, btn_w_px, btn_h_px, num_grad, num_fg)
        self.create_gradient_button('+', lambda: self.show('+'), 270, 125, btn_w_px, btn_h_px, op_grad, op_fg)

        # Row 3
        self.create_gradient_button('4', lambda: self.show('4'), 0, 200, btn_w_px, btn_h_px, num_grad, num_fg)
        self.create_gradient_button('5', lambda: self.show('5'), 90, 200, btn_w_px, btn_h_px, num_grad, num_fg)
        self.create_gradient_button('6', lambda: self.show('6'), 180, 200, btn_w_px, btn_h_px, num_grad, num_fg)
        self.create_gradient_button('-', lambda: self.show('-'), 270, 200, btn_w_px, btn_h_px, op_grad, op_fg)

        # Row 4
        self.create_gradient_button('7', lambda: self.show('7'), 0, 275, btn_w_px, btn_h_px, num_grad, num_fg)
        self.create_gradient_button('8', lambda: self.show('8'), 90, 275, btn_w_px, btn_h_px, num_grad, num_fg)
        self.create_gradient_button('9', lambda: self.show('9'), 180, 275, btn_w_px, btn_h_px, num_grad, num_fg)
        self.create_gradient_button('*', lambda: self.show('*'), 270, 275, btn_w_px, btn_h_px, op_grad, op_fg)

        # Row 5
        self.create_gradient_button('C', self.clear, 0, 350, btn_w_px, btn_h_px, c_grad, c_fg)
        self.create_gradient_button('0', lambda: self.show('0'), 90, 350, btn_w_px, btn_h_px, num_grad, num_fg)
        self.create_gradient_button('.', lambda: self.show('.'), 180, 350, btn_w_px, btn_h_px, num_grad, num_fg)
        self.create_gradient_button('=', self.solve, 270, 350, btn_w_px, btn_h_px, eq_grad, eq_fg)

    def create_gradient_button(self, text, command, x, y, w, h, grad_colors, fg_color):
        """Creates a tkinter Button with a gradient background."""

        # Create a PIL image
        pil_img = Image.new('RGB', (w, h), grad_colors[0])
        draw = ImageDraw.Draw(pil_img)

        # Get RGB values from hex
        c1 = ImageColor.getrgb(grad_colors[0])
        c2 = ImageColor.getrgb(grad_colors[1])

        # Draw vertical gradient
        for i in range(h):
            r = c1[0] + (c2[0] - c1[0]) * i // h
            g = c1[1] + (c2[1] - c1[1]) * i // h
            b = c1[2] + (c2[2] - c1[2]) * i // h
            draw.line((0, i, w, i), fill=(r, g, b))

        # Convert PIL image to PhotoImage
        photo = ImageTk.PhotoImage(pil_img)
        self.button_images.append(photo)  # IMPORTANT: Keep a reference!

        # Create the button using the image
        btn = Button(self.master, text=text, image=photo, command=command,
                     fg=fg_color, compound='center',
                     font=('Arial', 14, 'bold'),
                     relief='raised', bd=2,
                     borderwidth=0,  # Remove border to show image cleanly
                     highlightthickness=0)  # Remove highlight border

        # Set the size explicitly using width/height attributes (in pixels for image)
        btn.config(width=w, height=h)
        btn.place(x=x, y=y)

    def show(self, value):
        self.entry_value += str(value)
        self.equation.set(self.entry_value)

    def clear(self):
        self.entry_value = ''
        self.equation.set(self.entry_value)

    def solve(self):
        try:
            # Note: eval() can be insecure if used with untrusted input.
            # For a personal calculator, it's often acceptable.
            # You might need to add safety checks or a parser for production use.
            # Handle percentage if needed: self.entry_value = self.entry_value.replace('%', '/100')
            result = eval(self.entry_value)
            self.equation.set(result)
            self.entry_value = str(result)  # Keep result for next calculation
        except ZeroDivisionError:
            self.equation.set('Div by Zero')
            self.entry_value = ''
        except Exception as e:
            self.equation.set('Error')
            self.entry_value = ''


# Main part of the script
if __name__ == "__main__":
    root = Tk()
    app = Calculator(root)
    root.mainloop()