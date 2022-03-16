#第一步当然是导入这个库
import random, pygame, sys
from pygame.locals import *
import tkinter
from tkinter import  *
from PIL import ImageTk,Image

FPS = 30 # 设置刷新的帧数
Width = 640 # 这里设置界面宽度
Height = 480 # 这里设置界面高度
Speed_of_open = 30 # 在这里我们设置了翻牌的速度
Card_size = 50 # 单个牌的高与宽
Distance_between_card = 10 # 每个牌之间的距离
wide_num = 5 # 这里我设置了横着有多少个牌
high_num = 4 # 竖着有多少个牌


#这里我们进行异常处理，要保证我们牌的数量是偶数哦
assert (wide_num * high_num) % 2 == 0, '卡牌数量需要是偶数，此情况下，卡牌数量是单数，无法进行游戏'

#这里我们计算一下边缘部分的像素，后面有用
X_margin_横轴边缘像素 = int((Width - (wide_num * (Card_size + Distance_between_card))) / 2)
Y_margin_纵轴边缘像素 = int((Height - (high_num * (Card_size + Distance_between_card))) / 2)

#设置颜色        R     G    B
Gray_灰       = (100, 100, 100)
NavyBlue_海军蓝 = ( 60,  60, 100)
White_白      = (255, 255, 255)
Red_红        = (230,   0,   0)
Green_绿      = (  0, 255,   0)
Blue_深蓝     = (  0,   0, 255)
Yellow_黄     = (255, 255,   0)
Orage_橙      = (255, 128,   0)
Purple_粉     = (255,   0, 255)
Gyan_青       = (  0, 255, 255)

#这里为各种颜色进行变量名的美化
BGCOLOR = NavyBlue_海军蓝
LIGHTBGCOLOR = Gray_灰
CardCOLOR = White_白
HIGHLIGHTCOLOR = Blue_深蓝

#这里设置了一些图形的样式的名称，提高代码的可读性
DONUT = 'donut'
SQUARE = 'square'
DIAMOND = 'diamond'
LINES = 'lines'
OVAL = 'oval'

#对图形样式和颜色设置元组（不再更改），以便后面进行随机取样
ALLCOLORS = (Red_红, Green_绿, Blue_深蓝, Yellow_黄, Orage_橙, Purple_粉, Gyan_青)
ALLSHAPES = (DONUT, SQUARE, DIAMOND, LINES, OVAL)


#处理 同种图形超过 2 个的异常情况
assert len(ALLCOLORS) * len(ALLSHAPES) * 2 >= wide_num * high_num, "图形组合数量不够，牌面个数过多了，应该调整卡牌数量"

#下面是游戏的主程序开始

