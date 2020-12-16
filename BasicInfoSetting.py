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
    BISM.sleep()
    return "設定完成"

class BasicInfoStateMachine(object):

    states = ['default', 'waiting', 'home', 'often', 'contact', 'all_home', 'all_often']

    def __init__(self):
        self.machine = Machine(model=self, states=BasicInfoStateMachine.states, initial='default')

        # add_transition(trigger, source, dest)
        self.add_transition('sleep', '*', 'default')
        self.add_transition('start', '*', 'waiting')
        self.add_transition('setting_home', 'waiting', 'home')
        self.add_transition('setting_often', 'waiting', 'often')
        self.add_transition('setting_contact', '*', 'contact')
        self.add_transition('all_setting_home', '*', 'all_home')
        self.add_transition('all_setting_often', 'all_home', 'all_often')
