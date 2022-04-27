# 事件相关的内容

'''
  事件包含的内容。
    1、奖励事件
    2、惩罚事件
    3、传送事件
'''
class Event():
  def __init__(self, message, money, earnOthers):
    '''
      事件
      str            - message                    : 事件的信息
      int            - money                      : 事件的金钱
      bool           - earnOthers                 : 是否从其他玩家处获得
    '''
    self.message               = message
    self.money                 = money
    self.earnOthers            = earnOthers
    
    
    pass