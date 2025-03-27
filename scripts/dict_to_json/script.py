__author__="Otis Carmichael"

import json
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
    words_list = []
    repeat_word_count = 1
    sense_num = 0

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
        # print("Current: " + currentLine + "   Next: " + nextLine)
        # Appends the id at the start of the word. 
        if(type_ == '\\lx'):
            if (chunks[1].strip().lower() in words_list):
                repeat_word_count += 1
                id_ = chunks[1].strip().lower() + str(repeat_word_count)
            else: 
                id_ = chunks[1].strip().lower()
                repeated_type = ""
                repeat_word_count = 1
            # Handles the case of finishing the sense object
            if (sense_num > 0):
                currentFile.append("\n\t}\n]")
            currentFile.append("\n},\n{\n")
            currentFile.append("\t\"id\": \"" + id_ + "\"") 
            words_list.append(id_)
            sense_num = 0
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
        # Cases for sense numbers
        elif(type_ == '\\sn'):
            try:
                sense_num = int(chunks[1].strip())
                if (sense_num <= 1):
                    currentFile.append(",\n\t\"senses\": [")
                    currentFile.append("\n\t\t")
                else:
                    currentFile.append("},\n")
                currentFile.append("{\n\t\t\"" + types.get(type_) + "\": " + "\"" + chunks[1] + "\"")
            except ValueError:
                print("Bad sense number: " + chunks[1].strip())
                sense_num = 0
        # Creates example object that stores examples
        elif(type_ == '\\xv'):
            if (example_count <= 1):
                currentFile.append(",\n\t\"examples\": [")
            else:
                currentFile.append(",")
            currentFile.append("\n\t\t"  + "{\n\t\t\t\"Example\": " + str(example_count) + ",")
            example_count += 1
            currentFile.append("\n\t\t\"" + types.get(type_) + "\": " + "\"" + chunks[1] + "\",")
            # Handles the case where the next line is not an example, thus finishing the example object
            if (nextLineType not in ['\\xv', '\\xe', '\\rf', '\\sfx']):
                currentFile.append("\n\t\t]")
                example_count = 1
        elif(type_ in ['\\xe', '\\rf', '\\sfx']):
            currentFile.append("\n\t\t\t\"" + types.get(type_) + "\": " + "\"" + chunks[1] + "\"")
            
            if (nextLineType == "\\xv" or nextLineType not in ['\\xe', '\\rf', '\\sfx']):
                currentFile.append("\n\t\t}")
            else:
                currentFile.append(",")
            # Handles the case where the next line is not an example, thus finishing the example object
            if (nextLineType not in ['\\xv', '\\xe', '\\rf', '\\sfx']):
                currentFile.append("\n\t\t]")
                example_count = 1
        # Default
        else: 
            currentFile.append(",\n\t\t\"" + types.get(type_) + "\": " + "\"" + chunks[1] + "\"")

            
    # For using json prettifier eventually
    # json_lines = ""
    # for line in currentFile:
    #     json_lines += line
    # json_lines += "\n\t}\n]\n}"
    # json_object = json.loads(json_lines)
    # json_formatted_str = json.dumps(json_object, indent=2)
    # newFile.write(json_formatted_str)
    
    for line in currentFile:
        newFile.write(line)
    newFile.write('\n}\n]')
    
    newFile.close()



if __name__ == '__main__':
    import sys
    import hashlib
    from pathlib import Path
    convert_to_jsonld()
