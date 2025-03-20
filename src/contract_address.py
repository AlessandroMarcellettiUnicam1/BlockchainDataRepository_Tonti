from newdefaultdict import addressdefaultdict,colordefaultdict

NAME_TO_ADDRESS = addressdefaultdict(None,{
    "oval3":"0x83a5564378839eef0721bc68a0fbeb92e2de73d2",
    "fantomMiner":"0x6f123c6347521325d3a6cf08517a73bd1d64f191",
    "pancakeSwap":"0x152649ea73beab28c5b49b26eb48f7ead6d4c898"
})

ADDRESS_TO_NAME = addressdefaultdict(None,{
    "0x83a5564378839eef0721bc68a0fbeb92e2de73d2":"oval3",
    "0x6f123c6347521325d3a6cf08517a73bd1d64f191":"fantomMiner",
    "0x152649ea73beab28c5b49b26eb48f7ead6d4c898":"pancakeSwap"
})


ADDRESS_TO_COLOR = colordefaultdict(None, {
    "0x83a5564378839eef0721bc68a0fbeb92e2de73d2":"GREEN",
    "0x6f123c6347521325d3a6cf08517a73bd1d64f191":"BLUE",
    "0x152649ea73beab28c5b49b26eb48f7ead6d4c898":"RED"
})
