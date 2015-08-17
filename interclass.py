import pandas
import scipy.stats
from collections import Counter
import collections
import math
import numpy
from collections import defaultdict

def loadQuestions():

    # Add some abbreviations for the questions to make it easier to access them without making mistkaes

    questions = collections.OrderedDict()

    questions.update({'B,C,P required': u'Concepts from biology, chemistry, and physics are all required to fully understand any of these disciplines individually.'})
    questions.update({'Overlap interesting': u'I find the overlap between different branches of science (such as biology, chemistry, and physics) interesting.'})
    questions.update({'Draw upon knowledge': u'When completing a task in the sciences I draw upon knowledge from more than one of biology, chemistry, and physics.'})
    questions.update({'B important for P': u'Examples and concepts from biology are important when learning physics.'})
    questions.update({'B important for C': u'Examples and concepts from biology are important when learning chemistry.'})
    questions.update({'C important for B': u'Examples and concepts from chemistry are important when learning biology.'})
    questions.update({'C important for P': u'Examples and concepts from chemistry are important when learning physics.'})
    questions.update({'P important for B': u'Examples and concepts from physics are important when learning biology.'})
    questions.update({'P important for C': u'Examples and concepts from physics are important when learning chemistry.'})

    for shortq,longq in questions.iteritems():

        print('{0} : {1}...'.format(shortq,longq[0:20]))


    return questions

def renameFields(dataFrame,
                 origPhrases = None,
                 newPhrases = None):
    """
    Purpose: This function replaces the provided original columns (origPhrases)with the provided 
    phrases (newPhrases) in a Pandas data frame (dataFrame).

    If origPhrases is not provided, default values are provided based on experience

    Note that if the length of newPhrases is not the same as the length of 
    origPhrases, it will be assumed that newPhrases is of length one, and 
    the function first tries to make it the same length as origPhrases.

    Then, it is asserted that the length of newPhrases and origPhrases is
    the same, otherwise and error will be thrown.
    """
    
    if origPhrases is None:
        origPhrases = ['Please enter your 8 digit student ID number:',
                       'Please enter your student ID number (8 digits)',
                       'Username',
                       'Student ID']
        
    if newPhrases is None:
        newPhrases = ['StudentNumber']*len(origPhrases)
        
    elif len(newPhrases) != len(origPhrases):
        newPhrases = [newPhrases]*len(origPhrases)
        
    assert len(newPhrases) == len(origPhrases),'Please input either one replacement, or match length of origPhrases'
        
    for o,n in zip(origPhrases,newPhrases):
        dataFrame.rename(columns={o:n}, inplace=True)
        
    return dataFrame

def checkQuestions(dataFrame,
                   questionDict,
                   fname):
    """
    Purpose: This function checks the pandas data frame (dataFrame) to make sure that all the 
    interCLASS question statements are stored correctly and in the same format. The function checks 
    spelling, punctuation, capitalization. 

    The questions are stored in questionDict, and the check works by trying to access dataFrame 
    columns from a dictionary of questions (questionDict).

    Failed question statements are printed, and so is the filename (fname) for the offending excel file.

    """
    
    # Check to make sure that Q statements are stored the same way for all datasets

    check_questions = True
    
    for q in questionDict.values():
        try:
            x=dataFrame[q]
        except:
            check_questions = False
            print('{0} failed'.format(q))

    if check_questions:
        print('#### {0} #### \n All systems go, question statements are validated\n'.format(fname))
    else:
        print('#### {0} #### \n There were problems, please address them.\n'.format(fname))    

def likertReplace(dataFrame,
                  likertPhrase = None,
                  scores = None):
    """
    Purpose: This function replaces the likert phrases (likertPhrase) in a data frame (dataFrame) into numbers (scores)

    If no likertPhrases are provided, default 5 default values are provided, mapped as follows:

    'Strongly Disagree'     = -1
    'Disagree'              = -1
    'Neutral'               = 0
    'Agree'                 = 1
    'Strongly Agree'        = 1
    '<Unanswered>'          = numpy.nan
    """
    if likertPhrase is None:
        likertPhrase = ["Strongly Disagree", 
                        "Disagree", 
                        "Neutral", 
                        "Agree", 
                        "Strongly Agree",
                        "I don't understand the question",
                        "<Unanswered>"]

    # Choose Default scoring of the likert scale
    if scores is None:     
        scores = [-1,-1,0,1,1,numpy.nan,numpy.nan]

    # Replace likert scale with scores as specified    
    dataFrame = dataFrame.replace(to_replace=likertPhrase, value=scores)
    
    return dataFrame
    
