#CURRENT TESTING VERSION
#If the regulation is paragraph based instead of bullet points, count by keyword
#Otherwise, adds each bullet point or line as a count to the regulation
#When a ":" is found, it counts that line as a preamble, gets the format and counts the number of regulation keywords
#After the preamble, counts the lines afterwards it pertains to (which are a different format)
#When the format is changed back to normal, it multiplies the keywords in the preamble by the bullet points it pertains to
import re
import nltk
import os
#|\d\d?-\d\d?-\d\d?-\d\d?\. is purely for North Dakota
pattern = re.compile(r"\(.{1,4}\)|^.\.|;$|\d\d?-\d\d?-\d\d?-\d\d?\.", re.MULTILINE)
regulationKeyword = re.compile(r"must|may not|required|prohibited|shall", re.IGNORECASE)
filePath = "sentences.txt"

def getFormat(str):
    #(i) (ii) format
    if re.search(r"\(i{1,4}\)", str, re.IGNORECASE):
        return r"\(i{1,4}\)"
    #(a) (b) format
    elif re.search(r"\(\D{1,2}\)", str, re.IGNORECASE):
        return r"\(\D{1,2}\)"
    #(1) (2) format
    elif re.search(r"\(\d{1,2}\)", str, re.IGNORECASE):
        return r"\(\d{1,2}\)"
    #starts with i. ii. format
    elif re.search(r"^i{1,4}", str, re.IGNORECASE):
        return r"^i{1,4}"
    #starts with a. b. format
    elif re.search(r"^\D{1,2}\.", str, re.IGNORECASE):
        return r"^\D{1,2}\."
    #starts with 1. 2. format
    elif re.search(r"\d{1,2}\.", str, re.IGNORECASE):
        return r"\d{1,2}\."
    #No format i.e. paragraph/anything
    else:
        return r"."
    
count = 0
tempCount = 0
regulationCount = 0
inParagraph = False
format = False
#Check if it had formatting. If none, count keywords instead
with open(filePath, "r", encoding="utf8") as f:
    text = f.read()
    if not pattern.search(text):
        matches = regulationKeyword.findall(text)
        count = len(matches)
        print(str(count) + " No format found")
#If it has formatting, run this
if count is 0:
    with open(filePath, "r", encoding="utf8") as f:
        for line in f :
            if format is not False and re.search(format, line, re.MULTILINE):
                #Consider whether or not to set regulationCount to 1 when 0 or leave it as 0
                print(format)
                if regulationCount is 0:
                    regulationCount = 1
                if tempCount is 0:
                    tempCount = 1
                #Multiplies number of keywords found in the preamble by the number of items found in the list and adds it to count
                print (str(tempCount) + " " + str(regulationCount))
                count += tempCount * regulationCount
                regulationCount = 0
                tempCount = 0
                format = False
            #If it ends in a ":" it is a preamble
            if line.endswith(":\n") or line.endswith(": \n"):
                #Gets the format and counts number of regulation keywords
                format = getFormat(line)
                print(format)
                for word in line.split():
                    if regulationKeyword.search(word):
                        regulationCount += 1
            #If a non-preamble list spot, adds count to the total or to be multiplied
            elif pattern.search(line) and ":" not in line :
                if format is False:
                    count += 1
                else:
                    tempCount += 1
    #If leftover tempCount + regulationCount, add them
    if regulationCount is not 0 or tempCount is not 0:
        if regulationCount is 0:
            regulationCount = 1
        if tempCount is 0:
            tempCount = 1
        count += tempCount * regulationCount
    print(count)