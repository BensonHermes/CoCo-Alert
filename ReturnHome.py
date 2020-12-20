from linebot.models import *
from transitions import Machine
from datetime import datetime, timedelta

def StartReturnHome(RHSM):
    current = datetime.now()
    while RHSM.state == 'counting' and current < RHSM.time:
    return


def SetReturnHomeTime():
    message = TemplateSendMessage(
        alt_text = '選擇回家時間',
        template = ButtonsTemplate(
            title = '回家時間',
            text = '請選擇到家的時間',
            actions = [
                {
                    'type': 'datetimepicker',
                    'label': '選擇時間',
                    'data': 'return_home_time',
                    'mode': 'time'
                }
            ]
        )
    )
    return message

def parsetime(data):
    current = datetime.now()
    dateformat = "%Y/%m/%d"
    date = datetime.strftime(dateformat, current)
    result = datetime.strptime(date+' '+data, dateformat+' %H:%M')
    if result < current:
        result = result + timedelta(day=1)
    return result
        

class ReturnHomeMachine(object):

    states = ['default', 'set_time', 'counting', 'warning']

    def __init__(self):
        self.machine = Machine(model=self, states=ReturnHomeMachine.states, initial='default')
        self.time = ''

        # add_transition(trigger, source, dest)
        self.machine.add_transition('reset', '*', 'default')
        self.machine.add_transition('set_time', '*', 'set_time')
        self.machine.add_transition('start_counting', 'set_time', 'counting')
        self.machine.add_transition('warn', 'counting', 'waning')


# def StartReturnHome():
#     message = TemplateSendMessage(
#         alt_text = '設置出發點',
#         template = ButtonsTemplate(
#             title = '出發點',
#             text = '設置返家的出發點',
#             actions = [
#                 MessageTemplateAction(
#                     label='使用常用位置',
#                     text='使用常用位置'
#                 ),
#                 MessageTemplateAction(
#                     label='選擇位置',
#                     text='選擇位置'
#                 )
#             ]
#         )
#     )
#     return message