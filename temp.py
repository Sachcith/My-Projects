class Board:
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