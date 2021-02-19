import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as mdates
import seaborn as sns 

from faceVerification import *
# Data


def drawGraph(xVal, data, lbs):

    colors = {
                "DPJ": "#FF0000",
                "LDP": '#008000',
                "Komeito": "#2471A3",
                "SDP": "#5DADE2",
                "JIP": "#82E0AA",
                "PP": "#F5B041",
                'CP': '#A93226'
                };

    wrongList = []
    rightList = []
    missList = []

    lg = len(data[0])

    tempList = []

    colorList = [colors[d] for d in lbs]

    # colorList = ['#FF0000','#0000FF','#00FF00']

    for a in data:
        tempList.append([])

    lNum = len(data)
    for i in range(lg):
        sumVal = 0
        for l in data:
            sumVal += l[i]
        for k in range(lNum):
            tempList[k].append(data[k][i]/sumVal * 100)
            # tempList[k].append(data[k][i])


    unifiData = [wrongList, missList, rightList]
    
    x = [dt.datetime.strptime(d, '%Y_%m').date() for d in xVal]

    pal = sns.color_palette("Set1")

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    # plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    # print(mdates.DayLocator())
    plt.stackplot(x, tempList, labels=lbs, colors=colorList, alpha=0.9)
    plt.ylabel('Percentage')
    # plt.xticks(1)

    # plt.gcf().autofmt_xdate()

    plt.legend(loc='upper left')

    plt.show()


def getPartyData():

    isFirstLine = True
    monthList = []

    missList = []
    wrongList = []
    sameList = []

    lastMonth = ''
    sameVal = 0
    missVal = 0
    wrongVal = 0

    res = {}

    with open('results8.csv', 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';', quotechar='"')
        for row in spamreader:
            if isFirstLine:
                isFirstLine = False
                continue

            date = row[0][0:7]
            myList = row[7].split(' | ')

            for name in myList:
                if name == '':
                    continue
                if name not in res:
                    res[name] = {}

                if date not in res[name]:
                    res[name][date] = 1
                else:
                    res[name][date] += 1

    return res

def accuracy():

    isFirstLine = True
    monthList = []

    missList = []
    wrongList = []
    sameList = []

    lastMonth = ''
    sameVal = 0
    missVal = 0
    wrongVal = 0

    checkDict = {}
    k = 0

    totalSame = 0
    totalMiss = 0
    totalWrong = 0
    with open('results8.csv', 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';', quotechar='"')
        for row in spamreader:
            if isFirstLine:
                isFirstLine = False
                continue

            date = row[0][0:7]

            nameListGT = row[6].split(' | ')
            myList = row[9].split(' | ')

            sv = 0
            mv = 0
            wv = 0

            for name in nameListGT:
                if name == '':
                    continue
                if name in myList:
                    totalSame += 1
                    sv += 1
                else:
                    totalMiss += 1
                    mv += 1
            for name in myList:
                if name == '':
                    continue
                if name not in nameListGT:
                    wv += 1
                    totalWrong += 1
            

            if date != lastMonth:
                if lastMonth != '':
                    missList.append(missVal)
                    sameList.append(sameVal)
                    wrongList.append(wrongVal)

                missVal = mv
                sameVal = sv
                wrongVal = wv    
                monthList.append(date)
                lastMonth = date
            else:
                missVal += mv
                sameVal += sv
                wrongVal += wv

        missList.append(missVal)
        sameList.append(sameVal)
        wrongList.append(wrongVal)

    return [monthList, wrongList, missList, sameList]

