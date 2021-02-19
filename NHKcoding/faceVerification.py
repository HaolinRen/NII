
import csv
import os
import json

V_DATA_PATH = '/Users/hren/Workspace/visualCloud/Web/server/data/'

TRUTH_GROUND_PATH = 'data/printNews.csv'


def getAllNews():
    res = {}
    with open('allNews.csv', 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in spamreader:
            title = row[0]
            uniTitle = title.split('.')[0]
            if uniTitle not in res:
                res[uniTitle] = 1
            else:
                print(uniTitle)
                res[uniTitle] += 1
    print(len(res), ' segments total in truth ground.')
    return res


def getExtractions():
    res = {}
    finalRes = []
    isFirstLine = True

    captionsFaces = getCaptionData()

    with open('videoProcessed2.csv', 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';', quotechar='"')
        for row in spamreader:
            if isFirstLine:
                isFirstLine = False
                continue
            segmentID = row[0].split('/')[-1]
            segmentID = segmentID.split('.')[0]

            faceName = row[1].split('.')[0]
            if faceName == 'a':
                continue

            if faceName == 'Yoshihiko Noda':
                faceName = 'Yoshihiko NODA'

            if faceName == 'Akihiro OHTA':
                faceName = 'Akihiro OTA'

            if faceName == 'Toru Hashimoto':
                faceName = 'Toru HASHIMOTO'
            if segmentID not in res:
                res[segmentID] = [faceName]
            else:
                if faceName not in res[segmentID]:
                    res[segmentID].append(faceName)


    testDict = {}

    isFirstLine = True

    lg = 0
    with open('finalRes4.csv', 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';', quotechar='"')
        for row in spamreader:
            segmentTitle = row[0]
            if isFirstLine:
                isFirstLine = False
                a = row
                a.append('P_2')
                a.append('P_c')
                finalRes.append(a)
                continue
            a = row

            if row[6] == '':
                continue
            if row[1] != '0':
                testDict[row[0]] = int(row[2])
            if segmentTitle in res:
                nameList = ' | '.join(res[segmentTitle])
                a.append(nameList)
            else:
                a.append('')

            if segmentTitle in captionsFaces:
                nameList = ' | '.join(captionsFaces[segmentTitle])
                a.append(nameList)
            else:
                a.append('')
            finalRes.append(a)
            lg += 1
    print('lg', lg)
    return finalRes


# getExtractions()
def getTData():
    fullRes = {}
    res = {}
    titleToPerson = {}
    DOC_TITLE_INDEX = 2
    NAME_INDEX = 4
    START_TIME_INDEX = 5
    END_TIME_INDEX = 6
    DURATION_TIME_INDEX = 7
    COMMENT_INDEX = 8
    is_title = True

    rowIndex = 0
    with open(TRUTH_GROUND_PATH, 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in spamreader:
            if is_title:
                is_title = False
                continue
            rowIndex += 1
            full_name = row[NAME_INDEX].upper()
            doc_title = row[DOC_TITLE_INDEX].split('.')[0]
            start_time = row[START_TIME_INDEX]
            end_time = row[END_TIME_INDEX]
            duration = row[DURATION_TIME_INDEX]
            comment = row[COMMENT_INDEX]

            if row[NAME_INDEX] == '' or full_name == 'NOTHING':
                continue

            if doc_title not in titleToPerson:
                titleToPerson[doc_title] = [full_name]
            else:
                if full_name not in titleToPerson[doc_title]:
                    titleToPerson[doc_title].append(full_name)


            # time_temp_index = doc_title + '-' + start_time + '-' + end_time

            if full_name not in res:
                # res[full_name] = {}
                res[full_name] = []
            if doc_title not in res[full_name]:
                res[full_name].append(doc_title)

            # if doc_title not in res[full_name]:
            #     res[full_name][doc_title] = {}
            
            # if time_temp_index not in res[full_name][doc_title]:
            #     res[full_name][doc_title][time_temp_index] = {}

            # res[full_name][doc_title][time_temp_index] = {
            #     'start': start_time,
            #     'end': end_time,
            #     'duration': duration,
            #     'comment': comment
            # }
    return {
        'tp': titleToPerson,
        'pt': res
    }

def getJsonData(file_path):
    with open(V_DATA_PATH + file_path) as json_data:
        d = json.load(json_data)
        json_data.close()
        return d

def getCaptionData():
    ground_truth = getAllNews()

    nameDict = {
        '小泉純一郎': 'Junichiro Koizumi',
        '小泉前総理': 'Junichiro Koizumi',
        '小泉総理大臣': 'Junichiro Koizumi',

        '安倍晋三': 'Shinzo Abe',
        '安倍幹事長': 'Shinzo Abe',
        '安倍総理大臣': 'Shinzo Abe',
        '安倍総裁': 'Shinzo Abe',
        '安倍前総理大臣': 'Shinzo Abe',
        '安倍副長官': 'Shinzo Abe',
        '安倍新総裁': 'Shinzo Abe',

        '福田康夫': 'Yasuo Fukuda',

        '福田官房長官': 'Yasuo Fukuda',
        '福田総理大臣': 'Yasuo Fukuda',
        '福田前官房長官': 'Yasuo Fukuda',

        '福田前総理大臣': 'Yasuo Fukuda',
        '福田長官': 'Yasuo Fukuda',

        '麻生太郎': 'Taro Aso',
        '麻生政務調査会長': 'Taro Aso',
        '麻生総理大臣': 'Taro Aso',
        '麻生総裁': 'Taro Aso',
        '麻生総務大臣': 'Taro Aso',
        '麻生幹事長': 'Taro Aso',
        '麻生幹事長': 'Taro Aso',

        '谷垣禎一': 'Sadakazu Tanigaki',
        '谷垣総裁': 'Sadakazu Tanigaki',


        '鳩山由紀夫': 'Yukio Hatoyama',
        '鳩山総理大臣': 'Yukio Hatoyama',
        '鳩山幹事長': 'Yukio Hatoyama',
        '鳩山元総理大臣': 'Yukio Hatoyama',
        '鳩山大臣': 'Yukio Hatoyama',


        '菅直人': 'Naoto Kan',
        '菅元代表': 'Naoto Kan',
        '菅前総理大臣': 'Naoto Kan',
        '菅副総理': 'Naoto Kan',
        '菅幹事長': 'Naoto Kan',

        '岡田克也': 'Katsuya Okada',
        '岡田外務大臣': 'Katsuya Okada',
        '岡田副総理': 'Katsuya Okada',
        '岡田大臣': 'Katsuya Okada',


        '前原誠司': 'Seiji Maehara',

        '前原前外務大臣': 'Seiji Maehara',
        '前原大臣': 'Seiji Maehara',
        '前原外務大臣': 'Seiji Maehara',
        '前原代表': 'Seiji Maehara',

        '小沢一郎': 'Ichiro Ozawa',
        '小沢大臣': 'Ichiro Ozawa',
        '小沢幹事長': 'Ichiro Ozawa',
        '小沢党首': 'Ichiro Ozawa',


        '野田佳彦': 'Yoshihiko Noda',
        '野田総理大臣': 'Yoshihiko Noda',
        '野田財務大臣': 'Yoshihiko Noda',
        '野田財務副大臣': 'Yoshihiko Noda',
        '野田新総理大臣': 'Yoshihiko Noda',

        '神崎武法': 'Takenori Kanzaki',

        '神崎代表': 'Takenori Kanzaki',

        '太田昭宏': 'Akihiro Ota',
        '太田代表': 'Akihiro Ota',

        '山口那津男': 'Natsuo Yamaguchi',
        '山口代表': 'Natsuo Yamaguchi',

        '志位和夫': 'Kazuo Shii',

        '志位委員長': 'Kazuo Shii',

        '土井たか子': 'Takako Doi',
        '土井党首': 'Takako Doi',

        '福島瑞穂': 'Mizuho Fukushima',

        '福島党首': 'Mizuho Fukushima',
        '福島大臣': 'Mizuho Fukushima',

        '石原慎太郎': 'Shintaro Ishihara',

        '石原大臣': 'Shintaro Ishihara',
        '石原国土交通大臣': 'Shintaro Ishihara',
        '石原代表': 'Shintaro Ishihara',
        '石原幹事長': 'Shintaro Ishihara',
        '石原知事': 'Shintaro Ishihara',

        '橋下徹': 'Toru Hashimoto',
        '橋下代表': 'Toru Hashimoto',
        '橋下市長': 'Toru Hashimoto',

        '渡辺代表': 'Yoshimi Watanabe',
        '渡辺喜美': 'Yoshimi Watanabe',

        '枝野幸男': 'Yukio EDANO',
        '枝野幹事長': 'Yukio EDANO',
        '枝野官房長官': 'Yukio EDANO',
        '枝野経済産業大臣': 'Yukio EDANO',

    }

    for oneName in nameDict:
        egName = nameDict[oneName].split(' ')
        firstName = egName[0]
        sedName = egName[1].upper()

        fullName = firstName + ' ' + sedName
        nameDict[oneName] = fullName

    '''
    '安倍晋三': ['安倍幹事長', '安倍総理大臣', '安倍総裁', '安倍前総理大臣', '安倍副長官', '安倍新総裁']
    '福田康夫': ['福田さん', '福田官房長官', '福田総理大臣', '福田前官房長官', '福田前総理大臣', '福田長官']
    '麻生太郎': ['麻生総理大臣', '麻生政務調査会長', '麻生総裁', '麻生総務大臣', '麻生幹事長', '麻生総理', ]
    '谷垣禎一': ['谷垣総裁']
    '鳩山由紀夫': ['鳩山大臣', '鳩山総理大臣', '鳩山幹事長', '鳩山元総理大臣', '鳩山大臣']
    '菅直人': ['菅総理大臣', '菅元代表', '菅前総理大臣', '菅副総理', '菅幹事長']
    '岡田克也': ['岡田外務大臣', '岡田幹事長', '岡田副総理', '岡田大臣']
    '前原誠司': ['前原前外務大臣', '前原大臣', '前原外務大臣', '前原代表']
    '小沢一郎': ['小沢大臣','小沢幹事長', '小沢党首']
    '野田佳彦': ['野田総理大臣', '野田財務大臣', '野田財務副大臣', '野田新総理大臣']
    '神崎武法': ['神崎代表']
    '太田昭宏': ['太田代表', '太田知事']
    '山口那津男': ['山口代表']
    '志位和夫': ['志位委員長']
    '土井たか子': ['土井党首']
    '福島瑞穂': ['福島党首', '福島大臣']
    '石原慎太郎': ['石原大臣', '石原国土交通大臣', '石原代表', '石原幹事長', '石原知事']
    '橋下徹': ['橋下代表', '橋下市長']
    '渡辺喜美': ['渡辺代表']
    
    '''

    jpNames = nameDict.keys()

    cpd = getJsonData('date_to_topics_to_captions.json')
    k = 0

    segFaceDict = {}
    for oneSeg in cpd:
        for onesub in cpd[oneSeg]:
            if onesub == '1' or onesub == '2' or onesub == '3':
                tempName = oneSeg + '_' + onesub
                if tempName in ground_truth:
                    captions = cpd[oneSeg][onesub]
                    for oneCap in captions:
                        for oneName in jpNames:
                            if oneName in oneCap:
                                if tempName not in segFaceDict:
                                    segFaceDict[tempName] = [nameDict[oneName]]
                                else:
                                    if nameDict[oneName] not in segFaceDict[tempName]:
                                        segFaceDict[tempName].append(nameDict[oneName])
                                k += 1
                    k += 1

    print(len(ground_truth))
    print(len(segFaceDict))

    testDict = {}
    for oneSeg in segFaceDict:
        testDict[oneSeg] = len(segFaceDict[oneSeg])
    return segFaceDict


# getTData()

def getPersonTime():
    nameDict = {'HATOYAMA': 'Yukio HATOYAMA', 'KOIZUMI': 'Junichiro KOIZUMI', 'KANZAKI': 'Takenori KANZAKI', 'ASO': 'Taro ASO', 'FUKUDA': 'Yasuo FUKUDA', 'FUKUSHIMA': 'Mizuho FUKUSHIMA', 'OKADA': 'Katsuya OKADA', 'OTA': 'Akihiro OHTA', 'KAN': 'Naoto KAN', 'ABE': 'Shinzo ABE', 'DOI': 'Takako DOI', 'KAMEI': 'Shizuka KAMEI', 'SHII': 'Kazuo SHII', 'OZAWA': 'Ichiro OZAWA', 'EDANO': 'Yukio EDANO', 'TANIGAKI': 'Sadakazu TANIGAKI', 'NODA': 'Yoshihiko NODA', 'YAMAGUCHI': 'Natsuo YAMAGUCHI', 'MAEHARA': 'Seiji MAEHARA', 'WATANABE': 'Yoshimi WATANABE', 'ISHIHARA': 'Shintaro ISHIHARA', 'HASHIMOTO': 'Toru HASHIMOTO'}
    is_title = True
    DOC_TITLE_INDEX = 2
    NAME_INDEX = 4
    START_TIME_INDEX = 5
    END_TIME_INDEX = 6
    DURATION_TIME_INDEX = 7
    COMMENT_INDEX = 8
    
    res = {}

    with open(TRUTH_GROUND_PATH, 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in spamreader:
            if is_title:
                is_title = False
                continue

            full_name = row[NAME_INDEX].upper()
            doc_title = row[DOC_TITLE_INDEX][:7]
            duration = row[DURATION_TIME_INDEX]
            print(doc_title)


            if full_name != '' and full_name != 'NOTHING':
                name = nameDict[full_name]
                if name not in res:
                    res[name] = {}


                t = duration.split(':')
                hour = int(t[0])
                minutes = int(t[1])
                sec = int(t[2])

                if doc_title not in res[name]:
                    res[name][doc_title] = 0

                res[name][doc_title] += minutes * 60 + sec
            
    return res

# getCaptionData()

# getPersonTime()

def writeJsonData(fileName, data):
    with open(fileName, 'w') as outfile:
        json.dump(data, outfile)

def writeCsv(fileName, data):
    with open(fileName, mode='w') as csvfile:
        csvfile_writer = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in data:
            csvfile_writer.writerow(row)


def compareTwoData(td, tl):
    topics = td.keys()

def checkPersonDoc(td, pt):
    temp = {
        'KOIZUMI': 'Junichiro KOIZUMI',
        'OKADA': 'Takeshi OKADA',
        'ABE': 'Shinzo ABE',
        'FUKUDA': 'Yasuo FUKUDA'
    }
    testDict = {}
    # print(td, pt)
    res = [['name_in_truth', 'sgements_number', 'name in visualCloud', 'sgements_number', 'same_sgement_number']]
    for oneName in td:
        if oneName in temp:
            tempName = temp[oneName]
        else:
            tempName = ''
        tempRes = []
        personTopicList = td[oneName].keys()
        
        index = 0
        for fullName in pt:
            nameList = fullName.split(' ')

            firstName = nameList[0].upper()
            if len(nameList) > 1:
                lastName = nameList[1].upper()

            if lastName in temp:
                lastName = temp[lastName]

            if oneName == firstName or oneName == lastName or tempName == fullName:        
                tempRes.append(oneName)
                tempRes.append(len(personTopicList))
                tempRes.append(fullName)
                tempRes.append(len(pt[fullName]))
                testDict[fullName] = td[oneName]
                for oneTopic in pt[fullName]:
                    uniNameList = oneTopic.split('-Topic')
                    doctNum = int(uniNameList[1])
                    if doctNum < 4:
                        uniName = uniNameList[0] + '_' + uniNameList[1]

                        if uniName in personTopicList:
                            index += 1

        tempRes.append(index)
        if len(tempRes) == 5:
            res.append(tempRes)
    # writeCsv('compareRes.csv',res)

    # writeJsonData('truthdict2.json',testDict)


def getMyMethodScreenTime():

    isFirstLine = True
    myMethodDict = {}
    lastTime = 0


    with open('videoProcessed2.csv', 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';', quotechar='"')
        for row in spamreader:
            if isFirstLine:
                isFirstLine = False
                continue
            segmentID = row[0].split('/')[-1].split('.')[0]

            faceName = row[1].split('.')[0]

            if faceName == 'Yoshihiko Noda':
                faceName = 'Yoshihiko NODA'

            if faceName == 'Akihiro OHTA':
                faceName = 'Akihiro OTA'

            if faceName == 'Toru Hashimoto':
                faceName = 'Toru HASHIMOTO'


            if faceName not in myMethodDict:
                myMethodDict[faceName] = {}
            tempPair = [int(row[5]), int(row[6])]
            if segmentID not in myMethodDict[faceName]:
                myMethodDict[faceName][segmentID] = [tempPair]
            else:
                k = 0
                isFound = False
                for onePair in myMethodDict[faceName][segmentID]:
                    if myMethodDict[faceName][segmentID][k][1] >= tempPair[0]-1:
                        myMethodDict[faceName][segmentID][k] = [myMethodDict[faceName][segmentID][k][0], tempPair[1]]
                        isFound = True
                    k += 1
                if not isFound:
                    myMethodDict[faceName][segmentID].append(tempPair)
    return myMethodDict

def getGroundScreenTime():
    is_title = True
    DOC_TITLE_INDEX = 2
    NAME_INDEX = 4
    START_TIME_INDEX = 5
    END_TIME_INDEX = 6
    DURATION_TIME_INDEX = 7
    COMMENT_INDEX = 8

    nameDict = {'HATOYAMA': 'Yukio HATOYAMA', 'KOIZUMI': 'Junichiro KOIZUMI', 'KANZAKI': 'Takenori KANZAKI', 'ASO': 'Taro ASO', 'FUKUDA': 'Yasuo FUKUDA', 'FUKUSHIMA': 'Mizuho FUKUSHIMA', 'OKADA': 'Katsuya OKADA', 'OTA': 'Akihiro OTA', 'KAN': 'Naoto KAN', 'ABE': 'Shinzo ABE', 'DOI': 'Takako DOI', 'KAMEI': 'Shizuka KAMEI', 'SHII': 'Kazuo SHII', 'OZAWA': 'Ichiro OZAWA', 'EDANO': 'Yukio EDANO', 'TANIGAKI': 'Sadakazu TANIGAKI', 'NODA': 'Yoshihiko NODA', 'YAMAGUCHI': 'Natsuo YAMAGUCHI', 'MAEHARA': 'Seiji MAEHARA', 'WATANABE': 'Yoshimi WATANABE', 'ISHIHARA': 'Shintaro ISHIHARA', 'HASHIMOTO': 'Toru HASHIMOTO'}

    gtDict = {}
    testDict = {}
    k = 0
    with open(TRUTH_GROUND_PATH, 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in spamreader:
            if is_title:
                is_title = False
                continue

            full_name = row[NAME_INDEX].upper()
            doc_title = row[DOC_TITLE_INDEX][:18]
            duration = row[DURATION_TIME_INDEX]
            
            if row[5] == row[6]:
                continue

            if full_name != '' and full_name != 'NOTHING':
                name = nameDict[full_name]
                if name not in gtDict:
                    gtDict[name] = {}

                if doc_title not in gtDict[name]:
                    gtDict[name][doc_title] = []

                startTime = row[START_TIME_INDEX].split(':')
                endTime = row[END_TIME_INDEX].split(':')


                startMinute = int(startTime[1]) * 60
                startSecond = int(startTime[2]) + startMinute

                endMinute = int(endTime[1]) * 60
                endSecond = int(endTime[2]) + endMinute

                isExist = False
                k = 0
                for onePair in gtDict[name][doc_title]:
                    if onePair[0] >= startSecond and onePair[1] <= endSecond:
                        gtDict[name][doc_title][k] = [startSecond, endSecond]
                        isExist = True
                        continue
                    if onePair[0] <= startSecond and onePair[1] < endSecond and onePair[1] >= startSecond:
                        gtDict[name][doc_title][k] = [onePair[0], endSecond]
                        isExist = True
                        continue
                    # '2002_01_29_19_00_2': [[369, 392], [370, 393], [509, 523], [595, 596], [636, 646]],
                    if onePair[0] <= startSecond and onePair[1] >= endSecond:
                        isExist = True
                        break
                    k += 1
                if not isExist:
                    gtDict[name][doc_title].append([startSecond, endSecond])   
    return gtDict

def MyMethodScreenTime():

    is_title = True
    DOC_TITLE_INDEX = 2
    NAME_INDEX = 4
    START_TIME_INDEX = 5
    END_TIME_INDEX = 6
    DURATION_TIME_INDEX = 7
    COMMENT_INDEX = 8

    nameDict = {'HATOYAMA': 'Yukio HATOYAMA', 'KOIZUMI': 'Junichiro KOIZUMI', 'KANZAKI': 'Takenori KANZAKI', 'ASO': 'Taro ASO', 'FUKUDA': 'Yasuo FUKUDA', 'FUKUSHIMA': 'Mizuho FUKUSHIMA', 'OKADA': 'Katsuya OKADA', 'OTA': 'Akihiro OTA', 'KAN': 'Naoto KAN', 'ABE': 'Shinzo ABE', 'DOI': 'Takako DOI', 'KAMEI': 'Shizuka KAMEI', 'SHII': 'Kazuo SHII', 'OZAWA': 'Ichiro OZAWA', 'EDANO': 'Yukio EDANO', 'TANIGAKI': 'Sadakazu TANIGAKI', 'NODA': 'Yoshihiko NODA', 'YAMAGUCHI': 'Natsuo YAMAGUCHI', 'MAEHARA': 'Seiji MAEHARA', 'WATANABE': 'Yoshimi WATANABE', 'ISHIHARA': 'Shintaro ISHIHARA', 'HASHIMOTO': 'Toru HASHIMOTO'}

    gtDict = {}
    testDict = {}
    k = 0
    with open(TRUTH_GROUND_PATH, 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in spamreader:
            if is_title:
                is_title = False
                continue

            full_name = row[NAME_INDEX].upper()
            doc_title = row[DOC_TITLE_INDEX][:18]
            duration = row[DURATION_TIME_INDEX]
            
            if row[5] == row[6]:
                continue

            if full_name != '' and full_name != 'NOTHING':
                name = nameDict[full_name]
                if name not in gtDict:
                    gtDict[name] = {}

                if doc_title not in gtDict[name]:
                    gtDict[name][doc_title] = []

                startTime = row[START_TIME_INDEX].split(':')
                endTime = row[END_TIME_INDEX].split(':')


                startMinute = int(startTime[1]) * 60
                startSecond = int(startTime[2]) + startMinute

                endMinute = int(endTime[1]) * 60
                endSecond = int(endTime[2]) + endMinute

                isExist = False
                k = 0
                for onePair in gtDict[name][doc_title]:
                    if onePair[0] >= startSecond and onePair[1] <= endSecond:
                        gtDict[name][doc_title][k] = [startSecond, endSecond]
                        isExist = True
                        continue
                    if onePair[0] <= startSecond and onePair[1] < endSecond and onePair[1] >= startSecond:
                        gtDict[name][doc_title][k] = [onePair[0], endSecond]
                        isExist = True
                        continue
                    # '2002_01_29_19_00_2': [[369, 392], [370, 393], [509, 523], [595, 596], [636, 646]],
                    if onePair[0] <= startSecond and onePair[1] >= endSecond:
                        isExist = True
                        break
                    k += 1
                if not isExist:
                    gtDict[name][doc_title].append([startSecond, endSecond])
                    


    isFirstLine = True
    myMethodDict = {}
    lastTime = 0


    with open('videoProcessed2.csv', 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';', quotechar='"')
        for row in spamreader:
            if isFirstLine:
                isFirstLine = False
                continue
            segmentID = row[0].split('/')[-1].split('.')[0]

            faceName = row[1].split('.')[0]

            if faceName == 'Yoshihiko Noda':
                faceName = 'Yoshihiko NODA'

            if faceName == 'Akihiro OHTA':
                faceName = 'Akihiro OTA'

            if faceName == 'Toru Hashimoto':
                faceName = 'Toru HASHIMOTO'


            if faceName not in myMethodDict:
                myMethodDict[faceName] = {}
            tempPair = [int(row[5]), int(row[6])]
            if segmentID not in myMethodDict[faceName]:
                myMethodDict[faceName][segmentID] = [tempPair]
            else:
                k = 0
                isFound = False
                for onePair in myMethodDict[faceName][segmentID]:
                    if myMethodDict[faceName][segmentID][k][1] >= tempPair[0]-1:
                        myMethodDict[faceName][segmentID][k] = [myMethodDict[faceName][segmentID][k][0], tempPair[1]]
                        isFound = True
                    k += 1
                if not isFound:
                    myMethodDict[faceName][segmentID].append(tempPair)

    sameVal = 0
    missingVal = 0
    wrongVal = 0

    monthSameVal = 0
    monthMissVal = 0
    monthWrongVal = 0

    totalTime = 0
    res = {}
    for oneName in gtDict:
        gtList = gtDict[oneName]
        res[oneName] = {}
        if oneName in myMethodDict:
            myList = myMethodDict[oneName]

            for oneSeg in myList:
                month = oneSeg[:7]
                if month not in res[oneName]:
                    res[oneName][month] = {
                        'miss': 0,
                        'same': 0,
                        'wrong': 0
                    }
                if oneSeg in gtList:
                    for onePair in myList[oneSeg]:
                        isFound = False
                        for pair2 in gtList[oneSeg]:
                            if onePair[0] > pair2[1] or onePair[1] < pair2[0]:
                                continue
                            else:

                                isFound = True
                                if onePair[0] <= pair2[0]:

                                    if onePair[0] < pair2[0]:
                                        res[oneName][month]['wrong'] += onePair[1] - onePair[0]
                                        wrongVal += pair2[0] - onePair[0]
                                    if pair2[1] >= onePair[1]:
                                        onePair = [0, -1]
                                        break
                                    else:
                                        onePair = [pair2[1]+1, onePair[1]]
                                else:
                                    if onePair[1] > pair2[1]:
                                        onePair = [pair2[1]+1, onePair[1]]
                                    else:
                                        onePair = [0, -1]
                                        break

                        if isFound:
                            if onePair[1] >= onePair[0]:
                                res[oneName][month]['wrong'] += onePair[1] - onePair[0] + 1
                                wrongVal += onePair[1] - onePair[0] + 1

                        if not isFound:
                            wrongVal += onePair[1] - onePair[0] + 1
                            res[oneName][month]['wrong'] += onePair[1] - onePair[0] + 1
                else:
                    for onePair in myList[oneSeg]:
                        wrongVal += onePair[1] - onePair[0] + 1
                        res[oneName][month]['wrong'] += onePair[1] - onePair[0] + 1


            for oneSeg in gtList:
                month = oneSeg[:7]
                if month not in res[oneName]:
                    res[oneName][month] = {
                        'miss': 0,
                        'same': 0,
                        'wrong': 0
                    }
                if oneSeg in myList:
                    for onePair in gtList[oneSeg]:
                        isFound = False
                        totalTime += onePair[1] - onePair[0] + 1
                        for pair2 in myList[oneSeg]:
                            if onePair[0] > pair2[1] or onePair[1] < pair2[0]:
                                continue
                            else:
                                isFound = True
                                if onePair[0] <= pair2[0]:

                                    if onePair[0] < pair2[0]:
                                        res[oneName][month]['miss'] += onePair[1] - onePair[0]
                                        missingVal += pair2[0] - onePair[0]
                                    if pair2[1] >= onePair[1]:
                                        sameVal += onePair[1] - pair2[0] + 1
                                        res[oneName][month]['same'] += onePair[1] - onePair[0] + 1
                                        onePair = [0, -1]
                                        break
                                    else:
                                        sameVal += pair2[1] - pair2[0] + 1
                                        res[oneName][month]['same'] += onePair[1] - onePair[0] + 1
                                        onePair = [pair2[1]+1, onePair[1]]
                                else:
                                    if onePair[1] > pair2[1]:
                                        onePair = [pair2[1]+1, onePair[1]]
                                        sameVal += pair2[1] - onePair[0] + 1
                                    else:
                                        sameVal += onePair[1] - onePair[0] + 1
                                        res[oneName][month]['same'] += onePair[1] - onePair[0] + 1
                                        onePair = [0, -1]
                                        break

                        if isFound:
                            if onePair[1] >= onePair[0]:
                                res[oneName][month]['miss'] += onePair[1] - onePair[0] + 1
                                missingVal += onePair[1] - onePair[0] + 1

                        if not isFound:
                            res[oneName][month]['miss'] += onePair[1] - onePair[0] + 1
                            missingVal += onePair[1] - onePair[0] + 1
                else:
                    for onePair in gtList[oneSeg]:
                        missingVal += onePair[1] - onePair[0] + 1
                        totalTime += onePair[1] - onePair[0] + 1
                        res[oneName][month]['miss'] += onePair[1] - onePair[0] + 1




    print(missingVal)
    print(sameVal)
    print(wrongVal)
    print(totalTime)
    return res


# print(truth_data)

# MyMethodScreenTime()
# print(len(truth_data['pt']))
# personTopic = getJsonData('personToTopicListAll.json')
# 2010_04_28_19_00_1
def getVCTopics():
    ad = getJsonData('date_to_topics.json')
    k = 0

    sumVal = 0

    tempDict = {}

    for i in ad:

        for k in ad[i]:
            title = i + '_' + k
            tempDict[title] = 1

    return tempDict

def checkSameSegmentsPersonNum(ad, td):
    personDict = {}
    count = 0
    k = 0
    missPersonDict = {}
    temp = {
        'KOIZUMI': 'Junichiro KOIZUMI',
        'OKADA': 'Takeshi OKADA',
        'ABE': 'Shinzo ABE',
        'FUKUDA': 'Yasuo FUKUDA',
        'NODA': 'Yoshihiko NODA'
    }
    res = [['Segment_Name', 'num_P_v', 'num_P_t', 'face_in_P_v_and_P_t', 'face_in_P_t_not_in_P_v','face_in_P_v_not_in_P_t','P_t','P_v']]

    perfectNum = 0

    outIndex = 0
    wrongIndex = 0

    for oneTitle in td['tp']:
        if oneTitle in ad:
            pl = ad[oneTitle]
            k += 1
            sameNum = 0
            outNum = 0
            wrongNum = 0

            text0 = '|'.join(td['tp'][oneTitle])
            text1 = '|'.join(ad[oneTitle])
            for oneName in td['tp'][oneTitle]:
                if oneName in temp:
                    oneName = temp[oneName]
                for name2 in pl:
                    if oneName in name2:
                        sameNum += 1
                        break
                if sameNum == 0:
                    outNum += 1

            for oneName in ad[oneTitle]:
                isFound = False
                for name2 in td['tp'][oneTitle]:
                    if name2 in oneName:
                        isFound = True
                if not isFound:
                    wrongNum += 1

            if sameNum != 0 and outNum == 0 and wrongNum == 0:
                perfectNum += 1
            if outNum != 0:
                outIndex += 1
            if wrongNum != 0:
                wrongIndex += 1

            res.append([oneTitle,len(ad[oneTitle]), len(td['tp'][oneTitle]), sameNum, outNum, wrongNum, text0, text1])
            for one in pl:
                if one not in personDict:
                    personDict[one] = 0
        else:
            count += 1
            for onePerson in td['tp'][oneTitle]:
                missPersonDict[onePerson] = 0
    writeCsv('results.csv', res)
    print(perfectNum, outIndex, wrongIndex)
    # print(count)
    # print('k', k)
    # print('miss ', len(missPersonDict))
    # print(len(personDict))

# checkSameSegmentsPersonNum(allt2p, truth_data)

# print(len(allt2p))
# checkPersonDoc(truth_data, personTopic)

# topicPersonDict = getJsonData('topic_to_persons.json')


# checkTopicDoc(truth_data, topicPersonDict)

def getVideoData():

    pwd = os.getcwd()
    faceNameList = os.listdir('/Volumes/RHL_ED_MAC/NII/excerpts')
    return faceNameList

def testFileNumber():
    diskFiles = getVideoData()
    allFlist =[]
    with open('allNews.csv', 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in spamreader:
            allFlist.append(row[0])
    for i in diskFiles:
        if i not in allFlist:
            print(i)
    for j in allFlist:
        if j not in diskFiles:
            print(j)

def run2():
    allsegTruth = getAllNews()
    truth_data = getTData()

    topicChecker = {}
    facesT = truth_data['pt'].keys()
    print(len(truth_data['tp']), ' titles have person')
    print(len(facesT), ' persons invovling in news')
    
    
    title2P = getJsonData('topic_to_persons.json')

    personTopic = getJsonData('personToTopicListAll.json')
    print(len(personTopic), ' V persons total')


    k = 0
    s = 0

    facesV = personTopic.keys()


    Dict = {
        'KOIZUMI': 'Junichiro KOIZUMI',
        'OKADA': 'Katsuya OKADA',
        'ABE': 'Shinzo ABE',
        'FUKUDA': 'Yasuo FUKUDA',
        'NODA': 'Yoshihiko Noda',
        'ASO': 'Taro ASO',
        'OTA': 'Akihiro OTA',
        'HASHIMOTO': 'Toru HASHIMOTO'
    }

    faceDict = {}
    revFaceDict = {}

    for oneFace in facesT:
        if oneFace in Dict:
            tempFace = Dict[oneFace]
        else:
            tempFace = oneFace
        for oneFaceV in facesV:
            if tempFace in oneFaceV:
                faceDict[oneFaceV] = oneFace
                revFaceDict[oneFace] = oneFaceV


    revFaceDict['HASHIMOTO'] = 'Toru HASHIMOTO'
    
    del faceDict['Azuma KOSHIISHI']

    print(revFaceDict)

    res = [['Segment_Name','num_P_v','num_P_t','face_in_P_v_and_P_t','face_in_P_t_not_in_P_v','face_in_P_v_not_in_P_t','P_t','P_v']]
    # res = []
    sameseg = 0


    sumVal = 0

    vsVal = 0

    true_positive = 0

    false_negative = 0

    false_positive = 0

    hasPeople = 0
    noFaceNum = 0

    missFaceNum = 0

    vcWrong = 0

    sumPopulation = 0

    for oneTitle in allsegTruth:
        tempTitle = oneTitle[:-2] + '-Topic' + oneTitle[-1]
        npv = 0

        fpvt = 0
        fpt = 0
        fpv = 0

        lt = 0
        lv = 0

        arrt = ''
        arrv = ''

        tempArr = []

        if oneTitle in truth_data['tp']:
            tempArr = truth_data['tp'][oneTitle]
        
        if tempTitle in title2P:
            sameseg += 1
            k += 1
            pv = []
            pt = []
            for oneName in title2P[tempTitle]:
                if oneName == 'Ryutaro HASHIMOTO':
                    continue
                
                if oneName in faceDict:
                    # if oneName == 'Akihiro OTHA':
                    #     oneName = 'Akihiro OTA'
                    pv.append(oneName)

            for oneName in tempArr:
                if oneName in revFaceDict:
                    oneName = revFaceDict[oneName]
                    # if oneName == 'Akihiro OTHA':
                    #     oneName = 'Akihiro OTA'
                    pt.append(oneName)

            for i in pt:
                sumVal += 1
                if i in pv:
                    fpvt += 1
                    true_positive += 1
                else:
                    fpt += 1
                    false_positive += 1

            for j in pv:
                vsVal += 1
                if not j in pt:
                    fpv += 1
                    false_negative += 1

            lt = len(pt)
            lv = len(pv)

            if lt > 0 or lv > 0:
                sumPopulation += 1

            if lt == 0 and lv > 0:
                vcWrong += 1

            arrt = ' | '.join(pt)
            arrv = ' | '.join(pv)
        else:
            lt = len(tempArr)
            fpt = lt
            pt = []
            
            for oneName in tempArr:
                if oneName in revFaceDict:
                    oneName = revFaceDict[oneName]
                    # if oneName == 'Akihiro OTHA':
                    #     oneName = 'Akihiro OTA'
                    pt.append(oneName)
                    false_negative += 1
                    sumVal += 1
            
            if lt > 0:
                missFaceNum += 1
                sumPopulation += 1
            else:
                if lt == 0:
                    noFaceNum += 1
            arrt = ' | '.join(pt)

        arrt = arrt.replace('Noda', 'NODA')
        arrv = arrv.replace('Noda', 'NODA')
        arrt = arrt.replace('Akihiro OHTA', 'Akihiro OTA')
        arrv = arrv.replace('Akihiro OHTA', 'Akihiro OTA')
        res.append([oneTitle, lv, lt, fpvt, fpt, fpv, arrt, arrv])

    print('false_negative', false_negative)
    print('true_positive', true_positive)
    print('false_positive', false_positive)
    print('sumVal', sumVal)
    print('vsumval', vsVal)
    print('noFaceNum', noFaceNum)
    print('miss face num', missFaceNum)
    print('same segments visualCloud and ground', sameseg)
    print('vc hasd data, t no data', vcWrong)
    writeCsv('finalRes4.csv', res)

    return
    exsame = 0
    # ['Segment_Name', 'num_P_v', 'num_P_t', 'face_in_P_v_and_P_t', 'face_in_P_t_not_in_P_v', 'face_in_P_v_not_in_P_t', 'P_t', 'P_v']

    missingVal = 0
    wrongVal = 0
    sameVal = 0

    faceDict = {}
    faceDictIn = {}
    faceDictMissing = {}
    faceDictWrong = {}

    faceTimes = 0

    tft = 0

    samedect = 0
    print(len(res), '_______ size')
    for oneRes in res:
        if oneRes[2] == 0 and oneRes[1] > 1:
            samedect += 1

        ft = oneRes[6].split(' | ')
        fv = oneRes[7].split(' | ')
        for i in ft:
            if i == '':
                continue
            tft += 1

            if i not in faceDict:
                faceDict[i] = {
                    'tt': 1,
                    'tv': 0,
                    'right': 0,
                    'wrong': 0,
                    'missing': 0
                }
            else:
                faceDict[i]['tt'] += 1

            if i in fv:
                if i not in faceDictIn:
                    faceDictIn[i] = 1
                else:
                    faceDictIn[i] += 1
            else:
                faceDict[i]['missing'] += 1
                missingVal += 1
                if i not in faceDictMissing:
                    faceDictMissing[i] = 1
                else:
                    faceDictMissing[i] += 1

        for j in fv:
            if j == '':
                continue

            if j not in faceDict:
                faceDict[j] = {
                    'tt': 0,
                    'tv': 1,
                    'right': 0,
                    'wrong': 0,
                    'missing': 0
                }
            else:
                faceDict[j]['tv'] += 1

            faceTimes += 1
            if j not in ft:
                wrongVal += 1
                faceDict[j]['wrong'] += 1
                if j not in faceDictWrong:
                    faceDictWrong[j] = 1
                else:
                    faceDictWrong[j] += 1
            else:
                sameVal += 1
                faceDict[j]['right'] += 1

    print('same detect', samedect)

    # writeCsv('finalRes3.csv', res)

    # print(faceDict)
    totalSize = 1865

    personList = [['Name', 'Detections in ground truth', 'Detections in VC', 'Right Detection (True Positive)', 'Wrong Detection (False Positive)', 'Missing Detection (False Negative)', 'No Detection (True Negative)', 'Total sgements', 'Prevalence', 'Accuracy', 'True Positive Rate']]
    for onePerson in faceDict:
        # personList.append([onePerson, faceDict[onePerson]['tt'], faceDict[onePerson]['tv'], faceDict[onePerson]['right'], faceDict[onePerson]['wrong'], faceDict[onePerson]['missing']])
        tt = faceDict[onePerson]['tt']
        tv = faceDict[onePerson]['tv']
        tRight = faceDict[onePerson]['right']
        # if tv > 0:
        #     ptr = str(tRight) + ' (' + str(round(float(tRight)/totalSize*100, 2)) + '%)' 
        # else:
        #     ptr = str(tRight) + ' (0%)'

        tWrong = faceDict[onePerson]['wrong']

        # if tWrong > 0:
        #     ptw = str(tWrong) + ' (' + str(round(float(tWrong)/totalSize*100, 2)) + '%)' 
        # else:
        #     ptw = str(tWrong) + ' (0%)'

        tMiss = faceDict[onePerson]['missing']

        # if tMiss > 0:
        #     ptm = str(tMiss) + ' (' + str(round(float(tMiss)/totalSize*100, 2)) + '%)' 
        # else:
        #     ptm = str(tMiss) + ' (0%)'

        trueNegative = totalSize - tWrong - tMiss - tRight;

        # tn = str(trueNegative) + ' (' + str(round(float(trueNegative)/totalSize*100, 2)) + '%)'
        a0 = float(tRight + tMiss)

        prevalence = str(round(a0 /totalSize, 2)*100) + '%'; 

        a1 = float(tRight + trueNegative)

        accuracy = str(round(a1 /totalSize, 2)*100) + '%' 

        tpr = str(round(float(tRight)/(tRight+tMiss), 2)*100) + '%' 

        personList.append([onePerson, tt, tv, tRight, tWrong, tMiss, trueNegative, totalSize, prevalence, accuracy, tpr])

    writeCsv('personFaceList3.csv', personList)
    print('truth face times', tft)
    print('same face time', sameVal)
    print('face total time', faceTimes)
    print('missing face time', missingVal)
    print('wrong face times', wrongVal)



    # print('false_negative-seg', pvv)
    # print('exact same', exsame)
    # print('true false_negative-seg', fvv)
    # print('seg have faces', elval)


def run3(targetIndex):
    testDict = {}
    VCNAME_INDEX = 7
    TWO_INDEX = 8
    CPATION_INDEX = 9
    GT_INDEX = 6

    total = 0

    sameVal = 0
    wrongVal = 0
    missingVal = 0

    with open('finalRes7.csv', 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';', quotechar='"')
        for row in spamreader:

            if row[GT_INDEX] != '':

                gtList = row[GT_INDEX].split(' | ')
                vList = row[targetIndex].split(' | ')

                for name in gtList:

                    total += 1
                    if name in vList:
                        sameVal += 1
                    else:
                        missingVal += 1

                for name in vList:
                    if name not in gtList:
                        wrongVal += 1
    print('total: ', total, ' same: ', sameVal, ' missing: ', missingVal, ' wrong: ', wrongVal)

    '''
    my method: total:  885  same:  596  missing:  289  wrong:  123

    visual cloud: total:  885  same:  216  missing:  669  wrong:  203
    
    total:  885  same:  256  missing:  629  wrong:  204


    print(testDict)
    '''


# run3(9)
# run2()
# testFileNumber()

# getAllNews()
def testSameSegments():
    td = getAllNews()
    tv = getVCTopics()

    print(len(td), ' ground truth size ')
    print(len(tv), ' visual cloud size')
    sameVal = 0
    for i in td:
        if i in tv:
            sameVal += 1
    print('sameval ', sameVal)

# testSameSegments()

# finalRes = getExtractions()
# writeCsv('results8.csv', finalRes)


def finalCompare():
    finalRes = getExtractions()

    exsame = 0

    missingVal = 0
    wrongVal = 0
    sameVal = 0

    faceDict = {}
    faceDictIn = {}
    faceDictMissing = {}
    faceDictWrong = {}

    faceTimes = 0

    tft = 0

    samedect = 0

    for oneRes in finalRes:
        ft = oneRes[6].split(' | ')
        fv = oneRes[8].split(' | ')
        for i in ft:
            if i == '':
                continue
            tft += 1

            if i not in faceDict:
                faceDict[i] = {
                    'tt': 1,
                    'tv': 0,
                    'right': 0,
                    'wrong': 0,
                    'missing': 0
                }
            else:
                faceDict[i]['tt'] += 1

            if i in fv:
                if i not in faceDictIn:
                    faceDictIn[i] = 1
                else:
                    faceDictIn[i] += 1
            else:
                faceDict[i]['missing'] += 1
                missingVal += 1
                if i not in faceDictMissing:
                    faceDictMissing[i] = 1
                else:
                    faceDictMissing[i] += 1

        for j in fv:
            if j == '':
                continue

            if j not in faceDict:
                faceDict[j] = {
                    'tt': 0,
                    'tv': 1,
                    'right': 0,
                    'wrong': 0,
                    'missing': 0
                }
            else:
                faceDict[j]['tv'] += 1

            faceTimes += 1
            if j not in ft:
                wrongVal += 1
                faceDict[j]['wrong'] += 1
                if j not in faceDictWrong:
                    faceDictWrong[j] = 1
                else:
                    faceDictWrong[j] += 1
            else:
                sameVal += 1
                faceDict[j]['right'] += 1

    print('same detect', samedect)

    writeCsv('finalRes7.csv', finalRes)

    # print(faceDict)
    totalSize = 1865

    for onePerson in faceDict:
        # personList.append([onePerson, faceDict[onePerson]['tt'], faceDict[onePerson]['tv'], faceDict[onePerson]['right'], faceDict[onePerson]['wrong'], faceDict[onePerson]['missing']])
        tt = faceDict[onePerson]['tt']
        tv = faceDict[onePerson]['tv']
        tRight = faceDict[onePerson]['right']
        # if tv > 0:
        #     ptr = str(tRight) + ' (' + str(round(float(tRight)/totalSize*100, 2)) + '%)' 
        # else:
        #     ptr = str(tRight) + ' (0%)'

        tWrong = faceDict[onePerson]['wrong']

        # if tWrong > 0:
        #     ptw = str(tWrong) + ' (' + str(round(float(tWrong)/totalSize*100, 2)) + '%)' 
        # else:
        #     ptw = str(tWrong) + ' (0%)'

        tMiss = faceDict[onePerson]['missing']

        # if tMiss > 0:
        #     ptm = str(tMiss) + ' (' + str(round(float(tMiss)/totalSize*100, 2)) + '%)' 
        # else:
        #     ptm = str(tMiss) + ' (0%)'

        trueNegative = totalSize - tWrong - tMiss - tRight;

        # tn = str(trueNegative) + ' (' + str(round(float(trueNegative)/totalSize*100, 2)) + '%)'
        a0 = float(tRight + tMiss)

        prevalence = str(round(a0 /totalSize, 2)*100) + '%'; 

        a1 = float(tRight + trueNegative)

        accuracy = str(round(a1 /totalSize, 2)*100) + '%' 

        # tpr = str(round(float(tRight)/(tRight+tMiss), 2)*100) + '%' 


    print('truth face times', tft)
    print('same face time', sameVal)
    print('face total time', faceTimes)
    print('missing face time', missingVal)
    print('wrong face times', wrongVal)

# finalCompare()




# truth face times 823
# same face time 529
# face total time 672
# missing face time 294
# wrong face times 143
