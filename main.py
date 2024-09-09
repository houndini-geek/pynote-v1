from tkinter import * 
from tkinter import filedialog
from tkinter import messagebox
import pyperclip as clb
import os



window = Tk()
window.title("Pynote");
# Set minimum window size (width, height)
window.minsize(400, 300)
# Set maximum window size (width, height)
window.maxsize(800, 600)


current_file =  None
selected_text = ''

def openFile():
    # Open a file dialog, restricting it to only .txt files
    global current_file;
    current_file = filedialog.askopenfilename(
        title="Open file",
        initialdir='',
        filetypes=[("Text files", "*.txt")]  # Restrict to .txt files
    )
    if current_file:
        #print(file)
        # Open the file and read its content
        with open(current_file, 'r') as f:
            content = f.read()
        
        # Clear the textarea and insert the content of the file
        textarea.delete(1.0, 'end')
        textarea.insert('end', content)


def saveFileAs():
    file = filedialog.asksaveasfile(
        title="Save file",
        defaultextension='.txt',
        filetypes=[
            ("Text documents (*.txt)",".txt")
        ]
    );
    if file: 
        textValue = str(textarea.get(1.0,END))
        file.write(textValue)
        file.close()



def saveFile():
    global current_file;
    if current_file:
        # Save updates to the opened file without asking for a file name
        with open(current_file,'w') as f: #Write mode to overwrite the file
            f.write(str(textarea.get(1.0,END)))
            
    else:
        saveFileAs()

def cutText():
    try:
        # Check if there is any selected text
        if textarea.tag_ranges("sel"):
            # Get the selected text
            selected_text = textarea.get("sel.first", "sel.last")

            # Clear the clipboard
            window.clipboard_clear()

            # Append the selected text to the clipboard
            window.clipboard_append(selected_text)

            # Delete the selected text from the Text widget
            textarea.delete("sel.first", "sel.last")
        else:
            print("No text selected to cut.")
    except:
        print("Error while cutting text.")



def copyText():
    try:
        global selected_text;
        # Check if there is any selected text
        if textarea.tag_ranges("sel"):
            # Get the selected text
            selected_text = textarea.get("sel.first", "sel.last")
            
            # Clear the clipboard
            window.clipboard_clear()

            # Append the selected text to the clipboard
            window.clipboard_append(selected_text)
        else:
            print("No text selected")
    except:
        print("Error while copying text.")


def pasteText():
    try:

        # Get the content from the clipboard
        clipboard_content = window.clipboard_get()

        # Check if there is a selected text
        if textarea.tag_ranges("sel"):
            # If text is selected, replace it with clipboard content
            textarea.delete("sel.first", "sel.last")
            textarea.insert("insert", clipboard_content)
        else:
            # If no text is selected, paste at the current cursor position
            textarea.insert("insert", clipboard_content)
    except:
        print("No text available to paste from clipboard.")

def undoText():
    try:
        textarea.edit_undo() # Perform undo
    except:
        print("Nothing to undo")

def redoText():
    try:
        textarea.edit_redo() # Perform redo
    except:
        print('Nothing to redo')


def deleteText():
    if textarea.selection_get():
        textarea.delete('sel.first','sel.last')


def openNewWindow(): 
    newWin = Toplevel(window)
    newWin.title("Pynote");
# Set minimum window size (width, height)
    newWin.minsize(400, 300)
# Set maximum window size (width, height)
    newWin.maxsize(800, 600)
    

# Create a Scrollbar widget
    scrollbar = Scrollbar(window)

# Create a Text widget with the yscrollcommand linked to the scrollbar
    textarea = Text(window, wrap='none', yscrollcommand=scrollbar.set, undo=True)
    textarea.config(width=70, height=40, font=("Consolas", 10), padx=5, pady=5)
    textarea.pack(side='left', fill=BOTH, expand=True)

# Configure the scrollbar
    scrollbar.pack(side=RIGHT, fill=Y)  # Attach the scrollbar to the right side of the window

    scrollbar.config(command=textarea.yview)  # Link scrollbar to the Text widget