def nameAccuracy3():

    isFirstLine = True
    monthList = []

    missList = []
    wrongList = []
    sameList = []

    lastMonth = ''
    sameVal = 0
    missVal = 0
    wrongVal = 0

    nameDictv = {}

    nameDictm = {}

    nameDictc = {}

    tempNameList = []

    res = {}
    with open('resu.csv', 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';', quotechar='"')
        for row in spamreader:
            if isFirstLine:
                isFirstLine = False
                continue

            date = row[0][0:7]



            nameListGT = row[6].split(' | ')
            if len(nameListGT) == 0:
                continue
            
            myList = row[7].split(' | ')

            sv = 0
            mv = 0
            wv = 0


            for name in nameListGT:
                if name == '':
                    continue
                if name not in tempNameList:
                    tempNameList.append(name)
                if name not in nameDictv:
                    nameDictv[name] = {
                        'same': 0,
                        'miss': 0,
                        'wrong': 0
                    }
                if name in myList:
                    sv += 1
                    nameDictv[name]['same'] += 1
                else:
                    mv += 1
                    nameDictv[name]['miss'] += 1

            for name in myList:
                if name not in nameDictv:
                    nameDictv[name] = {
                            'same': 0,
                            'miss': 0,
                            'wrong': 0
                        }
                if name not in nameListGT:
                    nameDictv[name]['wrong'] += 1


            myList = row[9].split(' | ')

            for name in nameListGT:
                if name == '':
                    continue
                if name not in nameDictc:
                    nameDictc[name] = {
                        'same': 0,
                        'miss': 0,
                        'wrong': 0
                    }
                if name in myList:
                    sv += 1
                    nameDictc[name]['same'] += 1
                else:
                    mv += 1
                    nameDictc[name]['miss'] += 1

            for name in myList:
                if name not in nameDictc:
                    nameDictc[name] = {
                            'same': 0,
                            'miss': 0,
                            'wrong': 0
                        }
                if name not in nameListGT:
                    nameDictc[name]['wrong'] += 1


            myList = row[8].split(' | ')

            for name in nameListGT:
                if name == '':
                    continue
                if name not in nameDictm:
                    nameDictm[name] = {
                        'same': 0,
                        'miss': 0,
                        'wrong': 0
                    }
                if name in myList:
                    sv += 1
                    nameDictm[name]['same'] += 1
                else:
                    mv += 1
                    nameDictm[name]['miss'] += 1

            for name in myList:
                if name not in nameDictm:
                    nameDictm[name] = {
                            'same': 0,
                            'miss': 0,
                            'wrong': 0
                        }
                if name not in nameListGT:
                    nameDictm[name]['wrong'] += 1

        for name in nameDictv:
            if name == '':
                continue
            if name not in res:
                res[name] = []

            vl = nameDictv[name]
            ml = nameDictm[name]
            cl = nameDictc[name]

            res[name].append(vl['same']/(vl['same']+vl['miss']))
            res[name].append(ml['same']/(ml['same']+ml['miss']))
            res[name].append(cl['same']/(cl['same']+cl['miss']))

    temp = []


    st = MyMethodScreenTime()

    nameList = []

    vlList = []
    mlList = []

    clList = []
    for name in tempNameList:

        # res.append(nameDictm)
        nameList.append(name)
        nameList.append('')        
        nameList.append('')
        if name in nameDictc:
            tc = nameDictc[name]['same']
            mc = nameDictc[name]['miss']
            wc = nameDictc[name]['wrong']
        else:
            tc = 0
            mc = 0
            wc = 0

        clList.append(tc)
        clList.append(mc)
        clList.append(wc)

        if name in nameDictv:
            tv = nameDictv[name]['same']
            mv = nameDictv[name]['miss']
            wv = nameDictv[name]['wrong']
        else:
            tv = 0
            mv = 0
            wv = 0

        vlList.append(tv)
        vlList.append(mv)
        vlList.append(wv)

        if name in nameDictm:
            tm = nameDictm[name]['same']
            mm = nameDictm[name]['miss']
            wm = nameDictm[name]['wrong']
        else:
            tm = 0
            mm = 0
            wm = 0
        mlList.append(tm)
        mlList.append(mm)
        mlList.append(wm)


    drawHorizonChart(nameList, clList, mlList)

