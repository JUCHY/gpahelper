# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 00:35:15 2018

@author: Juchen
"""

try:
    newfile = open('datafile.txt','r')
    stringfile = newfile.read()
    newfile.close()
 # TODO: write code...
except:
    stringfile = ''
 # TODO: write code...
else:
    grades = stringfile.split('\n')
    listoflists = []
    listoflists.append(grades[0])
    for x in grades[1:]:
        replist = x.split('\t')
        listoflists.append(replist)
class data:
    global cumGPA
    global personGPA
    cumGPA = float(listoflists[0])
    personGPA = str(cumGPA)
def calculategpa():
    global cumGPA
    global personGPA
    gradesum = 0
    counter = 0
    for x in listoflists[1:]:
        gpa = float(x[1])
        gradesum += gpa
        counter += 1
    average = gradesum/counter
    listoflists[0] = average
    cumGPA = average
    personGPA = str(cumGPA)
def addclass(classname, classgpa):
    listtoappend = [classname,classgpa]
    listoflists.append(listtoappend)
def removeclass(classname):
    i = 1
    traverse = len(listoflists)
    while i < traverse:
        someword = listoflists[i]
        if someword[0] == classname:
            del listoflists[i]
            i -= 1
            traverse -=1
        i+=1
def savefunction():
    somefile = open('datafile.txt','w')
    counter = 0
    for x in listoflists:
        if len(x)==2:
            if counter == len(listoflists)-1:
                somefile.write(str(x[0])+'\t'+str(x[1]))
                counter += 1
            else:
                somefile.write(str(x[0])+'\t'+str(x[1])+'\n')
                counter += 1                
        else:
            somefile.write(str(x)+'\n')
            counter += 1
    somefile.close()