import contract_address
import flet as ft

shade = [100,300,500,700,900]

i = {
    "0x83a5564378839eef0721bc68a0fbeb92e2de73d2":0,
    "0x6f123c6347521325d3a6cf08517a73bd1d64f191":0,
    "0x152649ea73beab28c5b49b26eb48f7ead6d4c898":0
}

def add_to_dict(key):
    if(key not in ACTIVITY_TO_COLOR):
        ACTIVITY_TO_COLOR[key]=getattr(ft.Colors,f"{contract_address.ADDRESS_TO_COLOR[key[0]]}_{shade[i.setdefault(key[0],0)]}")
        if(i[key[0]]<4):
            i[key[0]]+=1
        else:
            i[key[0]] = 0

ACTIVITY_TO_COLOR = dict()