def nameAccuracy():

    isFirstLine = True
    monthList = []

    missList = []
    wrongList = []
    sameList = []

    lastMonth = ''
    sameVal = 0
    missVal = 0
    wrongVal = 0

    nameDictv = {}

    nameDictm = {}

    nameDictc = {}

    res = {}
    with open('results8.csv', 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';', quotechar='"')
        for row in spamreader:
            if isFirstLine:
                isFirstLine = False
                continue

            date = row[0][0:7]



            nameListGT = row[6].split(' | ')
            if len(nameListGT) == 0:
                continue

            
            myList = row[7].split(' | ')

            sv = 0
            mv = 0
            wv = 0

            for name in nameListGT:

                if name == '':
                    continue
                if name not in nameDictv:
                    nameDictv[name] = {
                        'same': 0,
                        'miss': 0,
                        'wrong': 0
                    }
                if name in myList:
                    sv += 1
                    nameDictv[name]['same'] += 1
                else:
                    mv += 1
                    nameDictv[name]['miss'] += 1


            myList = row[9].split(' | ')

            for name in nameListGT:
                if name == '':
                    continue
                if name not in nameDictc:
                    nameDictc[name] = {
                        'same': 0,
                        'miss': 0,
                        'wrong': 0
                    }
                if name in myList:
                    sv += 1
                    nameDictc[name]['same'] += 1
                else:
                    mv += 1
                    nameDictc[name]['miss'] += 1


            myList = row[8].split(' | ')

            for name in nameListGT:
                if name == '':
                    continue
                if name not in nameDictm:
                    nameDictm[name] = {
                        'same': 0,
                        'miss': 0,
                        'wrong': 0
                    }
                if name in myList:
                    sv += 1
                    nameDictm[name]['same'] += 1
                else:
                    mv += 1
                    nameDictm[name]['miss'] += 1

        for name in nameDictv:
            if name not in res:
                res[name] = []

            vl = nameDictv[name]
            ml = nameDictm[name]
            cl = nameDictc[name]
            res[name].append(vl['same']/(vl['same']+vl['miss']))
            res[name].append(ml['same']/(ml['same']+ml['miss']))
            res[name].append(cl['same']/(cl['same']+cl['miss']))

    temp = []

    st = MyMethodScreenTime()

    for name in res:
        missVal = 0
        sameVal = 0
        for seg in st[name]:
            missVal += st[name][seg]['miss']
            sameVal += st[name][seg]['same']

        t = 0
        if missVal + sameVal > 0:
            t = sameVal/(missVal + sameVal)
        temp.append({
            'name': name,
            'vl': res[name][0],
            'ml': res[name][1],
            'sl': res[name][2],
            'tl': t
            })

    stres = sorted(temp, key=lambda k: k['ml'])

    nameList = []
    vlList = []
    mlList = []

    for item in stres:
        nameList.append(item['name'])
        vlList.append(item['ml'])
        mlList.append(item['tl'])



    partyDrawHorizon(nameList, vlList, mlList)


def screenTimeAcc():
    data = MyMethodScreenTime()
    checkDict = {}
    for oneFace in data:
        for oneSeg in data[oneFace]:
            if oneSeg not in checkDict:
                checkDict[oneSeg] = data[oneFace][oneSeg]
            checkDict[oneSeg]['miss'] += data[oneFace][oneSeg]['miss']
            checkDict[oneSeg]['same'] += data[oneFace][oneSeg]['same']
            checkDict[oneSeg]['wrong'] += data[oneFace][oneSeg]['wrong']

    al = []

    for item in checkDict:
        temp = checkDict[item]
        temp['date'] = item
        al.append(temp)

    stres = sorted(al, key=lambda k: k['date'])
    
    monthList = []
    wrongList = []
    missList = []
    sameList = []

    for a in stres:
        monthList.append(a['date'])
        wrongList.append(a['wrong'])
        missList.append(a['miss'])
        sameList.append(a['same'])

    print(monthList, wrongList, missList, sameList)
    drawGraph(monthList, [wrongList, missList, sameList], ['False Positive', 'False Negative', 'True Positive'])


# screenTimeAcc()

# t = accuracy()

# drawGraph(t[0], [t[1], t[2], t[3]], ['False Positive', 'Flase Negative', 'True Positive'])

def partyConnection():
    nameDict = {'Yukio HATOYAMA': 'DPJ',
                'Junichiro KOIZUMI': 'LDP', 
                'Takenori KANZAKI': 'Komeito',
                'Taro ASO': 'LDP',
                'Yasuo FUKUDA': 'LDP',
                'Mizuho FUKUSHIMA': 'SDP',
                'Katsuya OKADA': 'DPJ',
                'Akihiro OHTA': 'Komeito',
                'Naoto KAN': 'DPJ',
                'Shinzo ABE': 'LDP',
                'Takako DOI': 'SDP',
                'Shizuka KAMEI': 'LDP',
                'Kazuo SHII': 'CP',
                'Ichiro OZAWA': 'DPJ',
                'Yukio EDANO': 'DPJ',
                'Sadakazu TANIGAKI': 'LDP',
                'Yoshihiko NODA': 'DPJ',
                'Natsuo YAMAGUCHI': 'Komeito',
                'Seiji MAEHARA': 'DPJ',
                'Yoshimi WATANABE': 'PP',
                'Shintaro ISHIHARA': 'JIP',
                'Toru HASHIMOTO': 'JIP'
                }
    td = getPersonTime()
    res = []

    partyDict = {}
    for oneFace in td:
        partyOne = nameDict[oneFace]
        if partyOne not in partyDict:
            partyDict[partyOne] = {}
        for anotherFace in td:
            if oneFace == anotherFace:
                continue
            partyTwo = nameDict[anotherFace]
            if partyTwo not in partyDict[partyOne]:
                partyDict[partyOne][partyTwo] = 0

            for oneSeg in td[oneFace]:
                if oneSeg in td[anotherFace]:
                    partyDict[partyOne][partyTwo] += 1


    testDict = {}
    for oneParty in partyDict:
        for p2 in partyDict[oneParty]:
            temp = oneParty + p2

            res.append([oneParty, p2, partyDict[oneParty][p2]])


