from linebot.models import FlexSendMessage
from transitions import Machine
from flex_button import *
from db import *

nccu_lat = 24.9861694
nccu_long = 121.5749262

def GetWarn(event, GWSM):
    latitude = event.message.latitude
    longitude = event.message.longitude
    lat1 = min(latitude, nccu_lat) - 0.002
    lat2 = max(latitude, nccu_lat) + 0.002
    long1 = min(longitude, nccu_long) - 0.002
    long2 = max(longitude, nccu_long) + 0.002

    text = "在回家的路上會經過的求助地點如下：\n"
    res = getWarnPlaceInRange(lat1, long1, lat2, long2)
    num = 1
    for (DeptNm, BranchNm, Address, Contact) in res:
        place = DeptNm + BranchNm
        text += "%d:\n地點: %s\n地址: %s\n聯絡人:  %s" % (num, place, Address, Contact)
        num += 1

    message = FlexSendMessage(
        alt_text = '警示地點查詢結果',
        contents = getWarnMapFlex(text, latitude, longitude, 0, 0)
    )
    return message

class GetWarnStateMachine(object):

    states = ['default', 'locate']

    def __init__(self):

        self.start_location = {}
        self.machine = Machine(model=self, states=GetWarnStateMachine.states, initial='default')

        # add_transition(trigger, source, dest)
        self.machine.add_transition('reset', '*', 'default')
        self.machine.add_transition('locate', '*', 'locate')

# testing data:
# NCCU: 24.9861694,121.5749262