from ast import If
import re
from turtle import title
from fetchData import params
from fetchData import results
import requests
import json
import constants


class Fetch:

    cveParams = None
    cpeParams = None

    def __init__(self):
        self.cpeParams = params.CpeParams(constants.apiKey)
        self.cveParams = params.CveParams(constants.apiKey)

        self.cpeParams.addOns = 'cves'
        self.cveParams.addOns = 'dictionaryCpes'
        print("Fetch Create success", constants.production)

    def productions(self):

        cpeResults = []
        self.cpeParams.keyword = constants.production

        url = constants.cpeUrls + '?' + str(self.cpeParams)
        response = json.loads(requests.get(url).text)

        totalResults = constants.totalResults if constants.totalResults != None\
            and constants.totalResults < response['totalResults'] else response['totalResults']
        print('totalResult:', totalResults)
        for startIndex in range(self.cpeParams.startIndex, totalResults, self.cpeParams.resultsPerPage):
            self.cpeParams.startIndex = startIndex
            url = constants.cpeUrls + '?' + str(self.cpeParams)
            response = requests.get(url).json()

            for cpe in response['result']['cpes']:
                if constants.regexStr != None:
                    if re.search(constants.regexStr, cpe['titles'][0]['title'], re.M | re.I) != None:
                        cpeResults.append(cpe)
                elif constants.regexStr == None:
                    cpeResults.append(cpe)

        self.cpeParams.startIndex = 0
        self.cpeParams.keyword = None

        return cpeResults

    def cves(self):

        self.cveParams.cpeMatchString = constants.cpe23uri
        url = constants.cveUrls + '?' + str(self.cveParams)
        response = requests.get(url).json()
        print(url)
        totalResults = constants.totalResults if constants.totalResults != None\
            and constants.totalResults < response['totalResults'] else response['totalResults']
        print('totalResult:', totalResults)

        cveResults = []
        for startIndex in range(self.cveParams.startIndex, totalResults, self.cveParams.resultsPerPage):

            self.cveParams.startIndex = startIndex
            url = constants.cveUrls + '?' + str(self.cveParams)
            response = requests.get(url).json()

            for cve in response['result']['CVE_Items']:
                cveResults.append(cve)

        self.cveParams.startIndex = 0

        return cveResults

    def cveDetails(self, cve):

        url = constants.cveUrls + "/" + cve+'?'+str(self.cveParams)
        print(url)
        respose = requests.get(url)
        print(respose.text)
