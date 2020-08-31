import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox


text_contents = dict()


def create_file(content="", title='Untitled'):
    container = ttk.Frame(notebook)
    container.pack()
    text_area = tk.Text(notebook)
    text_area.insert("end", content)
    text_area.pack(side='left', fill='both', expand=True)
    notebook.add(text_area, text=title)
    notebook.select(text_area)
    text_contents[str(text_area)] = hash(content)


def save_file():
    filepath = filedialog.asksaveasfilename()
    try:
        filename = os.path.basename(filepath)
        text_widget = root.nametowidget(notebook.select())
        content = text_widget.get("1.0", "end-1c")
        with open(filepath, 'w') as file:
            file.write(content)
    except(AttributeError, FileNotFoundError):
        print('Save operation cancelled.')
        return
    notebook.tab("current", text=filename)
    text_contents[str(text_widget)] = hash(content)


def get_text_widget():
    text_widget = root.nametowidget(notebook.select())
    return text_widget


def check_for_changes():
    current = get_text_widget()
    content = current.get('1.0', 'end-1c')
    name = notebook.tab('current')['text']
    if hash(content) != text_contents[str(current)]:
        if name[-1] != '*':
            notebook.tab('current', text=name + '*')
    elif name[-1] == '*':
        notebook.tab('current', text=name[:-1])


def current_tab_unsaved():
    text_widget = get_text_widget()
    content = text_widget.get('1.0', 'end-1c')
    return hash(content) != text_contents[str(text_widget)]


def confirm_close():
    return messagebox.askyesno(message='You have unsaved changes. Are you sure you want to close?',
                               icon='question', title='Unsaved changes')


def close_current_tab():
    current = get_text_widget()
    if current_tab_unsaved() and not confirm_close():
        return
    if len(notebook.tabs()) == 1:
        create_file()
    notebook.forget(current)


def confirm_quit():
    unsaved = False
    for tab in notebook.tabs():
        text_widget = root.nametowidget(tab)
        content = text_widget.get('1.0', 'end-1c')
        if hash(content) != text_contents[str(text_widget)]:
            unsaved = True
            break
    if unsaved and not confirm_close():
        return
    root.destroy()


def open_file():
    file_path = filedialog.askopenfilename()
    try:
        filename = os.path.basename(file_path)
        with open(file_path, 'r') as file:
            content = file.read()
    except(AttributeError, FileNotFoundError):
        print('Save operation cancelled.')
        return
    create_file(content, filename)


def show_about_info():
    messagebox.showinfo(title='About', message='blabla')


root = tk.Tk()
root.title('Hello')
root.option_add('*tearOff', False)
main = ttk.Frame(root)
main.pack(padx=1, pady=(4, 0), expand=True, fill='both')
menubar = tk.Menu()
root.config(menu=menubar)
file_menu = tk.Menu(menubar)
help_menu = tk.Menu(menubar)
menubar.add_cascade(menu=file_menu, label='File')
menubar.add_cascade(menu=help_menu, label='Help')
file_menu.add_command(label='New', command=create_file, accelerator='Ctrl+N')
file_menu.add_command(label='Open...', command=open_file, accelerator='Ctrl+O')
file_menu.add_command(label='Save', command=save_file, accelerator='Ctrl+S')
file_menu.add_command(label='Close Tab', command=close_current_tab, accelerator='Ctrl+Q')
file_menu.add_command(label='Exit', command=confirm_quit)
help_menu.add_command(label='About', command=show_about_info)
notebook = ttk.Notebook(main)
notebook.pack(fill='both', expand=True)
create_file()
root.bind("<Control-n>", lambda event: create_file())
root.bind("<Control-o>", lambda event: open_file())
root.bind("<Control-s>", lambda event: save_file())
root.bind("<Control-q>", lambda event: close_current_tab())
get_text_widget()
root.mainloop()