def main():
    #在后面其他函数中也需要用到这两个变量，所以先标记全局
    global FPSCLOCK, Background_背景


    #初始化pygame的库
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    #设定游戏界面的大小
    Background_背景 = pygame.display.set_mode((Width, Height),0,32)
    #额外加的背景
    Background_背景图片 = pygame.image.load('Back2.jpg').convert()
    Background_背景.blit(Background_背景图片, (0, 0))
    ################################
    pygame.mixer.music.load('背景音乐.ogg')  # 背景音乐
    pygame.mixer.music.set_volume(0.05)  # 设置音量
    pygame.mixer.music.play(-1)  # 播放音乐
    sound_begin = pygame.mixer.Sound('是时候表演真正的技术了.wav')  # 播放开始！
    sound_begin.set_volume(0.7)
    sound_begin.play(0, 0)
    ################################

    #先对鼠标的坐标位置进行一次赋值存储，以便后面对于鼠标的位置进行存储操作
    mouse_x_position = 0
    mouse_y_position = 0
    #这里为我们的游戏界面去设置一个窗口标题 — “记忆训练小游戏”
    pygame.display.set_caption('宇宙最牛逼的记忆训练小游戏，彩蛋满满哦')


    #这里是两个数据结构的函数，记下标记############################################################################
    mainBoard = getRandomizedBoard()
    revealedCards = generateRevealedCardsData(False)

    firstSelection = None # 记录每次翻牌的两次记录中，第一次的翻牌坐标
    Background_背景.blit(Background_背景图片,(0,0)) #这里重新刷新屏幕的背景
    startGameAnimation(mainBoard)   #开始的一个动画操作，给玩家一个残存的记忆印象，这个函数将在后面写出，记下标记#######################################

    #########################################以下是计数器
    n_open_num = 0 #已经翻多少次牌的计数
    n_dacheng_num = 0 #已经翻出多少张牌
    n_lianxudachen = 0 #记录连续达成



    while True:

     # 游戏主要程序的部分
        mouseClicked = False    #光标没有按下

        Background_背景.blit(Background_背景图片,(0,0)) # 每次循环开始，先重新绘制游戏背景，去掩盖之前的画面
        drawBoard(mainBoard, revealedCards)    #同样调用后面的函数，记下标记################################################

        for event in pygame.event.get(): # 捕捉游戏进程当中的每次事件


            #这是一个关闭游戏的接口，当按下ESC键的时候或者点击右上角的插口的时候，这个游戏程序都会关闭
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            #当光标移动时，记录光标移动的坐标
            elif event.type == MOUSEMOTION:
                mouse_x_position, mouse_y_position = event.pos
            #当光标按下时，记录光标按下时的坐标
            elif event.type == MOUSEBUTTONUP:
                mouse_x_position, mouse_y_position = event.pos
                mouseClicked = True  #鼠标按下




        # 这里调用了一个后来我们写的关于获取光标按下时所在卡牌的位置信息，记下标记###########################################################
        Card_x_position, Card_y_position = getCardAtPixel(mouse_x_position, mouse_y_position)
        if Card_x_position != None and Card_y_position != None:
            # 这种情况下，光标在某张卡牌上面
            if not revealedCards[Card_x_position][Card_y_position]: #如果光标在未翻过的牌面上，画出蓝框
                drawHighlightCard(Card_x_position, Card_y_position)
            if not revealedCards[Card_x_position][Card_y_position] and mouseClicked:  #光标出现在未翻过的卡牌上，并且发生了翻牌动作


                revealCardsAnimation(mainBoard, [(Card_x_position, Card_y_position)]) #进行绘出牌面图案的动作
                revealedCards[Card_x_position][Card_y_position] = True #这个位置的牌变为翻开状态
                if firstSelection == None: # 如果这是第一次的翻牌动作
                    firstSelection = (Card_x_position, Card_y_position)  #记录第一次卡牌翻面时候的位置
                    #########################翻开卡牌声音
                    sound_open = pygame.mixer.Sound('开牌声音1.ogg')  # 播放开牌！
                    sound_open.set_volume(1)
                    sound_open.play(0, 0)

                    pygame.time.wait(100)


                else: # 第一次的翻牌位置已经被储存，进行第二次的翻牌
                    # 下面检查两次翻牌的牌面颜色图案是否一样
                    icon1shape, icon1color = getShapeAndColor(mainBoard, firstSelection[0], firstSelection[1])   #得到第一次翻的卡牌的颜色与形状
                    icon2shape, icon2color = getShapeAndColor(mainBoard, Card_x_position, Card_y_position)       #得到第二次翻的卡牌的颜色与形状

                    if icon1shape != icon2shape or icon1color != icon2color:
                        n_open_num += 1 ###############################################

                        ###############记数 当超过双杀时终结
                        if n_lianxudachen >= 2:
                            sound_shutdown = pygame.mixer.Sound('终结.ogg')  # 播放终结！
                            sound_shutdown.set_volume(0.5)
                            sound_shutdown.play(0, 0)
                        if n_open_num  %10 == 0:
                            sound_tooslow = pygame.mixer.Sound('动作太慢了.ogg')  # 播放终结！
                            sound_tooslow.set_volume(0.5)
                            sound_tooslow.play(0, 0)
                        else:
                            pygame.time.wait(100)
                            sound_shibai = pygame.mixer.Sound('翻牌失败.ogg')  # 播放终结！
                            sound_shibai.set_volume(0.5)
                            sound_shibai.play(0, 0)

                        n_lianxudachen = 0 #####################终结连杀

                        # 如果两者卡牌的颜色和形状中有一个不一样
                        pygame.time.wait(1000) # 这里暂定1000微秒，即暂停一秒钟
                        coverCardsAnimation(mainBoard, [(firstSelection[0], firstSelection[1]), (Card_x_position, Card_y_position)])    #触发重新覆盖上这个牌面的动画
                        revealedCards[firstSelection[0]][firstSelection[1]] = False   #这张牌重新变成没有翻面的状态
                        revealedCards[Card_x_position][Card_y_position] = False       #第二张牌重新变成没有翻页的状态


                    elif hasWon(revealedCards): # 这里设置玩家胜利条件，当所有牌面都翻过来时候，玩家胜利
                        n_open_num += 1
                        n_lianxudachen += 1
                        n_dacheng_num += 1

                        if n_lianxudachen == 2:
                            sound_2kill = pygame.mixer.Sound('双杀.ogg')  # 播放双杀！
                            sound_2kill.set_volume(0.5)
                            sound_2kill.play(0, 0)
                        if n_lianxudachen == 3:
                            sound_3kill = pygame.mixer.Sound('三杀.ogg')  # 播放三杀！
                            sound_3kill.set_volume(0.5)
                            sound_3kill.play(0, 0)
                        if n_lianxudachen == 4:
                            sound_4kill = pygame.mixer.Sound('四杀.ogg')  # 播放四杀！
                            sound_4kill.set_volume(0.5)
                            sound_4kill.play(0, 0)
                        if n_lianxudachen == 5:
                            sound_5kill = pygame.mixer.Sound('五杀.ogg')  # 播放五杀！
                            sound_5kill.set_volume(0.5)
                            sound_5kill.play(0, 0)

                        #为了处理最后一次翻牌音效，进行的功能性暂停
                        pygame.time.wait(1500)
                        ############################游戏结束更新num

                        n_open_num = 0
                        n_dacheng_num = -1
                        n_lianxudachen = 0

                        gameWonAnimation(mainBoard)     #进行游戏胜利动画
                        pygame.time.wait(2000)          #等待2秒钟的时间



                        # 重新设置游戏版面
                        mainBoard = getRandomizedBoard()     #随机重排牌面
                        revealedCards = generateRevealedCardsData(False)   #将牌面全部变为反面
                        ##################可以在此处重新设置卡牌增多动作，但需要先了解下面数据结构的轮子，记下标记######################################################

                        # 这里将界面重新绘制，等待1秒钟时间
                        drawBoard(mainBoard, revealedCards)
                        pygame.display.update()
                        pygame.time.wait(1000)

                        # 重新开始游戏开局动画
                        startGameAnimation(mainBoard)
                    ###################################################################记数
                    if icon1shape == icon2shape and icon1color == icon2color:
                        n_open_num += 1
                        n_lianxudachen += 1
                        n_dacheng_num += 1
                        if n_lianxudachen < 2:
                            if n_dacheng_num == 1:
                                sound_firstblood = pygame.mixer.Sound('一血.ogg')  # 播放一血！
                                sound_firstblood.set_volume(0.5)
                                sound_firstblood.play(0, 0)
                            if n_dacheng_num == 2:
                                sound_3card = pygame.mixer.Sound('翻出三组牌.ogg')  # 播放3牌！
                                sound_3card.set_volume(0.5)
                                sound_3card.play(0, 0)
                            if n_dacheng_num == 3:
                                sound_4card = pygame.mixer.Sound('翻出四组牌.ogg')  # 播放4血！
                                sound_4card.set_volume(0.5)
                                sound_4card.play(0, 0)
                            if n_dacheng_num == 4:
                                sound_5card = pygame.mixer.Sound('翻出五组牌.ogg')  # 播放5血！
                                sound_5card.set_volume(0.5)
                                sound_5card.play(0, 0)
                            if n_dacheng_num == 5:
                                sound_6card = pygame.mixer.Sound('翻出六组牌.ogg')  # 播放6血！
                                sound_6card.set_volume(0.5)
                                sound_6card.play(0, 0)
                            if n_dacheng_num == 6 :
                                sound_7card = pygame.mixer.Sound('翻出七组牌.ogg')  # 播放7血！
                                sound_7card.set_volume(0.5)
                                sound_7card.play(0, 0)
                            if n_dacheng_num >= 7:
                                sound_8card = pygame.mixer.Sound('超神.ogg')  # 播放8血！
                                sound_8card.set_volume(0.5)
                                sound_8card.play(0, 0)
                            n_lianxudachen = 1
                        if n_lianxudachen >= 2:
                            if n_lianxudachen ==2:
                                sound_2kill = pygame.mixer.Sound('双杀.ogg')  # 播放双杀！
                                sound_2kill.set_volume(0.5)
                                sound_2kill.play(0, 0)
                            if n_lianxudachen ==3:
                                sound_3kill = pygame.mixer.Sound('三杀.ogg')  # 播放三杀！
                                sound_3kill.set_volume(0.5)
                                sound_3kill.play(0, 0)
                            if n_lianxudachen ==4:
                                sound_4kill = pygame.mixer.Sound('四杀.ogg')  # 播放四杀！
                                sound_4kill.set_volume(0.5)
                                sound_4kill.play(0, 0)
                            if n_lianxudachen == 5:
                                sound_5kill = pygame.mixer.Sound('五杀.ogg')  # 播放五杀！
                                sound_5kill.set_volume(0.5)
                                sound_5kill.play(0, 0)



                    firstSelection = None # 这时候重新设置第一次翻牌的位置，为没有翻牌状态


        # 时刻更新界面
        pygame.display.update()
        FPSCLOCK.tick(FPS)

