from Cleaner import retrieveAndClean# The cleaner

prob = {} # The probability data
classProb = {} # The probability data of the class values
bin_minmax_data = {} # holda relevant data considering each attribute
num_of_bins = -1 # number of bins of the discretization

# This function will classify a single record
# record - the given record
def testRecord(record):
    max = -1
    maxC = ""
    #print(record)
    #print(prob)
    for key in classProb:
        value = float(classProb[key])
        #multiply all of the probabillities
        # need to take care of missing test values (making the numeric into bins and so on)
        # a record would be a map between attribute to the value

        for key2 in record:
            value = value * prob[key2][record[key2]][key]
        if value > max:
            max = value
            maxC = key
    return maxC

# This function will test all of the records in the test file (int the given path)
# and will write the output to the output file (in the given path)
# test_path - the full path of the test file
# output_path - the full path of the output file
def test(test_path,output_path):
    array_of_test = getCleanDataTest(test_path)

    outputFile = open(output_path, "w")
    with outputFile:
        for i in range(0,len(array_of_test)):
            classification = testRecord(array_of_test[i])
            if classification[0].lower() == "y":
                classification = "yes"
            else:
                classification = "no"
            outputFile.write("%d %s \n" % (i+1, classification))
    outputFile.close()


# This function is responsible for cleaning the data in the test set (in the given path)
# test_path - the full path of the test file
def getCleanDataTest(test_path):
    try:
        testFile = open(test_path, "r")
    except IOError:
        print("could not open file")
    with testFile:
        arrayOfTest = []
        first =True
        arrayOfHeaders = []
        for record in testFile:
            if record[len(record) - 1] == '\n':
                record = record[:-1]
            if first:
                first = False
                arrayOfHeaders = record.split(",")
            else:
                dicOfTest = {}

                split = record.split(",")
                for i in range(0, len(split)-1):
                    name = arrayOfHeaders[i]
                    if len(split[i])==0:# Missing value
                        if bin_minmax_data[name]["isNumeric"]:
                            # If numeric
                            value = 0

                            for key in classProb:
                                value = value + float(bin_minmax_data[name]["avgVal"+key])*float(classProb[key])

                            split[i] = str(value)
                        else: # If not numeric
                            split[i] = bin_minmax_data[name]["max"]
                    #Assign bin
                    if bin_minmax_data[name]["isNumeric"]:
                        recordVal = float(split[i])

                        bin_width = float(bin_minmax_data[name]["width"])

                        num_bin = int(recordVal / bin_width)

                        if num_bin >= num_of_bins:
                            num_bin = num_of_bins-1
                        if num_of_bins<0:
                            num_bin = 0

                        split[i] = str(num_bin)
                    dicOfTest[arrayOfHeaders[i]] = split[i]
                arrayOfTest.append(dicOfTest)
    testFile.close()
    return arrayOfTest


# This function will be summoned from the gui when
# we want to create the model
# tran_path - the full path of the trainSet file
# stracture_path - the full path of the structure file
# number_of_buns - the number of bins for discretization
def clickTrain(train_path,stracture_path,number_of_bins):
    global prob
    global classProb

    global  bin_minmax_data
    global num_of_bins
    prob ,classProb,bin_minmax_data= train(train_path,stracture_path,number_of_bins)
    print(bin_minmax_data)
    num_of_bins = number_of_bins

# This function will create the model and train it using the data set
# tran_path - the full path of the trainSet file
# stracture_path - the full path of the structure file
# number_of_buns - the number of bins for discretization
def train(train_path,stracture_path,number_of_bins):
    preparedData,bin_minmax_data,attribures= retrieveAndClean(train_path,stracture_path,number_of_bins)

    probabilities = {}#For each attribute, for each pair of (value,classValue) calculate the probability

    counterOfClassValues = countClassValues(preparedData,attribures["class"])

    classValues = attribures["class"]
    for key in attribures:
        if key !="class":
            if bin_minmax_data[key]["isNumeric"]:
                probabilities[key] = probabilityForAttribute(key, number_of_bins, classValues, preparedData,
                                                                counterOfClassValues)
            else:
                probabilities[key] = probabilityForAttribute(key, attribures[key], classValues, preparedData,
                                                             counterOfClassValues)


    for key in counterOfClassValues:
        counterOfClassValues[key] = float(counterOfClassValues[key])/len(preparedData)
    return probabilities, counterOfClassValues,bin_minmax_data

# This function counts the number of records from each class from the given data
# data - the given data
# classvalues - the possible class values (in our case - y/n)
def countClassValues(data,classValues):
    dict = {}
    for i in range(0,len(classValues)):
        dict[classValues[i]] = 0
    for i in range(0, len(data)):
        classVal = data[i]["class"]
        dict[classVal] = dict[classVal] + 1
    return dict

# This function will calculate the relevant statistics for a single attribute from the data set
# attributeName - the name of the attribute
# values - the possible values for the given attribute
# classValues - the possible values for the "class" attribute
# data - The given data
# counterOfClassValues - The amount of records from each class in the data
def probabilityForAttribute(attributeName,values,classValues,data,counterOfClassValues):
    m =2
    if is_number(values):
        # numeric classValue = number of bins
        array = []
        for i in range(0,values):

            array.append(str(i))
        values = array


    #Initializing the dictionary
    counter = {}
    for i in range(0,len(values)):
        counter[values[i]] = {}
        for k in range(0, len(classValues)):
            counter[values[i]][classValues[k]] = 0

    # Scanning the records
    for i in range(0, len(data)):
        value = str(data[i][attributeName])
        classVal = data[i]["class"]
        counter[value][classVal] = counter[value][classVal] + 1

    for key in counter:
        for key2 in counter[key]:
            counter[key][key2] = (float(counter[key][key2])+m*(1/len(values)))/(counterOfClassValues[key2]+m)#M-estimator
    return counter

# This function will check if the given object is a number
# s - the given object
def is_number(s):
    try:
        float(s)
        return True
    except Exception:
        return False



