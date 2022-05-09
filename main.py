from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox
import os
from PyPDF4 import PdfFileMerger, PdfFileReader
import tempfile
import subprocess, platform
#from tkPDFViewer import tkPDFViewer as pdf

# Class defining the application
class app():
    
    # Initialisation function
    def __init__(self):
        
        # Create the window
        self.mainWindow = Tk()
        
        # Set the title of the window
        self.mainWindow.title("Vinay's PDF merger")
        
        # Set the geometry of the window
        self.mainWindow.geometry("300x400")

        self.mainWindow.resizable(False, False)
        
        # Initialise list to hold the file path
        self.files = []
        
        # Define the possible file types
        self.filetypes = (('PDFs', '*.pdf'),('All Files', "*.*"))
        
        
        # Create frame to hold file list
        self.frame = Frame(self.mainWindow)
        
        # Add scroll bar to the frame for the file list
        self.scrollbar = Scrollbar(self.frame, orient = VERTICAL)

        # Create the file list
        self.fileList = Listbox(self.frame, yscrollcommand = self.scrollbar.set, width=self.mainWindow.winfo_width(), selectmode="multiple")
        
        # Create a right click menu for selected items in the file list
        self.fileList.popup_menu = Menu(self.fileList, tearoff=0)
        
        # Add a delete option to that right click menu
        self.fileList.popup_menu.add_command(label="Delete",
                                    command=self.delete_selected)
                                    
        # Add a select all option to the right click menu
        self.fileList.popup_menu.add_command(label="Select All",
                                    command=self.select_all)
                                    
        # Bind right click on items in the filelist Note: Button-3 on windows, Button-2 mac
        self.fileList.bind("<Button-2>", self.popup)
        
        # Bind scroll bar to the yview of the filelist
        self.scrollbar.config(command=self.fileList.yview)
        
        # Pack the scrollbar
        self.scrollbar.pack(side=RIGHT, fill = Y)
        
        # Pack the frame holding the file list
        self.frame.pack(expand=True, padx=10, pady =10, fill=BOTH,)
        
        # Pack the file list
        self.fileList.pack(expand = True, fill=BOTH)

        
        # Create frame to hold the buttons
        self.frame2 = Frame(self.mainWindow, width = self.mainWindow.winfo_width())
        
        # Add browse button
        self.browseButton = Button(self.frame2, text = "Browse", width = 8, command = self.getFiles)
        
        # Add merge button
        self.mergeButton = Button(self.frame2, text = "Merge", width = 8, command = self.mergeFiles)
        
        # Add preview button
        self.previewButton = Button(self.frame2, text = "Preview", width = 8, command = self.previewFile)

        # Add about button
        self.aboutButton = Button(self.frame2, text = "About", width = 8, command = self.showAbout)
        
        # Pack browse button
        self.browseButton.grid(row = 0, column = 0)
        
        # Pack merge button
        self.mergeButton.grid(row = 0, column = 1)
        
        # Pack the preview button
        self.previewButton.grid(row = 1, column = 0)

        # Pack the about button
        self.aboutButton.grid(row = 1, column = 1)
        
        # Pack the frame holding the buttons
        self.frame2.pack(expand = True, padx =5)
        
    # Function to browse to pdf files
    def getFiles(self):

        # Browse for files
        files = fd.askopenfilenames(
            title='Select PDFs to merge',
            initialdir='/',
            filetypes=self.filetypes)
        
        # Split the path away from the file names, insert names into list and save paths and filenames
        for i in files:
            self.files.append(i)
            self.fileList.insert('end', os.path.split(i)[1])
        
    # Function to show right click menu
    def popup(self, event):
        try:
            self.fileList.popup_menu.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.fileList.popup_menu.grab_release()

    # Function to deleted selected items in the list
    def delete_selected(self):
        for i in self.fileList.curselection()[::-1]:
            self.files.pop(i)
            self.fileList.delete(i)

    # Function to select all items in the list
    def select_all(self):
        self.fileList.selection_set(0, 'end')
    
    # Function to merge the files
    def mergeFiles(self):
    
        # Checks if there are actually items to merge and handles accordingly
        if len(self.files) == 0:
            return
        else:
        
            # Instantiates the pdffilemerger object
            merger = PdfFileMerger()
        
            # Iterate over the files and read them in
            for i in self.files:
                merger.append(PdfFileReader(open(i, 'rb')))
                
            # Get the name of the file to save to
            file = fd.asksaveasfile(filetypes = self.filetypes, defaultextension = self.filetypes)
            
            # Write the merged pdf
            merger.write(file.name)
            
            merger.close()
            return
            
     # Function to peview the pdf
    def previewFile(self):
    
        # Checks if there are actually items to merge and handles accordingly
        if len(self.files) == 0:
            return
        else:
        
            # Instantiates the pdffilemerger object
            merger = PdfFileMerger()
        
            # Iterate over the files and read them in
            for i in self.files:
                merger.append(PdfFileReader(open(i, 'rb')))
                
            # Get the name of the file to save to
            file = tempfile.NamedTemporaryFile()
            
            # Write the merged pdf
            merger.write(file.name+".pdf")
            
            merger.close()
            if platform.system() == 'Darwin':       # macOS
                subprocess.call(('open', file.name+".pdf"))
               
            elif platform.system() == 'Windows':    # Windows
                os.startfile(file.name+".pdf")
            else:                                   # linux variants
                subprocess.call(('xdg-open', file.name+".pdf"))
            
            file.close()
            
            # todo: create in house pdf viewer to avoid spam pdf files
            '''
                        # Initializing tk
            root = Tk()
              
            # Set the width and height of our root window.
            root.geometry("550x750")
              
            # creating object of ShowPdf from tkPDFViewer.
            v1 = pdf.ShowPdf()
              
            # Adding pdf location and width and height.
            v2 = v1.pdf_view(root,
                             pdf_location = file.name,
                             width = 50, height = 100)
              
            # Placing Pdf in my gui.
            v2.pack()
            root.mainloop()
            '''
            return
    def showAbout(self):
        messagebox.showerror("About", "Created by Vinay", icon = 'info')
    
        

# Main function
def main():

    # Create application
    mainWindow = app()
    
    # Loop application
    mainWindow.mainWindow.mainloop()
    return

if __name__ == "__main__":
    main()
    exit(0)
