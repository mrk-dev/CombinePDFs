'''
Name       : combine_gui.py
Description: Defines the GUI for the Combine PDFs application
Date       : 22-Jan-2023
Author     : M. Schmidt

'''

import datetime
import os
import tkinter as tk
import tkinter.ttk as ttk

from tkinter import filedialog
from tkinter import messagebox

import combine_helper as ch


def create_window():
    '''
    Creates a window object for tkinter app initialization
    '''
    return tk.Tk()


class Application(tk.Frame):
    '''
    Class to define the Combine PDF GUI
    '''

    def __init__(self, master=None, pdf_folder=None, out_file=None, monitor_delay=-1):
        tk.Frame.__init__(self, master)
        self.PARENT = master
        master.title("Combine PDF Files")
        master.minsize(480, 85)
        master.resizable(height=False, width=True)
        master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(0, weight=1)
        master.iconbitmap("./combine.ico")

        self.monitorid = None
        self.monitordelay = monitor_delay

        self.grid(row=0, column=0, sticky=tk.N+tk.E+tk.W+tk.S)
        self.createWidgets()
        if not pdf_folder is None:
            self.FOLDERENTRY.insert(0, pdf_folder)
        if not out_file is None:
            self.OUTFILEENTRY.insert(0, out_file)

        self.rowconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(2, weight=1)
        master.lift()


    def createWidgets(self):
        self.FOLDERLABEL = ttk.Label(self, text="PDF Folder:")
        self.FOLDERLABEL.grid(row = 0, column = 0, sticky=tk.W, pady = 2, padx = 2)
        
        self.FOLDERENTRY = ttk.Entry(self)
        self.FOLDERENTRY.grid(row = 0, column = 1, columnspan = 3, sticky=tk.W+tk.E, pady = 2, padx = 2)

        self.FOLDERBROWSE = ttk.Button(self)
        self.FOLDERBROWSE["text"] = "..."
        self.FOLDERBROWSE["command"] = self.show_browse_folder_dialog
        self.FOLDERBROWSE.config(width = 3)
        self.FOLDERBROWSE.grid(row = 0, column = 4, padx=2, pady = 2, sticky=tk.W)
        self.FOLDERBROWSE.bind("<Enter>", self.folderbrowse_on_enter) 
        self.FOLDERBROWSE.bind("<Leave>", self.folderbrowse_on_exit)

        self.OUTFILELABEL = ttk.Label(self, text="Output File:")
        self.OUTFILELABEL.grid(row = 1, column = 0, sticky=tk.W, pady = 2, padx = 2)

        self.OUTFILEENTRY = ttk.Entry(self)
        self.OUTFILEENTRY.grid(row = 1, column = 1, columnspan = 3, sticky=tk.W+tk.E, pady = 2, padx = 2)

        self.OUTFILEBROWSE = ttk.Button(self)
        self.OUTFILEBROWSE["text"] = "..."
        self.OUTFILEBROWSE["command"] = self.show_saveas_dialog
        self.OUTFILEBROWSE.config(width = 3)
        self.OUTFILEBROWSE.grid(row = 1, column = 4, padx=2, pady = 2, sticky=tk.W)
        self.OUTFILEBROWSE.bind("<Enter>", self.outfilebrowse_on_enter) 
        self.OUTFILEBROWSE.bind("<Leave>", self.outfilebrowse_on_exit)

        self.AUTOFRAME = tk.Frame(self)
        self.AUTOFRAME.grid(row = 2, column = 0, columnspan = 3, sticky=tk.W)
        self.AUTOFRAME.bind("<Enter>", self.autoframe_on_enter) 
        self.AUTOFRAME.bind("<Leave>", self.autoframe_on_exit)

        self.AUTOVAR = tk.BooleanVar()
        self.CHECKAUTO = ttk.Checkbutton(self.AUTOFRAME, variable = self.AUTOVAR, command=self.autocheck)
        self.CHECKAUTO["text"] = "Automatic combine every"
        self.CHECKAUTO.grid(row = 0, column = 0, padx = 2, pady = 2)
        
        validate_cmd = (self.register(self.delay_validate)) 
        self.DELAYENTRY = ttk.Entry(self.AUTOFRAME, validate="all", validatecommand=(validate_cmd, "%P"), width=4)
        self.DELAYENTRY.grid(row = 0, column = 3, padx = 2, pady = 2)
        self.DELAYENTRY.delete(0, tk.END)
        if self.monitordelay == -1:
            self.DELAYENTRY.insert(0, "5")
        else:
            self.DELAYENTRY.insert(0, str(self.monitordelay))
        self.DELAYENTRY["state"] = "disabled"
        self.DELAYENTRY.bind("<FocusOut>", self.delay_focus_out)

        self.DELAYLABEL = ttk.Label(self.AUTOFRAME)
        self.DELAYLABEL["text"] = "seconds"
        self.DELAYLABEL.grid(row = 0, column = 4, padx = 2, pady = 2)

        self.HELPTIP = ttk.Label(self)
        self.HELPTIP.grid(row = 3, column = 0, columnspan = 3, sticky=tk.W)

        self.BUTTONFRAME = tk.Frame(self)
        self.BUTTONFRAME.grid(column = 4, row = 3, sticky=tk.S+tk.E, ipady=2, ipadx=2)

        self.OK = ttk.Button(self.BUTTONFRAME)
        self.OK["text"] = "Combine"
        self.OK["command"] = self.combine_pdfs
        self.OK.grid(column = 0, row = 1)
        self.OK.bind("<Enter>", self.ok_on_enter) 
        self.OK.bind("<Leave>", self.ok_on_exit)

        self.CANCEL = ttk.Button(self.BUTTONFRAME)
        self.CANCEL["text"] = "Close"
        self.CANCEL["command"] = self.quit
        self.CANCEL.grid(column = 1, row = 1)
        self.CANCEL.bind("<Enter>", self.cancel_on_enter) 
        self.CANCEL.bind("<Leave>", self.cancel_on_exit)
   

    def delay_validate(self, value):
        if value == "": return True
        if str.isdigit(value):
            if int(value) <= 9999:
                return True
            else:
                return False
        else:
            return False
        

    def delay_focus_out(self, event):
        delay = self.DELAYENTRY.get()
        self.set_monitor(delay)


    def set_monitor(self, delay_in_seconds):
      if str(delay_in_seconds) != str(self.monitordelay):
          print("Changing monitor delay to {0} seconds".format(delay_in_seconds))
          if not self.monitorid is None:
            self.PARENT.after_cancel(self.monitorid)
            self.monitordelay = -1
          if str.isdigit(str(delay_in_seconds)):
                self.monitorid = self.PARENT.after(int(delay_in_seconds) * 1000, self.monitor)
                self.monitordelay = int(delay_in_seconds)


    def monitor(self):
        print("Checking for pdfs...")
        try:
            outfile = ch.get_outfile_name(self.OUTFILEENTRY.get())
            pdf_folder = self.FOLDERENTRY.get()
            pdfs = ch.get_pdfs(self.FOLDERENTRY.get())
        
            if len(pdfs) <= 1:
                self.HELPTIP["text"] = "{0} PDF files found. Must be 2 or more".format(len(pdfs))
            elif len(outfile) == 0:
                self.HELPTIP["text"] = "Not a valid output file"
            elif len(pdf_folder) > 0 and len(outfile) > 0:
                pdf_count = ch.combinepdfs(self.FOLDERENTRY.get(), outfile)
                self.HELPTIP["text"] = "Combined {0} pdfs at {1}".format(pdf_count, datetime.datetime.now().strftime("%I:%M:%S%p"))

                # clean up
                ch.delete_pdfs(pdfs)
                
        except Exception as e:
            print("***WARNING*** could not automatically merge: {0}".format(e))
        finally:
            # re-establish monitoring
            delay = self.monitordelay
            self.monitordelay = -1
            self.set_monitor(delay)


    def show_saveas_dialog(self):
        dialog = filedialog.SaveAs(self, filetypes=[("PDF Files", ".pdf")])
        filename = dialog.show()
        if len(filename) > 0:
            filename = self._checkfile(filename)
            self.OUTFILEENTRY.delete(0, tk.END)
            self.OUTFILEENTRY.insert(0,filename)
    

    def show_browse_folder_dialog(self):
        filename = filedialog.askdirectory()
        self.FOLDERENTRY.delete(0, tk.END)
        self.FOLDERENTRY.insert(0,filename)


    def autocheck(self):
        if not self.AUTOVAR.get():
            self.OK["state"] = "normal"
            self.DELAYENTRY["state"] = "disabled"
            self.set_monitor("-1")
        else:
            self.OK["state"] = "disabled"
            self.DELAYENTRY["state"] = "normal"
            self.set_monitor(self.DELAYENTRY.get())


    def combine_pdfs(self):
        # Make sure file has pdf extension
        filename = self._checkfile(self.OUTFILEENTRY.get())
        if filename.lower() != self.OUTFILEENTRY.get().lower():
            self.OUTFILEENTRY.delete(0, tk.END)
            self.OUTFILEENTRY.insert(0,filename)

        try:
            file_count = ch.combinepdfs(self.FOLDERENTRY.get(), filename)
            messagebox.showinfo("Combine PDFs", "Successfully combined {0} PDF files.".format(file_count))
        except Exception as e:
            messagebox.showerror("Combine PDFs", "***ERROR*** Unable to combine PDF files\n{0}".format(e))


    def _checkfile(self, filename):
        if len(filename) > 0:
            fname, fext = os.path.splitext(filename)
            if fext.lower() != ".pdf":
                filename += ".pdf"

        return filename


    def folderbrowse_on_enter(self, event):
        self.HELPTIP.configure(text="Browse for folder with PDFs")


    def folderbrowse_on_exit(self, event):
        self.HELPTIP.configure(text="")


    def autoframe_on_enter(self, event):
        self.HELPTIP.configure(text="Automatically combine pdfs in folder at specified interval")


    def autoframe_on_exit(self, event):
        self.HELPTIP.configure(text="")


    def outfilebrowse_on_enter(self, event):
        self.HELPTIP.configure(text="Browse for output PDF file")


    def outfilebrowse_on_exit(self, event):
        self.HELPTIP.configure(text="")


    def ok_on_enter(self, event):
        self.HELPTIP.configure(text="Combine PDFs in PDF Folder to Output File")


    def ok_on_exit(self, event):
        self.HELPTIP.configure(text="")


    def cancel_on_enter(self, event):
        self.HELPTIP.configure(text="Close application")


    def cancel_on_exit(self, event):
        self.HELPTIP.configure(text="")
            
