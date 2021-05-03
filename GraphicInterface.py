# -*- coding: utf-8 -*-
"""
KAPassiveEarthPressure

This script opens a window to show the tables with the values of the passive 
earth pressure coefficients determined by Kerisel and ABSI

Created on Mon Oct 12 09:05:48 2020

Copyright (R) 2020 E. Jaramillo-Rincon & Universidad Nacional de Colombia.
Licencia BSD-2

"""
## Graphic Interface

import tkinter as tk
from tkinter import ttk 
import csv

## Functions to be used

# Changes the value of beta/phi and/or of delta/phi if phi is changed
def phiValue(*args):
    if deltaVar.get() == 0:
        if betaVar.get() and phiVar.get() != 0:
            betaoverphi.set(round((float(betaVar.get()) / 
                                   float(phiVar.get())), 2))
        else:
            betaoverphi.set(" ")
            
    elif betaVar.get() == 0:
        if deltaVar.get() and phiVar.get() != 0:
            deltaoverphi.set(round((float(deltaVar.get()) / 
                                    float(phiVar.get())), 2))
        else:
            deltaoverphi.set(" ")
            
    else:
         betaoverphi.set(round((float(betaVar.get()) / 
                                float(phiVar.get())), 2))
         
         deltaoverphi.set(round((float(deltaVar.get()) / 
                                 float(phiVar.get())), 2))
    return(betaoverphi)
    
# Changes the value of beta/phi if beta is changed
def betaValue(*args):
    if phiVar.get() != 0:
        betaoverphi.set(round((float(betaVar.get()) / float(phiVar.get())), 2))
    else:
        betaoverphi.set("-")
    return(betaoverphi)

# Changes the value of delta/phi if delta is changed
def deltaValue(*args):
    if phiVar.get() != 0:
        deltaoverphi.set(round((float(deltaVar.get()) / float(phiVar.get())), 2))
    else:
        deltaoverphi.set("-")
    return(deltaoverphi)
    
# Gets the information to show in the table
def dataTable(*args):
    # Bucle to get the data from the correct .csv
    for i in range(len(valuesDeltaoverphi)):
        if MenuDeltaoverphi.get() == valuesDeltaoverphi[i]:
            # List that will contain the data from the csv 
            data = []
            with open(FilesCases[i], 'r') as f:
                reader = csv.reader(f, delimiter=';')
                for line in reader:
                    data.append(line)
            # If the selection is changed, erase the values from the previous
            # selection
            tree.delete(*tree.get_children())
            
            # Bucle to get and insert the values from data list in the table
            for a in range(len(valuesBetaoverphi)):
                if MenuBetaoverphi.get() == valuesBetaoverphi[a]:
                    n = 29
                    for c in range(n):
                        tree.insert('', 'end', text=data[31 * a + c + 1][0],
                                    values=data[31 * a + c + 1][0:])
                else:
                    pass
            return(data)
        else:
            pass

# Gets the value of Kp from the table 
def ValueKp(*args):
    for i in range(len(deltaOverPhi0Vals)):
        if deltaOverPhi0Var.get() == deltaOverPhi0Vals[i]:
            # List that will contain the data from the csv 
            data = []
            with open(FilesCases[i], 'r') as f:
                reader = csv.reader(f, delimiter=';')
                for line in reader:
                    data.append(line)
                    
            for a in range(len(betaOverPhi0Vals)):
                if betaOverPhi0Var.get() == betaOverPhi0Vals[a]:
                    dataS=[]
                    n = 29
                    for c in range(n):
                        dataS.append(data[31 * a + c + 1][0:])
                    
            for b in range(len(lmb0Values)):
                if lmb0Var.get() == lmb0Values[b]:
                    RowKp = dataS[b]
                    
                    for d in range(len(phi0Values)):
                        if phi0Var.get() == phi0Values[d]:
                            if RowKp[d+1]=='  ':
                                kp0Read.set('-')
                                return(kp0Read)
                            else:
                                kp0Read.set(RowKp[d+1])
                                return(kp0Read)
                        else:
                            pass
                else:
                    pass
        else:
            pass
