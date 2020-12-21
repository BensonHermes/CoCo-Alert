def getWarnMapFlex():
   return {
      "type": "bubble",
      "body": {
         "type": "box",
         "layout": "vertical",
         "contents": [
            {
            "type": "box",
            "layout": "vertical",
            "margin": "lg",
            "spacing": "sm",
            "contents": [
               {
                  "type": "box",
                  "layout": "baseline",
                  "spacing": "sm",
                  "contents": [
                  {
                     "type": "text",
                     "text": "在回家的路上可能會經過的危險地點如下：",
                     "wrap": True,
                     "color": "#666666",
                     "size": "sm",
                     "flex": 5
                  }
                  ]
               }
            ]
            }
         ]
      },
      "footer": {
         "type": "box",
         "layout": "vertical",
         "spacing": "sm",
         "contents": [
            {
            "type": "button",
            "style": "link",
            "height": "sm",
            "action": {
               "type": "uri",
               "label": "打開地圖",
               "uri": "https://TeresaChou.github.io/WarnMap/"
            }
            },
            {
            "type": "spacer",
            "size": "sm"
            }
         ],
         "flex": 0
      }
   }