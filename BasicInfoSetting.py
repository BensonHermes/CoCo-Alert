from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *
from transitions import Machine

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
                CarouselColumn(
                    text='設定常用地點',
                    actions=[
                        MessageTemplateAction(
                            label='點我設定',
                            text='設定常用地點'
                        )
                    ]
                ),
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

def BasicInfoSetting(event, BISM):
    # msg = event.message.text
    # if BISM.state == 'default':
    #     if '全部重新設定' in msg:
    #         BISM.all_setting_home()
    #         return "請利用下方的+號按鈕，輸入住家位置"
    #     elif '查看目前設定' in msg:
    #         return "目前設定："
    #     elif '設定住家地址' in msg:
    #         BISM.setting_home();
    #         return "請利用下方的+號按鈕，輸入住家位置"
    #     elif '設定常用地點' in msg:
    #         BISM.setting_often();
    #         return "請利用下方的+號按鈕，輸入常用地點位置"
    #     elif '設定緊急聯絡人' in msg:
    #         BISM.setting_contact();
    #         return "請利用下方的+號按鈕，輸入緊急連絡人資訊"
    BISM.reset()
    print("testing here")
    return "設定完成"

class BasicInfoStateMachine(object):

    states = ['default', 'home', 'often', 'contact', 'all_home', 'all_often']

    def __init__(self):
        self.machine = Machine(model=self, states=BasicInfoStateMachine.states, initial='default')

        # add_transition(trigger, source, dest)
        self.machine.add_transition('reset', '*', 'default')
        self.machine.add_transition('setting_home', '*', 'home')
        self.machine.add_transition('setting_often', '*', 'often')
        self.machine.add_transition('setting_contact', '*', 'contact')
        self.machine.add_transition('all_setting_home', '*', 'all_home')
        self.machine.add_transition('all_setting_often', 'all_home', 'all_often')
