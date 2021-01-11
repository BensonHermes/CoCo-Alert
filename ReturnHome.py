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

def ReturnHome(line_bot_api, event, BISM, RHSM):
    user_id = event.source.user_id

    # set target time
    target_time = parsetime(event.postback.params['time'])
    target_time = target_time.astimezone(timezone(timedelta(hours=8)))
    # RHSM.time = target_time

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
        if RHSM.arrived:
            return '歡迎回家:)'
        else:
            return '行程取消'

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
        if RHSM.arrived:
            return '歡迎回家:)'
        else:
            return '行程取消'

    contact_info = []
    if BISM.info.ready:
        contact_info = [BISM.info.contact_name, BISM.info.contact_token]
    else:
        contact_info = getContactInfo(user_id)[0]
    # contact_id = "U0ed3d02a2d6e794697b114d7977d48aa"
    note = f"{BISM.info.name}到了預計時間還沒回家，請快確認他的人身安全吧！"
    message = TextSendMessage(text=note)
    line_bot_api.push_message(contact_info[1], message)

    RHSM.reset()
    return '呼叫緊急聯絡人' + contact_info[0]

def Demo(line_bot_api, event, BISM, RHSM):
    user_id = event.source.user_id
    place = "注意！您已來到危險警示地區：指南路一段道南橋下涵洞附近\n\
所屬轄區：台北市政府警察局文山第一分局\n\
轄區聯絡人：陳警務員、02-27592016、02-27269541"
    message = TextSendMessage(text=place, quick_reply=noted_button())
    line_bot_api.reply_message(event.reply_token, message)

    # set target time
    RHSM.set_time()
    target_time = getNow() + timedelta(minutes=3)
    RHSM.start_counting()

    current = getNow()
    while RHSM.state == 'counting' and current < target_time:
        printTime(current, target_time)
        time.sleep(10)
        current = getNow()

    if RHSM.state == 'default':
        return

    note = place + "\n\n若未回覆，1分鐘後將會通知緊急連絡人"
    message = TextSendMessage(text=note, quick_reply=noted_button())
    line_bot_api.push_message(user_id, message)
    RHSM.warn()

    target_time = target_time + timedelta(seconds=30)
    current = getNow()
    while RHSM.state == 'warning' and current < target_time:
        printTime(current, target_time)
        time.sleep(10)
        current = getNow()

    if RHSM.state == 'default':
        return

    contact_info = []
    if BISM.info.ready:
        contact_info = [BISM.info.contact_name, BISM.info.contact_token]
    else:
        contact_info = getContactInfo(user_id)[0]

    note = f"{BISM.info.name}在危險地方已經超過五分鐘了，請快確認他的人身安全吧！\n\
位置：(24.987556, 121.569168)"
    message = TextSendMessage(text=note)
    line_bot_api.push_message(contact_info[1], message)

    RHSM.reset()
    return '呼叫緊急聯絡人' + contact_info[0]

class ReturnHomeMachine(object):

    states = ['default', 'set_time', 'counting', 'warning']

    def __init__(self):
        self.machine = Machine(model=self, states=ReturnHomeMachine.states, initial='default')
        # self.time = ''
        self.arrived = False

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