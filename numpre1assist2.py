# 数独解読プログラム

goal = [0b100000000,0b010000000,0b001000000,
        0b000100000,0b000010000,0b000001000,
        0b000000100,0b000000010,0b000000001]

def fileLead(filePath):
    # テキストを１行づつ読み込む
    import os
    fileName = filePath
    targetFile = open(fileName)
    obj = targetFile.readlines()
    sudata = [[0 for i in range(9)] for j in range(9)]
    for i in range(9):
        for j in range(9):
            sudata[i][j] = int(obj[i][j])
    return sudata

def questionPrint(sudata):
    # 問題表示
    for i in sudata:
        print(i)
    print()

def suisokuBanShoki(sudata, goal):
    # 推定盤の初期化
    shokiS = 0b111111111
    suiteiBan = [[shokiS for i in range(9)] for j in range(9)]
    for i in range(9):
        for j in range(9):
            for k in range(9):
                if sudata[i][j] == (k + 1):
                    suiteiBan[i][j] = goal[k]
    return suiteiBan

def lineSearch(sudata):
    # 行方向に検索し、存在していない数を候補として行ごとlineGuessに蓄積
    lineGuess = []
    for i in range(9):
        lineGuessNum = 0b111111111
        for j in range(9):
            lineGuessNum = suiteiSan(sudata[i][j], lineGuessNum)
        lineGuess.append(lineGuessNum)
    return lineGuess

def lineSuitei(sudata, suiteiBan, lineGuess):
    # 数値が確定していない推定盤に行推定値を入れる
    for i in range(9):
        for j in range(9):
            if sudata[i][j] == 0:
                suiteiBan[i][j] = suiteiBan[i][j] & lineGuess[i]
    return suiteiBan

def retsuSearch(sudata):
    # 列方向に検索し、存在していない数を候補として列ごとretsuSuiに蓄積
    retsuGuess = []
    for j in range(9):
        retsuGuessNum = 0b111111111
        for i in range(9):
            retsuGuessNum = suiteiSan(sudata[i][j], retsuGuessNum)
        retsuGuess.append(retsuGuessNum)
    return retsuGuess

def retsuSuitei(sudata, suiteiBan, retsuGuess):
    # 推定盤に列推定値を加味する
    for i in range(9):
        for j in range(9):
            if sudata[i][j] == 0:
                suiteiBan[i][j] = suiteiBan[i][j] & retsuGuess[j]
    return suiteiBan

