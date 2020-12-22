def getWarnMapFlex(latitude1, longitude1, latitude2, longitude2):
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
                           "color": "#000000",
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