def loadExcelasDF(rawPath= None,
                  filenames = None,
                  sheetname = 0,
                  scores = None,
                  removeStalwarts = None,
                  replaceLikert = False):
    """
    Purpose: This function loads provided excel files (filenames) as a dataFrame.
    """
    # Specify the rawPath of the csv files
    if rawPath is None:
        rawPath = '/phd/TA/python/Year 3 - InterClass/raw/'
    
    # Initialize empty df 
    allData = pandas.DataFrame()

    # Initialize questions
    questionDict = loadQuestions()
    loadCols = questionDict.keys()
    loadCols.append('Permission')
    loadCols.append('StudentNumber')
    loadCols.append('Course')

    # Iterate through all the filenames and append them to a single Data Frame    
    for fname in filenames:

        # Load in the dataframe from the csv file
        df = pandas.io.excel.read_excel(rawPath+fname,
                                        sheetname) 
    
        # Rename the student ID fileds
        df = renameFields(df)

        # Rename the Permission fileds
        df = renameFields(df, origPhrases=['Authorization'],
                              newPhrases=['Permission'])        
    
        # Check the questions for each df
        if questionDict is not None:
            checkQuestions(df,questionDict,fname)
        else:
            print('Warning: questions have not been checked')
        
        # Rename the question fields
        df = renameFields(df,origPhrases = questionDict.values(),
                             newPhrases = questionDict.keys())

        # Add permissions with default 1 if does not exist

        if 'Permission' not in df.columns:
            df['Permission'] = 1
            print('\t Added Permission fields \n')

        # Append them to one big dataframe
        allData = allData.append(df[loadCols])    
        
    # Set the index of the dataframe to be StudentNumber
    allData.set_index('StudentNumber',inplace=True)
    
    # Replace Likert scale with scores
    if replaceLikert:
        allData = likertReplace(allData,scores=scores)

    # Replace Do not agrees with -1

    allData = likertReplace(allData,'Do Not Agree',-1)

    if removeStalwarts:
        return allData[allData['Permission']>=0]

    else: 
        return allData        

def makePlotDict(allData,
                 questionDict,
                 courseList):

    """
    Purpose: This function takes a complete dataFrame (allData) and produces a ready-made dictionary (plotDict) 
    that can be plotted or printed as needed.

    The function loops through the provided questions (questionDict) and courses (courseList) and stores 
    the mean, standard error, and number of students
    """
    
    # Initializing the dictionary
    plotDict = collections.OrderedDict()
    for u in questionDict.keys():
        plotDict[u] = {}

    # Filling the dictionary with mean, sem, N
    for x,y in questionDict.iteritems():
        for c in courseList:
            currD = allData[allData['Course']==c]        

            # Screening for empty numbers/blanks, to prevent nans
            testDat = currD[x]
            testDat = testDat[numpy.isfinite(testDat)]

            # Calculating and storing the mean, sem, and N for the dataset
            m = round(scipy.stats.nanmean(testDat),2)
            s = round(scipy.stats.sem(testDat),2)
            n = len(testDat)
            plotDict[x].update({c:[m,s,n]})
            
    return plotDict

