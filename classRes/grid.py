# 方格类相关的内容
import json
from pyclbr import Function
from classRes.basicResourceClass import BasicClass
from classRes.building import Building
from util import bank

canvasConfig   = json.load(open('./canvas.config.json', encoding='UTF-8'))
gridConfig     = canvasConfig['gridConfig']
buildingConfig = canvasConfig['buildingConfig']
streetNameList = canvasConfig['buildingName']
class Grid(BasicClass):
  # 宽高和图片，所包含的内容
  def __init__(self, x, y, img, width, height, eventFunction = None|Function, building:Building = None, streetName = None):
    '''
      Building - building          : 该格子所对应的建筑物
      function - eventFunction     : 到达该格子触发的事件函数
    '''
    BasicClass.__init__(self, x, y, img, width, height)
    self.width         = width
    self.height        = height
    self.building      = building
    self.eventFunction = eventFunction
    self.streetName    = streetName
  # 寻找该格子所对应的建筑
  def findRelationBuilding(self):
    return self.building
  # 设置该格子所对应的建筑物
  def setRelationBuilding(self, building):
    if self.building == None:
      self.building = building



# 实现触发惩罚的函数
def triggerPunishFunc():
  pass

# 初始化格子列表
def initGrid(gridList, gridWidth, gridHeight, img, count = 36):
  '''
    :param list   gridList     存放所有格子的列表
    :param int    count        格子的总数量
    :param int    gridwidth    格子的宽度
    :param int    gridHeight   格子的高度
    :param object img          图片
  '''
  streetNameIndex = 0
  # 初始化第一行
  for column in range(0, 9):
    gridList.append(Grid(column * gridConfig['width'] + gridConfig['width'], buildingConfig['height'], img, gridWidth, gridHeight, None, None, streetNameList[streetNameIndex]))
    streetNameIndex += 1
  gridList[0].eventFunction = bank
  # 初始化第二行右侧到第八行右侧
  for column in range(1, 8):
    # gridList.append(Grid(gridConfig['width'], gridConfig['height'] * column + buildingConfig['height'], img, gridWidth, gridHeight))
    gridList.append(Grid(canvasConfig['width'] - gridConfig['width'] - buildingConfig['width'], gridConfig['height'] * column + buildingConfig['height'], img, gridWidth, gridHeight, None, None, streetNameList[streetNameIndex]))
    streetNameIndex += 1
  # 初始化最后一行
  for column in range(8, 0, -1):
    gridList.append(Grid(column * gridConfig['width'] + buildingConfig['width'], canvasConfig['height'] - gridHeight - buildingConfig['height'], img, gridWidth, gridHeight, None, None, streetNameList[streetNameIndex]))
    streetNameIndex += 1
  # 初始化第二行左侧到第八行左侧
  for column in range(8, 0, -1):
    gridList.append(Grid(gridConfig['width'], gridConfig['height'] * column + buildingConfig['height'], img, gridWidth, gridHeight, None, None, streetNameList[streetNameIndex]))
    streetNameIndex += 1
    # gridList.append(Grid(canvasConfig['width'] - gridConfig['width'] - buildingConfig['width'], gridConfig['height'] * column + buildingConfig['height'], img, gridWidth, gridHeight))


