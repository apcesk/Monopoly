# 整个程序的入口文件
# 先引入要用的库
import pygame
from pygame.locals import *
import tkinter
from tkinter import messagebox
import easygui, random, sys, time
from easygui import *
# 导入json的配置文件
import json
# 导入格子类
from classRes.grid import Grid,initGrid
# 导入建筑类
from classRes.building import Building,initBuildingImages,initBuildings
# 导入角色类
from classRes.character import Character,initCharacters,initCharacterImages
# 导入游戏状态类
from classRes.gameVariable import GameVariable
from util import buyBuilding, inputPlayerNames, payForBuilding, showAllPersonInfo
# 设置画布的宽和高
JSON_CONFIG               = json.load(open('./canvas.config.json',  encoding='UTF-8'))
GRID_CONFIG               = JSON_CONFIG['gridConfig']
BUILDING_CONFIG           = JSON_CONFIG['buildingConfig']
CHARACTER_CONFIG          = JSON_CONFIG['playerConfig']
GAME_STATUS               = JSON_CONFIG['gameStatus']
PLAYER_NAME_LIST          = JSON_CONFIG['playerName']
gridImg                   = pygame.image.load('./images/grid/grid.jpg')
buildingImgList           = initBuildingImages([], './images/building/building', 0, 5, '.jpg')
characterImgList          = initCharacterImages([], './images/character/p', 1, 4, '.jpg')
# 是否处于投骰子的状态
IS_DICING                 = False
# 背景图片
backgroundImg             = pygame.image.load('./images/background/bg.jpg')
# 所有的方格(地块)
grids                     = []
# 所有的建筑
buildings                 = []
# 所有的玩家
players                   = []
# 游戏状态
GameVariable.gameStatus   = GAME_STATUS[0]
# 初始化pygame
pygame.init()
# 初始化字体
pygame.font.init()

# 初始化画布
canvas                    = pygame.display.set_mode((JSON_CONFIG['width'], JSON_CONFIG['height']))
# 初始化文字工具
font                      = pygame.font.Font(None, 20)
# 字体信息
fonts                     = []
# 设置游戏的标题
pygame.display.set_caption(JSON_CONFIG['title'])
# 初始化所有的方格
initGrid(grids, GRID_CONFIG['width'], GRID_CONFIG['height'], gridImg)
# 初始化所有的建筑
initBuildings(buildings, grids, buildingImgList[0])
# 初始化输入玩家的姓名
inputPlayerNames(PLAYER_NAME_LIST)
# 初始化所有的玩家
initCharacters(players, characterImgList, grids[0], PLAYER_NAME_LIST)
# 当前的玩家
GameVariable.playerInfo   = players
GameVariable.nowPlayer    = GameVariable.playerInfo[0]


# 切换到下一个游戏状态
def changeNextGameStatus():
  global GameVariable,fonts
  # 游戏状态播报清空，并且修改游戏的状态区显示的内容
  fonts = []
  middleAreaTextSetting(GAME_STATUS[(GAME_STATUS.index(GameVariable.gameStatus) + 1) % len(GAME_STATUS)])
  return GAME_STATUS[(GAME_STATUS.index(GameVariable.gameStatus) + 1) % len(GAME_STATUS)]
# 绘制函数
def componentPaint():
  global grids, buildings, players
  # 画背景
  canvas.blit(backgroundImg, (0, 0))
  for grid in grids:
    grid.selfPaint(canvas)
  for building in buildings:
    building.selfPaint(canvas)
  for player in players:
    player.selfPaint(grids, canvas)
  for f in fonts:
    fw, fh = f.get_size()
    canvas.blit(f, (JSON_CONFIG['width'] / 2 - fw / 2, JSON_CONFIG['height'] / 2 - fh / 2))

# 设置中间区域显示的游戏进程内容
def middleAreaTextSetting(text):
  _ = font.render(text, True, (255, 255, 255))
  fonts.append(_)

# 绘制投骰子的动画函数
def dicingPaint(player: Character, t: time):
  global GameVariable, IS_DICING, fonts
  # 投骰子的动画
  IS_DICING = True
  # 进行中间区域的游戏状态播报
  fonts = []
  middleAreaTextSetting(player.name + ' dicing: ' + str(GameVariable.diceNumber))
  if time.time() - t >= 1:
    print(t)
    IS_DICING = False
    # 投完了骰子进行修改游戏状态
    GameVariable.gameStatus = changeNextGameStatus()