def arrowPlotData(plotDict,
                  desiredCourses,
                  questionDictKeys,
                  delta = None):

    """
    Purpose: This function takes a ready-made dictionary (plotDict), and the courses of interest 
    (desiredCourses), and the questions of interest (questionDictKeys), and returns two dictionaries 
    that can be provided to arrowPlot to construct the arrowPlot

    The delta flag allows you to create an arrow plot with the second course data subtracted from the first course.
    """

    if delta is True:
        assert len(desiredCourses) == 2, 'Please make sure a pair of courses is provided'
        
        mean = []

        for q in questionDictKeys:        
            mean.append(plotDict[q][desiredCourses[1]][0] -\
                        plotDict[q][desiredCourses[0]][0])
            
        return {'mean':mean}

    else:
        # Initializing the dictionaries
        plotGenerator = collections.OrderedDict()
        plotGeneratorErr = collections.OrderedDict()

        for u in desiredCourses:
            plotGenerator[u] = []
            plotGeneratorErr[u] = []

        # Mean and SEM in the same dictionary 
        stats = {}

        for c in desiredCourses:
            for q in questionDictKeys:        
                plotGenerator[c].append(plotDict[q][c][0])
                plotGeneratorErr[c].append(plotDict[q][c][1])

            # This syntax is a bit confusing, but it's worth doing it this way
            # This is a dictionary of dictionaries
            # The top level dictionary has keys corresponding to courses
            # the next level dictionary has keys corresponding to mean or SEM
            # the values of this dictionary is a list of means and SEMs

            stats.update({c:{'mean':plotGenerator[c]}})
            stats[c].update({'sem':plotGeneratorErr[c]})

        return stats



def studentsInBoth(allData,
                   desiredCourses,
                   question,
                   raw = False):        
    """
    Purpose: This function takes a complete dataFrame (allData), courses of interest (desiredCourses), 
    and a single question (questionValue) to return the list of students in both courses 
    """
    assert len(desiredCourses) == 2, 'Please make sure a pair of courses is provided'
    
    tmp = []
    
    # Populate tmp
    for c in desiredCourses:
        currD = allData[allData['Course']==c]        

        # Screening for empty numbers/blanks, to prevent nans
        testDat = currD[question]
        testDat = testDat[numpy.isfinite(testDat)]

        tmp.append(testDat)
    
    # Find students that exist in both pre and post tests    

    preStudents = list(tmp[0].index)
    postStudents = list(tmp[1].index)
    
    # Get the ones that exist in both
    prePostStudents = list(set(preStudents) & set(postStudents))

    # Return the tmp list (required for IndividualStudents function below)
    if raw:
        return prePostStudents, tmp

    else:
        return prePostStudents


def individualStudents(allData,
                       desiredCourses,
                       question,
                       rawData = False):

    """
    Purpose: This function takes a complete dataFrame (allData), courses of interest (desiredCourses), 
    and a single question (questionValue) to return the difference between invidual students as a dictionary

    Notably, the function checks and uses only students that are present in both courses. 
    At this stage, the differences are all provided and the dictionary keys are the pair of values 
    '[-1.0, 1.0]' with the first value from the first course in desiredCourses and the second value from the 
    second course in desiredCourses (i.e. Post - Pre)
    """
    # Get the students in both courses using the helper function
    prePostStudents,tmp = studentsInBoth(allData,desiredCourses,question,raw=True)
    
    # Initialize the comparisons dict
    comparisons = {}

    for i in prePostStudents:
        comparisons[i] = []
        
    # Get the comparisons and store them 

    for s,pre,post in zip(list(tmp[0].index),list(tmp[0]),list(tmp[1])):

        comparisons[s] = [pre,post]

    if rawData:
        return comparisons

    else:
        
        # Find out the number of students doing one thing or another
        diff = defaultdict(int)
        for l in comparisons.values():
            diff[str(l)] += 1    

    return diff

def collapseChanges(result):
    
    inc = 0
    dec = 0
    sm = 0

    for k,v in result.iteritems():
        
        # Convert the ridiculous string into a list of ints

        if len(k) > 3 : # This is to avoid messages for blank values
            try:
                st = k[1:-1].split(',')
                k = [float(it) for it in st]

            except ValueError:
                print('The key you are using: ({0}) is invalid'.format(k))
                raise
                
            else:
                # Check to see if the differences are increasing, decreasing or staying the same 
                if k[1] - k[0] > 0:
                    inc+=v
                elif k[1] - k[0] < 0:
                    dec+=v 
                elif k[1] - k[0] == 0:
                    sm+=v

    return {'Increase':inc,
            'Decrease':dec,
            'Same':sm}    