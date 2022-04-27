# 角色类相关的内容



import json
from classRes.basicResourceClass import BasicClass
import pygame.image as pi
import random
from classRes.building import Building

# from classRes.grid import Grid
characterConfig = json.load(open('./canvas.config.json',  encoding='UTF-8'))['playerConfig']

class Character(BasicClass):
  def __init__(self, x:int, y:int, img:object, width:int, height:int, name:str, gender: bool, birthday: str, orderNumber: int, nowGrid = None):
    super().__init__(x, y, img, width, height)
    '''
      string       - name               : 姓名
      bool         - gender             : 性别True为男,False为女
      string       - birthday           : 生日
      int          - orderNumber        : 次序
      int          - diceCount          : 骰子数量
      float        - money              : 拥有的金钱数量
      diceCount    - number             : 拥有的骰子数量
      bool         - out                : 是否出局
      Grid         - nowGrid            : 当前所在的格子
      bool         - moving             : 是否处于移动状态
    '''
    self.name                = name
    self.gender              = gender
    self.birthday            = birthday
    self.orderNumber         = orderNumber
    self.diceCount           = 1
    self.money               = 50000
    self.buildings           = []
    self.diceCount           = 1
    self.out                 = False
    self.nowGrid             = nowGrid
    self.moving              = False
    self.moveCount           = 0
    self.targetGrid          = None
  # 创建一个使人物移动的方法
  def move(self, grids: list):
    if self.moving == True:
      return 0
    # 投骰子
    diceNumber      = self.dicing()
    # 修改移动状态
    self.moving     = True
    # 保存移动的步数
    self.moveCount  = diceNumber
    # 测试用
    # diceNumber = 1
    self.targetGrid = grids[(grids.index(self.nowGrid) + diceNumber) % len(grids)]
    # 把骰子的数目返回出去
    return diceNumber
  # 创建一个修改人物金钱的方法
  def updateMoney(self, updateCount: int):
    if self.money + updateCount > 0:
      self.money += updateCount
    else:
      self.out = True

  # 重新实现移动方法
  def selfPaint(self, grids, canvas):
    # 如果该角色处于移动状态
    if self.moving == True:
      self.nowGrid = grids[(grids.index(self.nowGrid) + 1) % len(grids)]
      self.x       = self.nowGrid.x + self.width // 2
      self.y       = self.nowGrid.y + self.height // 2
      # 到达了指定地点，停止移动
      if self.nowGrid == self.targetGrid:
        self.moving = False
    canvas.blit(self.img, (self.x, self.y))
  
  # 创建一个添加building的方法
  def addBuiding(self, building: Building, needMoney:bool = False, cost:int = 0):
    # 若当前房屋没有所属人，且当前要购买的人员能够付出足够的钱购买该房子
    if building.belongCharacter == None and self.money >= building.cost * building.floor:
      self.buildings.append(building)
      building.updateBelongPerson(self)
      # 修改金钱
      if needMoney:
        self.money = self.money - cost
    

  # 创建一个查找指定建筑物的方法
  def findBuilding(self, building):
    '''
      若在自身所包含的建筑中找到了指定的建筑
      则返回True
      否则返回False
    '''
    if building in self.buildings:
      return True
    return False

  # 创建一个移除建筑物的方法
  def removeBuilding(self, building):
    # 移除掉自身所拥有的房屋
    self.buildings.remove(building)
    # 移除掉该房屋所对应的拥有人
    building.updateBelongPerson(None)

  # 创建一个投骰子的方法(暂时没有实现动画)
  def dicing(self):
    diceNumber = []
    for _ in range(self.diceCount):
      diceNumber.append(random.randint(1, 6))
    print(self.name + '投掷出了点数' + str(sum(diceNumber)))
    return sum(diceNumber)
  # 创建一个修改骰子数量的方法
  def updateDiceCount(self, updateCount):
    self.diceCount += updateCount
    if self.diceCount == 0:
      self.diceCount = 1

def initCharacters(characterList: list, characterImgList: list, startPosition: object, playerNameList: list):
  for i in range(4):
    characterList.append(Character(
      startPosition.x + characterConfig['width']//2, 
      startPosition.y + characterConfig['height']//2,
      characterImgList[i], 
      characterConfig['width'], 
      characterConfig['height'], 
      playerNameList[i], True, '1998/07/08', i + 1,
      startPosition
    ))


# 初始化角色图片的函数
def initCharacterImages(characterImgList: list, imgFileName: str, keyword: int, maxKeyword: int, fileType: str):
  for i in range(keyword, maxKeyword + 1):
    characterImgList.append(pi.load(imgFileName + str(i) + fileType))
  return characterImgList