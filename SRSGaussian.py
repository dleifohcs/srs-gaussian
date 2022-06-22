#!/Users/steven/opt/anaconda3/bin/python3

####################################################################################################
# This code is for working with GAUSSIAN files.
# Steven R. Schofield, University College London, June 2022
# GNU General Public License v3.0
####################################################################################################

####################################################################################################
# This provides a header output when the programme starts
####################################################################################################
def startscript():
  print("Gaussian tools *******************************************************************************")
  print("Steven R. Schofield, University College London (June 2022, GNU General Public License v3.0)")

####################################################################################################
# Reads the frequencies and reduced masses from a gaussian .log file
####################################################################################################
def readFreq(name):
  import numpy as np
  
  # add the .param extension
  filename = name + ".log"
  
  # Output to screen
  print()
  print("Opening "+ filename+" for reading.")

  # Open file
  myfile = open(filename, "r")

  # Make list to store the frequencies and masses  in
  freqList = []
  massList = []
  forceList = []
  
  # Loop over the lines of the input file
  for line in myfile:
    words = line.split()
    if len(words) > 0 and words[0] == "Frequencies":
      freqList.append(float(words[2]))
      freqList.append(float(words[3]))
      freqList.append(float(words[4]))
    if len(words) > 0 and words[0] == "Red." and words[1] == "masses":
      massList.append(float(words[3]))
      massList.append(float(words[4]))
      massList.append(float(words[5]))
    if len(words) > 0 and words[0] == "Frc" and words[1] == "consts":
      forceList.append(float(words[3]))
      forceList.append(float(words[4]))
      forceList.append(float(words[5]))
      
  freqs = np.array(freqList)
  masses = np.array(massList)
  forces = np.array(forceList)

  print("DONE")
  
  # Close file
  myfile.close()
  return freqs, masses, forces