# partyConnection()

def screenTime():
    nameDict = {'Yukio HATOYAMA': 'DPJ',
                'Junichiro KOIZUMI': 'LDP', 
                'Takenori KANZAKI': 'Komeito',
                'Taro ASO': 'LDP',
                'Yasuo FUKUDA': 'LDP',
                'Mizuho FUKUSHIMA': 'SDP',
                'Katsuya OKADA': 'DPJ',
                'Akihiro OTA': 'Komeito',
                'Naoto KAN': 'DPJ',
                'Shinzo ABE': 'LDP',
                'Takako DOI': 'SDP',
                'Shizuka KAMEI': 'LDP',
                'Kazuo SHII': 'CP',
                'Ichiro OZAWA': 'DPJ',
                'Yukio EDANO': 'DPJ',
                'Sadakazu TANIGAKI': 'LDP',
                'Yoshihiko NODA': 'DPJ',
                'Natsuo YAMAGUCHI': 'Komeito',
                'Seiji MAEHARA': 'DPJ',
                'Yoshimi WATANABE': 'PP',
                'Shintaro ISHIHARA': 'JIP',
                'Toru HASHIMOTO': 'JIP'
                }

    dateList = []
    td = getPartyData()
    res = []
    partyList = []
    partyDict = {}
    for oneFace in td:
        partyName = nameDict[oneFace]
        if partyName not in partyList:
            partyList.append(partyName)
            partyDict[partyName] = {}


        for oneTime in td[oneFace]:
            if oneTime not in dateList:
                dateList.append(oneTime)
            if oneTime not in partyDict[partyName]:
                partyDict[partyName][oneTime] = 0
            partyDict[partyName][oneTime] += 1#td[oneFace][oneTime]


    dateList.sort()

    for oneParty in partyList:
        tempList = []

        for oneTime in dateList:
            if oneTime in partyDict[oneParty]:
                tempList.append(partyDict[oneParty][oneTime])
            else:
                tempList.append(0)
        res.append(tempList)

    res[0][0]  = 1

    drawGraph(dateList, res, partyList)


def screenTimeMyMethod():
    data = getMyMethodScreenTime()
    myData = {}

    for name in data:
        myData[name] = {}
        for item in data[name]:
            month = item[0:7]
            for pair in data[name][item]:
                if month not in myData[name]:
                    myData[name][month] = pair[1] - pair[0]
                else:
                    myData[name][month] += pair[1] - pair[0]
    return myData



# screenTimeMyMethod()

def drawHorizonChart(titles, leftList, rightList):
    
    # Sort by number of sales staff
    colors = ['#1f77b4','#aec7e8','#ff7f0e','#ffbb78','#2ca02c','#98df8a','#d62728','#ff9896','#9467bd','#c5b0d5','#8c564b','#c49c94','#e377c2','#f7b6d2','#7f7f7f','#c7c7c7','#bcbd22','#dbdb8d','#17becf','#9edae5']
    
    colorsDict = {
                "DPJ": "#FF0000",
                "LDP": '#008000',
                "Komeito": "#2471A3",
                "SDP": "#5DADE2",
                "JIP": "#82E0AA",
                "PP": "#F5B041",
                'CP': '#A93226'
                };

    colorList = []

    tempColors = ['#2ca02c','#9467bd','#ff9896']

    for oneItem in titles:
        colorList.append(colorsDict[oneItem])


    y = np.arange(len(titles))

    fig, axes = plt.subplots(ncols=2, sharey=True)
    axes[0].barh(y, leftList, align='center', color=colorList, zorder=10)
    axes[0].set(title='Total Number of TV news segments')

    axes[1].barh(y, rightList, align='center', color=colorList, zorder=10)
    axes[1].set(title='Average screen time of each TV news segment (seconds)')

    axes[0].invert_xaxis()
    axes[0].set(yticks=y, yticklabels=titles)
    axes[0].yaxis.tick_right()

    for ax in axes.flat:
        ax.margins(0.03)
        ax.grid(True)

    fig.tight_layout()
    fig.subplots_adjust(wspace=0.4)
    plt.show()


