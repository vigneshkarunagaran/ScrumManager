from tkinter.scrolledtext import ScrolledText
from tkinter import *
from tkinter import ttk
import json
import random


def loadSettingDB():
    global DB
    with open('setting.json', 'r') as fo:
        DB = json.load(fo)


loadSettingDB()

teamMembers = DB["teamMembers"]
priorityList = []


root = Tk()

root.title("Scrum Manager")
# root.resizable(False, False)
# screen_width = root.winfo_screenwidth()
# screen_height = root.winfo_screenheight()
# root.geometry("{}x{}+{}+{}".format(int(screen_width/2),
#               580, int(screen_width/2), 0))

tab_parent = ttk.Notebook(root)
mainTab = ttk.Frame(tab_parent)
# settingsTab = ttk.Frame(tab_parent)
tab_parent.add(mainTab, text="Generator")
# tab_parent.add(settingsTab, text="Settings")
tab_parent.pack(expand=1, fill='both')

priorityFrame = ttk.Frame(mainTab, padding=5)
priorityFrame.grid()
messageFrame = ttk.Frame(mainTab, padding=5)
messageFrame.grid()
triggerFrame = ttk.Frame(mainTab, padding=5)
triggerFrame.grid()


def setMessage(log, messType='LOW'):
    message = log + '\n'
    messageBox.tag_config('HIGH', foreground='blue')
    messageBox.tag_config('LOW', foreground='black')
    messageBox.insert(END, message, messType)
    messageBox.yview(END)


def addPriority():
    if memberSelected.get() != '':
        priorityMember = memberSelected.get()
        priorityBox.delete('1.0', END)
        if priorityMember not in priorityList:
            priorityList.append(priorityMember)
            teamMembers.remove(priorityMember)
        else:
            priorityList.remove(priorityMember)
            priorityList.insert(0, priorityMember)
        priorityBox.insert(END, 'Priority : \n'+str(priorityList))
        priorityBox.yview(END)
    else:
        priorityBox.insert(END, 'Select a member', 'red')


def generate():
    messageBox.delete('1.0', END)
    for member in priorityList:
        setMessage(member, 'HIGH')
    random.shuffle(teamMembers)
    for member in teamMembers:
        setMessage(member)


def reset():
    priorityBox.delete('1.0', END)
    messageBox.delete('1.0', END)
    global teamMembers
    global priorityList
    loadSettingDB()
    teamMembers = DB["teamMembers"]
    priorityList = []


memberSelected = StringVar()
teMembers = OptionMenu(priorityFrame, memberSelected, *teamMembers)
teMembers.grid(column=0, row=0, sticky='WE')
teMembers.config(width=40)

Button(priorityFrame, text="Prioritize",
       command=addPriority, width=10).grid(column=1, row=0, sticky='WE')

priorityBox = ScrolledText(messageFrame, height=5, width=45)
priorityBox.grid(column=0, row=0)

messageBox = ScrolledText(messageFrame, height=15, width=45)
messageBox.grid(column=0, row=1)

Button(triggerFrame, text="Reset",
       command=reset, width = 20).grid(column=0, row=2, sticky='WE')

Button(triggerFrame, text="Generate",
       command=generate, width = 20).grid(column=1, row=2, sticky='WE')

root.mainloop()
