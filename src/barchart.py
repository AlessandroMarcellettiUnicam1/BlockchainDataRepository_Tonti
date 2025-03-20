import flet as ft
import contract_address
import activity
import stats
import math

class BarChart(ft.BarChart):
    def __init__(self,fun,title):
        super().__init__(
            left_axis=ft.ChartAxis(
                title=ft.Text(title),
                title_size=40,
                show_labels=False,                
            ),
            
            border = ft.border.only(bottom=ft.border.BorderSide(1, ft.Colors.GREY_400),
                                    left=ft.border.BorderSide(1, ft.Colors.GREY_400)),
            horizontal_grid_lines=ft.ChartGridLines(
                color=ft.Colors.GREY_300,
                width=1,
                dash_pattern=[3, 3],
                interval=10
            ),
            tooltip_bgcolor=ft.Colors.WHITE
        )
        self.set_bargroup(fun)

    def set_bargroup(self,fun):
        if(self.bottom_axis!=None and self.bar_groups!=None):
            self.bottom_axis.labels.clear()
            self.bar_groups.clear()
        df = fun()
        bottom_label = []
        label_index = 2
        y_index = 3 if not fun==stats.get_input_name else 4
        i = 0
        max_value = df[0].max()
        if(max_value>100):
            d=10
        else:
            d=1
        for row in df.itertuples():
            if(len(row[label_index])>18):
                text = row[label_index][0:18]+"..."
            else:
                text = row[label_index]
            bottom_label.append(
                ft.ChartAxisLabel(
                    value = i,
                    label = ft.Container(content=ft.Text(text,rotate=ft.Rotate(-math.pi/6)))
                )
            )
            self.bar_groups.append(
                ft.BarChartGroup(
                    x = i,
                    bar_rods=[
                        ft.BarChartRod(
                            from_y = 0,
                            to_y = row[y_index]/d,
                            width = 20,
                            tooltip = str(row[y_index]),
                            border_radius=0,
                            color = activity.ACTIVITY_TO_COLOR.get((row[1],row[label_index]),contract_address.ADDRESS_TO_COLOR[row[1]]),
                            tooltip_style = ft.TextStyle(color=ft.Colors.BLACK)
                        )
                    ]
                )
            )
            i+=1
        self.bottom_axis = ft.ChartAxis(
                labels = bottom_label
            )