def partyDrawHorizon(titles, leftList, rightList):
    
    # Sort by number of sales staff
    colors = ['#1f77b4','#aec7e8','#ff7f0e','#ffbb78','#2ca02c','#98df8a','#d62728','#ff9896','#9467bd','#c5b0d5','#8c564b','#c49c94','#e377c2','#f7b6d2','#7f7f7f','#c7c7c7','#bcbd22','#dbdb8d','#17becf','#9edae5']
    
    nameDict = {'Yukio HATOYAMA': 'DPJ',
                'Junichiro KOIZUMI': 'LDP', 
                'Takenori KANZAKI': 'Komeito',
                'Taro ASO': 'LDP',
                'Yasuo FUKUDA': 'LDP',
                'Mizuho FUKUSHIMA': 'SDP',
                'Katsuya OKADA': 'DPJ',
                'Akihiro OTA': 'Komeito',
                'Naoto KAN': 'DPJ',
                'Shinzo ABE': 'LDP',
                'Takako DOI': 'SDP',
                'Shizuka KAMEI': 'LDP',
                'Kazuo SHII': 'CP',
                'Ichiro OZAWA': 'DPJ',
                'Yukio EDANO': 'DPJ',
                'Sadakazu TANIGAKI': 'LDP',
                'Yoshihiko NODA': 'DPJ',
                'Natsuo YAMAGUCHI': 'Komeito',
                'Seiji MAEHARA': 'DPJ',
                'Yoshimi WATANABE': 'PP',
                'Shintaro ISHIHARA': 'JIP',
                'Toru HASHIMOTO': 'JIP'
                }

    colorsDict = {
                "DPJ": "#FF0000",
                "LDP": '#008000',
                "Komeito": "#2471A3",
                "SDP": "#5DADE2",
                "JIP": "#82E0AA",
                "PP": "#F5B041",
                'CP': '#A93226'
                };

    colorList = []

    for name in titles:
        partyID = nameDict[name]
        color = colorsDict[partyID]
        colorList.append(color)

    y = np.arange(len(titles))

    fig, axes = plt.subplots(ncols=2, sharey=True)
    axes[0].barh(y, leftList, align='center', color=colorList, zorder=10)
    axes[0].set(title='Total Number of TV news segments')

    axes[1].barh(y, rightList, align='center', color=colorList, zorder=10)
    axes[1].set(title='Average screen time of each TV news segment (seconds)')

    axes[0].invert_xaxis()
    axes[0].set(yticks=y, yticklabels=titles)
    axes[0].yaxis.tick_right()

    for ax in axes.flat:
        ax.margins(0.03)
        ax.grid(True)

    fig.tight_layout()
    fig.subplots_adjust(wspace=1.1)
    plt.show()

