from transitions import Machine

def GetWarn(event):
    message = {
        'type': 'flex',
        'alt_text': '警示地點查詢結果',
        'contents': {
            'type': 'bubble',
            'body': {
                'type': 'box',
                'layout': 'vertical',
                'contents': [
                    {
                        'type': 'text',
                        'text': '在回家的路上可能會經過的危險地點如下：'
                    }
                ]
            },
            'body': {
                'type':'button',
                'action': {
                    'type': 'uri',
                    'label': '打開地圖',
                    'uri': 'https://TeresaChou.github.io/WarnMap'
                }
            }
        }
    }
    return message

class GetWarnStateMachine(object):

    states = ['default', 'locate']

    def __init__(self):
        self.machine = Machine(model=self, states=GetWarnStateMachine.states, initial='default')

        # add_transition(trigger, source, dest)
        self.machine.add_transition('reset', '*', 'default')
        self.machine.add_transition('locate', '*', 'locate')

# testing data:
# NCCU: 24.9861694,121.5749262