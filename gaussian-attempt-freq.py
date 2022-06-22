#!/Users/steven/opt/anaconda3/bin/python3

####################################################################################################
# This code is for working with Gaussian files.
# Steven R. Schofield, University College London, June 2022
####################################################################################################

# Load required packages
import sys
import numpy as np
import pandas as pd
import os

# load main functions
import SRSGaussian as gaus


######################################################################################################
# Begin Programme
######################################################################################################

# Display programme start message.
gaus.startscript()

if len(sys.argv) != 3:
    print("Error, expecting two input filename")
    sys.exit()
    
# Get file name and unit cell multiples from command line options.
file1=str(sys.argv[1])    # filename
file2=str(sys.argv[2])

# remove extension if present
file1 = os.path.splitext(file1)[0]
file2 = os.path.splitext(file2)[0]

# Filename for the new file to be written
outfilename = file1+"_"+file2+"_frequencies"

# Read in frequencies from the .log file file information
freqs1, masses1, forces1 = gaus.readFreq(file1)
freqs2, masses2, forces2 = gaus.readFreq(file2)

# Count the number of negative and positive values
freqs1NegVals = np.sum(np.array(freqs1) < 0, axis=0)
freqs2NegVals = np.sum(np.array(freqs2) < 0, axis=0)
freqs1PosVals = np.sum(np.array(freqs1) >= 0, axis=0)
freqs2PosVals = np.sum(np.array(freqs2) >= 0, axis=0)

# Check if is a TS calculation
freqs1isTS = 'No'
if freqs1[0] < 0 and freqs1NegVals == 1:
    freqs1isTS = 'Yes'

# Check if is a TS calculation
freqs2isTS = 'No'
if freqs2[0] < 0 and freqs2NegVals == 1:
    freqs2isTS = 'Yes'


# convert frequencies in cm^-1 to Hz (not including the 1/2pi term) using the reduced masses and force constants from the gaussian output
newfreqs1 = np.sqrt(forces1 / masses1) / (2 * 29979245800 * 3.14)
newfreqs2 = np.sqrt(forces2/ masses2) / (2 * 29979245800 * 3.14)
print(freqs1)
print()
print(freqs1/newfreqs1)

#Calculate the product of frequencies
freqs1Prod = np.prod(freqs1[freqs1NegVals:freqs1PosVals+freqs1NegVals])
freqs2Prod = np.prod(freqs2[freqs2NegVals:freqs2PosVals+freqs2NegVals])

# Write some output to screen
file1namelen = len(file1)
file2namelen = len(file2)
filenamelen = max(file1namelen,file2namelen)

print()
print('{0:{1}} {2:^17} {3:^17} {4:^17} {5:^17}'.format('File',filenamelen,'Positive values','Negative values','Transition state?','Product of positive frequencies'))
print('{0:{1}} {2:^17} {3:^17} {4:^17} {5:^17}'.format(file1,filenamelen,freqs1PosVals,freqs1NegVals,freqs1isTS,freqs1Prod))
print()

print()
print('{0:{1}} {2:^17} {3:^17} {4:^17} {5:^17}'.format('File',filenamelen,'Positive values','Negative values','Transition state?','Product of positive frequencies'))
print('{0:{1}} {2:^17} {3:^17} {4:^17} {5:^17}'.format(file2,filenamelen,freqs2PosVals,freqs2NegVals,freqs2isTS,freqs2Prod))
print()


attemptFreq = freqs1Prod / freqs2Prod

print('The ratio of the product of frequencies for {0} / {1} is {2:e}'.format(file1,file2,attemptFreq))


