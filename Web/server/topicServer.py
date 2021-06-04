import sys
import os
import json

TOPIC_DICT_FILE = 'server/data/topic_to_persons_kw-all.json'
TOPIC_INFO_FILE = 'server/data/date_to_topics.json'
PERSON_TO_TOPIC_FILE = 'server/data/personToTopicListAll.json'
NEWS_CONTENT_INFO_FILE = 'server/data/date_to_topics_to_captions.json'

MAX_SEARCH_PERSON = 8
MAX_SEARCH_RESULT = 400

def getJsonData(path):
  pwd = os.getcwd()
  with open(pwd+'/'+path, 'rb') as loadFile:
    data = json.load(loadFile)
  return data

class myTopicServer():
  def __init__(self):
    print 'start loading the topic data ...'
    self.allTopic = self.getAllTopic()
    self.topicTimeDict = self.getTopicTime()
    self.personToTopic = self.getPersonToTopic()
    self.topicToCaption = self.getTopicCaptions()

  def getAllTopic(self):
    allData = getJsonData(TOPIC_DICT_FILE)
    print 'loading all the topics...'
    return allData

  def getTopicCaptions(self):
    topicCaptionDict = {}
    topicCaption = getJsonData(NEWS_CONTENT_INFO_FILE)
    for oneDate in topicCaption:
      for oneTopic in topicCaption[oneDate]:
        oneDateTopic = oneDate + '-Topic' + oneTopic
        topicCaptionDict[oneDateTopic] = topicCaption[oneDate][oneTopic]
    print 'loading the video caption for each topic...'
    return topicCaptionDict

  def getTopicTime(self):
    topicTimeDict = {}
    topicTime = getJsonData(TOPIC_INFO_FILE)
    for oneTime in topicTime:
      for oneTopic in topicTime[oneTime]:
        oneTimeTopic = oneTime + '-Topic' + oneTopic
        topicTimeDict[oneTimeTopic] = topicTime[oneTime][oneTopic]
    print 'loading the video interval for each topic...'
    return topicTimeDict

  def getFaceList(self):
    pwd = os.getcwd()
    faceNameList = os.listdir(pwd + '/client/data/faces')
    nameDict = {}
    for oneFace in faceNameList:
      faceName = oneFace.replace('.jpg', '')
      if faceName not in nameDict:
        nameDict[faceName] = oneFace
    return nameDict

  def getPersonToTopic(self):
    personToTopic = getJsonData(PERSON_TO_TOPIC_FILE)
    print 'loading the topics to each person...'
    return personToTopic

  def getRightDateFormat(self, dateInput):
    if '_' in dateInput:
      res = dateInput
    else:
      res = ''
      year = ''
      month = ''
      day = ''
      if len(dateInput) >= 4:
        year = dateInput[0:4]
        if len(dateInput) >= 6:
          month = dateInput[4:6]
        if len(dateInput) >= 8:
          day = dateInput[6:8]
        res = year + '_' + month + '_' + day
      else:
        res = dateInput
    return res

  def analyseRequest(self, para):

    self.getDateRestrictArr(para['dates'])
    faceNames = para['faceNames']
    faceResults = []
    res = []
    faceRes = []
    faceNameSize = len(faceNames)
    if faceNameSize > 0:
      self.filterMethod = self.matchFaceToTopics
      faceRes = self.logicalParser(self.allTopic.keys(), faceNames)
    
    keywords = para['keywords']
    keywordRes = []
    keywordSize = len(keywords)

    if keywordSize > 0:
      self.filterMethod = self.matchKeywordToTopics
      keywordRes = self.logicalParser(self.allTopic.keys(), keywords)

    if para['fkconj'] == 'AND' and keywordSize > 0 and faceNameSize > 0:
      tempArr = self.conjLeftRightResults(faceRes, keywordRes)
    else:
      tempArr = self.combineLeftRightResults(faceRes, keywordRes)

    numberChecker = 0
    for oneTopic in tempArr:
      if numberChecker >= para['maxSnpNum']:
        break
      content = ';'.join(self.allTopic[oneTopic])
      captions = '\n'.join(self.topicToCaption[oneTopic]) 
      res.append({
          'title': oneTopic.replace('Topic', 'Segment'),
          'content': content,
          'time_info': self.topicTimeDict[oneTopic],
          'video_file': oneTopic.split('-')[0]+'.webm',
          'captions': captions
      })
      numberChecker += 1
    return res


  def checkKeywords(self, keywords, content):
    co = content.lower()
    for oneWord in keywords:
      lo = oneWord.lower()
      if lo in co:
        return True
      else:
        return False

  def getDateRestrictArr(self, dateArr):
    res = []
    for oneDateRestict in dateArr:
      tempArr = oneDateRestict.split('-')
      t1 = self.getRightDateFormat(tempArr[0])
      t2 = self.getRightDateFormat(tempArr[1])
      if t1 != '' or t2 != '':
        res.append([t1, t2])
    self.dateArr = res

  def checkTimeArr(self, topicTitle):
    res = True
    for oneDateRestict in self.dateArr:
      res = self.checkTime(oneDateRestict[0], oneDateRestict[1], topicTitle)
      if res == True:
        return True
    return res


  def checkTime(self, startDate, endDate, topicTitle):
    res = False
    print startDate
    if startDate != '' and endDate != '':
      if startDate <= topicTitle and topicTitle <= endDate:
        res = True
    elif startDate != '':
      if startDate <= topicTitle:
        res = True
    elif endDate != '':
      if endDate >= topicTitle:
        res = True
    return res

  def getTopicFromFaces(self, faceStr):
    facesArr = faceStr.split(',')
    topics = []
    faceCounter = 0
    for oneFace in facesArr:
      faceCounter += 1
      if faceCounter >= MAX_SEARCH_PERSON:
        break
      if oneFace in self.personToTopic:
        topics += self.personToTopic[oneFace]
    return topics

  def getRightConj(self, rightExpression):
    lg = len(rightExpression)
    conj = 'AND'
    rightExp = ''
    for i in range(lg-1):
      if rightExpression[i].get('conj') != None:
        conj = rightExpression[i]['conj']
        rightExp = rightExpression[i+1:]
        break
    return {
      'rightExpression': rightExp,
      'conj': conj
    }

  def combineLeftRightResults(self, leftRes, rightRes):
    res = []
    for i in leftRes:
      res.append(i)
    for oneRes in rightRes:
      if oneRes not in leftRes:
        leftRes.append(oneRes)
    return leftRes

  def conjLeftRightResults(self, leftRes, rightRes):
    res = []
    for i in leftRes:
      if i in rightRes:
        res.append(i)
    return res

  def matchFaceToTopics(self, faceName, topicTarget):
    res = []
    if faceName in self.personToTopic:
      tempRes = self.personToTopic[faceName]
      for oneTopic in tempRes:
        if oneTopic in topicTarget and self.checkTimeArr(oneTopic):
          res.append(oneTopic)
    return res
  
  def matchKeywordToTopics(self, keyword, topicTarget):
    res = []
    if keyword == '':
      return res
    for oneTopic in topicTarget:
      if self.checkTimeArr(oneTopic):
        contentArr = self.allTopic[oneTopic]
        for oneWord in contentArr:
          if keyword in oneWord.lower():
            res.append(oneTopic)
            break
    return res

  def filterMethod(self, word, topicTarget):
    pass

  def logicalParser(self, topicTarget, expression):
    expSize = len(expression)
    if expSize == 0:
      return []
    elif expSize == 1:
      if expression[0].get('text') != None:
        return self.filterMethod(expression[0]['text'], topicTarget)
      else:
        return []
    else:
      if expression[0].get('text') != None:
        leftExpression = [expression[0]]
        rightInfo = self.getRightConj(expression[1:])
        rightExpression = rightInfo['rightExpression']
        conjExpression = rightInfo['conj']
        
      elif expression[0].get('bracket') != None:
        conjExpression = 'AND'
        if expression[0]['bracket'] == '(':
          count = 1
          startIndex = 1
          endIndex = 0
          for i in range(1, expSize):
            if expression[i].get('bracket') != None:
              if expression[i]['bracket'] == '(':
                count += 1
              elif expression[i]['bracket'] == ')':
                count -= 1
                if count == 0:
                  endIndex = i
                  break
          leftExpression = expression[startIndex : endIndex]
          rightInfo = self.getRightConj(expression[endIndex+1 :])
          rightExpression = rightInfo['rightExpression']
          conjExpression = rightInfo['conj']
        else:
          leftExpression = expression[1:]
          rightExpression = ''
      elif expression[0].get('conj') != None:
        leftExpression = expression[1:]
        rightExpression = ''
      
    leftResults = self.logicalParser(topicTarget, leftExpression)
    if conjExpression == 'AND':
      return self.logicalParser(leftResults, rightExpression)
    else:
      rightResults = self.logicalParser(topicTarget, rightExpression)
    return self.combineLeftRightResults(leftResults, rightResults)

