from tkinter import Tk, Label, Button, Entry, END, W, filedialog,messagebox
import tkinter as tk
from Classifier import clickTrain,test # The classifier

# The GUI class
class GUI:

    # The constructor of the GUI
    # master - The window
    def __init__(self, master):
        # Setting window
        self.master = master
        self.title = "Naïve Bayes Classifier"
        master.title(self.title)
        master.geometry('300x150')
        back = tk.Frame(master=self.master, padx=2, pady=2, relief=tk.SUNKEN)
        back.pack_propagate(0)


        # Data variables
        self.path = ""
        self.num_of_bins = 0
        self.train_path = ""
        self.structure_path = ""
        self.test_path = ""
        self.output_path = ""

        # GUI Elements

        # ********Labels********
        self.path_lbl_txt = Label(self.master,text="Directory Path")# Path label
        self.bin_lbl_txt = Label(self.master,text="Discretization Bins")# number of  bins label
        self.err_lbl = Label(self.master,text="",fg="red")# Error label

        # ********Buttons********
        self.browse = Button(master,text="Browse",command=lambda: self.Browse())
        self.build = Button(master,text="Build",command=lambda: self.Build())

        self.classify = Button(master,text="Classify",command=lambda: self.Classify())

        # ********Entries********
        self.path_entry = Entry(master)
        self.bin_entry = Entry(master)



        # LAYOUT
        self.path_lbl_txt.grid(row=4,column=1,columnspan=2,sticky=W)
        self.bin_lbl_txt.grid(row=5,column=1,columnspan=2,sticky=W)

        self.path_entry.grid(row=4,column=3,columnspan=6)
        self.bin_entry.grid(row=5,column=3,columnspan=6)

        self.browse.grid(row=4,column=9,columnspan=2)
        self.build.grid(row=8,column=3,columnspan=4)
        self.classify.grid(row=10,column=3,columnspan=4)

        self.err_lbl.grid(row=12, column=1, columnspan=3, sticky=W)

    # This function is activated when the browse button is being clicked
    def Browse(self):

        folder_path = filedialog.askdirectory()# returns emp[ty string if he dosent choose
        if folder_path != "":
            self.path_entry.delete(0, END)
            self.path_entry.insert(0, folder_path)
            self.errorMessage("")


    # This function is responsible for displaying
    # The errors
    def errorMessage(self,message):
        self.err_lbl["text"] = message

    # This function is summoned if something went wrong with the program
    def buildFail(self,message):
        self.train_path = ""
        self.output_path_path = ""
        self.structure_path = ""
        self.test_path = ""
        self.path=""
        self.num_of_bins = 0
        self.errorMessage(message)

    # This function is activated when the build button is being clicked
    def Build(self):
        try:
            self.BuildModel()
            messagebox.showinfo(self.title,"Building classifier using train-set is done!")
        except Exception:
            self.buildFail("Couldn't build model")

    # This function will build the model
    # (summon the function implemented in Classifier.py)
    def BuildModel(self):

        self.path = self.path_entry.get()
        self.num_of_bins = self.bin_entry.get()
        if not self.is_integer(self.num_of_bins):

            self.buildFail("Please enter a valid number of bins")
            raise ValueError()
            return

        self.num_of_bins = int(self.num_of_bins)
        if self.num_of_bins < 1:
            self.buildFail("The number of bins must be bigger than 0")
            raise ValueError()
            return

        if self.path =="":
            self.buildFail("Please Enter a valid path")
            raise ValueError()
            return


        self.train_path = self.path+ "/train.csv"
        self.output_path = self.path+ "/output.txt"
        self.structure_path = self.path+ "/Structure.txt"
        self.test_path = self.path+ "/test.csv"
        self.errorMessage("")
        clickTrain(self.train_path, self.structure_path, self.num_of_bins)

    # This function is activated when the classify button is being clicked
    def Classify(self):
        try:
            self.Classify_file()
            self.errorMessage("")
            messagebox.showinfo(self.title, "The classification complete!")
            self.master.destroy()
        except Exception:
            self.buildFail("Couldn't Classify")

    # This function will classify the test file
    # (summon the function implemented in Classifier.py)
    def Classify_file(self):
        test(self.test_path, self.output_path)

    # This function check if the given object is an integer
    # s - the given object
    def is_integer(self,s):
        try:
            int(s)
            return True
        except Exception:
            return False

root = Tk()
my_gui = GUI(root)
root.mainloop()
