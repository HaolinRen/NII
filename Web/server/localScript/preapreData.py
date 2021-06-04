import sys
import json
from os import listdir


def getJsonData(path):
  with open(path, 'rb') as loadFile:
    data = json.load(loadFile)
    return data

def saveJsonData(path, data):
  with open(path, 'w') as outFile:
    json.dump(data, outFile)

def savePersonList():
  res = {}
  personList = getJsonData('../data/topic_bcp.json')
  for oneTopic in personList:
    personNameArr = personList[oneTopic]
    for personName in personNameArr:
      if personName not in res:
        res[personName] = [oneTopic]
      else:
        res[personName].append(oneTopic)

  saveJsonData('../data/personToTopicListAll.json', res)

def findPersonFace():
  # personList = getJsonData('../data/haolinProcessed/personToTopicListAll.json')
  faceNameList = listdir('../../client/data/faces')
  nameDict = {}
  for oneFace in faceNameList:
    faceName = oneFace.replace('.jpg', '')
    if faceName not in nameDict:
      nameDict[faceName] = oneFace
  saveJsonData('../data/faceNameDict.json', nameDict)

def buildFakeEmiArr():
  res = []
  nameDict = getJsonData('../data/faceNameDict.json')
  personList = getJsonData('../data/topic_to_persons_kw-all.json')
  # count = 0

  def getDate(strDate):
    return strDate[0:4] + strDate[5:7] + strDate[8:10]

  for i in personList:
    mm = ''
    emiDate = getDate(i)
    
    for oneKey in personList[i]:
      tempArr = []   
      tempArr.append(i)
      tempArr.append(emiDate)
      tempArr.append(oneKey)
      tempArr.append(oneKey)
      tempArr.append('')
      tempArr.append('')
      tempArr.append('')
      tempArr.append('')
      tempArr.append(i)
      tempArr.append(oneKey)

      res.append(tempArr)
  return res
# savePersonList()

# findPersonFace()

# emiArr = buildFakeEmiArr()
# saveJsonData('../data/jpEmisTopics.json', emiArr)



