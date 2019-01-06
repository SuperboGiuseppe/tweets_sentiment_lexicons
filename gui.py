from tkinter import *
from tkinter import ttk
from PyQt4 import QtGui
import mongodb_functions as mdb
import io

"""
Giuseppe Superbo


Step 14 Design a simple GUI that allows you to demonstrate your key findings and run a small Demo
"""
def center_window(toplevel):
    """
    This procedure center the main window at the center of the screen by taking the screen resolution values from the system
    thanks to PyQt4
    :param toplevel:
    """
    toplevel.update_idletasks()
    app = QtGui.QApplication([])
    screen_width = app.desktop().screenGeometry().width()
    screen_height = app.desktop().screenGeometry().height()

    size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
    x = screen_width/2 - size[0]/2
    y = screen_height/2 - size[1]/2

    toplevel.geometry("+%d+%d" % (x, y))

def splash_screen():
    """
    This procedure spawn a splash screen before the main window is loaded
    """
    screen = Tk()
    splash_image = PhotoImage(file = "images/splashscreen.png")
    main_label = Label(screen, image=splash_image)
    screen.overrideredirect(1)
    main_label.pack()
    center_window(screen)
    screen.after(6000, lambda: screen.destroy())
    screen.mainloop()


def _convert65536(to_convert):
    """Converts a string with out-of-range characters in it into a
    string with codes in it.

    Based on <https://stackoverflow.com/a/28076205/4865723>.
    This is a workaround because Tkinter (Tcl) doesn't allow unicode
    characters outside of a specific range. This could be emoticons
    for example.
    """
    for character in to_convert[:]:
        if ord(character) > 65535:
            convert_with = '{' + str(ord(character)) + 'ū}'
            to_convert = to_convert.replace(character, convert_with)
    return to_convert

def extract_db(choice):
    """
    This procedure extract data from a specific collection of the DB and returns it in a buffer
    :param choice: collection to be extracted
    :return: buffer: data extracted from the collection
    """
    collection = mdb.open_collection(choice, 'tweets')
    cursor = collection.find({}, {"user":0})
    buffer = io.StringIO()

    for document in cursor:
        for key in document:
            #print(key)
            #print(document[key])
            temp = str(document[key])
            temp2 = _convert65536(temp)
            print(key, ":", temp2, file = buffer)
        print("\n\n", file = buffer)
        print("\n\n")
    return buffer

def main_window():
    """
    This procedure spawns, as soon after the splash screen, the main window where all the demo occures.
    It is composed by a main frame and a tab section where the user can choose which part of the project want
    to view.
    """
    def canvas_tab(event):
        """
        This procedure controls the tab sections in order to give a specific functionality to each tab.
        :param event: Event contains the coordinates of each tab
        """
        frame.canvas.delete("all")
        clicked_tab = tabControl.tk.call(tabControl._w, "identify", "tab", event.x, event.y)
        if(clicked_tab == 0):
            text_screen(0)
        if (clicked_tab == 1):
            text_screen(1)
        if (clicked_tab == 2):
            frame.language_image = PhotoImage(file = 'plots/tweets_per_language.png')
            frame.canvas.create_image(400, 325, image = frame.language_image, anchor=CENTER)
            frame.canvas.update()
        if (clicked_tab == 3):
            frame.language_image = PhotoImage(file='plots/distribution_of_words.png')
            frame.canvas.create_image(400, 325, image=frame.language_image, anchor=CENTER)
            frame.canvas.update()
        if (clicked_tab == 4):
            frame.language_image = PhotoImage(file='plots/textblob_plot.png')
            frame.canvas.create_image(400, 325, image=frame.language_image, anchor=CENTER)
            frame.canvas.update()


    def text_screen(tab):
        """
        This procedure spawn all the widgets to visualize correctly the text results of the project.
        A text area is spawned to print all the data. A scroolbar is spawned to scroll the text area.
        And finally a language selector is spawned in order to navigate between the collections.
        :param tab: Flag selector of each tab
        """
        def OptionMenu_Changed(event):
            language = dropmenu.get()
            if (language == "English" and tab == 0):
                update_textarea("tweets_en")
            if (language == "English" and tab == 1):
                update_textarea("tfidf_en")
            if (language == "Swedish" and tab == 0):
                update_textarea("tweets_sv")
            if (language == "Swedish" and tab == 1):
                update_textarea("tfidf_sv")
            if (language == "Finnish" and tab == 0):
                update_textarea("tweets_fi")
            if (language == "Finnish" and tab == 1):
                update_textarea("tfidf_fi")
            if (language == "Norwegian" and tab == 0):
                update_textarea("tweets_no")
            if (language == "Norwegian" and tab == 1):
                update_textarea("tfidf_no")
            if (language == "Danish" and tab == 0):
                update_textarea("tweets_da")
            if (language == "Danish" and tab == 1):
                update_textarea("tfidf_da")

        def update_textarea(collection):
            """
            This procedure loads a new set of data in the text area of the main window
            :param collection: The collection that is going to be printed in the text area
            """
            text.configure(state='normal')
            text.delete(1.0,END)
            buffer = extract_db(collection)
            text.insert('end', str(buffer.getvalue()))
            text.configure(state='disabled')

        dropmenu = StringVar(frame)
        dropmenu.set("English")
        text_frame = Frame(frame.canvas)
        options = OptionMenu(text_frame, dropmenu, "English", "Swedish", "Finnish", "Norwegian", "Danish", command=OptionMenu_Changed)
        text = Text(text_frame, state='disabled', width=130, height=36)
        if(tab==0):
            update_textarea("tweets_en")
        else:
            update_textarea("tfidf_en")
        scrollbarY = Scrollbar(text_frame, command=text.yview, orient="vertical")
        text.grid(row=1,column=0, sticky=N+W+E+S)
        scrollbarY.grid(row=1, column=1, sticky=N+S)
        #scrollbarY.pack(fill=Y, expand=True, side=RIGHT)
        #text.pack(fill=BOTH, expand=True, side=LEFT)
        options.grid(row=0, column=0)
        frame.canvas.create_window((0,0), window = text_frame , anchor = "nw")
        text_frame.grid_rowconfigure(0, weight=1)
        text_frame.grid_columnconfigure(0, weight=1)
        text.configure(xscrollcommand=scrollbarY.set)
        frame.canvas.pack()

    main = Tk()
    main.title("Sentiment Analysis of multi-lingual tweets using sentiment lexicons")
    main.minsize(1080, 700)
    main.resizable(width=False, height=False)
    tabControl = ttk.Notebook(main)
    tab1 = ttk.Frame(tabControl)
    tab2 = ttk.Frame(tabControl)
    tab3 = ttk.Frame(tabControl)
    tab4 = ttk.Frame(tabControl)
    tab5 = ttk.Frame(tabControl)
    tabControl.add(tab1, text = "TweetsDB")
    tabControl.bind("<Button-1>", canvas_tab)
    tabControl.add(tab2, text = "TF-IDF Matrix")
    tabControl.add(tab3, text = "Language distribution")
    tabControl.add(tab4, text = "Words distribution")
    tabControl.add(tab5, text = "TextBlob results")
    tabControl.grid(row = 0)
    tabControl.pack(side = TOP , anchor = NW)
    frame = Frame(main)
    frame.canvas = Canvas(main, width=900, height=650)
    text_screen(0)
    frame.canvas.pack(fill=BOTH, padx=10)
    main.mainloop()

def gui():
    splash_screen()
    main_window()

if __name__ == '__main__':
    gui()

