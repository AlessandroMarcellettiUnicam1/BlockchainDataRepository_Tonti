import flet as ft
import contract_address
import stats
import math
import numpy as np

class LineChart(ft.LineChart):
    def __init__(self):
        super().__init__(
            width=1450
        )
        self.set_bottom_axis()
        self.set_data_series()
    
    def set_bottom_axis(self):
        labels = []
        _,time = stats.count_transaction_time()
        for t in time:
            labels.append(
                ft.ChartAxisLabel(
                    value=t[0],
                    label=ft.Text(str(np.datetime64(t[1].start,'D')),
                                rotate=ft.Rotate(-math.pi/6))
                )
            )
        self.bottom_axis = ft.ChartAxis(
                title=ft.Text("Time"),
                labels = labels,
                show_labels=True
            )

    def set_data_series(self):
        if(self.data_series!=None):
            self.data_series.clear()
        data,_ = stats.count_transaction_time()
        contract = stats.contract
        i = 1
        points = dict()
        for c in contract:
            points[c] = []
        for d in data:
            if(d.empty):
                for k in points.keys():
                    points[k].append(ft.LineChartDataPoint(i,0))
                i+=1
                continue
            for row in d.itertuples():
                points[row[1]].append(ft.LineChartDataPoint(i,row[2]))
            i+=1
        lines = []
        for k in points.keys():
            lines.append(
                ft.LineChartData(
                    data_points=points[k],
                    color=contract_address.ADDRESS_TO_COLOR[k]
                )
            )
        self.data_series.extend(lines)
