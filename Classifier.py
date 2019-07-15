from Cleaner import retrieveAndClean# The cleaner

prob = {}
classProb = {}
def testRecord(record):
    max = -1
    maxC = ""
    for key in classProb:
        value = float(classProb[key])
        #multiply all of the probabillities
        # need to take care of missing test values (making the numeric into bins and so on)
        # a record would be a map between attribute to the value

        for key2 in record:
            value = value * prob[key2][record[value]]
        if value > max:
            max = value
            maxC = key
    return maxC


def clickTrain(train_path,stracture_path,number_of_bins):
    global prob
    global classProb
    prob ,classProb= train(train_path,stracture_path,number_of_bins)


def train(train_path,stracture_path,number_of_bins):
    preparedData,bin_minmax_data,attribures = retrieveAndClean(train_path,stracture_path,number_of_bins)
    print(preparedData)
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
    print(probabilities)

    for key in counterOfClassValues:
        counterOfClassValues[key] = float(counterOfClassValues[key])/len(preparedData)
    return probabilities


def countClassValues(data,classValues):
    dict = {}
    for i in range(0,len(classValues)):
        dict[classValues[i]] = 0
    for i in range(0, len(data)):
        classVal = data[i]["class"]
        dict[classVal] = dict[classVal] + 1
    return dict

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

   # print(counter)
   # print(values)
  #  print(attributeName+"                ffffff")
    # Scanning the records
    for i in range(0, len(data)):
        value = str(data[i][attributeName])
        classVal = data[i]["class"]
        #print("value "+value+" classval "+classVal)
        counter[value][classVal] = counter[value][classVal] + 1

    for key in counter:
        for key2 in counter[key]:
            counter[key][key2] = (float(counter[key][key2])+m*(1/len(values)))/(counterOfClassValues[key2]+m)#M-estimator
    return counter

def is_number(s):
    try:
        float(s)
        return True
    except Exception:
        return False

given_path = "C:\\Users\\guy schlesinger\\Desktop\עבודה 4 בינה"
train_path = given_path + "\\train.csv"
stracture_path = given_path + "\\Structure.txt"
number_of_bins = 10
#a ,b,c = retrieveAndClean(train_path,stracture_path,number_of_bins)
clickTrain(train_path,stracture_path,number_of_bins)
print(prob)