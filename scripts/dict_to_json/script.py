__author__="Otis Carmichael"

jsonld = dict

# Dictionary to map these codes to meaning
types = {
    r'\lx': 'Word',
    r'\mr': 'Morphemic_Analysis',
    r'\hm': 'Homonym_Number',
    r'\sv': '',
    r'\sf': 'Word_Sound', # Link to Audio File
    r'\sn': 'Sense_Number', # Start of Repeatable Block for Each Sense
    r'\ps': 'Part_of_Speech', # E.g. noun/verb etc.
    r'\pc': 'Image', # Link to Image
    r'\sy': 'Synonyms',
    r'\sd': 'Sense_Domain',
    r'\la': 'Latin_Name', # For Flora/Fauna
    r'\lt': 'Definition', # Followed by :
    r'\ge': 'English_Gloss', # English Translation
    r'\re': 'Reversal_Forms', # USE VALUES IN \ge for reversal
    r'\so': 'Source', # Speaker
    r'\xv': 'Vernacular_Example',
    r'\sfx': 'Audio_of_Example',
    r'\xe': 'English_Vernacular_Translation',
    r'\rf': 'Source_of_Vernacular',
    r'\va': 'Alternate_Pronunciation', # Alternate Phonological Forms
    r'\cf': 'See_Also', # Semantically Related Form
    r'\an': 'Antonym',
    r'\nt': 'Note', # Additional Information
    r'\cp': 'Comparative_Notes', # Relating to Other Languages
    r'\nq': 'Compiler_Notes', 
    r'\dt': 'Date',
    r'\lf': 'Derived_Works' # Words Morphologically Related to Head Word
}

def convert_to_jsonld():
    example_count = 1
    repeated_type = ""

    # Open the backslash word file and saves the lines
    file = open("scripts/dict_to_json/test.txt", "r")
    lines = file.readlines()
    file.close()
    print("lines read")

    path = Path().joinpath(Path('scripts/dict_to_json/waanyi' + '.json'))
    newFile = open(path, "w")

    currentFile = []
    currentFile.append('[{\n')

    nextLine = ""
    for line in lines:
        currentLine = nextLine
        nextLine = line.strip()

        if len(currentLine) < 0:
            print(f"-- [{file}] skipped currentLine. {currentLine}", file=sys.stderr)
            continue
        chunks = currentLine.split(" ", 1)
        if len(chunks) < 2:
            print(f"-- [{file}] skipped currentLine. {currentLine}", file=sys.stderr)
            continue
        type_ = chunks[0].strip()
        nextLineType = nextLine.split(" ", 1)[0].strip()
        if not 3 <= len(type_) <= 4:
            print(f"-- [{file}] bad extraction of type: {type_} {len(type_)}")
        if type_ not in types:
            print(f"-- [{file}] invalid type: {type_}")
            continue
        # Maybe need to set nextLineType here to avoid bad order
        print("Current: " + currentLine + "   Next: " + nextLine)
        # Appends the id at the start of the word. 
        if(type_ == '\\lx'):
            id_ = chunks[1].strip()
            currentFile.append("\n},\n{\n")
            currentFile.append("\t\"@id\": \"" + id_ + "\"") 
            example_count = 1
            repeated_type = ""
        # Handles repetitions by adding them to a list
        if(type_ == nextLineType and type_ != repeated_type):
            currentFile.append(",\n\t\t\"" + types.get(type_) + "\": " + "[\"" + chunks[1] + "\"")
            repeated_type = type_
        elif(type_ == repeated_type):
            currentFile.append(", \"" + chunks[1] + "\"")
            if(nextLineType != repeated_type):
                currentFile.append("]")
        # Creates example object that stores examples
        elif(type_ == '\\xv'):
            currentFile.append(",\n\t\"Example_" + str(example_count) + "\": {")
            example_count += 1
            currentFile.append("\n\t\t\"" + types.get(type_) + "\": " + "\"" + chunks[1] + "\",")
        elif(type_ in ['\\xe', '\\rf', '\\sfx']):
            currentFile.append("\n\t\t\"" + types.get(type_) + "\": " + "\"" + chunks[1] + "\"")
            
            currentFile.append("\n\t\t}") if (nextLineType == "\\xv" or nextLineType not in ['\\xe', '\\rf']) else currentFile.append(",")
        # Default
        else: 
            currentFile.append(",\n\t\"" + types.get(type_) + "\": " + "\"" + chunks[1] + "\"")

            

    
    # Do I need to iterate through the currentWord list?
    for line in currentFile:
        newFile.write(line)
    newFile.write('\n}\n]')

    #newFile.write("\n\t\t}\n\t]\n}")
    newFile.close()



if __name__ == '__main__':
    import sys
    import hashlib
    from pathlib import Path
    convert_to_jsonld()
