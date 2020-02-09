import re
import os

UUIDSection = ["REQUEST", "RESPONSE"]
TransactionStart = "<[A-Za-z]+:Envelope"
TransactionEnd = "</[A-Za-z]+:Envelope>"
BodyStart = "<[A-Za-z]+:Body>"

transactionDictionary = {}

# input
fileLocation = raw_input("Enter the path to the log file: ")
if not fileLocation:
    fileLocation = "../air/air.log"
log = open(fileLocation, "r")
contents = log.read()

# Regex which is used to parse transaction with meta data
transactionRegex = ""
i = 0
while i < len(UUIDSection):
    transactionRegex += UUIDSection[i] + ".*?" + TransactionEnd
    if i + 1 < len(UUIDSection):
        transactionRegex += "|"
    i += 1

# Regex which is used to find uuid
uuidRegex = ""
i = 0
while i < len(UUIDSection):
    UUIDSection[i]
    if i + 1 < len(UUIDSection):
        uuidRegex += ","
    i += 1

# populate transaction dictionary
transactions = re.findall(transactionRegex, contents, re.DOTALL)
for transaction in transactions:
    uuidStartIndex = re.search(uuidRegex, transaction).end() + 1
    uuidEndIndex = re.search("]", transaction).start()
    uuid = transaction[uuidStartIndex:uuidEndIndex]
    transactionStartIndex = re.search(TransactionStart, transaction).start()
    payloadStartIndex = re.search(BodyStart, transaction).end() + 1
    transactionType = re.search(r'[^\s]+', transaction[payloadStartIndex:].split(":")[1]).group().strip(">")
    entry = transactionDictionary.get(transactionType)
    transaction = transaction[transactionStartIndex:]
    if entry is None:
        transactionDictionary.update({transactionType: [(uuid, transaction)]})
    else:
        entry.append((uuid, transaction))
        transactionDictionary.update({transactionType: entry})

keys = transactionDictionary.keys()

# make log dir
if len(keys) > 0:
    logDir = fileLocation.rpartition("/")[0] + "/logs"
    if not os.path.exists(logDir):
        os.mkdir(logDir)

# create xml files
for key in keys:
    for index, entry in enumerate(transactionDictionary.get(key)):
        (uuid, transaction) = entry
        suffix = "_" + uuid
        file = open(logDir + "/" + key + suffix + ".xml", "w+")
        file.write(transaction)

print("xmls created. check " + logDir)
