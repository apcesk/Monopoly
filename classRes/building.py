# 建筑物相关的内容
'''
  建筑物和人之间的关系
    若考虑关系型数据库，则是一个映射表，描述建筑和人之间的关系

  建筑物和方格之间的关系
    初始化固定，同建筑物和人之间的关系
'''
# from classRes.character import Character
from classRes.basicResourceClass import BasicClass
import random
import pygame.image as pi
import json
import easygui as e

# from classRes.character import Character
# from classRes.grid import Grid
buildingConfig = json.load(open('./canvas.config.json',  encoding='UTF-8'))['buildingConfig']
buildingName   = json.load(open('./canvas.config.json',  encoding='UTF-8'))['buildingName']
class Building(BasicClass):

  def __init__(self, x, y, img, width, height, cost, floor, belongCharacter, belongGird, buildingName = '', streetNumber:int = None): 
    '''
      int - x                     : x坐标
      int - y                     : y坐标
      object - img                : 图片
      int - width                 : 宽
      int - height                : 高
      int - cost                  : 继续盖房子的花费
      int - floor                 : 房子的层数
      int - streetNumber          : 大街编号
      string - buildingName       : 建筑物名称
      Character - belongCharacter : 所属人
      function updateBelongPerson : 修改所属人
    '''
    # 实现父类的内容
    BasicClass.__init__(self, x, y, img, width, height)
    self.cost            = cost
    self.floor           = floor
    self.belongCharacter = belongCharacter
    self.belongGrid      = belongGird
    self.buildingName    = buildingName
    self.streetNumber    = streetNumber

  # 修改房屋所属人
  def updateBelongPerson(self,character):
    self.belongCharacter = character
  
  # 升级房屋的方法
  def addBuildingLevel(self, img):
    if self.floor < 5:
      self.floor = self.floor + 1
      self.img = img[self.floor]
    else:
      e.msgbox('This building is in top level!')

  # 房屋进行降级的方法
  def reduceBuildingLevel(self):
    pass

  # 房屋进行拍卖的方法
  # character为购买人，money为房屋的销售价格
  def sellBuilding(self, character, money):
    pass

  # 房屋收钱的方法
  def earnMoneyBuilding(self, character):
    # 获取房屋所有人的数据
    owner = self.belongCharacter
    # 修改被罚当前角色的金钱
    character.updateMoney(-self.cost * len(owner.buildings))
    owner.updateMoney(self.cost * len(owner.buildings))

  # 定义房屋的寻找所属人的方法
  def findOwner(self):
    return self.belongCharacter
  # 房屋的画方法---重写
  # def selfPaint(self, canvas):
  #   # print(self.floor)
  #   canvas.blit(self.img, (self.x, self.y))

def initBuildingImages(buildingImgList: list, imgFileName: str, 
                       keyword: int, maxKeyword: int, fileType: str):
  for i in range(keyword, maxKeyword + 1):
    buildingImgList.append(pi.load(imgFileName + str(i) + fileType))
  return buildingImgList


def initBuildings(buildings: list, grids: list, defaultImg: object):

  buildingNameIndex = 0
  # 根据格子初始化所有的建筑物的初始位置，也为每个建筑物绑定所对应的格子
  for column in range(1, 8):
    buildings.append(
      Building(
      grids[column].x, grids[column].y - buildingConfig['height'], defaultImg, 
      buildingConfig['width'], buildingConfig['height'], random.randint(120, 180), 0, None, grids[column],
      buildingName[column], 1
      ))
    buildingNameIndex += 1
    grids[column].setRelationBuilding(buildings[len(buildings) - 1])
  # 初始化第二行到第八行
  for column in range(9, 16):
    buildings.append(
        Building(
        grids[column].x + buildingConfig['width'], grids[column].y, defaultImg, 
        buildingConfig['width'], buildingConfig['height'], random.randint(120, 180), 0, None, grids[column],
        buildingName[column], 2
        )
      )
    buildingNameIndex += 1
    grids[column].setRelationBuilding(buildings[len(buildings) - 1])
  # 初始化最后一行
  for column in range(17, 24):
    buildings.append(
        Building(
        grids[column].x, grids[column].y + buildingConfig['height'], defaultImg, 
        buildingConfig['width'], buildingConfig['height'], random.randint(120, 180), 0, None, grids[column],
        buildingName[column], 3
        )
      )
    buildingNameIndex += 1
    grids[column].setRelationBuilding(buildings[len(buildings) - 1])
  for column in range(25, 32):
    buildings.append(
        Building(
        grids[column].x - buildingConfig['width'], grids[column].y, defaultImg, 
        buildingConfig['width'], buildingConfig['height'], random.randint(120, 180), 0, None, grids[column],
        buildingName[column], 4
        )
      )
    buildingNameIndex += 1
    grids[column].setRelationBuilding(buildings[len(buildings) - 1])
  # pass
