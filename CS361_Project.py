import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import tkinter.messagebox as messagebox
from PIL import Image, ImageTk


class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show)
        self.widget.bind("<Leave>", self.hide)

    def show(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 50
        y += self.widget.winfo_rooty() + 20
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        label = tk.Label(self.tooltip, text=self.text, background="#ffffe0", relief="solid", borderwidth=1,
                         wraplength=200)
        label.pack()

    def hide(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None


def continue_click():
    """To do"""
    pass


def browse_image(image_preview_label, custom_card_window):
    """Receives image label widget and opens select an image window"""
    image_path = filedialog.askopenfilename()
    if image_path:
        load_image_preview(image_path, image_preview_label)
        custom_card_window.focus_force()


def load_image_preview(image_path, image_preview_label):
    """Receives image path and label widget, resizes to make smaller"""
    img = Image.open(image_path)
    resize_image = img.resize((100, 100))
    img = ImageTk.PhotoImage(resize_image)
    image_preview_label.config(image=img)
    image_preview_label.image = img


def add_custom_card():
    """Opens a new window for adding a custom card to dictionary database"""

    def save_custom_card():
        """Saves custom cards to dictionary"""
        image_path = ''
        card_details = {}
        card_name = card_name_entry.get()
        categories = {}
        for i in range(len(category_entries)):
            categories[f"Category {i + 1}"] = category_entries[i].get()
        card_details[card_name] = {
            **categories,
            "Bonus": number_entry.get(),
            "Image": image_path
        }
        if not card_name_entry.get() or not number_entry.get() or not any(entry.get() for entry in category_entries):
            messagebox.showerror("Error", "Please fill out all required fields.")
        else:
            messagebox.showinfo("Confirmation", "Card Added to Wallet")
            custom_card_window.destroy()

    def add_category_entry():
        """Adds new category to the add custom card window"""
        row_index = len(category_entries) + 3
        category_label = tk.Label(custom_card_window, text=f"Category {row_index - 2}:")
        category_label.grid(row=row_index, column=0, padx=10, pady=5, sticky="e")
        category_entry = tk.Entry(custom_card_window)
        category_entry.grid(row=row_index, column=1, padx=10, pady=5, sticky="w")
        category_entries.append(category_entry)
        category_labels.append(category_label)
        bonus_label = tk.Label(custom_card_window, text="Bonus as %")
        bonus_label.grid(row=row_index, column=2, padx=10, pady=5, sticky="e")
        bonus_entry = tk.Entry(custom_card_window)
        bonus_entry.grid(row=row_index, column=3, padx=10, pady=5, sticky="w")
        number_entries.append(bonus_entry)
        add_category_button.grid(row=row_index + 1, column=0, columnspan=2, padx=10, pady=5)
        save_button.grid(row=len(category_entries) + 4, column=0, columnspan=4, padx=10, pady=10)

    custom_card_window = tk.Toplevel(master)
    custom_card_window.title("Add New Card")

    custom_card_window.grab_set()
    custom_card_window.lift()

    custom_card_window.columnconfigure(0, weight=1)
    custom_card_window.columnconfigure(1, weight=1)
    custom_card_window.columnconfigure(2, weight=1)
    custom_card_window.columnconfigure(3, weight=1)
    custom_card_window.rowconfigure(1, weight=1)

    card_name_label = tk.Label(custom_card_window, text="Card Name:")
    card_name_label.grid(row=0, column=0, padx=10, pady=5)
    card_name_entry = tk.Entry(custom_card_window)
    card_name_entry.grid(row=0, column=1, padx=10, pady=5)

    upload_frame = tk.Frame(custom_card_window)
    upload_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=5, sticky="we")
    image_label = tk.Label(upload_frame, text="Upload Image (Optional):")
    image_label.grid(row=0, column=0, padx=(0, 5), pady=5, sticky="e")
    browse_button = tk.Button(upload_frame, text="Browse", command=lambda: browse_image(image_preview_label,
                                                                                        custom_card_window))
    browse_button.grid(row=0, column=1, padx=(5, 0), pady=5, sticky="w")

    image_frame = tk.Frame(custom_card_window, bd=2, relief="solid")
    image_frame.grid(row=1, rowspan=2, column=2, columnspan=3, padx=5, pady=5, sticky="w")
    image_preview_label = tk.Label(image_frame)
    image_preview_label.grid(row=0, column=0, padx=10, pady=10)

    category1_label = tk.Label(custom_card_window, text="Category 1:")
    category1_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")
    category1_entry = tk.Entry(custom_card_window)
    category1_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

    category_entries = [category1_entry]
    category_labels = [category1_label]
    number_entries = []

    number_label = tk.Label(custom_card_window, text="Bonus as %")
    number_label.grid(row=3, column=2, padx=10, pady=5, sticky="e")
    number_entry = tk.Entry(custom_card_window)
    number_entry.grid(row=3, column=3, padx=10, pady=5, sticky="w")
    number_entries.append(number_entry)

    add_category_button = tk.Button(custom_card_window, text="Add Category", command=add_category_entry)
    add_category_button.grid(row=4, column=0, columnspan=2, padx=10, pady=5)
    save_button = tk.Button(custom_card_window, text="Save", command=save_custom_card)
    save_button.grid(row=5, column=0, columnspan=4, padx=10, pady=10)

    Tooltip(add_category_button,
            "Click to add new category. Add as many bonus categories as your card has, but at least \"Other\" is "
            "required")
    custom_card_window.mainloop()


def toggle_checkbox(checkbutton):
    """Toggles the state of the checkbox"""
    checkbutton.set(not checkbutton.get())


master = tk.Tk()
master.title("Credit Card Optimizer")

main_logo = tk.PhotoImage(file='icons/main logo.png')
master.iconphoto(True, main_logo)

master.columnconfigure(0, weight=1)  # Checkboxes and cards
master.columnconfigure(1, weight=1)  # Continue button
master.rowconfigure(0, weight=1)  # Instructions row
master.rowconfigure(1, weight=3)  # Checkboxes and cards row
master.rowconfigure(2, weight=1)  # Add custom card button row
master.rowconfigure(3, weight=1)  # Continue button row

instructions_label = tk.Label(master, text="Select credit cards below to add to wallet or add your own custom card",
                              font=("Arial", 12),
                              bg="#82b1ff", fg="black", padx=10, pady=5, borderwidth=2, relief="solid")
instructions_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="n")

