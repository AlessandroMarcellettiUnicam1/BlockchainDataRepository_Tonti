from transaction import get_transaction
import pandas as pd
import numpy as np
import range

transaction = get_transaction()

df = pd.DataFrame(transaction)
df["gasUsed"] = pd.to_numeric(df["gasUsed"], errors="coerce")
df["timestamp"] = pd.to_datetime(df["timestamp"].apply(lambda x : x["$date"] if isinstance(x,dict) else x),format="mixed",utc=True).dt.tz_localize(None)
df["blockNumber"] = pd.to_numeric(df["blockNumber"])
df_input = pd.json_normalize(transaction, "inputs", ["txHash","contractAddress","timestamp","blockNumber"],record_prefix="input.")
df_input["timestamp"] = pd.to_datetime(df_input["timestamp"].apply(lambda x : x["$date"] if isinstance(x,dict) else x),format="mixed",utc=True).dt.tz_localize(None)
df_input["blockNumber"] = pd.to_numeric(df_input["blockNumber"])
df_storageState = pd.json_normalize(transaction,"storageState",["txHash","contractAddress","timestamp","blockNumber"],record_prefix="storageState.")
df_storageState["timestamp"] = pd.to_datetime(df_storageState["timestamp"].apply(lambda x : x["$date"] if isinstance(x,dict) else x),format="mixed",utc=True).dt.tz_localize(None)
df_storageState["blockNumber"] = pd.to_numeric(df_storageState["blockNumber"])
df_internalTxs = pd.json_normalize(transaction,"internalTxs",["txHash","contractAddress","timestamp","blockNumber"],record_prefix="internalTxs.")
df_internalTxs["timestamp"] = pd.to_datetime(df_internalTxs["timestamp"].apply(lambda x : x["$date"] if isinstance(x,dict) else x),format="mixed",utc=True).dt.tz_localize(None)
df_internalTxs["blockNumber"] = pd.to_numeric(df_internalTxs["blockNumber"])
df_events = pd.json_normalize(transaction,"events",["txHash","contractAddress","timestamp","blockNumber"],record_prefix="events.")
df_events["timestamp"] = pd.to_datetime(df_events["timestamp"].apply(lambda x : x["$date"] if isinstance(x,dict) else x),format="mixed",utc=True).dt.tz_localize(None)
df_events["blockNumber"] = pd.to_numeric(df_events["blockNumber"])
time = range.Range(df["timestamp"].min(),df["timestamp"].max())
block = range.Range(df["blockNumber"].min(),df["blockNumber"].max())
time_filter = (df["timestamp"]>=time.start) & (df["timestamp"]<=time.end)
block_filter = ((df["blockNumber"]>=block.start) & (df["blockNumber"]<=block.end))
contract = set(df["contractAddress"].unique())
contract_filter = (df["contractAddress"].isin(contract))

def update_filter():
    global time_filter
    global block_filter
    global contract_filter
    time_filter=((df["timestamp"]>=time.start) & (df["timestamp"]<=time.end))
    block_filter = ((df["blockNumber"]>=block.start) & (df["blockNumber"]<=block.end))
    contract_filter = (df["contractAddress"].isin(contract))

def set_contract(c):
    global contract
    contract=c

def set_start_time(t):
    time.start=t

def set_end_time(t):
    time.end=t

def reset_time():
    time.start = df["timestamp"].min()
    time.end = df["timestamp"].max()

def set_start_block(b):
    block.start = b

def set_end_block(b):
    block.end = b

def reset_block():
    block.start = df["blockNumber"].min()
    block.end = df["blockNumber"].max()

def get_avg_gas():
    return df["gasUsed"][time_filter & block_filter & contract_filter].mean()

def get_avg_gas_contract():
    df_avg = df[time_filter & block_filter & contract_filter].groupby("contractAddress")["gasUsed"].mean().reset_index()
    return df_avg

