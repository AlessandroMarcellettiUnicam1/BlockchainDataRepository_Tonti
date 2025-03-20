import flet as ft

class Table(ft.DataTable):
    def __init__(self,column,row):
        super().__init__(
            column,
            row
        )
    
    def set_rows(self,new_rows):
        if(self.rows!=None):
            self.rows.clear()
        self.rows.extend(new_rows)
            
