import time
import crypt
from itertools import permutations

filename = 'shadow.txt'

#Description: Get current time
#Parameters: nil
#Return: string
def getTime():
    return time.strftime('%Y-%m-%d %H:%M:%S')

#Description: Get passwords
#Parameters: dictionary
#Return: dicitonary
def findPasswords(users):
    d = {}

    #Generate number 0 to 9
    numbers = [str(i) for i in range(0,10)]

    #Generate all possible permutations, account for starting with 0
    perms = [''.join(p) for i in range(0,7) for p in permutations(numbers,i)]
    for p in perms:
        #Loop through dicitonary
        for u in dict(users):
            #Get salt form hash and hash current p
            passhash = users[u]
            salt = passhash[0:12]
            c = crypt.crypt(p, salt)

            #Check if user hash is same as generated hash
            if passhash == c:
                #Same, put in return dictionary and remove from users dicitonary
                d[u] = p
                del users[u]

        #Check if dictionary is empty
        if not users:
            break

    return d

print 'Program starting time: ', getTime()

#Variables
users = {}

with open(filename,'r') as f:
    for line in f:
        #Split line into entries
        entry = line.split(':')

        #Entries
        u = entry[0]
        pw = entry[1]

        #Put in dictionary
        users[u] = pw

    f.close()

#Get passwords
users = findPasswords(users)
for u in users:
    print 'password of user ', u, ' is ', users[u]

print 'Program completed time: ', getTime()
