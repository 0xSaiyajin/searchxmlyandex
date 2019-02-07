# -*- coding: utf-8 -*-
# @author: 0xSaiyajin

import requests,json
import xml.etree.ElementTree as ET

class YandexXMLSearch:
    def __init__(self, username, api_key, query):
        self.username = username
        self.api_key = api_key
        self.search_url = 'https://yandex.com/search/xml?l10n=en&user=%s&key=%s&p=999&query=' %(self.username, self.api_key)
        self.query = query
        self.response = ET.ElementTree()
        self.search()
        
    def getQuery(self):
        return self.query
    
    def setQuery(self, query):
        self.query = query
        self.search()
        
    def getTotalPageCount(self):
        count = (self.getTotalResultCount() / 10) + 1   # count limitation.
        if count > 5:
            return 5
        else:
            return count
    
    def getTotalResultCount(self):
        results = [results for results in self.response.iter('results')][0]
        resultsCount = [count for count in results.iter('page')][0]
        return int(resultsCount.attrib['last'])
        
    def search(self):
        url = self.search_url+'"%s"' %(self.query)
        request = requests.get(url)
        response = ET.fromstring(request.content)[1]
        self.response = response
    
    def getResultJSONString(self):
        results = self.getAllResults()
        resultList = list()
        
        for result in results:
            try:
                result_id = [doc_id for doc_id in result.iter('doc')][0].attrib['id']
            except IndexError as e:
                result_id = str()
            try:
                result_url = [result_url for result_url in result.iter('url')][0].text
            except IndexError as e:
                result_url = str()
            try:
                result_domain = [result_domain for result_domain in result.iter('domain')][0].text
            except IndexError as e:
                result_domain = str()
            try:
                result_title = [result_title for result_title in result.iter('title')][0]
                cleaned_title = ET.tostring(result_title,
                                            method='xml').replace('<hlword>','').replace('</hlword>','')
                result_title = ET.fromstring(cleaned_title).text
            except IndexError as e:
                result_title = str()
            try:
                result_content = [result_content for result_content in result.iter('passage')][0]
                cleaned_content = ET.tostring(result_content,
                                              method='xml').replace('<hlword>','').replace('</hlword>','')
                result_content = ET.fromstring(cleaned_content).text
            except IndexError as e:
                result_content = str()
                
            result = {"result_id": result_id, "url": result_url, "domain": result_domain, "title": result_title, "body": result_content}
            resultList.append(result)
            
        JSONStrObj = json.dumps(resultList)
        return JSONStrObj
    
    def getJSONObject(self):
        JSONObject = json.loads(self.getResultJSONString())
        return JSONObject
        
    def getResponseDate(self):
        date = self.response.attrib['date']
        YYYY,MM,DD = date[0:4], date[4:6], date[6:8]
        h,m,s = date[9:11], date[11:13], date[13:15]
        newdateformat = "%s:%s:%s(UTC) %s.%s.%s" %(h,m,s, DD,MM,YYYY)
        return newdateformat
    
    def getAllResults(self):
        resultsTree = []
        for index in range(self.getTotalPageCount()):
            search_url = 'https://yandex.com/search/xml?l10n=en&user=%s&key=%s&p=%s&query=' %(self.username, self.api_key, index)
            url = search_url + '"%s"' %(self.query)
            request = requests.get(url)
            response = ET.fromstring(request.content)[1]
            results = [results for results in response.iter('results')][0]
            groups = [group for group in results.iter('group')]
            resultsTree.extend(groups)
        return resultsTree