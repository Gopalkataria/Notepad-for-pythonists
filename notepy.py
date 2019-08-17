import tkinter as tk
from tkinter.filedialog import *
import tkinter.font as tkFont
from tkinter.messagebox import *
import os 
import threading


class Editor:

    """ class for doing file opertaions with tk.Text objects """

    def __init__( self, text ):
        self.text  =  text

    def cut( self ):
        self.text.event_generate( "<<Cut>>" )

    def copy( self ):
        self.text.event_generate( "<<Copy>>" )

    def paste( self ):
        self.text.event_generate( "<<Paste>>" )

    def undo( self ):
        self.text.event_generate( "<<Undo>>" )

    def redo( self ):
        self.text.event_generate( "<<Redo>>" )


class File_Operation:

    """ Can be used to do certain file operations requires window (  tk.Tk object  ) and text (  tk.Text object  ) """

    file_types  =  ( ( "Python files", "*.py" ), ( "All files ", "*.* " ) )

    def __init__( self, window, text ):
        self.file_path  =  None
        self.window  =  window
        self.text  =  text

    def update_title( self ):
        self.window.title( str( self.file_path ) + "    - Notepad" )

    def open( self ):
        try:
            self.file_path  =  askopenfilename( filetypes = self.file_types )
            x  =  open( self.file_path, "r" )
            self.text.delete( 1.0, END )
            self.text.insert( 1.0, x.read(  ) )
            x.close(  )
            self.update_title(  )

        except FileNotFoundError:
            showerror( "File Not Found", " the File does not exist " )

    def saveAs( self ):
        try:
            self.file_path  =  asksaveasfilename( filetypes = self.file_types )
            self.save(  )
        except FileNotFoundError:
            showerror( "File Not Found", " the File does not exist " )

    def new( self ):
        save_bool  =  askyesno( 
            "Close file", " Do you want to save any unsaved changes ? " )
        if save_bool:
            self.save(  )

        self.text.delete( 1.0, END )
        self.file_path  =  None
        self.update_title(  )

    def save( self ):
        try:
            x  =  open( self.file_path, "w" )
            x.write( self.text.get( 1.0, END ) )
            x.close(  )
            self.update_title(  )
        except FileExistsError:
            showwarning( "File Not Found", " The file specified was not found " )
            self.saveAs(  )

        except TypeError:
            showinfo( "File not saved", " Please create a file then save it !" )
            self.saveAs(  )

    def run( self , event = None ):
        self.save(  )
        self.run_thread = Run_file_thread( self.file_path )
        self.run_thread.start()

    def help_on_app(  ):
        showinfo( title = " Help ", message = " This is a simple notepad \n This notepad was created using the tkinter library in python \n \n  created by Gopal Kataria \n version 1.0 (  released on 13 Aug 2019  ) " )


class Run_file_thread( threading.Thread ):
    def __init__(self, file_path  ):
        threading.Thread.__init__(self)
        self.file_path = file_path 
    
    def run(self):
        os.system( "py " + self.file_path )