def get_avg_gas_sender():
    df_avg_sender = df[time_filter & block_filter & contract_filter].groupby(["contractAddress","sender"])["gasUsed"].mean().reset_index()
    return df_avg_sender

def sender_transaction(sender):
    return df[(df["sender"] == sender) & time_filter & block_filter & contract_filter]

def most_smart_contract_used_sender(sender):
    d = sender_transaction(sender)
    return d.groupby("contractAddress").size().reset_index()

def get_all_sender():
    all_sender = df[time_filter & block_filter & contract_filter]["sender"].unique()
    return pd.DataFrame(all_sender,columns="sender")

def get_activity_count():
    count_df = df[time_filter & block_filter & contract_filter].groupby(["contractAddress","activity"]).size().reset_index()
    return count_df

def get_most_active_sender():
    return df[time_filter & block_filter & contract_filter].groupby("sender", as_index=False).size().sort_values("size",ascending=False).head()

def get_gas_used_activity():
    return df[time_filter & block_filter & contract_filter].groupby(["contractAddress","activity"])["gasUsed"].sum().reset_index()

def get_total_gas_used():
    return df[time_filter & block_filter & contract_filter]["gasUsed"].sum()

def get_percentage_activity_gas_used():
    total_gas_used = get_total_gas_used()
    data = get_gas_used_activity()
    data["gasUsed"]/=total_gas_used
    return data

def count_event_type():
    if(df_events.empty):
        return pd.DataFrame()
    f = ((df_events["timestamp"]>=time.start) & (df_events["timestamp"]<=time.end) &
          (df_events["blockNumber"]>=block.start) & (df_events["blockNumber"]<=block.end) & 
          df_events["contractAddress"].isin(contract))
    data = df_events[f].groupby(["contractAddress","events.eventName"]).size().reset_index()
    return data

def count_call_type():
    if(df_internalTxs.empty):
        return pd.DataFrame()
    f = ((df_internalTxs["timestamp"]>=time.start) & (df_internalTxs["timestamp"]<=time.end) &
          (df_internalTxs["blockNumber"]>=block.start) & (df_internalTxs["blockNumber"]<=block.end) & 
          df_internalTxs["contractAddress"].isin(contract))
    data = df_internalTxs[f].groupby(["contractAddress","internalTxs.callType"]).size().reset_index()
    return data

def count_storage_state_variable_name():
    if(df_storageState.empty):
        return pd.DataFrame()
    f = ((df_storageState["timestamp"]>=time.start) & (df_storageState["timestamp"]<=time.end) &
          (df_storageState["blockNumber"]>=block.start) & (df_storageState["blockNumber"]<=block.end) & 
          df_storageState["contractAddress"].isin(contract))
    data = df_storageState[f].groupby(["contractAddress","storageState.variableName"]).size().reset_index()
    return data

def get_input_name():
    if(df_input.empty):
        return pd.DataFrame()
    f = ((df_input["timestamp"]>=time.start) & (df_input["timestamp"]<=time.end) &
          (df_input["blockNumber"]>=block.start) & (df_input["blockNumber"]<=block.end) & 
          df_input["contractAddress"].isin(contract))
    data = df_input[f].groupby(["contractAddress","input.inputName","input.type"]).size().reset_index()
    return data

def count_transaction_time():
    time_range = range.Range(time.start,time.start+np.timedelta64(7,"D"))
    l = []
    t = []
    i = 1
    while(time_range.end<=time.end):
        l.append(df[(df["timestamp"]>=time_range.start) & (df["timestamp"]<time_range.end) & block_filter & contract_filter].groupby("contractAddress").size().reset_index())
        t.append((i,range.Range(time_range.start,time_range.end)))
        time_range.start,time_range.end = time_range.end,time_range.end+np.timedelta64(7,"D")
        i+=1
    return l,t

def get_contract_address():
    return df["contractAddress"].unique()
