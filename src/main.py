import flet as ft
import piechart
import table
import tab
import table_function
import barchart
import stats
import numpy as np
import linechart
import contract_address

def main(page: ft.Page):
    def update_table_sender(e):
        data_sender = stats.get_most_active_sender()
        data_avg = stats.get_avg_gas_sender()
        rows = []
        for row in data_sender.itertuples():
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(
                            ft.Text(row[1])                            
                        ),
                        ft.DataCell(
                            ft.Text(row[2])
                        ),
                        ft.DataCell(
                            ft.Text("%.2f"%float(data_avg[data_avg["sender"]==row[1]]["gasUsed"].values[0]))
                            
                        )
                    ]  ,
                    on_select_changed=update_table_sender
                )
            )
            if(row[1]==e.control.cells[0].content.value):
                rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(
                                content=ft.Container(
                                        content= ft.DataTable(
                                        columns=[
                                            ft.DataColumn(label=ft.Text("Smart Contract")),
                                            ft.DataColumn(label=ft.Text("Occurrences"))
                                        ],
                                        rows=table_function.get_rows_most_used_contract(row[1]),
                                    )
                                )
                            ),
                            ft.DataCell(content=ft.Text("")),
                            ft.DataCell(content=ft.Text(""))
                        ],
                    )
                )
                for i in table_function.get_rows_most_used_contract(row[1]):
                    rows.append(
                        ft.DataRow(
                        cells=[
                            ft.DataCell(content=ft.Text("")),
                            ft.DataCell(content=ft.Text("")),
                            ft.DataCell(content=ft.Text(""))
                        ],
                    ))
        table_senders.rows.clear()
        table_senders.rows.extend(rows)
        page.update()

    
    def select_gas_table(e):
        if(selection_button_gas.selected=={"1"}):
            tab_gas.content.controls[1].controls[1] = ft.Container(content=table_gas)
        elif(selection_button_gas.selected=={"2"}):
            tab_gas.content.controls[1].controls[1] = ft.Container(content = table_avg_gas)
        tab_gas.update()
        page.update()

    def update_tables():
        table_gas.set_rows(table_function.get_rows_gas())
        table_avg_gas.set_rows(table_function.get_row_avg())
        table_senders.set_rows(table_function.get_row_sender(update_table_sender))
        table_activity.set_rows(table_function.get_row_count())
        table_input.set_rows(table_function.get_row_internal(stats.get_input_name))
        table_storage_state.set_rows(table_function.get_row_internal(stats.count_storage_state_variable_name))
        table_event.set_rows(table_function.get_row_internal(stats.count_event_type))
        table_call.set_rows(table_function.get_row_internal(stats.count_call_type))

    def update_charts():
        piechart_gas.update_sections()
        barchart_activity.set_bargroup(stats.get_activity_count)
        barchart_call.set_bargroup(stats.count_call_type)
        barchart_event.set_bargroup(stats.count_event_type)
        barchart_input.set_bargroup(stats.get_input_name)
        barchart_storage_state.set_bargroup(stats.count_storage_state_variable_name)
        time_chart.set_bottom_axis()
        time_chart.set_data_series()

    def piechart_event(e: ft.PieChartEvent):
        for idx, section in enumerate(piechart_gas.sections):
            if idx == e.section_index:
                section.title = section.activity
            else:
                section.title = str(section.value)+"%"
        piechart_gas.update()

    def submit(e):
        if(start_time.value!=""):
            stats.set_start_time(np.datetime64(start_time.value))
        if(end_time.value!=""):
            stats.set_end_time(np.datetime64(end_time.value))
        if(start_block.value!=""):
            stats.set_start_block(np.int64(start_block.value))
        if(end_block.value!=""):
            stats.set_end_block(np.int64(end_block.value))
        contracts = set()
        for i in selected_checkbox:
            contracts.add(contract_address.NAME_TO_ADDRESS[i])
        stats.set_contract(contracts)
        stats.update_filter()
        update_tables()
        update_charts()
        page.update()

    def reset(e):
        stats.reset_time()
        stats.reset_block()
        for c in checkbox:
            c.value = True
            selected_checkbox.add(c.label)
        start_time.value=""
        end_time.value=""
        start_block.value=""
        end_block.value=""
        stats.set_contract(stats.get_contract_address())
        stats.update_filter()
        update_tables()
        update_charts()
        page.update()
    
    def check_contract_selected(e):
        if e.control.value:
            selected_checkbox.add(e.control.label)
        else:
            if len(selected_checkbox) > 1:
                selected_checkbox.remove(e.control.label)
            else:
                e.control.value = True
                e.control.update()

    start_time = ft.TextField(label="Start time (YYYY-MM-DD)")
    end_time = ft.TextField(label="End time (YYYY-MM-DD)")
    start_block = ft.TextField(label="Start block")
    end_block = ft.TextField(label="End block")
    button_submit = ft.ElevatedButton(text = "Submit",on_click=submit)
    button_reset = ft.ElevatedButton(text="Reset",on_click=reset)
    piechart_gas = piechart.PieChart(piechart_event)
    table_gas = table.Table(
        table_function.get_column_gas(),
        table_function.get_rows_gas()
    )
    barchart_activity = barchart.BarChart(stats.get_activity_count,"#Activity")
    table_activity = table.Table(
        table_function.get_column_count(),
        table_function.get_row_count()
    )
    table_avg_gas = table.Table(
        table_function.get_column_avg(),
        table_function.get_row_avg()
    )
    table_senders = table.Table(table_function.get_column_sender(),table_function.get_row_sender(update_table_sender))
    input_time = ft.Row(
        controls = [
            start_time,
            end_time
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )
    input_block = ft.Row(
        controls = [
            start_block,
            end_block
        ],
        alignment=ft.MainAxisAlignment.CENTER
    )
    buttons = ft.Row(
        controls = [
            button_submit,
            button_reset
        ],
        alignment=ft.MainAxisAlignment.CENTER
    )
    
    selected_checkbox = set()
    checkbox = []
    for c in stats.get_contract_address().tolist():
        selected_checkbox.add(contract_address.ADDRESS_TO_NAME[c])
        checkbox.append(
            ft.Checkbox(
                label = contract_address.ADDRESS_TO_NAME[c],
                value=True,
                on_change=check_contract_selected
            )
        )
    contract_column = ft.Column(
        controls= checkbox,
        alignment=ft.MainAxisAlignment.CENTER,
        height = 200,
        wrap=True
    )
    selection_button_gas = ft.SegmentedButton(
        on_change=select_gas_table,
        selected={"1"},
        allow_multiple_selection=False,
        style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10)
            ),
        segments = [
            ft.Segment(
                value="1",
                label=ft.Text("Gas Used")
            ),
            ft.Segment(
                value="2",
                label=ft.Text("Average Gas Used")
            )
        ]
    )
    time_chart = linechart.LineChart()
    
    barchart_input = barchart.BarChart(stats.get_input_name,"#Input")
    barchart_event = barchart.BarChart(stats.count_event_type,"#Event")
    barchart_call = barchart.BarChart(stats.count_call_type,"#Call")
    barchart_storage_state = barchart.BarChart(stats.count_storage_state_variable_name,"#Variable name")
    table_input = table.Table(table_function.get_column_input(),table_function.get_row_internal(stats.get_input_name))
    table_storage_state = table.Table(table_function.get_column_storage_state(),
                                      table_function.get_row_internal(stats.count_storage_state_variable_name))
    table_event = table.Table(table_function.get_column_event(),table_function.get_row_internal(stats.count_event_type))
    table_call = table.Table(table_function.get_column_internal_txs(),table_function.get_row_internal(stats.count_call_type))
    tab_gas = tab.Tab("Gas used",chart=piechart_gas,table=table_gas,button=selection_button_gas)
    t = ft.Tabs(
        tabs = [
            tab_gas,
            tab.Tab("Activity",chart=barchart_activity,table=table_activity),
            tab.Tab("Most Active Senders",table=table_senders),
            tab.Tab("Time",chart=time_chart),
            tab.Tab("Inputs",chart=barchart_input,table=table_input),
            tab.Tab("Events",chart=barchart_event,table=table_event),
            tab.Tab("Call",chart=barchart_call,table=table_call),
            tab.Tab("Storage State",chart=barchart_storage_state,table=table_storage_state)
        ]
    )
    page.window.maximized=True
    page.scroll=ft.ScrollMode.AUTO
    page.add(input_time)
    page.add(input_block)
    page.add(contract_column)
    page.add(buttons)
    page.add(t)
    
    
ft.app(main)