# 事件处理函数
def handleEvent():
  global GameVariable
  # 遍历pygame中的事件队列
  for event in pygame.event.get():
    # 如果按下了退出
    if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
      pygame.quit()
      sys.exit()
    # 如果是处于等待状态，并且按下了空格键
    elif GameVariable.gameStatus == GAME_STATUS[0] and \
       event.type == pygame.KEYDOWN and event.key == 32:
      # 切换游戏状态
      GameVariable.gameStatus = changeNextGameStatus()
      print(GameVariable.gameStatus)
    # 如果处于等待状态，并且按下了S键，则弹出每个角色的相关信息
    elif GameVariable.gameStatus == GAME_STATUS[0] and \
      event.type == pygame.KEYDOWN and event.key == K_s:
        # 调用展示人员信息的函数
        showAllPersonInfo(GameVariable)



# 判断当前玩家是否处于移动状态，若不处于移动状态，则可以进行下一个状态
def isMoving(player: Character):
  print('人物移动中.....')
  if not player.moving:
    GameVariable.gameStatus = changeNextGameStatus()

# 触发当前人物所在的格子的事件，并在事件结束过后，游戏切换到下一个状态
def triggerGridEvent(player: Character):
  print('触发了格子事件')
  # 触发当前格子所对应的函数
  # player.nowGrid.eventFunction()
  # 修改游戏的状态,如果当前的事件触发完毕，则修改状态
  # if 事件触发完毕:
  GameVariable.gameStatus = changeNextGameStatus()

# 定义一个买房子的事件函数
def triggerBuyBuildingEvent(player: Character, buildingImgList: list):
  # 调用购买房屋的方法
  buyBuilding(player, buildingImgList)
  print('触发了买房子的事件')
  GameVariable.gameStatus = changeNextGameStatus()

# 定义一个房子收费的事件函数
def triggerMoneyReduceEvent(player: Character):
  payForBuilding(player)
  print('触发了房子收费的事件')
  GameVariable.gameStatus = changeNextGameStatus()

# 定义一个切换玩家的函数
def nextPlayer():
  global GameVariable
  GameVariable.nowPlayer = GameVariable.playerInfo[(GameVariable.playerInfo.index(GameVariable.nowPlayer) + 1) % len(GameVariable.playerInfo)]

# 控制游戏进程状态
def controlGameState():
  global fonts,IS_DICING,GameVariable
  # 等待状态
  if GameVariable.gameStatus == GAME_STATUS[0]:
    componentPaint()
    t = time.time()
  # 投骰子的状态
  elif GameVariable.gameStatus == GAME_STATUS[1]:
    # 让当前的人进行投骰子
    if IS_DICING == False:
      GameVariable.time = time.time()
      GameVariable.diceNumber = GameVariable.nowPlayer.move(grids)
      # 画骰子的动画
    dicingPaint(GameVariable.nowPlayer, GameVariable.time)
    componentPaint()
    # 画组件
  # 移动状态
  elif GameVariable.gameStatus == GAME_STATUS[2]:
    # 画组件
    componentPaint()
    # 如果当前的角色不处于移动状态了，则可以修改状态
    isMoving(GameVariable.nowPlayer)
  # 触发格子事件状态
  elif GameVariable.gameStatus == GAME_STATUS[3]:
    # 判断当前人物所在的格子
    triggerGridEvent(GameVariable.nowPlayer)
  # 触发房子购买事件状态
  elif GameVariable.gameStatus == GAME_STATUS[4]:
    # 触发买房子的ui对话框提示
    triggerBuyBuildingEvent(GameVariable.nowPlayer, buildingImgList)
  # 触发房子收费的事件状态
  elif GameVariable.gameStatus == GAME_STATUS[5]:
    triggerMoneyReduceEvent(GameVariable.nowPlayer)
    # 下一个玩家
    nextPlayer()



# 执行循环，不断更新画布
while True:
  # 绘制所有的元素
  # componentPaint()
  
  # 控制游戏状态
  controlGameState()
  # 处理事件
  handleEvent()
  # 更新画布
  pygame.display.update()
  # 延时更新
  time.sleep(0.1)