#以下是所有的轮子，手动分割线—————————————————————————————————————————————

def generateRevealedCardsData(val):    #这个轮子用于画出游戏界面，是一个列表式的数据结构，同样记下标记#####################

    revealedCards = []
    for i in range(wide_num):
        revealedCards.append([val] * high_num)
    return revealedCards


def getRandomizedBoard():     #这个轮子同样用于画出游戏界面，随机绘制出不同的图案
    # 一开始，图标的存储列表当然是空的，这里利用了列表的可变性，每次利用完一个图案，后面可以进行删除
    icons = []
    for color in ALLCOLORS:   #这里用一个嵌套的for循环去获取随机的颜色和图案，这里产出了所有的图案颜色组合
        for shape in ALLSHAPES:
            icons.append( (shape, color) )

    random.shuffle(icons) # 随机打乱每个图标在列表中的顺序
    numIconsUsed = int(wide_num * high_num / 2) # 统计出总共需要多少个图案
    icons = icons[:numIconsUsed] * 2 # 这里更新图案列表，将图案列表中的前numIconsUsed个图案*2，获得所有需要的图案
    random.shuffle(icons)      #这里再次将列表中所有图案的顺序打乱

    # 这里绘制出所有牌面组合出来的样式，并且填充进入图案
    board = []   #整个版面一开始，当然也是一个空的列表
    for x in range(wide_num):
        column = []
        for y in range(high_num):
            column.append(icons[0])
            del icons[0] # 每次删除完图案列表里刚刚填入的那个图案
        board.append(column)
    return board
    #上述画完坐标轴如下
      # 0 1 2 3 4 5
    # 0
    # 1
    # 2
    # 3
    # 4

