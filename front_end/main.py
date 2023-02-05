from asyncio.windows_events import NULL
import tkinter as tk
from tkinter import *
import sys
import mysql.connector

db = mysql.connector.connect(
host = "localhost",
user = "root",
passwd = "root",
database = "hospital"
)

mycursor = db.cursor(buffered=True)

mycursor.callproc("SelectAllPatients")
selectedpatients = []
SAPout = ""
for i,result in enumerate(mycursor.stored_results()):
    selectedpatients.append(result.fetchall())
for i in range(5):
    SAPout+=(str(selectedpatients[0][i][0])) + "|" + (str(selectedpatients[0][i][1])) + "|" + (str(selectedpatients[0][i][2])) + "|" + (str(selectedpatients[0][i][3])) + "|" + (str(selectedpatients[0][i][4])) + "\n"


mycursor.callproc("AvgNumMedsByDiabetes")
PWDM = []
PWDMout = ""
for i,result in enumerate(mycursor.stored_results()):
    PWDM.append(result.fetchall())
for i in range(2):
    PWDMout+=(str(PWDM[0][i][0]) + "|" + str(PWDM[0][i][1]) + "\n")


mycursor.callproc("EmergencyAdmission")
EMA = []
EMAout = ""
for i,result in enumerate(mycursor.stored_results()):
    EMA.append(result.fetchall())
for i in range(5):
    EMAout+=(str(EMA[0][i][0]) + "|" + str(EMA[0][i][1]) + "|" + str(EMA[0][i][2]) + "\n")

mycursor.callproc("VisitCountAdSource")
VCA = []
VCAout = ""
for i,result in enumerate(mycursor.stored_results()):
    VCA.append(result.fetchall())
for i in range(7):
    VCAout+=(str(VCA[0][i][0]) + "|" + str(VCA[0][i][1]) + "\n")



