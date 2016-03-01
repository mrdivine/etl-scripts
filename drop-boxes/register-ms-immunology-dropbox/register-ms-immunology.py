'''

Note:
print statements go to: ~openbis/servers/datastore_server/log/startup_log.txt
'''
import sys
sys.path.append('/home-link/qeana10/bin/')

import checksum
import re
import os
import ch.systemsx.cisd.etlserver.registrator.api.v2
from java.io import File
from org.apache.commons.io import FileUtils
from ch.systemsx.cisd.openbis.generic.shared.api.v1.dto import SearchCriteria
from ch.systemsx.cisd.openbis.generic.shared.api.v1.dto import SearchSubCriteria

# ETL script for registration of MS data coming from immunology departmen
# expected:
# *Q[Project Code]^4[Sample No.]^3[Sample Type][Checksum]*.*
pattern = re.compile('Q\w{4}[0-9]{3}[a-zA-Z]\w')

def isExpected(identifier):
    try:
        id = identifier[0:9]
        #also checks for old checksums with lower case letters
        return checksum.checksum(id)==identifier[9]
    except:
        return False

def process(transaction):
    context = transaction.getRegistrationContext().getPersistentMap()

    # Get the incoming path of the transaction
    incomingPath = transaction.getIncoming().getAbsolutePath()

    key = context.get("RETRY_COUNT")
    if (key == None):
        key = 1

    # Get the name of the incoming file
    name = transaction.getIncoming().getName()
        
    identifier = pattern.findall(name)[0]
    if isExpected(identifier):
        experiment = identifier[1:5]
        project = identifier[:5]
        parentCode = identifier[:10]
    else:
        print "The identifier "+identifier+" did not match the pattern Q[A-Z]{4}\d{3}\w{2} or checksum"


    for root, subFolders, files in os.walk(incomingPath):
        if subFolders:
            subFolder = subFolders[0]
        for f in files:
            if f.endswith('.tsv'):
                metadataFile = open(os.path.join(root, f), 'r')
    
    metadataFile.readline()
    for line in metadataFile:
        splitted = line.split('\t')
        file = splitted[0]
        instr = splitted[1]
        date = splitted[2]
        share = splitted[3]
        repl = splitted[4]

        newMSExperiment = transaction.createNewExperiment(newExpID, "Q_MS_MEASUREMENT")
        newMSExperiment.setPropertyValue('Q_CURRENT_STATUS', 'FINISHED')

        newMSSample = transaction.createNewSample('/' + space + '/' + 'MS'+ parentCode, "Q_MS_RUN")
        newMSSample.setParentSampleIdentifiers([sa.getSampleIdentifier()])
        newHMSSample.setExperiment(newHLATypingExperiment)
  
       
	
    search_service = transaction.getSearchService()
    sc = SearchCriteria()
    sc.addMatchClause(SearchCriteria.MatchClause.createAttributeMatch(SearchCriteria.MatchClauseAttribute.CODE, parentCode))
    foundSamples = search_service.searchForSamples(sc)

    parentSampleIdentifier = foundSamples[0].getSampleIdentifier()
    space = foundSamples[0].getSpace()
    sa = transaction.getSampleForUpdate(parentSampleIdentifier)

    # register new experiment and sample
    existingExperimentIDs = []
    existingExperiments = search_service.listExperiments("/" + space + "/" + project)
    
    numberOfExperiments = len(search_service.listExperiments("/" + space + "/" + project)) + 1

    for eexp in existingExperiments:
        existingExperimentIDs.append(eexp.getExperimentIdentifier())

    newExpID = '/' + space + '/' + project + '/' + project + 'E' +str(numberOfExperiments)

    while newExpID in existingExperimentIDs:
        numberOfExperiments += 1 
        newExpID = '/' + space + '/' + project + '/' + project + 'E' +str(numberOfExperiments)

    newHLATypingExperiment = transaction.createNewExperiment(newExpID, "Q_NGS_HLATYPING")
    newHLATypingExperiment.setPropertyValue('Q_CURRENT_STATUS', 'FINISHED')

    newHLATypingSample = transaction.createNewSample('/' + space + '/' + 'HLA'+ parentCode, "Q_NGS_HLATYPING")
    newHLATypingSample.setParentSampleIdentifiers([sa.getSampleIdentifier()])
    newHLATypingSample.setExperiment(newHLATypingExperiment)

    for root, subFolders, files in os.walk(incomingPath):
        if subFolders:
            subFolder = subFolders[0]
        for f in files:
            if f.endswith('.alleles'):
                resultFile = open(os.path.join(root, f), 'r')

    resultContent = resultFile.read()
    newHLATypingSample.setPropertyValue("Q_HLA_TYPING", resultContent)

    # create new dataset 
    dataSet = transaction.createNewDataSet("Q_NGS_HLATYPING_DATA")
    dataSet.setMeasuredData(False)
    dataSet.setSample(newHLATypingSample)

    transaction.moveFile(incomingPath, dataSet)
