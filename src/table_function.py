import flet as ft
import stats
import contract_address

def get_rows_gas():
    data = stats.get_gas_used_activity()
    rows = []
    for row in data.itertuples():
        rows.append(ft.DataRow(
            cells = [
                ft.DataCell(ft.Text(contract_address.ADDRESS_TO_NAME[row[1]])),
                ft.DataCell(ft.Text(row[2])),
                ft.DataCell(ft.Text(row[3]))
            ]
        ))
    rows.append(ft.DataRow(
            cells = [
                ft.DataCell(ft.Text("Total")),
                ft.DataCell(ft.Text("")),
                ft.DataCell(ft.Text(stats.get_total_gas_used()))
            ]
        ))
    return rows

def get_column_gas():
    return [
            ft.DataColumn(ft.Text("Smart Contract")),
            ft.DataColumn(ft.Text("Activity")),
            ft.DataColumn(ft.Text("Gas Used"))
        ]

def get_column_count():
    return [
        ft.DataColumn(ft.Text("Smart Contract")),
        ft.DataColumn(ft.Text("Activity")),
        ft.DataColumn(ft.Text("Count"))
    ]

def get_row_count():
    data = stats.get_activity_count()
    total = 0
    rows = []
    for row in data.itertuples():
        rows.append(ft.DataRow(
            cells = [
                ft.DataCell(ft.Text(contract_address.ADDRESS_TO_NAME[row[1]])),
                ft.DataCell(ft.Text(row[2])),
                ft.DataCell(ft.Text(row[3]))
            ]
        ))
        total+=row[3]
    rows.append(ft.DataRow(
            cells = [
                ft.DataCell(ft.Text("Total")),
                ft.DataCell(ft.Text("")),
                ft.DataCell(ft.Text(total))
            ]
        ))
    return rows

def get_column_sender():
    return [
        ft.DataColumn(ft.Text("Sender")),
        ft.DataColumn(ft.Text("#Transaction")),
        ft.DataColumn(ft.Text("Average gas used"))
    ]

def get_rows_most_used_contract(sender):
    data_contract_address = stats.most_smart_contract_used_sender(sender)
    rows = []
    for d in data_contract_address.itertuples():
        rows.append(
            ft.DataRow(
                cells = [
                    ft.DataCell(
                        content=ft.Text(contract_address.ADDRESS_TO_NAME[d[1]])
                        
                    ),
                    ft.DataCell(
                        content=ft.Text(d[2])
                    )
                ]
            )
        )
    return rows


def get_row_sender(function):
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
                on_select_changed=function
            )
        )
    return rows

def get_column_avg():
    return [
        ft.DataColumn(ft.Text("Smart Contract")),
        ft.DataColumn(ft.Text("Average gas used"))
    ]

def get_row_avg():
    data = stats.get_avg_gas_contract()
    data_avg = stats.get_avg_gas()
    rows = []
    for row in data.itertuples():
        rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(
                            ft.Text(contract_address.ADDRESS_TO_NAME[row[1]])                            
                    ),
                    ft.DataCell(
                        ft.Text("%.2f"%float(row[2]))
                    )
                ]
            )
        )
    rows.append(
        ft.DataRow(
            cells=[
                ft.DataCell(
                    ft.Text("All")
                ),
                ft.DataCell(
                    ft.Text("%0.2f"%data_avg)
                )
            ]
        )
    )
    return rows

def get_row_internal(function):
    data = function()
    rows = []
    for row in data.itertuples():
        contract_name = contract_address.ADDRESS_TO_NAME[row[1]]
        if(len(contract_name)>20):
            contract_name = contract_name[0:20]+"..."
        if(function!=stats.get_input_name):
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(
                            ft.Text(contract_name)                            
                        ),
                        ft.DataCell(
                            ft.Text(row[2])
                        ),
                        ft.DataCell(
                            ft.Text(row[3])
                        )
                    ]
                )
            )
        else:
            input_name = row[2]
            if(len(input_name)>18):
                input_name = row[2][0:18]+"..."
            rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(
                        ft.Text(contract_name)                            
                    ),
                    ft.DataCell(
                        ft.Text(input_name)
                    ),
                    ft.DataCell(
                        ft.Text(row[3])
                    ),
                    ft.DataCell(
                        ft.Text(row[4])
                    )
                ]
            )
        )
    return rows

def get_column_storage_state():
    return [
        ft.DataColumn(ft.Text("Smart Contract")),
        ft.DataColumn(ft.Text("Variable Name")),
        ft.DataColumn(ft.Text("Occurrences"))
    ]

def get_column_input():
    return [
        ft.DataColumn(ft.Text("Smart Contract")),
        ft.DataColumn(ft.Text("Input Name")),
        ft.DataColumn(ft.Text("Input Type")),
        ft.DataColumn(ft.Text("Occurrences"))
    ]

def get_column_event():
    return [
        ft.DataColumn(ft.Text("Smart Contract")),
        ft.DataColumn(ft.Text("Event Name")),
        ft.DataColumn(ft.Text("Occurrences"))
    ]

def get_column_internal_txs():
    return [
        ft.DataColumn(ft.Text("Smart Contract")),
        ft.DataColumn(ft.Text("Call Type")),
        ft.DataColumn(ft.Text("Occurrences"))
    ]