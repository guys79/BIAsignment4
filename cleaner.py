given_path = "C:\\Users\\guy schlesinger\\Desktop\עבודה 4 בינה"
train_path = given_path + "\\train.csv"
stracture_path = given_path + "\\Structure.txt"
number_of_bins = 10
# This function will retrieve and clean the data in the training set
def retrieveAndClean():
    # First step: reading the records from the file
    # Any empty cell will contain "missingUnique"
    try:
        testFile = open(train_path,"r")
    except IOError:
        print ("could not open file")
    with testFile:
        arrayOfHandledRecords = []
        first = True
        arrayOfHeaders = []
        for record in testFile:
            if record[len(record)-1] == '\n':
                record = record[:-1]
            if first:
                first = False
                arrayOfHeaders = record.split(",")

            else:
                recordHandler(arrayOfHandledRecords, record,arrayOfHeaders)


    # Second step: complete missing values
    attributes = getStructure()  # The structure
    attributes_minmax_bins = {}
    print(arrayOfHandledRecords)
    for i in range(0,len(arrayOfHeaders)):

        attributes_minmax_bins[arrayOfHeaders[i]] = {"isNumeric":attributes[arrayOfHeaders[i]] == "NUMERIC"}
        fillMissingForAttribute(arrayOfHandledRecords, attributes[arrayOfHeaders[i]], arrayOfHeaders[i], attributes["class"],attributes_minmax_bins)
    print(arrayOfHandledRecords)

    # Third step: Discretization
    for i in range(0,len(arrayOfHeaders)):
        if attributes[arrayOfHeaders[i]] == "NUMERIC":
            divideToBins(number_of_bins,arrayOfHandledRecords,arrayOfHeaders[i],attributes_minmax_bins,i)
    return arrayOfHandledRecords,attributes_minmax_bins

def divideToBins(number_of_bins,arrayOfHandledRecords,attributeName,attributes_minmax_bins,i):
    #print(attributeName)
    max = float(arrayOfHandledRecords[0][attributeName])
    min = max


    for i in range(1, len(arrayOfHandledRecords)):
        recordVal = float(arrayOfHandledRecords[i][attributeName])

        if recordVal>max:
            max = recordVal
        elif recordVal<min:
            min = recordVal
    bin_width = (max-min)/number_of_bins
    attributes_minmax_bins[attributeName]["width"] = bin_width
    attributes_minmax_bins[attributeName]["min"] = min


    print(attributeName+" width = "+str(bin_width)+" max = "+str(max)+" min = "+str(min))
    for i in range(0, len(arrayOfHandledRecords)):
        recordVal = float(arrayOfHandledRecords[i][attributeName])
        num_bin = int((recordVal-min)/bin_width)
        arrayOfHandledRecords[i][attributeName] = num_bin
        #print(str(arrayOfHandledRecords[i][attributeName]) +" "+ str(num_bin))

def fillMissingForAttribute(arrayOfHandledRecords,possibleValues,attributeName,possibleClassValues,attributes_minmax_bins):

    if possibleValues == "NUMERIC":
        # Incase of numeric
        dicOfCounters = {}
        dicOfSummers = {}
        for i in range(0, len(possibleClassValues)):
            dicOfCounters[possibleClassValues[i]] = 0
            dicOfSummers[possibleClassValues[i]] = 0
        for i in range(0, len(arrayOfHandledRecords)):
            recordVal = arrayOfHandledRecords[i][attributeName]

            if recordVal != "Missing" + attributeName:
                classVal = arrayOfHandledRecords[i]["class"]
                dicOfCounters[classVal] = dicOfCounters[classVal] + 1
                dicOfSummers[classVal] = dicOfSummers[classVal] + float(recordVal)

        dicOfAverage = {}
        for key in dicOfCounters:
            dicOfAverage[key] = (dicOfSummers[key]*1.0)/dicOfCounters[key]
            attributes_minmax_bins[attributeName]["avgVal"+key] = dicOfAverage[key]

        for i in range(0, len(arrayOfHandledRecords)):
            recordVal = arrayOfHandledRecords[i][attributeName]
            if recordVal == "Missing" + attributeName:
                arrayOfHandledRecords[i][attributeName] = dicOfAverage[arrayOfHandledRecords[i]["class"]]


    else:
        # Incase of categorical
        dicOfCounters = {}
        for i in range(0, len(possibleValues)):
            dicOfCounters[possibleValues[i]] = 0
        for i in range(0,len(arrayOfHandledRecords)):
            recordVal = arrayOfHandledRecords[i][attributeName]
            if recordVal!= "Missing"+attributeName:
                dicOfCounters[recordVal] = dicOfCounters[recordVal] +1

        maxVal = -1;
        max = ""
        for key in dicOfCounters:
            if dicOfCounters[key]>maxVal:
                maxVal = dicOfCounters[key]
                max = key
        attributes_minmax_bins[attributeName]["max"] = max
        for i in range(0, len(arrayOfHandledRecords)):
            recordVal = arrayOfHandledRecords[i][attributeName]
            if recordVal == "Missing" + attributeName:
                arrayOfHandledRecords[i][attributeName] = max



# arrayOfHandledRecords - The array that we will put the rexord in
# record - The given record
# arrayOfHeaders - The order of the attributes
def recordHandler(arrayOfHandledRecords, record,arrayOfHeaders):
    dictionayOfValues = {}
    split = record.split(",")
    if len(split)!=len(arrayOfHeaders):
        return
    for i in range(0,len(split)):
        if len(split[i]) == 0:
            dictionayOfValues[arrayOfHeaders[i]] = "Missing"+arrayOfHeaders[i]
        else:
            dictionayOfValues[arrayOfHeaders[i]] = split[i]
    arrayOfHandledRecords.append(dictionayOfValues)
    #print(dictionayOfValues)





# This function gets the attributes from the structure file
def getStructure():
    try:
        stractureFile = open(stracture_path,"r")
    except IOError:
        print ("could not open file")
    with stractureFile:
        dicOfAttributes = {}

        for line in stractureFile:

            split = line.split()
            for i in range(3, len(split)):
                split[2] = split[2]+" "+split[i]
            values = getValues(split[2])
            dicOfAttributes[split[1]]=values


    stractureFile.close()
    return dicOfAttributes

# This function returns the string that descrices the values of an arrtribute as an array
# (if there is more than 1 value)
def getValues(values):
    if '{' not in values:
        return values
    values = values[1:-1]#Taking of the ()
    split = values.split(",")
    return split

print(retrieveAndClean())