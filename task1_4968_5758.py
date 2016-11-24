import time

filename = 'access_log'

#Description: Get current time
#Parameters: nil
#Return: string
def getTime():
    return time.strftime('%Y-%m-%d %H:%M:%S')

#Description: Add to dictionary
#Parameters: dictionary, string
#Return: string
def addToDict(d,page):
    if d.has_key(page):
        d[page] = d[page] + 1
    else:
        d[page] = 1

    return d

#Description: Get most visited page in dictionary
#Parameters: dictionary
#Return: tuple (page,count)
def getMostVisited(dict):
    page = ''
    largest = 0
    for p in dict:
        num = dict[p]
        if num > largest:
            largest = num
            page = p

    return (page,largest)

print 'Program starting time: ', getTime()

#Variables
count = 0
hitsjs = 0
hitsip = 0
largestbytes = 0
largestpage = ''
pages = {}
with open(filename,'r') as f:
    for line in f:
        count = count + 1

        #Get entry
        entry = line.split()

        #Get page from entry and remove 'http://www.the-associates.co.uk'
        page = entry[6].replace('http://www.the-associates.co.uk','')
        size = entry[9]

        #Check if part of page
        if '/assets/js/the-associates.js' in page:
            hitsjs = hitsjs + 1

        #Check if has ip
        if '10.99.99.186' in entry[0]:
            hitsip = hitsip + 1

        #Check if size is not '-' and if it is larger than current largest
        if size.isdigit() and int(size) > largestbytes:
            largestbytes = int(size)
            largestpage = page

        #Add page to dictionary
        pages = addToDict(pages,page)

    f.close()

#Get most visited page from dicitonary
mostVisited = getMostVisited(pages)

print 'Total entries were ', count
print 'Total hits of \'/assets/js/the-associates.js\' were ', hitsjs
print 'Total hits made by 10.99.99.186 were ', hitsip
print 'The largest page/object was ', largestpage, ' with the size of ', largestbytes, ' bytes'
print 'The highest number of hits was ', mostVisited[1], ' for the page ', mostVisited[0]

print 'Program completed time: ', getTime()
