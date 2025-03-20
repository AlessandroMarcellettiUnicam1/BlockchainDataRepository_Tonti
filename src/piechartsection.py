import flet as ft
import activity

class PieChartSection(ft.PieChartSection):
    def __init__(self,value,act,smart_contract):
        activity.add_to_dict((smart_contract,act))
        super().__init__(
            value,
            title= str(value)+"%",
            title_position=0.8,
            title_style=ft.TextStyle(color=ft.Colors.BLACK),
            color = activity.ACTIVITY_TO_COLOR[(smart_contract,act)],
            radius = 150,
        )
        self.activity = act