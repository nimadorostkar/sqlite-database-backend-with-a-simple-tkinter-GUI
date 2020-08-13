from tkinter import *
from backend import Database

db = Database("recipe.db")

class Window(object):

    def __init__(self, window):
        self.window = window
        self.window.wm_title("Recipe Index")

        searchLbl = Label(window, text="Search by...")
        searchLbl.grid(row=0,column=0,sticky="W")

        recipeLbl = Label(window, text="Recipes (Click to see more)")
        recipeLbl.grid(row=0,column=2)

        ingredientSearchLbl = Label(window, text="Ingredient:")
        ingredientSearchLbl.grid(row=1,column=0)

        self.ingredientSearchVar = StringVar()
        self.ingredientSearchEntry = Entry(window, textvariable=self.ingredientSearchVar)
        self.ingredientSearchEntry.grid(row=1,column=1)

        tagSearchLbl = Label(window, text="Tagged:")
        tagSearchLbl.grid(row=2,column=0)

        self.tagSearchVar = StringVar()
        self.tagSearchVar.set("Select Option:")
        if (db.getTags() != []):
            options = []
            for i in db.getTags():
                options += i
        else:
            options = ["No current tags"]
        tagMenu = OptionMenu(window, self.tagSearchVar, *options)
        tagMenu.config(width=18)
        tagMenu.grid(row=2,column=1,padx=10)

        searchBtn = Button(window, text="Search", command=self.search_command)
        searchBtn.config(width=13)
        searchBtn.grid(row=3,column=0,pady=5,ipady=5,padx=5)

        viewBtn = Button(window, text="View All Recipes",command=self.view_command)
        viewBtn.config(width=13)
        viewBtn.grid(row=3,column=1,pady=5,ipady=5,padx=5)

        self.list = Listbox(window, width=25, height=14)
        self.list.grid(row=1,column=2,rowspan=8)

        scrollbar = Scrollbar(window)
        scrollbar.config(width=13)
        scrollbar.grid(row=1,column=3,rowspan=8,sticky='ns')

        self.list.configure(yscrollcommand=scrollbar.set)
        scrollbar.configure(command=self.list.yview)

        self.list.bind('<<ListboxSelect>>', self.getSelection)

        selectLbl = Label(window, text="Add/Update Recipes:")
        selectLbl.grid(row=4,column=0,columnspan=2,pady=5,sticky="W")

        nameLbl = Label(window, text="Name: ")
        nameLbl.grid(row=5,column=0)

        self.nameVar = StringVar()
        self.nameEntry = Entry(window,textvariable=self.nameVar)
        self.nameEntry.grid(row=5,column=1)

        urlLbl = Label(window, text="URL: ")
        urlLbl.grid(row=6,column=0)

        self.urlVar = StringVar()
        self.urlEntry = Entry(window,textvariable=self.urlVar)
        self.urlEntry.grid(row=6,column=1)

        ingredientsLbl = Label(window, text="Ingredients: ")
        ingredientsLbl.grid(row=7,column=0)

        self.ingredientsVar = StringVar()
        self.ingredientsEntry = Entry(window,textvariable=self.ingredientsVar)
        self.ingredientsEntry.grid(row=7,column=1)

        tagLbl = Label(window, text="Tagged: ")
        tagLbl.grid(row=8,column=0)

        self.tagVar = StringVar()
        self.tagEntry = Entry(window, textvariable=self.tagVar)
        self.tagEntry.grid(row=8,column=1)

        addBtn = Button(window, text="Add New Recipe", command=self.add_command)
        addBtn.config(width=13)
        addBtn.grid(row=9,column=0,pady=5,ipady=5,padx=5)

        clearBtn = Button(window, text="Clear All", command=self.clear_command)
        clearBtn.config(width=13)
        clearBtn.grid(row=9,column=1,pady=5,ipady=5)

        updateBtn = Button(window, text="Update Selected", command=self.update_command)
        updateBtn.config(width=13)
        updateBtn.grid(row=10,column=0,ipady=5,padx=5)

        deleteBtn = Button(window, text="Delete Selected", command=self.delete_command)
        deleteBtn.config(width=13)
        deleteBtn.grid(row=10,column=1,ipady=5)

        self.errorTextVar = StringVar()
        errorLbl = Label(window, textvariable=self.errorTextVar)
        errorLbl.grid(row=9,column=2)

    def getSelection(self,event):
        if self.list.curselection() != ():
            index = self.list.curselection()[0]
            self.selection = self.list.get(index)
            self.clear_command()
            self.recipe = db.getRecipe(self.selection)
            self.nameEntry.insert(END,self.selection)
            self.urlEntry.insert(END,self.recipe[0][2])
            self.ingredientString = ', '.join(self.recipe[1])
            self.ingredientsEntry.insert(END,self.ingredientString)
            self.tagEntry.insert(END,self.recipe[0][3])

    def view_command(self):
        self.list.delete(0,END)
        for row in db.view():
            self.list.insert(END,row[0])

    def search_command(self):
        self.list.delete(0, END)
        ingredientList = self.ingredientSearchVar.get().lower().split(",")
        for row in db.search(self.tagSearchVar.get(), ingredientList):
            self.list.insert(END,row[1])

    def add_command(self):
        if self.nameVar.get() == "":
            self.errorMessage("name")
        else:
            ingredientList = self.ingredientsVar.get().lower().split(", ")
            db.insert(self.nameVar.get(), self.urlVar.get(), self.tagVar.get().title(), ingredientList)
            self.list.delete(0,END)
            self.list.insert(END,self.nameVar.get())
            self.errorTextVar.set("")

    def delete_command(self):
        id = db.getRecipe(self.selection)[0][0]
        db.delete(id)
        self.view_command()
        self.clear_command()

    def update_command(self):
        if self.nameVar.get() == "":
            self.errorMessage("name")
        else:
            recipe = db.getRecipe(self.selection)
            db.update(recipe[0][0], self.nameVar.get(), self.urlVar.get(), self.tagVar.get().title(), self.ingredientsVar.get().lower().split(", "))
            self.view_command()
            self.clear_command()

    def clear_command(self):
        self.ingredientSearchEntry.delete(0,END)
        self.tagSearchVar.set("Select Option:")
        self.nameEntry.delete(0,END)
        self.urlEntry.delete(0,END)
        self.ingredientsEntry.delete(0,END)
        self.tagEntry.delete(0,END)
        self.window.update()

    def errorMessage(self, error):
        if error == "name":
            self.errorTextVar.set("Please enter a name")

window = Tk()
Window(window)
window.mainloop()