def List1D_into_list2D(groupSize, theList):
    # 将一维列表分解成二维列表的一个简单轮子
    result = []
    for i in range(0, len(theList), groupSize):
        result.append(theList[i:i + groupSize])
    return result


def Actural_position(Card_x_position, Card_y_position):
    # 这个轮子将方块坐标转化为像素坐标，供游戏本体识别
    left = Card_x_position * (Card_size + Distance_between_card) + X_margin_横轴边缘像素
    top = Card_y_position * (Card_size + Distance_between_card) + Y_margin_纵轴边缘像素
    return (left, top)


def getCardAtPixel(x, y):   #这是一个统一像素坐标和方块坐标的轮子，将像素坐标转化为方块坐标
    for Card_x_position in range(wide_num):
        for Card_y_position in range(high_num):
            left, top = Actural_position(Card_x_position, Card_y_position)   #这里获得光标下方块坐标的像素坐标值
            CardRect = pygame.Rect(left, top, Card_size, Card_size)     #这里获得每个牌的像素坐标
            if CardRect.collidepoint(x, y):                          #如果光标下的像素坐标在某个牌下的像素坐标内部
                return (Card_x_position, Card_y_position)           #则返回那张牌的方块坐标
    return (None, None)       #若光标不在某个牌的像素坐标，那么返回，光标无选中牌面