class databaseGUI:
    def __init__(self):
        #initialize the canvas
        root = Tk()
        canvas = Canvas(root, width=1200, height = 800)
        canvas.grid(columnspan=3)
        statement = tk.Label(root, text="Enter Username and Password:",font=("Arial",25))
        statement.place(relx=.5,anchor=CENTER,y=100)

        usrentry= Entry(root, width= 40)
        usrentry.focus_set()
        pswentry= Entry(root, width= 40,show="*")
        pswentry.focus_set()
        
        usrentry.place(relx=.5,anchor=CENTER,y=400)
        pswentry.place(relx=.5,anchor=CENTER,y=500)
        usrtxt = tk.Label(root, text="Username:",font=("Arial",15))
        usrtxt.place(relx=.5,anchor=CENTER,y = 350)
        pswtxt = tk.Label(root, text="Password:",font=("Arial",15))
        pswtxt.place(relx=.5,anchor=CENTER,y = 450)
        #this is how you store "global variables"
        self.numEntries = IntVar()
        self.numEntries = 0

        self.customselect = StringVar()
        self.customselect = ""
        self.customfrom = StringVar()
        self.customfrom = ""
        self.customwhere = StringVar()
        self.customwhere = ""
        
        #opens the main menu
        def mainfunc():
            #remove objects on screen
            statement.place_forget()
            openbutton.place_forget()
            
            #instructions
            instructions.place(relx=.5,anchor=CENTER,y=100)

            #buttons
            insertbutton.place(relx=.5,anchor=CENTER,y=300)
            querybutton.place(relx=.5,anchor=CENTER,y=450)
            custombutton.place(relx=.75,anchor=CENTER,y=450)
            storedpbutton.place(relx=.5,anchor=CENTER,y=600)  
            mainmenubutton.place(x=10,y=10)

            
        #function button 1 - insert
        def insertfunc():
            instructions.place_forget()
            insertbutton.place_forget()
            querybutton.place_forget()
            storedpbutton.place_forget()
            custombutton.place_forget()

            self.numEntries = 0
            insertinstructions.configure(text ="Enter the PatientID and click OKAY to continue.")
            okbutton.place(relx=.5,anchor=CENTER,y=500)
            PIDlabel.place(relx=.25,anchor=CENTER,y=200)
            Agelabel.place(relx=.75,anchor=CENTER,y=200)
            Weightlabel.place(relx=.25,anchor=CENTER,y=300)
            Genderlabel.place(relx=.75,anchor=CENTER,y=300)
            insertinstructions.place(relx=.5,anchor=CENTER,y=100)
            entry.place(relx=.5,anchor=CENTER,y=400)
                
        #okay button func
        def okfunc():
            
            insertinstructions.place_forget()
            #these check which entry we are on and update the graphic
            if(self.numEntries==0):
                string= entry.get()
                PIDlabel.configure(text="PatientID: " + string)
        
            if(self.numEntries==1):
                string= entry.get()
                Agelabel.configure(text="Age: " + string)

            if(self.numEntries==2):
                string= entry.get()
                Weightlabel.configure(text="Weight: " + string)

            if(self.numEntries==3):
                string= entry.get()
                Genderlabel.configure(text="Gender: " + string)
            entry.delete(0,1000)
            #updates the instructions
            entries = ["PatientID","Age","Weight","Gender"]
            self.numEntries = self.numEntries + 1
            if(self.numEntries<4):
                insertinstructions.configure(text="Enter the " + entries[self.numEntries] + " and click OKAY to continue.")
                insertinstructions.place(relx=.5,anchor=CENTER,y=100)

            if(self.numEntries>=4):
                insertinstructions.configure(text="Press CONFIRM to submit insert.")
                insertinstructions.place(relx=.5,anchor=CENTER,y=100)
                okbutton.place_forget()
                entry.place_forget()
                confirmbutton.place(relx=.5,rely=.5,anchor=CENTER)

        #confirm function for insert    
        def confirmfunc():
            mainmenu()

        #function SQL query
        def queryfunc():
            instructions.place_forget()
            insertbutton.place_forget()
            querybutton.place_forget()
            storedpbutton.place_forget()
            custombutton.place_forget()

            queryinstructions.place(relx=.5,anchor=CENTER,y=100)
            okbutton2.place(relx=.75,anchor=CENTER,y=700)
            QueryResultsLabel.configure(text="Results:")
            QueryResultsLabel.place(relx=.5,anchor=CENTER,rely=.5)
            entry.place(relx=.5,anchor=CENTER,y=700)

        def queryokfunc():
            
            string= entry.get()
            entry.delete(0,1000)
            mycursor.execute(string)
            storeresults = []
            results = ""
            for x in mycursor:
                storeresults.append(x)
            numcols = len(storeresults[0])
            numrows = len(storeresults)
            for i in range(5):
                if(numrows>i):
                    for j in range(numcols):
                        if j<numcols-1:
                            results+=str(storeresults[i][j]) + "|"
                        else:
                            results+=str(storeresults[i][j])
                results+="\n"
            QueryResultsLabel.configure(text="Results for: " + string + "\n\n" + results)
        #custom query function - 2.5
        def customfunc():
            instructions.place_forget()
            insertbutton.place_forget()
            querybutton.place_forget()
            storedpbutton.place_forget()
            custombutton.place_forget()

            custominstructions.configure(text = "Select which table to access:")
            custominstructions.place(relx=.5,anchor=CENTER,y=100)
            cb1.place(relx=.33,anchor=CENTER,y=500)
            cb2.place(relx=.67,anchor=CENTER,y=500)
            

        #user selected patients
        def cb1func():
            cb1.place_forget()
            cb2.place_forget()
            custominstructions.place_forget()
            custominstructions.configure(text = "Select which data to display from Patients:")
            custominstructions.place(relx=.5,anchor=CENTER,y=100)

            patdatab1.place(relx=.25,anchor=CENTER,y=500)
            patdatab2.place(relx=.5,anchor=CENTER,y=500)
            patdatab3.place(relx=.75,anchor=CENTER,y=500)
            self.customfrom = "Patients"

        def alldatafunc():
            self.customselect = "*"
            if(self.customfrom=="Patients"):
                PatientsConstraintsetup()
            if(self.customfrom=="Hospital_visits"):
                HospitalConstraintsetup()

        def PatientIDdatafunc():
            self.customselect = "Patient_ID"
            PatientsConstraintsetup()

        def VisitIDdatafunc():
            self.customselect = "Visit_ID"
            PatientsConstraintsetup()

        def PatientsConstraintsetup():
            patdatab1.place_forget()
            patdatab2.place_forget()
            patdatab3.place_forget()
            custominstructions.place_forget()
            custominstructions.configure(text = "Select constraints for data in Patients:")
            custominstructions.place(relx=.5,anchor=CENTER,y=100)

            pconstb1.place(relx=.33,anchor=CENTER,y=500)
            pconstb2.place(relx=.33,anchor=CENTER,y=600)
            pconstb3.place(relx=.67,anchor=CENTER,y=500)
            pconstb4.place(relx=.67,anchor=CENTER,y=600)

        def pmaleconstfunc():
            self.customwhere = "gender='Male'"
            cqresultsfunc()
        
        def pfemaleconstfunc():
            self.customwhere = "gender='Female'"
            cqresultsfunc()

        def ageOconstfunc():
            self.customwhere = "age>40"
            cqresultsfunc()

        def ageYconstfunc():
            self.customwhere = "age<40"
            cqresultsfunc()

        #user selected hospital visits
        def cb2func():
            cb1.place_forget()
            cb2.place_forget()
            custominstructions.place_forget()
            custominstructions.configure(text = "Select which data to display from Hospital Visits:")
            custominstructions.place(relx=.5,anchor=CENTER,y=100)

            hosdatab1.place(relx=.25,anchor=CENTER,y=500)
            hosdatab2.place(relx=.5,anchor=CENTER,y=500)
            hosdatab3.place(relx=.75,anchor=CENTER,y=500)
            self.customfrom = "Hospital_visits"

        def LOSdatafunc():
            self.customselect = "Length_of_stay"
            HospitalConstraintsetup()

        def ADSdatafunc():
            self.customselect = "Admission_source"
            HospitalConstraintsetup()

        def HospitalConstraintsetup():
            hosdatab1.place_forget()
            hosdatab2.place_forget()
            hosdatab3.place_forget()
            custominstructions.place_forget()
            custominstructions.configure(text = "Select constraints for data in Hospital Visits:")
            custominstructions.place(relx=.5,anchor=CENTER,y=100)

            hconstb1.place(relx=.33,anchor=CENTER,y=500)
            hconstb2.place(relx=.33,anchor=CENTER,y=600)
            hconstb3.place(relx=.67,anchor=CENTER,y=500)
            hconstb4.place(relx=.67,anchor=CENTER,y=600)

        def emergencyconstfunc():
            self.customwhere = "Admission_type='Emergency'"
            cqresultsfunc()

        def electiveconstfunc():
            self.customwhere = "Admission_type='Elective'"
            cqresultsfunc()

        def longLOSconstfunc():
            self.customwhere = "Length_of_stay>4"
            cqresultsfunc()

        def shortLOSconstfunc():
            self.customwhere = "Length_of_stay<4"
            cqresultsfunc()

        def cqresultsfunc():
            pconstb1.place_forget()
            pconstb2.place_forget()
            pconstb3.place_forget()
            pconstb4.place_forget()
            hconstb1.place_forget()
            hconstb2.place_forget()
            hconstb3.place_forget()
            hconstb4.place_forget()
            allstring = ""
            if(self.customselect=="*"):
                allstring = "all"
            else:
                allstring = self.customselect
            displaystring = "Displaying results for:\n" + allstring + " data from " + self.customfrom + " where " + self.customwhere
            custominstructions.place_forget()
            custominstructions.configure(text=displaystring)
            custominstructions.place(relx=.5,anchor=CENTER,y=100)

            querystring = "SELECT " + self.customselect + " from " + self.customfrom + " where " + self.customwhere
            
            mycursor.execute(querystring)
            storeresults = []
            results = ""
            for x in mycursor:
                storeresults.append(x)
            numcols = len(storeresults[0])
            numrows = len(storeresults)
            for i in range(5):
                if(numrows>i):
                    for j in range(numcols):
                        if j<numcols-1:
                            results+=str(storeresults[i][j]) + "|"
                        else:
                            results+=str(storeresults[i][j])
                results+="\n"
            QueryResultsLabel.place(relx=.5,anchor=CENTER,rely=.5)
            QueryResultsLabel.configure(text="\n\n" + results)
            
        #function query
        def storedpfunc():
            instructions.place_forget()
            insertbutton.place_forget()
            querybutton.place_forget()
            storedpbutton.place_forget()
            custombutton.place_forget()
            StoredPLabel.configure(text="Results:")

            
            instructionsp.place(relx=.5,anchor=CENTER,y=100)
            StoredPLabel.place(relx=.5,anchor=CENTER,rely=.25)
            qb1.place(relx=.25,anchor=CENTER,y=600)
            qb2.place(relx=.5,anchor=CENTER,y=600)
            qb3.place(relx=.75,anchor=CENTER,y=600) 
            qb4.place(relx=.5,anchor=CENTER,y=700)

        def qb1func():
            StoredPLabel.configure(text="Results:\n" + "VisitID|PatientID|Race|Gender|Age\n\n" + SAPout)
            StoredPLabel.place(relx=.5,anchor=CENTER,rely=.4)

        def qb2func():
            StoredPLabel.configure(text="Results:\n" + "AVG # MEDS|Diabetes Status\n\n" + PWDMout)
            StoredPLabel.place(relx=.5,anchor=CENTER,rely=.4)

        def qb3func():
            StoredPLabel.configure(text="Results:\n" + "PatientID|Age|Gender\n\n" + EMAout)
            StoredPLabel.place(relx=.5,anchor=CENTER,rely=.4)

        def qb4func():
            StoredPLabel.configure(text="Results:\n" + "Admission Source|Number of Admissions\n\n" + VCAout)
            StoredPLabel.place(relx=.5,anchor=CENTER,rely=.4)

        #working how I want it to
        def mainmenu():
            okbutton.place_forget()
            PIDlabel.place_forget()
            Agelabel.place_forget()
            Weightlabel.place_forget()
            Genderlabel.place_forget()
            insertinstructions.place_forget()
            entry.place_forget()
            confirmbutton.place_forget()
            qb1.place_forget()
            qb2.place_forget()
            qb3.place_forget()
            qb4.place_forget()
            instructionsp.place_forget()
            StoredPLabel.place_forget()
            queryinstructions.place_forget()
            okbutton2.place_forget()
            QueryResultsLabel.place_forget()
            qentry.place_forget()
            pswtxt.place_forget()
            usrtxt.place_forget()
            usrentry.place_forget()
            pswentry.place_forget()
            custominstructions.place_forget()
            cb1.place_forget()
            cb2.place_forget()
            patdatab1.place_forget()
            patdatab2.place_forget()
            patdatab3.place_forget()
            hosdatab1.place_forget()
            hosdatab2.place_forget()
            hosdatab3.place_forget()
            pconstb1.place_forget()
            pconstb2.place_forget()
            pconstb3.place_forget()
            pconstb4.place_forget()
            hconstb1.place_forget()
            hconstb2.place_forget()
            hconstb3.place_forget()
            hconstb4.place_forget()
            
            mainfunc()       
                
        #close
        def exit():
            root.destroy()  

        #BUTTONS
             
        #button1 - insert
        inserttext = tk.StringVar()
        insertbutton = tk.Button(root, textvariable= inserttext, command=lambda:insertfunc(), font="Raleway",bg="#20bebe", fg="white", height=2,width=20)
        inserttext.set("INSERT")
        #button2 - custom query
        querytext = tk.StringVar()
        querybutton = tk.Button(root, textvariable= querytext, command=lambda:queryfunc(), font="Raleway",bg="#20bebe", fg="white", height=2,width=20)
        querytext.set("SQL QUERY")
        #button2.5 - user query
        customtext = tk.StringVar()
        custombutton = tk.Button(root, textvariable= customtext, command=lambda:customfunc(), font="Raleway",bg="#20bebe", fg="white", height=2,width=20)
        customtext.set("CUSTOM QUERY")
        #button3 - Stored Procedure
        storedptext = tk.StringVar()
        storedpbutton = tk.Button(root, textvariable= storedptext, command=lambda:storedpfunc(), font="Raleway",bg="#20bebe", fg="white", height=2,width=20)
        storedptext.set("STORED PROCEDURES")
        #okay button - works in insert
        okbuttontext = tk.StringVar()
        okbutton = tk.Button(root, textvariable= okbuttontext, command=lambda:okfunc(), font="Raleway",bg="#20bebe", fg="white", height=2,width=15)
        okbuttontext.set("OKAY")
        #okaybutton2 - works in queryfunc
        okbutton2 = tk.Button(root, textvariable= okbuttontext, command=lambda:queryokfunc(), font="Raleway",bg="#20bebe", fg="white", height=2,width=15)
        #query buttons - should set them up to show queries
        qb1text = tk.StringVar()
        qb1 = tk.Button(root, textvariable= qb1text, command=lambda:qb1func(), font="Raleway",bg="#20bebe", fg="white", height=2,width=20)
        qb1text.set("DisplayPatientInfo")
        
        qb2text = tk.StringVar()
        qb2 = tk.Button(root, textvariable= qb2text, command=lambda:qb2func(), font="Raleway",bg="#20bebe", fg="white", height=2,width=20)
        qb2text.set("AVG#MEDSbyPatientType")
        
        qb3text = tk.StringVar()
        qb3 = tk.Button(root, textvariable= qb3text, command=lambda:qb3func(), font="Raleway",bg="#20bebe", fg="white", height=2,width=20)
        qb3text.set("EmergencyAdmissionInfo")

        qb4text = tk.StringVar()
        qb4 = tk.Button(root, textvariable= qb4text, command=lambda:qb4func(), font="Raleway",bg="#20bebe", fg="white", height=2,width=20)
        qb4text.set("VisitsByAdmissionType")

        #custom query buttons
        cb1text = tk.StringVar()
        cb1 = tk.Button(root, textvariable= cb1text, command=lambda:cb1func(), font="Raleway",bg="#20bebe", fg="white", height=2,width=20)
        cb1text.set("Patients")

        cb2text = tk.StringVar()
        cb2 = tk.Button(root, textvariable= cb2text, command=lambda:cb2func(), font="Raleway",bg="#20bebe", fg="white", height=2,width=20)
        cb2text.set("Hospital Visits")

        #custom patients buttons
        patdatatext1 = StringVar()
        patdatab1 = tk.Button(root, textvariable= patdatatext1, command=lambda:alldatafunc(), font="Raleway",bg="#20bebe", fg="white", height=2,width=20)
        patdatatext1.set("ALL")

        patdatatext2 = StringVar()
        patdatab2 = tk.Button(root, textvariable= patdatatext2, command=lambda:PatientIDdatafunc(), font="Raleway",bg="#20bebe", fg="white", height=2,width=20)
        patdatatext2.set("PatientID")

        patdatatext3 = StringVar()
        patdatab3 = tk.Button(root, textvariable= patdatatext3, command=lambda:VisitIDdatafunc(), font="Raleway",bg="#20bebe", fg="white", height=2,width=20)
        patdatatext3.set("VisitID")

        #patients constraints buttons
        pconsttext1 = StringVar()
        pconstb1 = tk.Button(root, textvariable= pconsttext1, command=lambda:pmaleconstfunc(), font="Raleway",bg="blue", fg="white", height=2,width=20)
        pconsttext1.set("GENDER: MALE")

        pconsttext2 = StringVar()
        pconstb2 = tk.Button(root, textvariable= pconsttext2, command=lambda:pfemaleconstfunc(), font="Raleway",bg="pink", fg="white", height=2,width=20)
        pconsttext2.set("GENDER: FEMALE")

        pconsttext3 = StringVar()
        pconstb3 = tk.Button(root, textvariable= pconsttext3, command=lambda:ageOconstfunc(), font="Raleway",bg="#20bebe", fg="white", height=2,width=20)
        pconsttext3.set("AGE > 40")

        pconsttext4 = StringVar()
        pconstb4 = tk.Button(root, textvariable= pconsttext4, command=lambda:ageYconstfunc(), font="Raleway",bg="#20bebe", fg="white", height=2,width=20)
        pconsttext4.set("AGE < 40")

        #custom hospital visits buttons
        hosdatatext1 = StringVar()
        hosdatab1 = tk.Button(root, textvariable= hosdatatext1, command=lambda:alldatafunc(), font="Raleway",bg="#20bebe", fg="white", height=2,width=20)
        hosdatatext1.set("ALL")

        hosdatatext2 = StringVar()
        hosdatab2 = tk.Button(root, textvariable= hosdatatext2, command=lambda:LOSdatafunc(), font="Raleway",bg="#20bebe", fg="white", height=2,width=20)
        hosdatatext2.set("Length of Stay")

        hosdatatext3 = StringVar()
        hosdatab3 = tk.Button(root, textvariable= hosdatatext3, command=lambda:ADSdatafunc(), font="Raleway",bg="#20bebe", fg="white", height=2,width=20)
        hosdatatext3.set("Admission Source")

        #hospital constraints buttons
        hconsttext1 = StringVar()
        hconstb1 = tk.Button(root, textvariable= hconsttext1, command=lambda:emergencyconstfunc(), font="Raleway",bg="red", fg="black", height=2,width=20)
        hconsttext1.set("Admission: Emergency")

        hconsttext2 = StringVar()
        hconstb2 = tk.Button(root, textvariable= hconsttext2, command=lambda:electiveconstfunc(), font="Raleway",bg="green", fg="black", height=2,width=20)
        hconsttext2.set("Admission: Elective")

        hconsttext3 = StringVar()
        hconstb3 = tk.Button(root, textvariable= hconsttext3, command=lambda:longLOSconstfunc(), font="Raleway",bg="#20bebe", fg="white", height=2,width=20)
        hconsttext3.set("Visit Length > 4 days")

        hconsttext4 = StringVar()
        hconstb4 = tk.Button(root, textvariable= hconsttext4, command=lambda:shortLOSconstfunc(), font="Raleway",bg="#20bebe", fg="white", height=2,width=20)
        hconsttext4.set("Visit Length < 4 days")

        #main menu button
        mainmenutext = tk.StringVar()
        mainmenubutton = tk.Button(root, textvariable= mainmenutext, command=lambda:mainmenu(), font="Raleway",bg="yellow", fg="black", height=2,width=15)
        mainmenutext.set("Main Menu")
          
        #close button
        closetext = tk.StringVar()
        closebutton = tk.Button(root, textvariable= closetext, command=lambda:exit(), font="Raleway",bg="red", fg="black", height=2,width=15)
        closetext.set("EXIT")
        closebutton.place(x=1050,y=10)    

        #openbutton
        opentext = tk.StringVar()
        openbutton = tk.Button(root, textvariable= opentext, command=lambda:mainmenu(), font=("Raleway",20),bg="navy", fg="white", height=2,width=15)
        opentext.set("LOGIN")
        openbutton.place(x=900,y=475,anchor=CENTER)

        #confirmbutton
        confirmtext = tk.StringVar()
        confirmbutton = tk.Button(root, textvariable= confirmtext, command=lambda:confirmfunc(), font=("Raleway",20),bg="brown", fg="white", height=3,width=20)
        confirmtext.set("CONFIRM")

        #INSTRUCTIONS
        instructions = tk.Label(root, text="Select an action to continue:",font=("Arial",25))
        instructionsp = tk.Label(root, text="Select a Stored Procedure:",font=("Arial",25))
        insertinstructions = tk.Label(root, text="Enter the PatientID and click OKAY to continue.",font=("Arial",25))
        queryinstructions = tk.Label(root, text="Enter a custom Query and click OKAY to see results.",font=("Arial",25))
        custominstructions = tk.Label(root, text="Select which table to access:",font=("Arial",25))

        #LABELS
        PIDlabel=Label(root, text="PatientID:", font=("Courier 22 bold"))
        Agelabel=Label(root, text="Age:", font=("Courier 22 bold"))
        Weightlabel=Label(root, text="Weight:", font=("Courier 22 bold"))
        Genderlabel=Label(root, text="Gender:", font=("Courier 22 bold"))
        StoredPLabel=Label(root, text="Results:", font=("Courier 22 bold"))
        QueryResultsLabel = Label(root, text="Results:", font=("Courier 22 bold"))

        #Entries

        #insert entry
        entry= Entry(root, width= 40)
        entry.focus_set()
        #query entry
        qentry= Entry(root, width= 70)
        qentry.focus_set()



        root.mainloop()

#calls the class to start
databaseGUI()