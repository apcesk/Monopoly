

# 定义展示所有玩家信息的函数
from classRes.character import Character
from classRes.gameVariable import GameVariable
import easygui as e

# 定义展示人员信息的方法
def showAllPersonInfo(_: GameVariable):
  message = ''
  for player in _.playerInfo:
    message += str(player.name) + ':' + str(player.money) + '\n'
  e.msgbox(message)
  
# 定义购买房屋的方法
def buyBuilding(player: Character, buildingImgList:list):
  # 获得当前所在位置的房屋信息
  grid                                = player.nowGrid
  # 建筑的信息
  building                            = grid.building
  # 若当前格子没有房屋
  if building == None:
    return
  # 若当前房屋没有所属人，则可以进行购买操作
  canBuy = True if building.belongCharacter == None else False
  print('canBuy: ' + str(canBuy))
  # 若当前房屋有所属人，则购买人仅应为房屋的所属人
  # 获取当前建筑物所需要的购买金钱
  buildingCost = building.cost * (building.floor + 1)
  # ynmessage
  ynmessage = 'Do u want to buy this building named: '+ grid.streetName + '?(cost: ' + str(buildingCost) + ')'
  if canBuy == False:
    # 说明当前房屋有所属人，则要进行判断所属人是否是当前人
    if building.belongCharacter != player:
      return
    else:
      # 重新写提示消息
      ynmessage = 'Do u want to level up this building named: ?'+ grid.streetName + '(cost: ' + str(buildingCost) + ')'
  # 获取是否要购买当前房屋
  confirBuyBuilding                   = e.ynbox(ynmessage, 'Buy building!', ('Yes!', 'No!'))
  # 如果确认购买
  if confirBuyBuilding:
    # 如果当前人的存款小于房屋的售价，
    if player.money < buildingCost:
      e.msgbox('you didn\'t have enough money!')
    else:
      # 进行购买
      print('需要花费:' + str(building.cost * building.floor))
      player.addBuiding(building, True, buildingCost)
      building.addBuildingLevel(buildingImgList)
    # e.msgbox('购买！')
  print('buying')
  
# 输入每个玩家的姓名
def inputPlayerNames(playerNameList: list):
  confirmEnterPlayerName = e.ynbox('你要修改默认游戏玩家的名称吗？', '请确认', ('是的,我要修改','不,我使用默认'))
  if confirmEnterPlayerName == False:
    return
  for i in range(4):
    playerNameList[i] = e.enterbox('输入玩家' + str(i+1) + '的名字','输入玩家姓名')
  
# 定义一个房屋收费的方法
def payForBuilding(player: Character):
  # 首先判断当前位置的房屋的所属，是否不等于当前的人员
  # 当前所在的格子
  grid                   = player.nowGrid
  # 当前所在的建筑物
  building               = grid.building
  # 如果当前的房屋有所属人，并且当前的房屋所属人不是当前所在的人员
  if building != None and building.belongCharacter != None and building.belongCharacter != player:
    e.msgbox('You should pay for this building! named: ' + building.buildingName, "Pay!", "Pay!")
    # 触发房屋的收钱方法
    building.earnMoneyBuilding(player)
    


# 实现传送格子的函数
def transferFunc(gridList, player):
  
  pass


rewaredMessage = []

# 实现触发奖励的事件函数
def triggerAwardFunc():
    pass


# 银行函数
def bank(player):
  # 将player对应的金钱+2000
  player.updateMoney(2000)