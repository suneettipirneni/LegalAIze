import os
import tkinter as tk
from tkinter import filedialog
from ml import generate_index, query_index

# Create a new tkinter window
window = tk.Tk()
window.title('LegalAIze Semantic Doc Finder')

# Create a label to display instructions to the user
label = tk.Label(text="Please select a folder or enter a folder path:")
label.pack()

# Create a text entry box for the user to enter a folder path
path_entry = tk.Entry(width=100)
path_entry.pack()

# Create a button to open a file dialog box for the user to select a folder
def select_folder():
    folder_path = filedialog.askdirectory()
    path_entry.delete(0, tk.END)
    path_entry.insert(0, folder_path)
button = tk.Button(text="Select Folder", command=select_folder)
button.pack()

label = tk.Label(text="", pady=5)
label.pack()

# Create a function to retrieve the selected folder path and search text
def get_folder_and_search_text():
    folder_path = path_entry.get()
    search_text = search_entry.get()
    return folder_path, search_text

# Create a function to update the listbox with a list of files in the selected folder
def update_listbox():
    folder_path = path_entry.get()
    search_text = search_entry.get()
    file_list = os.listdir(folder_path)
    if search_text:
        file_list = [filename for filename in file_list if search_text in filename]
    listbox.delete(0, tk.END)
    for filename in file_list:
        listbox.insert(tk.END, filename)

# Create a function to generate an index of files in the selected folder
def generate_index_func():
    # get folder path
    folder_path = path_entry.get()
    generate_index(folder_path)
    messages_label['text'] = 'Index generated successfully.'

def update_message():
    messages_label['text'] = 'Generating index...'

# Create a function to load an index of files in the selected folder
def load_index():
    folder_path = path_entry.get()
    if not os.path.exists(os.path.join(folder_path, 'index')):
        messages_label['text'] = 'Index not found, please generate an index first.'
    messages_label['text'] = 'Index loaded successfully.'

# Create a button to retrieve the folder path and search text, generate an index, update the listbox, and close the window
generate_button = tk.Button(text="Generate Index", command=lambda: [update_message(), generate_index_func()], pady=5)
generate_button.pack()

# Create a button to retrieve the folder path and search text, load an index, update the listbox, and close the window
load_button = tk.Button(text="Load Index", command=lambda: [load_index()], pady=5)
load_button.pack()

def on_click(event):
    # Get the selected item index from the listbox
    index = listbox.curselection()[0]
    # Get the text of the selected item
    item_text = listbox.get(index)
    # open file 
    os.startfile(item_text)

def search():
    # get search text
    search_text = search_entry.get()
    folder_path = path_entry.get()
    results = query_index(search_text, os.path.join(folder_path, 'index'))
    # update listbox
    listbox.delete(0, tk.END)
    for filename in results:
        listbox.insert(tk.END, filename)

label = tk.Label(text="", pady=10)
label.pack()

# Create a label and a text entry box for the user to enter search text
search_label = tk.Label(text="Enter search keywords", pady=10)
search_label.pack()
search_entry = tk.Entry(width=100)
search_entry.pack()


search_button = tk.Button(text="Search files", command=lambda: [search()])
search_button.pack()

label = tk.Label(text="", pady=10)
label.pack()


# Create a label to display the list of files
file_list_label = tk.Label(text="List of Files", pady=5)
file_list_label.pack()

# Create a listbox widget to display the list of files
listbox = tk.Listbox(width=100)
listbox.pack()
listbox.bind("<Button-1>", on_click)
# messages label
messages_label = tk.Label(text='')
messages_label.pack()

# Start the tkinter event loop
window.mainloop()
