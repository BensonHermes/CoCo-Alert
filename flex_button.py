def getWarnMapFlex(text, latitude1, longitude1, latitude2, longitude2):
   pos = "?"
   if latitude1 > 0:
      pos += "latitude1=" + "{:.6f}".format(latitude1) + "&longitude1=" + "{:.6f}".format(longitude1)
   if latitude2 > 0:
      if pos != "?":
         pos += "&"
      pos += "latitude2=" + "{:.6f}".format(latitude2) + "&longitude2=" + "{:.6f}".format(longitude2)
   if pos == "?":
      pos = ""
      
   
   return {
      "type": "bubble",
      "body": {
         "type": "box",
         "layout": "vertical",
         "contents": [
            {
               "type": "text",
               "text": "在回家的路上會經過的危險地點如下：",
               "wrap": True,
               "size": "lg"
            },
            {
               "type": "box",
               "layout": "vertical",
               "margin": "lg",
               "contents": [
                  {
                     "type": "box",
                     "layout": "baseline",
                     "spacing": "sm",
                     "contents": [
                        {
                           "type": "text",
                           "text": text,
                           "wrap": True,
                           "color": "#666666",
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
                  "uri": "https://TeresaChou.github.io/WarnMap/index.html" + pos
               }
            }
            # {
            #    "type": "spacer",
            #    "size": "sm"
            # }
         ],
         "flex": 0
      }
   }

def chooseLocationButton():
   return {
      'items': [
         {
            'type': 'action',
            'action': {
               'type':'location',
               'label': '按我選擇地點'
            }
         }
      ]
   }

def arriveHomeButton():
   return {
      'items': [
         {
            'type': 'action',
            'action': {
               'type':'postback',
               'label': '到家了',
               'data': 'arrive_home'
               # 'text': '到家了/行程取消'
            }
         },
         {
            'type': 'action',
            'action': {
               'type':'postback',
               'label': '行程取消',
               'data': 'cancel_schedule'
               # 'text': '到家了/行程取消'
            }
         }
      ]
   }

def noted_button():
   return {
      'items': [
         {
            'type': 'action',
            'action': {
               'type':'postback',
               'label': '知道了',
               'data': 'demo_noted'
            }
         }
      ]
   }