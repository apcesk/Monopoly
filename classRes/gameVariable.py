

class GameVariable():
  '''
    Character|None          nowPlayer               : 当前的玩家
    string                  gameStatus              : 游戏当前的状态
    int                     gameTurns               : 游戏回合数
    list<Character>         playerInfo              : 玩家信息
    time                    time                    : 记录上一次投骰子的时间
    int                     diceNumber              : 当前玩家投掷的骰子点数
  '''
  nowPlayer           = None
  gameStatus          = None
  gameStatusList      = None
  gameTurns           = 0 
  playerInfo          = []
  time                = 0
  diceNumber          = 0
  