# Files to be used 
FilesCases = [r'./CasesKREA/1stCaseKREA.csv',
              r'./CasesKREA/2ndCaseKREA.csv',
              r'./CasesKREA/3rdCaseKREA.csv',
              r'./CasesKREA/4thCaseKREA.csv',
              r'./CasesKREA/5thCaseKREA.csv',
              r'./CasesKREA/6thCaseKREA.csv',
              r'./CasesKREA/7thCaseKREA.csv',
              r'./CasesKREA/8thCaseKREA.csv']

# Create the root
root = tk.Tk()
# Title for the interface's window
root.title('Kerisel and Absi Passive Earth Pressure Coefficients')
# Not resizeable window
root.resizable(False, False)




## Title and configuration of frame 0 ##
titleFrame0 = tk.LabelFrame(root, text="READING FROM TABLE", padx=20, pady=20)
titleFrame0.grid(row=0, column=0)

## Lambda's label and entry configuration and positioning
lmbText0 = '\u03BB: Angle between the wall and the vertical:'
lmb0 = tk.Label(titleFrame0, text = lmbText0, width=35)
lmb0.grid(row = 1, columnspan = 4, column = 0)

lmb0Var = tk.StringVar()

lmb0Values = ['50 °', '45 °', '40 °', '35 °', '30 °', '25 °', '20 °', '15 °',
              '10 °', '5 °', '0 °', '-5 °', '-10 °', '-15 °', '-20 °','-25 °',
              '-30 °', '-35 °', '-40 °', '-45 °', '-50 °', '-55 °', '-60 °',
              '-65 °', '-70 °', '-75 °', '-80 °', '-85 °', '-90 °']

lmb0Entry = ttk.Combobox(titleFrame0, values =lmb0Values, state='readonly', 
                         textvariable=lmb0Var)
lmb0Entry.grid(row = 1, column = 5)
lmb0Entry.config(justify='right', width=5)
lmb0Entry.bind("<<ComboboxSelected>>", ValueKp)


## Phi's label and entry configuration and positioning
phiText0 = '\u03C6: Friction angle of the soil:'
phi0 = tk.Label(titleFrame0, text = phiText0, width=35)
phi0.grid(row = 2, columnspan = 4, column = 0)

phi0Var = tk.StringVar()

phi0Values = ['10 °', '15 °', '20 °', '25 °', '30 °', '35 °', '40 °', '45 °']
phi0Entry = ttk.Combobox(titleFrame0, values= phi0Values, state='readonly', 
                         textvariable = phi0Var)
phi0Entry.grid(row = 2, column = 5)
phi0Entry.config(justify='right', width=5)
phi0Entry.bind("<<ComboboxSelected>>", ValueKp)


## Beta over phi.
betaOverPhiText0 = '\u03B2/\u03C6: '
betaOverPhi0 = tk.Label(titleFrame0, text = betaOverPhiText0, width=35)
betaOverPhi0.grid(row = 3, columnspan = 4, column = 0)

betaOverPhi0Var = tk.StringVar()

betaOverPhi0Vals = ["-1", "-4/5", "-2/3", "-3/5", "-2/5", "-1/3", "-1/5", "0",
                    "1/5", "1/3", "2/5", "3/5", "2/3", "4/5", "1"]
betaOverPhi0Entry = ttk.Combobox(titleFrame0, values=betaOverPhi0Vals, 
                                 state='readonly', textvariable = betaOverPhi0Var)
betaOverPhi0Entry.grid(row = 3, column = 5)
betaOverPhi0Entry.config(justify='right', width=5)
betaOverPhi0Entry.bind("<<ComboboxSelected>>", ValueKp)


## Delta ober phi.
deltaOverPhiText0 = '\u03B4/\u03C6: '
deltaOverPhi0 = tk.Label(titleFrame0, text = deltaOverPhiText0, width=35)
deltaOverPhi0.grid(row = 4, columnspan = 4, column = 0)

deltaOverPhi0Var = tk.StringVar()

deltaOverPhi0Vals = ['-1', '-2/3', '-2/5', '-1/3', '0', '1/3', '2/5', '2/3']
deltaOverPhi0Entry = ttk.Combobox(titleFrame0, values=deltaOverPhi0Vals, 
                                  state='readonly', textvariable = deltaOverPhi0Var)
deltaOverPhi0Entry.grid(row = 4, column = 5)
deltaOverPhi0Entry.config(justify='right', width=5)
deltaOverPhi0Entry.bind("<<ComboboxSelected>>", ValueKp)


