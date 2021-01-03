from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *
from transitions import Machine
from db import *
from flex_button import *

def BasicInfoSettingEntrance():
    message = TemplateSendMessage(
        alt_text='基本資料設定',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    text='全部重新設定',
                    actions=[
                        MessageTemplateAction(
                            label='點我重新設定',
                            text='全部重新設定'
                        )
                    ]
                ),
                CarouselColumn(
                    text='查看目前設定',
                    actions=[
                        MessageTemplateAction(
                            label='點我查看',
                            text='查看目前設定'
                        )
                    ]
                ),
                CarouselColumn(
                    text='設定用戶名稱',
                    actions=[
                        MessageTemplateAction(
                            label='點我設定',
                            text='設定用戶名稱'
                        )
                    ]
                ),
                CarouselColumn(
                    # thumbnail_image_url='',
                    # title='',
                    text='設定住家地址',
                    actions=[
                        # PostbackTemplateAction(
                        #     label='回傳一個訊息',
                        #     data='將這個訊息偷偷回傳給機器人'
                        # ),
                        MessageTemplateAction(
                            label='點我設定',
                            text='設定住家地址'
                        )
                        # URITemplateAction(
                        #     label='進入1的網頁',
                        #     uri='https://upload.wikimedia.org/wikipedia/commons/thumb/8/88/Number_1_in_green_rounded_square.svg/200px-Number_1_in_green_rounded_square.svg.png'
                        # )
                    ]
                ),
                # CarouselColumn(
                #     text='設定常用地點',
                #     actions=[
                #         MessageTemplateAction(
                #             label='點我設定',
                #             text='設定常用地點'
                #         )
                #     ]
                # ),
                CarouselColumn(
                    text='設定緊急聯絡人',
                    actions=[
                        MessageTemplateAction(
                            label='點我設定',
                            text='設定緊急聯絡人'
                        )
                    ]
                )
            ]
        )
    )
    return message

def setId(id, user_id):
    return

def BasicInfoSetting(event, BISM):
    # print("user id", event.source.user_id)
    # print("message type", event.message.type)
    user_id = event.source.user_id
    if event.message.type == 'text':
        msg = event.message.text
        if BISM.state == 'default':
            if '全部重新設定' in msg:
                BISM.all_setting_id()
                return "用戶名稱設置：請輸入用戶名稱"
            elif '查看目前設定' in msg:
                return getCurrentSetting(event.source.user_id)
            elif '設定用戶名稱' in msg:
                BISM.setting_id()
                return "請輸入用戶名稱"
            elif '設定住家地址' in msg:
                BISM.setting_home()
                return "請點選下方的按鈕，輸入住家位置"
            # elif '設定常用地點' in msg:
            #     BISM.setting_often()
            #     return "請利用左下方的選單，輸入常用地點位置"
            elif '設定緊急聯絡人' in msg:
                BISM.setting_contact()
                return "請輸入緊急連絡人名稱"
        elif BISM.state == 'id':
            success = setUserName(user_id, msg)
            if success:
                BISM.reset()
                return "設定完成"
            else:
                return "此名稱已被使用過，請輸入另外的名稱"
        elif BISM.state == 'contact': 
            success = setContact(user_id, msg)
            BISM.reset()
            if success:
                return "設定完成"
            else: 
                return "找不到此人。請確認對方已加入機器人好友，並已設定名稱"
        elif BISM.state == 'all_id':
            success = setUserName(user_id, msg)
            if success:
                BISM.all_setting_home()
                return "住家設置：請點選下方的按鈕，輸入住家位置"
            else:
                return "此名稱已被使用過，請輸入另外的名稱"
    elif event.message.type == 'location':
        if BISM.state == 'home':
            setHome(
                user_id,
                event.message.address,
                event.message.latitude,
                event.message.longitude
                )
            BISM.reset()
            return "設定完成"
        # elif BISM.state == 'often':
        #     BISM.reset()
        #     return "設定完成"
        elif BISM.state == 'all_home':
            setHome(
                user_id,
                event.message.address,
                event.message.latitude,
                event.message.longitude
                )
            # BISM.all_setting_often()
            # return "常用地點設置：請利用左下方的選單，輸入常用地點位置"
        # elif BISM.state == 'all_often':
            BISM.setting_contact()
            return "緊急聯絡人設置：請輸入緊急聯絡人名稱"
    BISM.reset()
    return "無法辨識"

def getCurrentSetting(user_id):
    info = getUserInfo(user_id)
    info = info[0]
    result = '用戶名稱：' + info[0]
    result += '\n住家位置：' + info[1]
    result += '\n緊急聯絡人：' + info[2]

    return result

class BasicInfoStateMachine(object):

    states = ['default', 'id', 'home', 'contact', 'all_id', 'all_home', 'all_often']

    def __init__(self):
        self.machine = Machine(model=self, states=BasicInfoStateMachine.states, initial='default')

        # add_transition(trigger, source, dest)
        self.machine.add_transition('reset', '*', 'default')
        self.machine.add_transition('setting_id', '*', 'id')
        self.machine.add_transition('setting_home', '*', 'home')
        # self.machine.add_transition('setting_often', '*', 'often')
        self.machine.add_transition('setting_contact', '*', 'contact')
        self.machine.add_transition('all_setting_id', '*', 'all_id')
        self.machine.add_transition('all_setting_home', 'all_id', 'all_home')
        # self.machine.add_transition('all_setting_often', 'all_home', 'all_often')
