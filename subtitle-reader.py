import re
import os, glob

class SubtitleReader:
    # Constructor
    # Inputs: None
    # Sets self.intensifiers to a list of intensifiers
    # ASSUMPTION: intensifiers in the file are separated by newlines
    def __init__(self, filename = None):
        self.intensifiers = []

        # If filename is given, initialize with that file:
        if filename == None:
            file, filename = self.loop_file_input()
        else:
            file = open(filename, 'r')

        # Open file and read intensifiers into list
        intensifier_list = file.read().split('\n')
        intensifier_regex = r'(' + r'|'.join(intensifier_list) + r')'
        self.intensifiers = re.compile(intensifier_regex, re.IGNORECASE)

        # ALWAYS CLOSE THE FILE!
        file.close()
    
    def loop_file_input(self):
        working_file = False
        while (working_file == False):
            # Inputs:
            filename = input("Enter filename: ")
            if filename.lower() == "q" or filename.lower() == "quit":
                        exit(0)
            # Try out the file:
            try:
                file = open(filename, 'r')
                working_file = True
            except:
                print("File not found")
        return file, filename
         

    # Read the subtitles from a file and write the paragraphs with intensifiers to a new file
    def read_subtitles(self, filename = None, output_path = None):
        # Read from this file:
        read_file = None
        if filename == None:
            read_file, filename = self.loop_file_input()
        else:
            read_file = open(filename, 'r')

        # Write to this file:
        if output_path != None:
            write_name = output_path + filename.split("\\")[-1] + '.out'
        else:
            write_name = filename + '.out'
        write_file = open(write_name, 'w')
        
        # Use regular expressions to break this file into <p ... </p> tags
        prargraph_regex = re.compile(r'<p.*?</p>', re.DOTALL)
        intra_paragraph_regex = re.compile(r'>.*?</p>', re.DOTALL)
        
        all_paragraphs = prargraph_regex.findall(read_file.read())
        for paragraph in all_paragraphs:
            # Check regex to see if there is an intensifier in this paragraph. 
            # Write the whole paragraph to the file if so.
            intensifiers = self.intensifiers.findall(paragraph)
            if (len(intensifiers) > 0):
                # Write the times:
                beginning, ending = self.xml_time_to_readable(paragraph)
                write_file.write(beginning + " --> " + ending + "\n")
                # Write the words said in the subtitle:
                write_file.write(intra_paragraph_regex.findall(paragraph)[0][1:-4])
                write_file.write("\n\n")

        # ALWAYS CLOSE THE FILES
        read_file.close()
        write_file.close()

    # Convert the time in the xml file to a readable time
    def xml_time_to_readable(self, ms_string, tick_rate = 10000000):
        beginning_regex = re.compile(r'begin=".*?"', re.DOTALL)
        ending_regex = re.compile(r'end=".*?"', re.DOTALL)
        inside_regex = re.compile(r'".*?"', re.DOTALL)
        # Get our beginning and ending times as strings of 'begin="_____t"' and 'end="_____t"'
        beginning = beginning_regex.findall(ms_string)[0]
        ending = ending_regex.findall(ms_string)[0]
        # Get the times as strings of '_____' by themselves
        beginning = inside_regex.findall(beginning)[0][1:-2]
        ending = inside_regex.findall(ending)[0][1:-2]
        # Convert them into integer values, and then into seconds
        # The last 6 digits are decimals:
        beginning = int(beginning) // tick_rate
        ending = int(ending) // tick_rate
        # Convert into seconds, minutes, hours | Format: HH:MM:SS
        beginning = str(beginning // 3600) + ":" + str((beginning // 60) % 60) + ":" + str(beginning % 60)
        ending = str(ending // 3600) + ":" + str((ending // 60) % 60) + ":" + str(ending % 60)

        # We're done, return the strings
        return beginning, ending
    
    def read_all_in_folder(self, input_path = None, output_path = None):
        if (input_path == None):
            input_path = input("Enter folder name: ")
        
        # Get all the files in the folder
        for filename in glob.glob(os.path.join(input_path, '*.xml')):
            self.read_subtitles(filename, output_path = output_path)


# ACTUAL MAIN FUNCTION
def main():
    reader = SubtitleReader(filename = 'intensifiers.txt')
    # reader.read_subtitles()
    reader.read_all_in_folder(input_path = "./input-files/", output_path = "./output-files/")

if __name__ == "__main__":
    main()
