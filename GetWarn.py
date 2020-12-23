from linebot.models import FlexSendMessage
from transitions import Machine
from flex_button import *

def GetWarn(event, GWSM):
    latitude = event.message.latitude
    longitude = event.message.longitude
    message = FlexSendMessage(
        alt_text = '警示地點查詢結果',
        contents = getWarnMapFlex(latitude, longitude, 0, 0)
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