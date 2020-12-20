from linebot.models import *
from linebot import LineBotApi
from transitions import Machine
from datetime import datetime, timedelta
import time

def ReturnHome(event, RHSM):
    # set target time
    target_time = parsetime(event.postback.params['time'])
    RHSM.time = target_time
    note = target_time.strftime("回家時間：%Y/%m/%d %H:%M")
    message = TextSendMessage(text=note)
    line_bot_api.reply_message(event.reply_token, message)
    RHSM.start_counting()

    current = datetime.now()
    while RHSM.state == 'counting' and current < target_time:
        time.sleep(10)
        current = datetime.now()

    if RHSM.state == 'default':
        return '回家行程取消'

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
    current = time.localtime()
    dateformat = "%Y/%m/%d"
    # date = current.strftime(dateformat)
    date = time.strftime(dateformat, current)
    result = datetime.strptime(date+' '+data, dateformat+' %H:%M')
    print(result, current)
    if result < current:
        print("here")
        result.day += 1
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