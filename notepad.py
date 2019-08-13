import tkinter as tk
from tkinter.filedialog import *
import tkinter.font as tkFont 
from tkinter.messagebox import * 
import os as sys

window = tk.Tk()
window.geometry("800x400")

window.title("   NotePy   ")

menu_bar = tk.Menu(window)

txt_frame = tk.Frame( window , bg = "#000000" )
 
my_font = tkFont.Font( family =  "fira code" , size =  18 )

txt = tk.Text(txt_frame , undo=True , font = my_font  , wrap = "word" )

scroll_bar = tk.Scrollbar( txt_frame , bg = "#000000" , width = 20 , jump = True , highlightcolor = "#ffffff" )
scroll_bar.pack( side = "right" , anchor = "e", fill = "y"  )
txt.configure( yscrollcommand = scroll_bar.set )
scroll_bar.configure( command = txt.yview )


class editor :
    def cut():
        txt.event_generate("<<Cut>>")

    def copy():
        txt.event_generate("<<Copy>>")

    def paste():
        txt.event_generate("<<Paste>>")

    def undo():
        txt.event_generate("<<Undo>>")

    def redo():
        txt.event_generate("<<Redo>>")
    

file_types = (("Python files", "*.py"), ("All files ", "*.* "))

class File_Operation :

    def __init__( self ):
        self.file_path = None  

    def update_title( self ) :
        window.title( self.file_path + "    - Notepad")
    
    def open( self ):
        try :
            self.file_path = askopenfilename( filetypes = file_types )
            x = open( self.file_path , "r")
            txt.delete( 1.0 , END )
            txt.insert( 1.0 , x.read( ) )
            x.close()
            self.update_title()
            
        except FileNotFoundError:
            showerror("File Not Found", " the File does not exist ")


    
    def saveAs(self):
        try :
            self.file_path = asksaveasfilename( filetypes = file_types  )
            self.save()
        except FileNotFoundError :
            showerror( "File Not Found" , " the File does not exist ")

    
    def new(self):
        save_bool =   askyesno( "Close file" , " Do you want to save any unsaved changes ? ")
        if save_bool : 
            self.save()

        txt.delete( 1.0 , END )
        self.file_path = None 
        self.update_title()



    def save(self):
        try  : 
            x = open(self.file_path , "w")
            x.write(txt.get(1.0, END))
            x.close()
            self.update_title()
        except FileExistsError :
            showwarning("File Not Found" , " The file specified was not found ")
            self.saveAs() 

        except TypeError :
            showinfo( "File not saved" , " Please create a file then save it !" )
            self.saveAs()
            
    def run(self):
        self.save() 
        sys.system("py " + self.file_path)


file_operation = File_Operation() 



file_menu = tk.Menu(menu_bar, tearoff=False )


file_menu.add_command(label=" Open ", command=file_operation.open)
file_menu.add_command(label=" New ",  command=file_operation.new)
file_menu.add_command(label=" Save ",  command=file_operation.save)
file_menu.add_command(label=" Save as ", command=file_operation.saveAs)


file_menu.add_separator()

file_menu.add_command(label=" Exit ", command=window.destroy)

menu_bar.add_cascade(label=" File ", menu=file_menu)

edit_menu = tk.Menu(menu_bar, tearoff=False)

edit_menu.add_command(label=" Undo ",  command=editor.undo)
edit_menu.add_command(label=" Redo ",  command=editor.redo)
edit_menu.add_command(label=" Copy ",  command=editor.copy)
edit_menu.add_command(label=" Paste ", command=editor.paste)

menu_bar.add_cascade(label=" Edit", menu=edit_menu)

help_menu = tk.Menu(menu_bar, tearoff=False)
def help_on_app():
    showinfo( title= " Help " , message = " This is a simple notepad \n This notepad was created using the tkinter library in python \n \n  created by Gopal Kataria \n version 1.0 ( released on 13 Aug 2019 ) ")
help_menu.add_command(label=" Help on this app  " , command = help_on_app )

menu_bar.add_cascade(label=" Help ", menu=help_menu)

ribbon_frame = tk.Frame(window)
buttons = [ ]

btn_font = tkFont.Font( family = "helvetica" , size  = 10 )



def add_btn_ribbon( name , cmd  ):
    
    buttons.append( tk.Button( ribbon_frame , text = name, command = cmd  , relief = "groove"  , font = btn_font ,  ))
    buttons[-1].pack( padx = 4 , pady = 4 , ipadx = 2 , ipady = 2 , side = "left"  )
 
empty_labels = []
def blank_label( content = "" ):
    empty_labels.append( tk.Label( ribbon_frame  , text = content , font = btn_font ))
    empty_labels[-1].pack( side="left" , anchor = "w")

add_btn_ribbon("  New  ", file_operation.new)
add_btn_ribbon("  Save  ", file_operation.save)
add_btn_ribbon("  Open  ", file_operation.open )

blank_label("Font Size")

def change_font_size(event):
    try :
        size = int(font_change.get() )
        my_font.config( size = size )
    except ValueError  :
        font_change.delete( 0 , 100 )
        font_change.insert( 0,  my_font.cget( "size" ))
    
    

font_change = tk.Entry( ribbon_frame , relief = "ridge" , width = 4    )
font_change.insert( 0 , "18")
font_change.pack(padx=4, pady=4, ipadx=2, ipady=2, side="left")


window.bind( "<Return>" , change_font_size )

blank_label()
add_btn_ribbon( "  Run  " , file_operation.run )
add_btn_ribbon( "  Copy  " , editor.copy ) 
add_btn_ribbon("  Paste  " , editor.paste )
add_btn_ribbon( "  Cut  " , editor.cut)
add_btn_ribbon( "  Undo  " , editor.undo )
add_btn_ribbon("  Redo  " , editor.redo )


ribbon_frame.pack(side="top", anchor="e", padx=4, pady=2 , fill = "x" )

info_frame = Label( txt_frame , height = 1 , text = " NOTE : Editor will stop working while the script is executing ") 
info_frame.pack( side = "bottom" , anchor = "s" , fill = "x" , ipady = 1 )

txt.pack(side="right", ipadx=4, ipady=4, anchor="e" , fill = "both" , expand = True  )


txt_frame.pack( side="left" , expand = True , fill = "both" )

window.protocol("WM_DELETE_WINDOW" , exit)

def exit():
    if askyesno( "Quit" , " do you want to save any changes ?") :
        file_operation.save()
        window.destroy()
    else :
        window.destroy()

window.config(menu=menu_bar )
if __name__ == "__main__":
    window.mainloop()
    

print(" Text editor exited ")
