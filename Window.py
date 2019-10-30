from tkinter.filedialog import *
from tkinter.scrolledtext import *
import Parser

class Application(Frame):

    def __init__(self, master=None):
        super(Application, self).__init__()
        master.title("UeCapabilityInformation Parser")
        master.resizable(width=TRUE, height=TRUE)

        #display screen centered
        master.update_idletasks()
        width = 1170
        height = 510
        x = self.calcX(master,width)
        y = self.calcY(master,height)
        master.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        master.deiconify()

        #Add menu
        master.option_add('tearOff',FALSE)
        self.frame = Frame(master, width=1170, height=510, pady=3, relief="groove", border=2)
        self.frame.pack()
        self.statusFrame = Frame(self.frame , width=338, height=200)
        self.statusFrame.pack()
        self.menu = Menu(master)
        self.fileMenu = Menu(self.menu, tearoff=0)
        self.fileMenu.add_command(label="Open", command=self.loadFile)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Exit",command=self.quitProgram)
        self.menu.add_cascade(label="File", menu=self.fileMenu)
        self.aboutMenu = Menu(self.menu, tearoff=0)
        self.aboutMenu.add_command(label="About...", command=self.loadAbout)
        self.menu.add_cascade(label="About", menu=self.aboutMenu)
        master.config(menu=self.menu)

        #add text box with a scroll bar
        self.scrolledText = ScrolledText(master=self.statusFrame,wrap=WORD,width=140,height=28)
        self.scrolledText.pack(padx=10, pady=10, fill=BOTH, expand=True)
        self.scrolledText.insert(END,"Paste UE Capability Information message here")

        #button Frame under text
        self.buttonFrame = Frame(self.frame)
        self.buttonFrame.pack()

        #Button Parse
        self.parserButton = Button(self.buttonFrame, text="Parse",width=10, command=self.parserFunc)
        self.parserButton.pack (side=RIGHT)

        #button Load
        self.loadFileButton = Button(self.buttonFrame, text="Open", width=10, command=self.loadFile)
        self.loadFileButton.pack(side=LEFT)

        #class member
        self.outFileName=""

    def quitProgram(self):
        quit()

    def loadAbout(self):
        #Display an About screen centered
        win = Toplevel()
        win.resizable(width=FALSE, height=FALSE)
        win.wm_title("About UECapabilityInformation parser")
        win.update_idletasks()
        width = 430
        height = 130
        x = self.calcX(win,width)
        y = self.calcY(win,height)
        win.geometry('{}x{}+{}+{}'.format(width, height, x, y))

        label = Label(win, text="UE Capability Information Parser v0.2\n\n"
                            "Written by Breno T. Minzon - breno.minzon@gmail.com\n\n"
                                "This application parses UE Capability Information message and creates an Excel\n"
                                "table with the parsed data")
        label.grid(row=0, column=0)
        button = Button(win, text="OK", width=10, command=win.destroy)
        button.grid(row=1,column=0)

    def calcX(self,win,width):
        frm_width = win.winfo_rootx() - win.winfo_x()
        win_width = width + 2 * frm_width
        return win.winfo_screenwidth() // 2 - win_width // 2

    def calcY(self,win,height):
        frm_width = win.winfo_rootx() - win.winfo_x()
        titlebar_height = win.winfo_rooty() - win.winfo_y()
        win_height = height + titlebar_height + frm_width
        return win.winfo_screenheight() // 2 - win_height // 2

    def loadFile(self):
        fileName = askopenfilename(initialdir = ".",title = "Select file",filetypes = (("Text","*.txt"),("all files","*.*")))
        if fileName != "":
            self.outFileName = fileName.replace(".txt",".xlsx")
            file = open(fileName, 'rU')
            lines = file.read()
            self.scrolledText.delete('1.0', END)
            self.scrolledText.insert(INSERT,lines)
            file.close()
        else:
            self.scrolledText.delete('1.0', END)
            self.scrolledText.insert(END, "Select a file or paste UE Capability Information message here")

    def parserFunc(self):
        text = self.convert(self.getStatusText())
        if (text != ['Paste UE Capability Information message here', '']):
            self.scrolledText.delete('1.0',END)
            Parser.readInformation(text,self.outFileName if self.outFileName != "" else "UeCapabilityInformation.xlsx")
            self.scrolledText.insert(END, "Successfuly parsed. Created file {}".format(self.outFileName if self.outFileName != "" else "UeCapabilityInformation.xlsx"))
        else:
            print("Empty file. Please paste a valid UECapabilityInformation file")

    def getStatusText(self):
        return self.scrolledText.get('0.0', END)

    def convert(self, text):
        return text.split('\n')

#This method is called from application main loop, and contruct the UI
def showUI():
    root = Tk()
    Application(root)
    root.mainloop()