frame = tk.Frame(master)
frame.grid(row=1, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="nsew")

chk_var_1 = tk.BooleanVar(value=False)
chk_var_2 = tk.BooleanVar(value=False)

chk_1 = ttk.Checkbutton(frame, variable=chk_var_1)
chk_2 = ttk.Checkbutton(frame, variable=chk_var_2)

chk_1.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="e")
chk_2.grid(row=1, column=0, padx=(10, 5), pady=10, sticky="e")

card_img_1 = tk.PhotoImage(file='cards/sapphire_preferred_card.png')
card_img_2 = tk.PhotoImage(file='cards/freedom_unlimited_card.png')

card_1 = tk.Label(frame, image=card_img_1, borderwidth=2)
card_2 = tk.Label(frame, image=card_img_2, borderwidth=2)

card_1.grid(row=0, column=1, padx=(5, 10), pady=10, sticky="w")
card_2.grid(row=1, column=1, padx=(5, 10), pady=10, sticky="w")

card_1.bind("<Button-1>", lambda event: toggle_checkbox(chk_var_1))
card_2.bind("<Button-1>", lambda event: toggle_checkbox(chk_var_2))

btn_add_custom_card = tk.Button(master, text="Add Your Own Card Here", command=add_custom_card, bg="#e0e0e0", bd=2,
                                relief="solid")
btn_add_custom_card.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="n")

Tooltip(btn_add_custom_card, "Add any cards not shown here to be added to your wallet. Include all cards for best,"
                             " results.")
#  btn_continue = tk.Button(master, text="Continue", command=continue_click, bg="#8BC34A",
#                         width=20, height=3)
#  btn_continue.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="n")

master.minsize(600, 400)

master.mainloop()