# Passive Earth pressure value, Kp.
kp0Read = tk.StringVar()
kp0Read.set(' ')
kp0Label = tk.Label(titleFrame0, text="Kp:")
kp0Label.grid(row=5, columnspan=4)
kp0Label2 = tk.Label(titleFrame0, textvariable=kp0Read)
kp0Label2.grid(row=5, column=5)
kp0Label2.config(justify='center', width=5)




### Title and configuration of frame 1
titleFrame1 = tk.LabelFrame(root, text="CALCULATION BY INTERPOLATION",padx=20,pady=20)
titleFrame1.grid(row=1, column=0)

## Lambda's label and entry configuration and positioning
lmbText = '\u03BB: Angle between the wall and the vertical:'
lmb = tk.Label(titleFrame1, text = lmbText, width=35)
lmb.grid(row = 1, columnspan = 4, column = 0)

lmbVar = tk.DoubleVar()

lmbEntry = tk.Entry(titleFrame1, textvariable=lmbVar)
lmbEntry.grid(row = 1, column = 5)
lmbEntry.config(justify='right', width=5)
glmb = tk.Label(titleFrame1, text='°')
glmb.grid(row = 1, column = 6)

## Phi's label and entry configuration and positioning
phiText = '\u03C6: Friction angle of the soil:'
phiLabel = tk.Label(titleFrame1, text = phiText, width=35)
phiLabel.grid(row=2, columnspan = 4, column = 0)

# Create the variable of the 'phi' entry as float
phiVar = tk.DoubleVar()

phiEntry = tk.Entry(titleFrame1, textvariable=phiVar)
phiEntry.grid(row=2, column=5)
phiEntry.config(justify='right', width=5)

# Bind the action of "focus out the entry" to the "phiValue" function
phiEntry.bind("<FocusOut>", phiValue)

gphi = tk.Label(titleFrame1, text='°')
gphi.grid(row=2, column=6)

## Beta's label and entry configuration and positioning
betaText = '\u03B2: Angle between the ground surface and the horizontal:'
betaLabel = tk.Label(titleFrame1, text = betaText, width=45)
betaLabel.grid(row = 3, columnspan = 4, column = 0)
gbeta = tk.Label(titleFrame1, text='°')
gbeta.grid(row=3, column=6)

# Create the variable of the 'beta' entry as float
betaVar = tk.DoubleVar()

betaEntry = tk.Entry(titleFrame1, textvariable = betaVar)
betaEntry.grid(row = 3, column = 5)
betaEntry.config(justify='right', width=5)

# Bind the action of "focus out the entry" to the "betaValue" function
betaEntry.bind("<FocusOut>", betaValue)

## Delta's label and entry configuration and positioning
deltaText = '\u03B4: Angle between the lateral earth pressure and the normal \
of the wall:'
deltaLabel = tk.Label(titleFrame1, text = deltaText, width=60)
deltaLabel.grid(row=4, columnspan = 4,column=0)
gdelta = tk.Label(titleFrame1, text='°')
gdelta.grid(row=4, column=6)

# Create the variable of the 'delta' entry as float
deltaVar = tk.DoubleVar()

deltaEntry = tk.Entry(titleFrame1, textvariable=deltaVar)
deltaEntry.grid(row=4, column=5)
deltaEntry.config(justify='right', width=5)

# Bind the action of "focus out the entry" to the "deltaValue" function
deltaEntry.bind("<FocusOut>",deltaValue)

# Create the variable of the 'betaoverphi' entry as string
betaoverphi = tk.StringVar()
# Saves the variable as the result of the function "betaoverphi"
betaoverphi = betaValue()

# Configuration and positioning the betaoverphi's variable
betaoverphiLabel = tk.Label(titleFrame1,text="\u03B2/\u03C6:")
betaoverphiLabel.grid(row=5, column=0)
betaoverphiLabel2 = tk.Label(titleFrame1, textvariable=betaoverphi, width = 5)
betaoverphiLabel2.grid(row=5, column=1)
betaoverphiLabel2.config(justify='center', width=5)

# Create the variable of the 'deltaoverphi' entry as string
deltaoverphi = tk.StringVar()
# Saves the variable as the result of the function "deltaoverphi"
deltaoverphi = deltaValue()