# # Create a horizontal scrollbar
# h_scrollbar = Scrollbar(window, orient='horizontal')

# # Link the horizontal scrollbar to the Text widget
# textarea.config(xscrollcommand=h_scrollbar.set)

# # Configure and place the horizontal scrollbar
# h_scrollbar.pack(side='bottom', fill='x')
# h_scrollbar.config(command=textarea.xview)

    menubar = Menu(window);
    window.config(menu=menubar);


    fileMenu = Menu(menubar, tearoff=0);
    menubar.add_cascade(label="File",menu=fileMenu);
    fileMenu.add_command(label="New window", command=openNewWindow);
    fileMenu.add_command(label="Open...", command=openFile);
    fileMenu.add_command(label="Save",command=saveFile);
    fileMenu.add_command(label="Save as...",command=saveFileAs);
    fileMenu.add_separator();
    fileMenu.add_command(label="Exit", command=closeWindow)

    editMenu = Menu(menubar,tearoff=0);
    menubar.add_cascade(label="Edit",menu=editMenu);
    editMenu.add_cascade(label="Cut",command=cutText)
    editMenu.add_cascade(label="Copy",command=copyText)
    editMenu.add_cascade(label="Paste",command=pasteText)
    editMenu.add_cascade(label="Undo",command=undoText);
    editMenu.add_cascade(label="Redo",command=redoText);
    editMenu.add_separator()
    editMenu.add_cascade(label="Delete",command=deleteText)



def closeWindow():
    global current_file  # This allows you to check and possibly modify the global variable

    # Check if the current file exists
    if not os.path.exists(str(current_file)):  # If the file doesn't exist
        answer = messagebox.askyesno(title="Unsaved Note", message="Note not saved. Do you want to save it?")
        
        if answer:  # If the user chooses "Yes" to save the file
            saveFileAs()  # Call the save function (assuming it saves the current file)
        else:
            window.quit()  # Close the application
    else:
        window.quit()  # Close the application if the file already exists





# Create a Scrollbar widget
scrollbar = Scrollbar(window)

# Create a Text widget with the yscrollcommand linked to the scrollbar
textarea = Text(window, wrap='none', yscrollcommand=scrollbar.set, undo=True)
textarea.config(width=70, height=40, font=("Consolas", 10), padx=5, pady=5)
textarea.pack(side='left', fill=BOTH, expand=True)

# Configure the scrollbar
scrollbar.pack(side=RIGHT, fill=Y)  # Attach the scrollbar to the right side of the window

scrollbar.config(command=textarea.yview)  # Link scrollbar to the Text widget

# # Create a horizontal scrollbar
# h_scrollbar = Scrollbar(window, orient='horizontal')

# # Link the horizontal scrollbar to the Text widget
# textarea.config(xscrollcommand=h_scrollbar.set)

# # Configure and place the horizontal scrollbar
# h_scrollbar.pack(side='bottom', fill='x')
# h_scrollbar.config(command=textarea.xview)

menubar = Menu(window);
window.config(menu=menubar);


fileMenu = Menu(menubar, tearoff=0);
menubar.add_cascade(label="File",menu=fileMenu);
fileMenu.add_command(label="New window", command=openNewWindow);
fileMenu.add_command(label="Open...", command=openFile);
fileMenu.add_command(label="Save",command=saveFile);
fileMenu.add_command(label="Save as...",command=saveFileAs);
fileMenu.add_separator();
fileMenu.add_command(label="Exit", command=closeWindow)

editMenu = Menu(menubar,tearoff=0);
menubar.add_cascade(label="Edit",menu=editMenu);
editMenu.add_cascade(label="Cut",command=cutText)
editMenu.add_cascade(label="Copy",command=copyText)
editMenu.add_cascade(label="Paste",command=pasteText)
editMenu.add_cascade(label="Undo",command=undoText);
editMenu.add_cascade(label="Redo",command=redoText);
editMenu.add_separator()
editMenu.add_cascade(label="Delete",command=deleteText)

window.mainloop()