def drawIcon(shape, color, Card_x_position, Card_y_position):     #这是绘制牌面图案的轮子
    quarter = int(Card_size * 0.25) # syntactic sugar
    half =    int(Card_size * 0.5)  # syntactic sugar

    left, top = Actural_position(Card_x_position, Card_y_position) # 这里获得像素坐标
    # 这里绘制每种牌面
    if shape == DONUT:
        pygame.draw.circle(Background_背景, color, (left + half, top + half), half - 5)
        pygame.draw.circle(Background_背景, BGCOLOR, (left + half, top + half), quarter - 5)
    elif shape == SQUARE:
        pygame.draw.rect(Background_背景, color, (left + quarter, top + quarter, Card_size - half, Card_size - half))
    elif shape == DIAMOND:
        pygame.draw.polygon(Background_背景, color, ((left + half, top), (left + Card_size - 1, top + half), (left + half, top + Card_size - 1), (left, top + half)))
    elif shape == LINES:
        for i in range(0, Card_size, 4):
            pygame.draw.line(Background_背景, color, (left, top + i), (left + i, top))
            pygame.draw.line(Background_背景, color, (left + i, top + Card_size - 1), (left + Card_size - 1, top + i))
    elif shape == OVAL:
        pygame.draw.ellipse(Background_背景, color, (left, top + quarter, Card_size, half))


def getShapeAndColor(board, Card_x_position, Card_y_position):
    # board[x][y][0] 储存牌面的形状
    # board[x][y][1] 储存牌面的颜色
    return board[Card_x_position][Card_y_position][0], board[Card_x_position][Card_y_position][1]   #返回一个牌面内容的颜色与形状


def drawCardCovers(board, Cards, coverage):
    # Draws Cards being coveRed_红/revealed. "Cards" is a list
    # of two-item lists, which have the x & y spot of the Card.
    for Card in Cards:
        left, top = Actural_position(Card[0], Card[1])
        pygame.draw.rect(Background_背景, BGCOLOR, (left, top, Card_size, Card_size))          #自己修改记下标记#######################################
        shape, color = getShapeAndColor(board, Card[0], Card[1])
        drawIcon(shape, color, Card[0], Card[1])
        if coverage > 0: # only draw the cover if there is an coverage Background_背景.blit(Background_背景图片, (0, 0))
            Card_cover_卡牌背面图片 = pygame.image.load('卡牌背面.jpg').convert()    #记下标记##############################################
            Background_背景.blit(Card_cover_卡牌背面图片,(left, top))

    pygame.display.update()
    FPSCLOCK.tick(FPS)


def revealCardsAnimation(board, CardsToReveal):
    # Do the "Card reveal" animation.
    for coverage in range(Card_size, (-Speed_of_open) - 1, -Speed_of_open):
        drawCardCovers(board, CardsToReveal, coverage)


def coverCardsAnimation(board, CardsToCover):
    # 翻回动画
    for coverage in range(0, Card_size + Speed_of_open, Speed_of_open):
        drawCardCovers(board, CardsToCover, coverage)


