from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *

def BasicInfoSetting():
    message = TemplateSendMessage(
        alt_text='基本資料設定',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    text='全部重新設定',
                    actions=[
                        MessageTemplateAction(
                            label='全部重新設定',
                            text='點我重新設定'
                        )
                    ]
                ),
                CarouselColumn(
                    text='查看目前設定',
                    actions=[
                        MessageTemplateAction(
                            label='查看目前設定',
                            text='點我查看'
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
                            label='設定住家地址',
                            text='點我設定'
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
                            label='設定常用地點',
                            text='點我設定'
                        )
                    ]
                ),
                CarouselColumn(
                    text='設定緊急聯絡人',
                    actions=[
                        MessageTemplateAction(
                            label='設定緊急聯絡人',
                            text='點我設定'
                        )
                    ]
                )
            ]
        )
    )
    return message