from linebot.models import *
from transitions import Machine
from datetime import datetime, timedelta, timezone
import time
from flex_button import *

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

def GiveWarn():
    return

def WarnContact():
    return

def getNow():
    return datetime.utcnow().astimezone(timezone(timedelta(hours=8)))

def parsetime(data):
    current = getNow()
    dateformat = "%Y/%m/%d"
    date = current.strftime(dateformat)
    result = datetime.strptime(date+' '+data, dateformat+' %H:%M')
    result = result.replace(tzinfo=timezone(timedelta(hours=8)))
    if result < current:
        result = result + timedelta(days=1)
    return result
        
def printTime(current, target):
    dateformat = "%Y/%m/%d %H:%M:%S"
    print("current: {}, target: {}"
        .format(current.strftime(dateformat), target.strftime(dateformat)))

def ReturnHome(line_bot_api, event, RHSM):
    user_id = event.source.user_id

    # set target time
    target_time = parsetime(event.postback.params['time'])
    target_time = target_time.astimezone(timezone(timedelta(hours=8)))
    RHSM.time = target_time

    note = target_time.strftime("預計回家時間：%Y/%m/%d %H:%M")
    message = TextSendMessage(text=note, quick_reply=arriveHomeButton())
    line_bot_api.reply_message(event.reply_token, message)
    RHSM.start_counting()

    current = getNow()
    while RHSM.state == 'counting' and current < target_time:
        printTime(current, target_time)
        time.sleep(10)
        current = getNow()

    if RHSM.state == 'default':
        return '歡迎回家:)'

    note = "預計回家時間已到，你到家了嗎？如果一分鐘後還沒到家，我會聯絡你的緊急聯絡人喔！"
    message = TextSendMessage(text=note, quick_reply=arriveHomeButton())
    line_bot_api.push_message(user_id, message)
    RHSM.warn()

    target_time = target_time + timedelta(seconds=30)
    current = getNow()
    while RHSM.state == 'warning' and current < target_time:
        printTime(current, target_time)
        time.sleep(10)
        current = getNow()

    if RHSM.state == 'default':
        return '歡迎回家:)'

    WarnContact()
    return '呼叫緊急聯絡人'

def WarnContact():
    return

class ReturnHomeMachine(object):

    states = ['default', 'set_time', 'counting', 'warning']

    def __init__(self):
        self.machine = Machine(model=self, states=ReturnHomeMachine.states, initial='default')
        self.time = ''

        # add_transition(trigger, source, dest)
        self.machine.add_transition('reset', '*', 'default')
        self.machine.add_transition('set_time', '*', 'set_time')
        self.machine.add_transition('start_counting', 'set_time', 'counting')
        self.machine.add_transition('warn', 'counting', 'warning')


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