def drawBoard(board, revealed):
    # 画出所有牌面组成的整体
    for Card_x_position in range(wide_num):
        for Card_y_position in range(high_num):
            left, top = Actural_position(Card_x_position, Card_y_position)
            if not revealed[Card_x_position][Card_y_position]:
                # 记下标记#########################################################################################
                Card_cover_卡牌背面图片 = pygame.image.load('卡牌背面.jpg').convert()  # 记下标记##############################################
                Background_背景.blit(Card_cover_卡牌背面图片, (left, top))
            else:
                # Draw the (revealed) icon.
                shape, color = getShapeAndColor(board, Card_x_position, Card_y_position)
                drawIcon(shape, color, Card_x_position, Card_y_position)


def drawHighlightCard(Card_x_position, Card_y_position):
    left, top = Actural_position(Card_x_position, Card_y_position)
    pygame.draw.rect(Background_背景, HIGHLIGHTCOLOR, (left - 5, top - 5, Card_size + 10, Card_size + 10), 4)


def startGameAnimation(board):
    # Randomly reveal the Cards 8 at a time.
    coveRed_红Cards = generateRevealedCardsData(False)
    Cards = []
    for x in range(wide_num):
        for y in range(high_num):
            Cards.append( (x, y) )
    random.shuffle(Cards)
    CardGroups = List1D_into_list2D(8, Cards)

    drawBoard(board, coveRed_红Cards)
    for CardGroup in CardGroups:
        revealCardsAnimation(board, CardGroup)
        pygame.time.wait(700)
        coverCardsAnimation(board, CardGroup)


def gameWonAnimation(board):
    # 游戏结束动画的轮子######################################
    coveRed_红Cards = generateRevealedCardsData(True)
    color1 = LIGHTBGCOLOR
    color2 = BGCOLOR
    Card_cover_卡牌背面图片 = pygame.image.load('卡牌背面.jpg').convert()  # 记下标记##############################################


    for i in range(0,3):
        if i == 0:
            Win_pic = pygame.image.load('胜利图1.jpg').convert()
            Background_背景.blit(Win_pic,(0,0))
            drawBoard(board, coveRed_红Cards)
            sound_ACE = pygame.mixer.Sound('团灭.ogg')  #播放团灭！
            sound_ACE.set_volume(0.5)
            sound_ACE.play(0, 0)
            pygame.display.update()
            pygame.time.wait(2000)
        if i ==1 :
            Win_pic_2 = pygame.image.load('胜利图2.jpg').convert()
            Background_背景.blit(Win_pic_2, (0, 0))
            drawBoard(board, coveRed_红Cards)
            pygame.display.update()
            sound_xipai = pygame.mixer.Sound('洗牌.ogg')  # 播放开始！
            sound_xipai.set_volume(0.7)
            sound_xipai.play(0, 0)
            pygame.time.wait(2000)

        if i ==2 :
            Win_pic_3 = pygame.image.load('胜利图3.jpg').convert()
            Background_背景.blit(Win_pic_3, (0, 0))
            drawBoard(board, coveRed_红Cards)
            sound_begin = pygame.mixer.Sound('是时候表演真正的技术了.wav')  # 播放开始！
            sound_begin.set_volume(0.7)
            sound_begin.play(0, 0)


            #################
            pygame.display.update()
            pygame.time.wait(2000)


def hasWon(revealedCards):
    #检查胜利条件的轮子
    for i in revealedCards:
        if False in i:
            return False # 如果有没有翻开的牌面，那么游戏未完成
    return True
#####################################################################

#进入GUI界面
root = Tk()
root.title("宇辰游戏启动端")
root.geometry("500x500")
#创建标签和按钮
lbl1=Label(root, text='未点击按钮',width=20)
lbl1.grid()
btn1 = Button(root, text='显示1', command=main)
btn1.grid()
btn2 = Button(root, text='显示2', command=main)
btn2.grid()
root.mainloop( )

