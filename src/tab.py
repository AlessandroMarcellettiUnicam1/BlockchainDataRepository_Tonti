import flet as ft

class Tab(ft.Tab):
    def __init__(self,tab_text,chart=None,table=None,button=None):
        if(chart!=None and table!=None and button==None):
            super().__init__(
                text = tab_text,
                content=ft.GridView(
                    controls=[
                        ft.Container(content=chart),
                        ft.Container(content=table, expand= True)
                    ],
                    runs_count=2,
                    padding = 15
                )
            )
        elif(chart!=None and table!=None and button!=None):
            super().__init__(
                text = tab_text,
                content=ft.Column(
                    controls=[
                        ft.Container(
                            content=button,
                            expand=True,
                            height=60,
                            alignment=ft.alignment.center
                        ),
                        ft.GridView(
                            controls=[
                                ft.Container(content=chart),
                                ft.Container(content=table)
                            ],
                            runs_count=2,
                            padding=0,
                            spacing=5
                        )  
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=5
                )
            )
        elif(chart!=None and table==None and button==None):
            super().__init__(
                text = tab_text,
                content=ft.Column(
                    controls = [
                        ft.Container(
                            content=chart,
                            margin = ft.margin.only(left=20)
                        )
                    ]
                )
            )
        elif(chart==None and table!=None and button==None):
            super().__init__(
                text = tab_text,
                content=ft.GridView(
                    controls=[table],
                    runs_count=1
                )
            )
