class Board:
    def __init__(self,height=6,width=7):
        self.height = height
        self.width = width
        self.board = self.createMatrix()
        self.valid = [0 for i in range(self.width)]

    def createMatrix(self):
        return [[0 for i in range(self.width)] for j in range(self.height)]
    
    def disp(self):
        for i in self.board:
            for j in i:
                if j!=0:
                    print(j,end=" ")
                else:
                    print("-",end=" ")
            print()
        print()

    def insert(self,column,data):
        if self.valid[column]==self.height:
            return False
        self.board[self.height-self.valid[column]-1][column]=data
        self.valid[column]+=1
        return True
    
    def delete(self,column):
        if self.valid[column]==0:
            return False
        self.valid[column]-=1
        self.board[self.height-self.valid[column]-1][column]=0
        return True
    
    def heurSupport(self,column,p=False):
        num = {"X":0,"O":0,0:0}
        pos = {0:0,1:0,2:0,3:0,4:0}
        x = [[-1,-2,-3],[0,0,0],[1,2,3],[1,2,3],[1,2,3],[0,0,0],[-1,-2,-3]]
        y = [[-1,-2,-3],[-1,-2,-3],[-1,-2,-3],[0,0,0],[1,2,3],[1,2,3],[1,2,3]]
        index = self.height - self.valid[column]
        temp = self.board[index][column]
        for i in range(7):
            num = {"X":0,"O":0,0:0}
            num[temp]=1
            flag = True
            for j in range(3):
                y1 = column + y[i][j]
                x1 = index + x[i][j]
                if x1>=0 and y1>=0 and x1<self.height and y1<self.width:
                    if self.board[x1][y1]==temp or self.board[x1][y1]==0:
                        num[self.board[x1][y1]]+=1
                    else:
                        flag=False
                        break
            if flag:
                pos[num[temp]]+=1
        
        seven = [0 for i in range(7)]
        for i in range(7):
            num = {"X":0,"O":0,0:0}
            num[temp]=1
            flag = True
            for j in range(3):
                y1 = column + y[i][j]
                x1 = index + x[i][j]
                if x1>=0 and y1>=0 and x1<self.height and y1<self.width:
                    if self.board[x1][y1]==temp:
                        num[self.board[x1][y1]]+=1
                    else:
                        break
            seven[i]=num[temp]
        xtemp = [0,1,2]
        for i in range(3):
            if seven[xtemp[i]]+seven[xtemp[i]+4]-1>=3:
                if seven[xtemp[i]]+seven[xtemp[i]+4]-1>3:
                    pos[4]+=1
                else:
                    pos[3]+=1
        if p:
            print(seven)
        return pos
    
    def score(self,pos):
        penality = 0
        for i in range(2,5):
            penality += pos[i]*(10**i)
        return penality

    def heuristic(self,column):
        ans = self.score(self.heurSupport(column))
        index = self.height - self.valid[column]
        temp = self.board[index][column]
        self.delete(column)
        if temp=="X":
            self.insert(column,"O")
            heur = self.heurSupport(column)
            for i in range(4):
                heur[i] = heur[i+1]
            heur[4]=0
            #ans = ans - self.score(heur)
            ans = ans - self.score(self.heurSupport(column))
        else:
            self.insert(column,"X")
            heur = self.heurSupport(column)
            for i in range(4):
                heur[i] = heur[i+1]
            heur[4]=0
            #ans = self.score(heur) - ans
            ans = ans - self.score(self.heurSupport(column))
        self.delete(column)
        self.insert(column,temp)
        return ans

class Connect4:
    __board = None
    __player = None
    def __init__(self):
        self.__board = Board()
        self.__player = True

    def next_move(self,player,cur_depth,max_depth,column=0):
        if cur_depth == max_depth:
            return self.__board.heuristic(column),column
        if player:
            ma = float('-inf')
            index = -1
            for i in range(7):
                if self.__board.insert(i,"X"):
                    temp,j = self.next_move(False,cur_depth+1,max_depth,i)
                    if temp >= ma:
                        ma = temp
                        index = i
                    self.__board.delete(i)
            return ma,index
        else:
            mi = float('inf')
            index = -1
            for i in range(7):
                if self.__board.insert(i,"O"):
                    temp,j = self.next_move(True,cur_depth+1,max_depth,i)
                    if temp <= mi:
                        mi = temp
                        index = i
                    self.__board.delete(i)
            return mi,index
            

    def start_game(self):
        print("Game Started")
        count = 42
        while count!=0:
            count-=1
            move = -1
            if self.__player:
                self.__player = False
                temp = int(input("Enter a value from 1-7: "))
                move = temp
                while temp>6 or temp<0:
                    print(temp,"is not in range.")
                    temp = int(input("Enter a value from 1-7: "))
                    move = temp
                temp = self.__board.insert(temp,"X")
                while temp!=True:
                    print("Column alread full")
                    temp = int(input("Enter a value from 1-7: "))
                    move = temp
                    while temp>6 or temp<0:
                        print(temp,"is not in range.")
                        temp = int(input("Enter a value from 1-7: "))
                        move = temp
                    temp = self.__board.insert(temp,"X")
            else:
                self.__player = True
                val,index = self.next_move(False,0,5)
                self.__board.insert(index,"O")
                move = index
            self.__board.heurSupport(move,True)
            self.__board.disp()
            final = self.__board.heuristic(move)
            if final>=10000:
                print("X won")
                break
            elif final<=-10000:
                print("O won")
                break
        print("Game Ended!!!")
            



'''board = Board()
board.disp()
board.insert(1,"O")
board.insert(2,"O")
board.insert(3,"O")
board.insert(4,"X")
board.insert(4,"X")
board.insert(4,"X")
board.insert(4,"O")
"""for i in range(2):
    print(board.delete(1))"""
board.disp()
print(board.heurSupport(4))
print(board.heuristic(4))
'''

x = [[-1,-2,-3],[0,0,0],[1,2,3],[1,2,3],[1,2,3],[0,0,0],[-1,-2,-3]]
y = [[-1,-2,-3],[-1,-2,-3],[-1,-2,-3],[0,0,0],[1,2,3],[1,2,3],[1,2,3]]
a = [["-" for i in range(7)] for j in range(7)]

for i in range(7):
    for j in range(3):
        y1 = 3 + y[i][j]
        x1 = 3 + x[i][j]
        print(x1,y1,i)
        if x1>=0 and y1>=0 and x1<7 and y1<7:
            a[x1][y1]=i

for i in a:
    for j in i:
        print(j,end=" ")
    print()
print()

temp = Connect4()
temp.start_game()