def horizonChart():
    pt = getPersonTime()
    print(pt)
    nameDict = {'Yukio HATOYAMA': 'DPJ',
                'Junichiro KOIZUMI': 'LDP', 
                'Takenori KANZAKI': 'Komeito',
                'Taro ASO': 'LDP',
                'Yasuo FUKUDA': 'LDP',
                'Mizuho FUKUSHIMA': 'SDP',
                'Katsuya OKADA': 'DPJ',
                'Akihiro OHTA': 'Komeito',
                'Naoto KAN': 'DPJ',
                'Shinzo ABE': 'LDP',
                'Takako DOI': 'SDP',
                'Shizuka KAMEI': 'LDP',
                'Kazuo SHII': 'CP',
                'Ichiro OZAWA': 'DPJ',
                'Yukio EDANO': 'DPJ',
                'Sadakazu TANIGAKI': 'LDP',
                'Yoshihiko NODA': 'DPJ',
                'Natsuo YAMAGUCHI': 'Komeito',
                'Seiji MAEHARA': 'DPJ',
                'Yoshimi WATANABE': 'PP',
                'Shintaro ISHIHARA': 'JIP',
                'Toru HASHIMOTO': 'JIP'
                }
    res = []
    for oneName in pt:
        temp = {
            'name': oneName,
            'tt': 0,
            'count': len(pt[oneName])
        }

        for oneMonth in pt[oneName]:
            temp['tt'] += pt[oneName][oneMonth]
        res.append(temp)

    partyDict = {}
    for oneName in pt:
        partyName = nameDict[oneName]

        if partyName not in partyDict:
            partyDict[partyName] = {
                'name': partyName,
                'tt': 0,
                'count': 0
            }
        partyDict[partyName]['count'] += len(pt[oneName])
        for oneSeg in pt[oneName]:
            partyDict[partyName]['tt'] += pt[oneName][oneSeg]

    nameList = []
    segList = []
    timeList = []

    tres = []
    for i in partyDict:
        tres.append(partyDict[i])

    stres = sorted(tres, key=lambda k: k['count'])

    for oneItem in stres:
        nameList.append(oneItem['name'])
        segList.append(oneItem['count'])
        timeList.append(oneItem['tt']/oneItem['count'])
    drawHorizonChart(nameList, segList, timeList)


def groundTruthHorizonChart():

    gtList = []
    gtData = getGroundScreenTime()
    for oneName in gtData:
        temp = {
            'count' : len(gtData[oneName]),
            'name': oneName,
            'tt': 0
        }
        
        for oneSeg in gtData[oneName]:
            timeList = gtData[oneName][oneSeg]
            for onePair in timeList:
               temp['tt'] += onePair[1] - onePair[0] + 1

        gtList.append(temp)

    stList = sorted(gtList, key=lambda k: k['count'])

    nameList = []
    l0 = []
    l1 = []
    for item in stList:
        nameList.append(item['name'])
        l0.append(item['count'])
        l1.append(item['tt']/item['count'])
    partyDrawHorizon(nameList, l0, l1)


def groundTruthPartyScreenTimeHorizonChart():

    nameDict = {'Yukio HATOYAMA': 'DPJ',
                'Junichiro KOIZUMI': 'LDP', 
                'Takenori KANZAKI': 'Komeito',
                'Taro ASO': 'LDP',
                'Yasuo FUKUDA': 'LDP',
                'Mizuho FUKUSHIMA': 'SDP',
                'Katsuya OKADA': 'DPJ',
                'Akihiro OTA': 'Komeito',
                'Naoto KAN': 'DPJ',
                'Shinzo ABE': 'LDP',
                'Takako DOI': 'SDP',
                'Shizuka KAMEI': 'LDP',
                'Kazuo SHII': 'CP',
                'Ichiro OZAWA': 'DPJ',
                'Yukio EDANO': 'DPJ',
                'Sadakazu TANIGAKI': 'LDP',
                'Yoshihiko NODA': 'DPJ',
                'Natsuo YAMAGUCHI': 'Komeito',
                'Seiji MAEHARA': 'DPJ',
                'Yoshimi WATANABE': 'PP',
                'Shintaro ISHIHARA': 'JIP',
                'Toru HASHIMOTO': 'JIP'
                }

    checkDict = {}
    gtList = []
    gtData = getGroundScreenTime()
    for oneName in gtData:

        partyName = nameDict[oneName]
        if partyName not in checkDict:
            checkDict[partyName] = {
                                        'count' : 0,
                                        'name': partyName,
                                        'tt': 0
                                    }

        checkDict[partyName]['count'] += len(gtData[oneName])
        
        for oneSeg in gtData[oneName]:
            timeList = gtData[oneName][oneSeg]
            for onePair in timeList:
               checkDict[partyName]['tt'] += onePair[1] - onePair[0] + 1

    for oneParty in checkDict:
        gtList.append(checkDict[oneParty])


    stList = sorted(gtList, key=lambda k: k['count'])

    nameList = []
    l0 = []
    l1 = []
    for item in stList:
        nameList.append(item['name'])
        l0.append(item['count'])
        l1.append(item['tt']/item['count'])
    drawHorizonChart(nameList, l0, l1)


def percentageCal(l):
    sumVal = 0
    for i in l:
        sumVal += i
    for i in l:
        print(i, i/sumVal)

# percentageCal([216, 668, 36])
# horizonChart()

# groundTruthPartyScreenTimeHorizonChart()

# nameAccuracy3()

# nameAccuracy()
# 
# screenTime()


