from flask import Flask,render_template,request
from flask_socketio import SocketIO,send

app = Flask(__name__)
socketio = SocketIO(app)

import time
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
                if j=="X":
                    print("🟢",end="")
                elif j=="O":
                    print("🔴",end="")
                else:
                    print("⚪",end="")
            print()
        for i in range(self.width):
            print(i+1,end=" ")
        print("\n")

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
        if column<0 or column>=self.width:
            return pos
        x = [[-1,-2,-3],[0,0,0],[1,2,3],[1,2,3],[1,2,3],[0,0,0],[-1,-2,-3]]
        y = [[-1,-2,-3],[-1,-2,-3],[-1,-2,-3],[0,0,0],[1,2,3],[1,2,3],[1,2,3]]
        index = self.height - self.valid[column]
        temp = self.board[index][column]
        seven = [0 for i in range(7)]
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
                        break
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
            ans = ans + 2*self.score(self.heurSupport(column))
        else:
            self.insert(column,"X")
            heur = self.heurSupport(column)
            for i in range(4):
                heur[i] = heur[i+1]
            heur[4]=0
            ans = -1*(ans + 2*self.score(self.heurSupport(column)))
        self.delete(column)
        self.insert(column,temp)
        return ans

    def winloss(self,column,p=False):
        num = {"X":0,"O":0,0:0}
        pos = {0:0,1:0,2:0,3:0,4:0}
        if column<0 or column>=self.width:
            return pos
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
                    if (self.board[x1][y1]==temp):
                        num[self.board[x1][y1]]+=1
                    else:
                        flag=False
                        break
                else:
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
    
class Connect4:
    board = None
    player = None
    def __init__(self):
        self.board = Board()
        self.player = True

    def next_move_alpha_beta(self,player,cur_depth,max_depth,column=0,alpha=float('-inf'),beta=float('inf'),p=False):
        if cur_depth!=0:
            score = self.board.winloss(column)
            if score[4]>0 and (not player):
                return 10**5 + max_depth - cur_depth,column
            if score[4]>0 and player:
                return -(10**5 + max_depth - cur_depth),column
        if cur_depth == max_depth:
            return self.board.heuristic(column),column

        if player:
            ma = float('-inf')
            index = -1
            hello = ["N" for i in range(7)]
            for i in [3,2,4,1,5,0,6]:
                if self.board.insert(i,"X"):
                    temp,j = self.next_move_alpha_beta(False,cur_depth+1,max_depth,i,alpha,beta)
                    hello[i]=temp + max_depth - cur_depth
                    self.board.delete(i)
                    if j!=-1:
                        if temp > ma:
                            ma = temp
                            index = i
                        alpha = max(temp,alpha)
                        if alpha >= beta:
                            break
            if hello==["N" for i in range(7)]:
                return 0,column
            if p:
                print(hello)
            return ma + max_depth - cur_depth,index
        else:
            mi = float('inf')
            index = -1
            hello = ["N" for i in range(7)]
            for i in [3,2,4,1,5,0,6]:
                if self.board.insert(i,"O"):
                    temp,j = self.next_move_alpha_beta(True,cur_depth+1,max_depth,i,alpha,beta)
                    hello[i]=temp - max_depth + cur_depth,j
                    self.board.delete(i)
                    if j!=-1:
                        if temp < mi:
                            mi = temp
                            index = i
                        beta = min(temp,beta)
                        if alpha >= beta:
                            break
            if hello==["N" for i in range(7)]:
                return 0,column
            if p:
                print(hello)
            return mi - max_depth + cur_depth,index
            

    def start_game(self):
        print("Game Started")
        count = 42
        self.board.disp()
        while count!=0:
            count-=1
            move = -1
            if self.__player:
                self.__player = False
                while True:
                    try:
                        temp = int(input("Enter a value from 1-7: "))
                        if temp<1 or temp>7:
                            continue
                        if not self.board.insert(temp-1,"X"):
                            continue
                        break
                    except KeyboardInterrupt:
                        exit()
                    except:
                        continue
                
                move = temp-1
            else:
                self.__player = True
                time1 = time.time()
                val,index = self.next_move_alpha_beta(False,0,6,p=True)
                print(f"Time taken by AI: {round(time.time()-time1,3)}s")
                self.board.insert(index,"O")
                move = index
                print(f"Index: {index} Value: {val}")
            final = self.board.winloss(move,True)
            print("Current move:",move+1)
            self.board.disp()
            if final[4]>0 and (not self.__player):
                print("🟢 won")
                break
            elif final[4]>0 and self.__player:
                print("🔴 won")
                break
        if count==0:
            print("Draw......Noice")
        print("Game Ended!!!")

board = Connect4()

@app.route('/')
def home():
    return render_template('index.html')

@socketio.on("move")
def move(data):
    col = int(data["col"])
    print(f"Column Clicked: {col}")
    if(board.board.insert(col,"X")==False):
        socketio.emit("debug",{"debug": "Column Already Full!!"})
    else:
        socketio.emit("debug",{"debug": "Okay!!"})
        socketio.emit("player",{"cell":col+7*(6-board.board.valid[col])})
        print(board.board.valid)

    



if __name__=="__main__":
    app.run(debug=True)