class Main_window :

    """ the main window of notepy  """

    def __init__( self ):

        self.window  =  tk.Tk(  )

        self.window.geometry( "800x400" )

        self.window.title( "   NotePy   " )

        self.make_text_frame(  )

        self.editor  =  Editor( self.text )

        self.file_operation  =  File_Operation( self.window, self.text )

        self.make_menu_bar()

        self.make_a_ribbon()

        self.packup()
        

    def make_text_frame( self ):

        self.my_font  =  tkFont.Font( family = "fira code", size = 18 )
        self.text_frame  =  tk.Frame( self.window, bg = "#000000" )

        self.text  =  tk.Text( self.text_frame, undo = True,
                            font = self.my_font, wrap = "word" )

        self.scroll_bar  =  tk.Scrollbar( self.text_frame, bg = "#000000",
                                       width = 20, jump = True, highlightcolor = "#ffffff" )

        self.scroll_bar.pack( side = "right", anchor = "e", fill = "y" )

        self.text.configure( yscrollcommand = self.scroll_bar.set )

        self.scroll_bar.configure( command = self.text.yview )

        self.text.pack( side = "right", ipadx = 4, ipady = 4,
                       anchor = "e", fill = "both", expand = True )


    def make_menu_bar( self ):

        self.menu_bar  =  tk.Menu( self.window )

        self.file_menu  =  tk.Menu(  self.menu_bar, tearoff = False )


        self.file_menu.add_command( label = " Open ", command = self.file_operation.open   )
        self.file_menu.add_command( label = " New ",  command = self.file_operation.new   )
        self.file_menu.add_command( label = " Save ",  command = self.file_operation.save   )
        self.file_menu.add_command( label = " Save as ", command = self.file_operation.saveAs   )


        self.file_menu.add_separator(  )

        self.file_menu.add_command( label = " Exit ", command = self.window.destroy )

        self.menu_bar.add_cascade( label = " File ", menu = self.file_menu )

        self.edit_menu  =  tk.Menu( self.menu_bar, tearoff = False )

        self.edit_menu.add_command( label = " Undo ",  command = self.editor.undo )
        self.edit_menu.add_command( label = " Redo ",  command = self.editor.redo )
        self.edit_menu.add_command( label = " Cut " , command  =  self.editor.cut )
        self.edit_menu.add_command( label = " Copy ",  command = self.editor.copy )
        self.edit_menu.add_command( label = " Paste ", command = self.editor.paste )

        self.menu_bar.add_cascade( label = " Edit", menu = self.edit_menu )

        self.help_menu  =  tk.Menu( self.menu_bar, tearoff = False )


        self.help_menu.add_command( label = " Help on this app  ", command = self.file_operation.help_on_app  )

        self.menu_bar.add_cascade( label = " Help ", menu = self.help_menu )

        self.run_menu = tk.Menu( self.menu_bar , tearoff = False )

        self.run_menu.add_command( label=" Run", command=self.file_operation.run)

        self.run_menu.add_command(  label=" Help on run ", command=self.help_on_run )

        self.menu_bar.add_cascade( label = "Run" , menu = self.run_menu )

        
        self.window.config( menu = self.menu_bar )

        
    def help_on_run(self):
        showinfo("Run Option " , " You can run your python code from Run menu or by pressing the f5 key, please note that you can't stop the code from running in the editor ")

    def add_btn_ribbon(self , name, cmd):

        self.buttons.append(tk.Button(self.ribbon_frame, text=name,
                                        command=cmd, relief="groove", font=self.btn_font,))
        self.buttons[-1].pack(padx=4, pady=4, ipadx=2,
                                ipady=2, side="left")

    def make_a_ribbon(self):


        self.ribbon_frame = tk.Frame(self.window)

        self.btn_font = tkFont.Font(family="helvetica", size=10)

        self.buttons = []

        self.empty_labels = []

        self.btns_dict = { "Open" : self.file_operation.open ,  "New" : self.file_operation.new , "Save" : self.file_operation.save , "Run" : self.file_operation.run }

      
        
        for name , func in self.btns_dict.items() :
            self.add_btn_ribbon( name , func )

        self.blank_label("Font Size")



        self.font_change = tk.Entry(self.ribbon_frame, relief="ridge", width=4)
        self.font_change.insert(0, "18")
        self.font_change.pack(padx=4, pady=4, ipadx=2, ipady=2, side="left")


        self.window.bind("<Return>", self.change_font_size_event  )
        self.window.bind("<F5>" , self.file_operation.run )

        self.blank_label()

        

    def blank_label(self , content=""):
            self.empty_labels.append(
                tk.Label(self.ribbon_frame, text=content, font=self.btn_font))
            self.empty_labels[-1].pack(side="left", anchor="w")


    def change_font_size_event(self, event):
        try:
            size = int(self.font_change.get())
            self.my_font.config(size=size)
        except ValueError:
            self.font_change.delete(0, 100)
            self.font_change.insert(0,  self.my_font.cget("size"))
            
    def start(self) :
        self.window.mainloop()
    
    def stop(self):
        self.window.destroy()

    def packup(self):
        ## every frame is gonna be packed over here in ORDER 

        self.ribbon_frame.pack(side="top", anchor="e",
                               padx=4, pady=2, fill="x")

        self.text_frame.pack(side="left", expand=True, fill="both")


message = """ NotePy \n A better text editor for Python \n your code will run here \n\n  """

x = Main_window()
print("welcome to the notepy editor. \nthis isn't an interactive shell but just a place where your script\n will run. ")
print("*You must not close this window ")
x.start()