# Configuration and positioning the deltaoverphi's variable
deltaoverphiLabel = tk.Label(titleFrame1, text="\u03B4/\u03C6:")
deltaoverphiLabel.grid(row=6, column=0)
deltaoverphiLabel2 = tk.Label(titleFrame1, textvariable=deltaoverphi)
deltaoverphiLabel2.grid(row=6, column=1)
deltaoverphiLabel2.config(justify='center', width=5)

# Passive Earth pressure value, Kp.
kpRead = "crear la funcion"
kpLabel = tk.Label(titleFrame1, text="Kp:")
kpLabel.grid(row=7, column=0)
kpLabel2 = tk.Label(titleFrame1, textvariable=kpRead)
kpLabel2.grid(row=7, column=1)
kpLabel2.config(justify='center', width=5)



## Create a second frame and position it 
frame2 = tk.LabelFrame(root, text='GRAPHIC REFERENCES FOR PARAMETERS', padx=20, pady=20)
frame2.grid(row=6, column=0)

## Create the image
RefGraph = tk.PhotoImage(master=frame2,file=r'./CasesKREA/RefGraph.png')
RefGraph2 = RefGraph.subsample(3)

# Save the image in a label for configuring a positioning
TextLabel = tk.Label(frame2, image=RefGraph2, compound='bottom')
TextLabel.grid(row=7, column=0, columnspan=6)
TextLabel.config(justify='center')

# Create a third frame
frame3 = tk.LabelFrame(root, text="EXPERIMENTAL VALUES OF PASSIVE EARTH PRESSURE (Kp)",
                       pady=5)
frame3.grid(row=0, column=7, rowspan=15)
frame3.config(bg="lightblue")

# Values that will appear in the dropdown menu for Beta/Phi
valuesBetaoverphi = ["-1", "-4/5", "-2/3", "-3/5", "-2/5", "-1/3", "-1/5", "0",
                     "1/5", "1/3", "2/5", "3/5", "2/3", "4/5", "1"]

# Configuration of the appearance of the label for Beta/phi
bopLabel = tk.Label(frame3, text='\u03B2/\u03C6:')
bopLabel.grid(row=1, column=7)
bopLabel.config(bg='lightblue')

# Configuration of the dropdown menu for beta/phi
MenuBetaoverphi = ttk.Combobox(frame3,values = valuesBetaoverphi, state='readonly')
MenuBetaoverphi.grid(row=1, column=8)
MenuBetaoverphi.bind("<<ComboboxSelected>>",dataTable)

# Configuration of the appearance of the label for delta/phi
dopLabel = tk.Label(frame3, text='\u03B4/\u03C6:')
dopLabel.grid(row=1, column=9)
dopLabel.config(bg='lightblue')

# Configuration of the dropdown menu for delta/phi
valuesDeltaoverphi = ['-1', '-2/3', '-2/5', '-1/3', '0', '1/3', '2/5', '2/3']
MenuDeltaoverphi = ttk.Combobox(frame3, values = valuesDeltaoverphi, state='readonly')
MenuDeltaoverphi.grid(row=1, column=10)
MenuDeltaoverphi.bind("<<ComboboxSelected>>", dataTable)

# Gets the correct data from the function "dataTable"
data = dataTable()

# Columns that will appear on the table
columnsT = ['\u03BB  |  \u03C6', ' 10° ', ' 15° ', ' 20° ', ' 25° ', ' 30° ',
            ' 35° ', ' 40° ', ' 45° ']

# Create the table as a "Treeview"
tree = ttk.Treeview(frame3)
tree['columns']=columnsT

# Define the first column by default in a Treeview
tree.column("#0")

# Bucle to create the columns for the table
for i in range(9):
    tree.column(columnsT[i],anchor="center", width=75)

# Define the heading of the first column by default in a Treeview
tree.heading("#0", text="Lambda\Phi")

# Bucle to create the headings that will appear on the table
for i in range(9):
    tree.heading(columnsT[i],text=columnsT[i])
    
# Configure the scrollbar 
verscrlbar = ttk.Scrollbar(frame3,  
                           orient ="vertical",  
                           command = tree.yview) 
verscrlbar.grid(row=2, column=15, sticky='nse')

# To hide the '#0' column set by default in a Treeview
tree['show']='headings'
tree.grid(row=2, column=7, columnspan=8)
tree.config(height=25, yscrollcommand = verscrlbar.set)

frame3.columnconfigure(1, weight=1)
frame3.rowconfigure(1, weight=1)

root.mainloop()


        
