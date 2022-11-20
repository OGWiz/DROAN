import pandas as pd
from tkinter import *
from pandastable import Table

class TableApp(Frame):
        """Basic test frame for the table"""
        def __init__(self, parent=None):
            self.parent = parent
            Frame.__init__(self)
            self.main = self.master
            self.main.geometry('600x400+200+100')
            self.main.title('Results')
            f = Frame(self.main)
            f.pack(fill=BOTH,expand=1)
            df = pd.read_excel('outputs/clean_detections.xlsx')
            self.table = pt = Table(f, dataframe=df,
                                    showtoolbar=True, showstatusbar=True)
            pt.show()
            return

if __name__ == '__main__':
    app = TableApp()
    #launch the app
    app.mainloop()