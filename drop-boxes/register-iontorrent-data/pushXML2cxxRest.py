import os
import sys

import requests
from requests.auth import HTTPBasicAuth
import configparser

authData = {}

def loadConfigFile():
    config = configparser.ConfigParser()

    homedir = os.path.expanduser("~")
    config.read(os.path.join(homedir, '.cxxrest/config.ini'))
    print config.sections()

    authData['authuser'] = config['CXXSETUP']['authuser']
    authData['password'] = config['CXXSETUP']['password']
    authData['serveraddr'] = config['CXXSETUP']['serveraddr']

def checkRESTinterface():
    response = requests.get(authData['serveraddr'] + '/centraxx/rest/info', verify=False)
    return response

def fetchPatientByMPI(mpiCode):
    restAuth = HTTPBasicAuth(authData['authuser'], authData['password'])
    restParams = {'psn': mpiCode, 'idType': 'mpi'}

    queryUrl = authData['serveraddr'] + '/centraxx/rest/export/decisiveId/patient'
    response = requests.get(queryUrl, params=restParams, auth=restAuth, verify=False)

    return response

def pushXML2CxxREST(filepath):
    filename = os.path.basename(filepath.strip())
    importUrl = authData['serveraddr'] + '/centraxx/rest/import/queue/' + filename
    restAuth = HTTPBasicAuth(authData['authuser'], authData['password'])
    headers = {'Content-Type': 'application/xml'}
    files = {'file': open(filepath, 'rb')}

    response = requests.post(importUrl, files=files, auth=restAuth, headers=headers, verify=False)

    return response

def triggerCxxImport(filepath):
    filename = os.path.basename(filepath.strip())
    importUrl = authData['serveraddr'] + '/centraxx/rest/import/queue/' + filename + '/start'
    restAuth = HTTPBasicAuth(authData['authuser'], authData['password'])

    response = requests.post(importUrl, auth=restAuth, verify=False)

    return response

def getSuccessfulImport(filepath):
    filename = os.path.basename(filepath.strip())
    importUrl = authData['serveraddr'] + '/centraxx/rest/import/successful/' + filename
    restAuth = HTTPBasicAuth(authData['authuser'], authData['password'])

    response = requests.post(importUrl, auth=restAuth, verify=False)

    return response

def getErroneousImport(filepath):
    filename = os.path.basename(filepath.strip())
    importUrl = authData['serveraddr'] + '/centraxx/rest/import/error/' + filename
    restAuth = HTTPBasicAuth(authData['authuser'], authData['password'])

    response = requests.post(importUrl, auth=restAuth, verify=False)

    return response

def showCxxImportQueue():
    queueUrl = authData['serveraddr'] + '/centraxx/rest/import/queue'
    restAuth = HTTPBasicAuth(authData['authuser'], authData['password'])

    response = requests.get(queueUrl, auth=restAuth, verify=False)

    return response






# load the username, password, server address etc.
loadConfigFile()

resp = pushXML2CxxREST(sys.argv[1])
print resp.status_code
resp = showCxxImportQueue()
print resp.status_code, resp.content

resp = triggerCxxImport(sys.argv[1])
print resp.status_code, resp.content
resp = getSuccessfulImport(sys.argv[1])
print resp.status_code, resp.content

resp = getErroneousImport(sys.argv[1])
print resp.status_code, resp.content

#print authData
#checkRESTinterface()
#resp = fetchPatientByMPI('')

#outfile = open('result.xml', 'w')
#outfile.write(resp.text.encode('utf-8'))
#outfile.close()