def ereaSearch(sudata):
    # ９マスエリア内を検索し、存在していない数を候補としてエリアごとereaGuessに蓄積
    ereaGuess = []
    for ereaNum in range(9):
        ereaGuessNum = 0b111111111
        for i in range(3):
            gyoPlusNum = (ereaNum // 3) * 3
            for j in range(3):
                retsuPlusNum = (ereaNum % 3) * 3
                ereaGuessNum = suiteiSan(sudata[gyoPlusNum + i][retsuPlusNum + j], ereaGuessNum)
        ereaGuess.append(ereaGuessNum)
    return ereaGuess

def ereaSuitei(sudata, suiteiBan, ereaGuess):
    # 推定盤にエリア推定値を加味する
    for ereaNum in range(9):
        for i in range(3):
            gyoPlusNum = (ereaNum // 3) * 3
            for j in range(3):
                retsuPlusNum = (ereaNum % 3) * 3
                if sudata[gyoPlusNum + i][retsuPlusNum + j] == 0:
                    suiteiBan[gyoPlusNum + i][retsuPlusNum + j] = suiteiBan[gyoPlusNum + i][retsuPlusNum + j] & ereaGuess[ereaNum]
    return suiteiBan

def suiteiSan(sudataNum, suiteiNum):
    # 盤値の推定値ビットを０にする
    suiteiList = [0b011111111, 0b101111111, 0b110111111,
                  0b111011111, 0b111101111, 0b111110111,
                  0b111111011, 0b111111101, 0b111111110]
    for i in range(9):
        if sudataNum == i + 1:
            suiteiNum = suiteiNum & suiteiList[i]
    return suiteiNum

def goalJudge(suitei, goal):
    # 1マスの推定値が確定したかどうか調べ、確定なら確定値を返す
    kakuteiChi = 1
    for g in goal:
        if suitei == g:
            return kakuteiChi
            break
        kakuteiChi += 1
    return 0

def banJudge(sudata, suiteiBan):
    # 推定値が１つならば、確定する。
    for i in range(9):
        for j in range(9):
            if sudata[i][j] == 0:
                kakuteiChi = goalJudge(suiteiBan[i][j], goal)
                if kakuteiChi != 0:
                    sudata[i][j] = kakuteiChi
                    suiteiBan[i][j] = goal[kakuteiChi - 1]
    return sudata

def finishHan(sudata):
    # 盤値をしらべて、０がなければTrueを返す。
    for i in sudata:
        if 0 in i:
            return False
            break
    return True

def uniLineCheck(sudata, suiteiBan, goal):
    # 行方向の推定値が１つしかないものを決定する
    for i in range(9):
        count = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
        for j in range(9):
            # if sudata[i][j] == 0:
                count = uniSuiteiCheck(suiteiBan[i][j], count, j, goal)
        for k in range(9):
            if count[k][0] == 1:
                sudata[i][count[k][1]] = k + 1
                suiteiBan[i][count[k][1]] = goal[k]
    return sudata

def uniRetsuCheck(sudata, suiteiBan, goal):
    for j in range(9):
        count = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
        for i in range(9):
            # if sudata[i][j] == 0:
                count = uniSuiteiCheck(suiteiBan[i][j], count, i, goal)
        for k in range(9):
            if count[k][0] == 1:
                sudata[count[k][1]][j] = k + 1
                suiteiBan[count[k][1]][j] = goal[k]
    return sudata

def uniEreaCheck(sudata, suiteiBan, goal):
    for ereaNum in range(9):
        count = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
        for i in range(9):
            gyoNum = (ereaNum // 3) * 3 + (i // 3)
            retsuNum = (ereaNum % 3) * 3 + (i % 3)
            count = uniSuiteiCheck(suiteiBan[gyoNum][retsuNum], count, i, goal)
        for k in range(9):
            if count[k][0] == 1:
                s = count[k][1]
                gyoNum = (ereaNum // 3) * 3 + (s // 3)
                retsuNum = (ereaNum % 3) * 3 + (s % 3)
                sudata[gyoNum][retsuNum] = k + 1
                suiteiBan[gyoNum][retsuNum] = goal[k]
    return sudata

def uniSuiteiCheck(banSui, count, posNum, goal):
    for i in range(9):
        if banSui & goal[i] == goal[i]:
            count[i][0] += 1
            count[i][1] = posNum
    return count

def changeNum(sudataBefore, sudataAfter):
    changeNum = 0
    for i in range(9):
        for j in range(9):
            if sudataBefore[i][j] != sudataAfter[i][j]:
                changeNum += 1
    return changeNum

def suiteichiHyouji(shiteiSuiteiChi, suiteiBan, suiteiHyoujiBan, goal):
    for i in range(9):
        for j in range(9):
            if suiteiBan[i][j] & goal[shiteiSuiteiChi - 1] == goal[shiteiSuiteiChi - 1]:
                suiteiHyoujiBan[i][j] = shiteiSuiteiChi

    return suiteiHyoujiBan

def changeKai(sudataShoki, sudata):
    change = 0
    for i in range(9):
        for j in range(9):
            if sudataShoki[i][j] != sudata[i][j]:
                change += 1
    return change

def kanousu(suiteiBan, goal):
    shokiKanouSu = 0
    kanouSuBan = [[shokiKanouSu for i in range(9)] for j in range(9)]
    kanouSuList = [[] for k in range(81)]
    for i in range(9):
        for j in range(9):
            kanousuCount = 0
            for k in range(9):
                if suiteiBan[i][j] & goal[k] == goal[k]:
                    kanousuCount += 1
                    kanouSuList[i*9+j].append(k + 1)
            kanouSuBan[i][j] = kanousuCount
    return kanouSuBan, kanouSuList

if __name__=='__main__':
    # 初期条件設定
    sufile = '/Volumes/KazuMoriHD 1/40Computer/Python/Numpre/numpyNumber2.txt'
    sudata = fileLead(sufile) # 数独データをファイルから読み込む
    kuriNum = 10 # 回答検索ループの最終回等がない場合の最大ループ回数
    # 初期盤面出力
    print('初期盤面')
    questionPrint(sudata)
    print()

    # 回答検索ループ
    round = 1
    change = 1
    while (finishHan(sudata) == False) and (round <= kuriNum) and (change >= 1):
        # sudataShoki = sudata[:]
        # 推定盤面の初期化
        suiteiBan = suisokuBanShoki(sudata, goal)
        # 行方向の推定
        suiteiBan = lineSuitei(sudata, suiteiBan, lineSearch(sudata))
        # 列方向の推定
        suiteiBan = retsuSuitei(sudata, suiteiBan, retsuSearch(sudata))
        # ９マスごとの推定
        suiteiBan = ereaSuitei(sudata, suiteiBan, ereaSearch(sudata))
        # Hyoujichiの推定値の存在する盤面の表示
        shiteiSuiteiChi = 0
        if shiteiSuiteiChi != 0:
            shokiSuiteiChi = 0
            suiteiHyoujiBan = [[shokiSuiteiChi for i in range(9)] for j in range(9)]
            print('指定推定値=' + str(shiteiSuiteiChi), end='\n')
            questionPrint(suiteichiHyouji(shiteiSuiteiChi, suiteiBan, suiteiHyoujiBan, goal))

        sudata = banJudge(sudata, suiteiBan)
        sudata = uniLineCheck(sudata, suiteiBan, goal)
        sudata = uniRetsuCheck(sudata, suiteiBan, goal)
        sudata = uniEreaCheck(sudata, suiteiBan, goal)
        # ループ回数増加
        print(str(round) + '回目')
        questionPrint(sudata)
        # 変化確認
        #change = changeKai(sudataShoki, sudata)
        round += 1

    if finishHan(sudata) == False:
        # マスごとの推定値の数を表示
        print('マスごとの可能数')
        kanousuBan, kanousuList = kanousu(suiteiBan, goal)
        questionPrint(kanousuBan)
        # マスごとの推定値を表示
        print('マスごとの可能性のある数リスト')
        gyo = 0
        retsu = 1
        for kanoulist in kanousuList:
            if retsu % 9 == 1:
                gyo += 1
                print()
                print (str(gyo) + '行目')
                if retsu // 9 >=1:
                    retsu = 1
            if retsu <= 9:
                print(kanoulist)
            retsu += 1

    #️ 確定盤表示
    print('確定盤面：' + str(round - 1) + '回実施')
    questionPrint(sudata)