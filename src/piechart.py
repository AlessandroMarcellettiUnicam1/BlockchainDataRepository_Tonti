import flet as ft
import piechartsection
import stats


class PieChart(ft.PieChart):
    def __init__(self,event):
        super().__init__(
            center_space_radius=15,
            on_chart_event=event
        )
        self.update_sections()
    
    def update_sections(self):
        percentage = stats.get_percentage_activity_gas_used()
        self.sections.clear()
        for row in percentage.itertuples():
            self.sections.append(piechartsection.PieChartSection("%.2f"%float(row[3]*100),row[2],row[1]))