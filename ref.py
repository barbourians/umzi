import sys
import time

# --------------------------------------------------------
# Get the filename as an input parameter
# --------------------------------------------------------
inputfiledir = 'c:\\python\\data\\umzi'
inputfiledir+='\\'
inputfilename = r''
inputfilename+=inputfiledir
inputfilename+='mptest'
inputfilename+='.txt'

# --------------------------------------------------------
# Open the input file
# --------------------------------------------------------
fin = open(inputfilename, 'r')

# --------------------------------------------------------
# Initialise all the variables
# --------------------------------------------------------
vBiblio = 0
vChapter = 0
vChapterTxt = ''
vError = 0
vLine = ''
vLineCount = 0
vOutput = ''
vPage = 0
vRefAuthor1 = ''
vRefFull = ''
vRefPage =''
vRefShort = ''
vRefYear = ''
vRev = ''
vShowBiblio = None

# --------------------------------------------------------
# Loop through the file to find the references
# --------------------------------------------------------
while 1:
    line=fin.readline() # check for EOF
    if not line: break
    
    vLine = line.strip()
    # Extract the page number if present
    if vLine[0:5] == 'Page ' and vLine.count(' of ') > 0: 
        vPage = vLine[5:vLine.find(' of ')]
        continue
    
    # If Reference section is reached then output the references
    if vLine[0:12] == '@@References':
        vShowBiblio = True;
        print ('--------------------------------------------------')
        print ('References')
        print ('==================================================')
        continue
    
    # If Appendix is reached then don't process references
    if vLine[0:10] == '@@Appendix':
        vShowBiblio = False;
        continue

    if vShowBiblio:
        vBiblio+=1

        # Store the full reference up to "Avalable online"
        vRefFull = vLine[0:vLine.find('Available online')]
        
        # Find the year by looking for the first open bracket plus a 2
        i = vLine.find('(2')
        # If year doesn't start with 2 then look for start with 1
        if i == -1: i = vLine.find('(1')

        # If year not found then show error
        if i == -1:
            vError+=1
            print ('### Error: Reference has no valid year', vLine)
            continue
        
        # Store the reference year
        vRefYear = vLine[i+1:i+5]

        # Authors list is up to the first open bracket
        i = vLine.find('(')
        # If no open bracket then show error
        if not i > 0:
            vError+=1
            print ('### Error: Reference has no year', vLine)
            continue
        
        # Extract the Author list
        vRefShort = vLine[0:i]
        
        # Extract the first Author
        vRefAuthor1 = vRefShort
        if vRefAuthor1.find(',') > 0:
            vRefAuthor1 = vRefAuthor1[0:vRefAuthor1.find(',')]
        if vRefAuthor1.find('.') > 0:
            vRefAuthor1 = vRefAuthor1[0:vRefAuthor1.find('.')]
        if vRefAuthor1.find('(') > 0:
            vRefAuthor1 = vRefAuthor1[0:vRefAuthor1.find('(')]

        # Trim the spaces
        vRefAuthor1 = vRefAuthor1.strip()
                
        print (vRefYear, vRefAuthor1,'~',vRefShort)
        continue
    
# End while

# Print reference count
print ('--------------------------------------------------')
print ('There are',str(vBiblio),'References')
print ('==================================================')

# Print error count
if vError > 0:
    print ('##################################################')
    print ('There are',str(vError),'ERROR LINES. Please fix!')
    print ('##################################################')
    
# --------------------------------------------------------
# Close the input file
# --------------------------------------------------------
fin.close()
