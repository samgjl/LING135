import re
import os, glob

class SubtitleReader:
    # Constructor
    # Inputs: None
    # Sets self.targets to a list of targets
    # ASSUMPTION: targets in the file are separated by newlines
    def __init__(self, filename = None):
        self.targets = []
        self.set_targets(filename)


    def set_targets(self, filename):
        # If filename is given, initialize with that file:
        if filename == None:
            file, filename = self.loop_file_input()
        else:
            file = open(filename, 'r')
        
        self.target_name = filename[0:-4].upper()
        # Open file and read targets into list
        target_list = [target for target in file.read().split('\n') if target != ''] # remove empty strings
        # ensure that the targets are separated by word boundaries
        target_list = [r'\b' + target.lower() + r'\b|' for target in target_list]
        # combine the targets into a single regex
        target_regex = r'(' + r''.join(target_list)
        target_regex = target_regex[0:-1] + r')' # remove the last '|'
        self.targets = re.compile(target_regex, re.IGNORECASE) # compile.

        # ALWAYS CLOSE THE FILE
        file.close()
    
    # Loop until a valid file is given
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
         

    # Read the subtitles from a file and write the paragraphs with targets to a new file
    def read_subtitles(self, filename = None, output_path = None, time_in_ms = False, verbose = False):
        target_totals = {}
        output = ""
        # Read from this file:
        read_file = None
        if filename == None:
            read_file, filename = self.loop_file_input()
        else:
            read_file = open(filename, 'r')

        # Write to this file:
        if output_path != None:
            write_name = output_path + filename.split("\\")[-1][0:-4] + '.' + self.target_name.lower()
        else:
            write_name = filename[0:-4] + '.' + self.target_name.lower()
        write_file = open(write_name, 'w')
        
        # Use regular expressions to break this file into <p ... </p> tags
        prargraph_regex = re.compile(r'<p.*?</p>', re.DOTALL)
        intra_paragraph_regex = re.compile(r'>.*?</p>', re.DOTALL)
        
        all_paragraphs = prargraph_regex.findall(read_file.read())
        for paragraph in all_paragraphs:
            # Check regex to see if there is an target in this paragraph. 
            # Write the whole paragraph to the file if so.
            targets = self.targets.findall(paragraph, re.IGNORECASE)
            if (len(targets) > 0):
                # Update dictionary of targets:
                for target in targets:
                    # if target in target_totals:
                    target = target.lower()
                    target_totals[target] = target_totals[target] + 1 if target in target_totals else 1

                # Convert the times:
                beginning, ending = self.xml_time_to_readable(paragraph, time_in_ms = time_in_ms)

                # Write the words said in the subtitle:
                intra_paragraph = re.sub(r"\n", "", "" + intra_paragraph_regex.findall(paragraph)[0][1:-4])
                intra_paragraph = re.sub(r"<br/>", "\n  ", "  " + intra_paragraph)
                intra_paragraph = re.sub(r"&quot;", '"', intra_paragraph)
                intra_paragraph = re.sub(r"<.*?>", "", intra_paragraph)

                # Add to the output:
                output += beginning + " --> " + ending + "\n" # Title: timing
                if (verbose):
                    output += "  " + self.target_name + ": " + str(targets) + "\n" # targets found
                output += intra_paragraph + "\n\n" # word context
        
        # Write everything to the file:
        if (verbose):
            write_file.write("----- TOTALS -----\n")
            for target in target_totals:
                write_file.write(f"  '{target}' : {str(target_totals[target])}\n")
            write_file.write("\n")
        write_file.write("----- TIME STAMPS -----\n\n" + output)
        # ALWAYS CLOSE THE FILES
        read_file.close()
        write_file.close()

    # Convert the time in the xml file to a readable time
    def xml_time_to_readable(self, ms_string, tick_rate = 10000000, time_in_ms = False):
        beginning_regex = re.compile(r'begin=".*?"', re.DOTALL)
        ending_regex = re.compile(r'end=".*?"', re.DOTALL)
        inside_regex = re.compile(r'".*?"', re.DOTALL)
        # Get our beginning and ending times as strings of 'begin="_____t"' and 'end="_____t"'
        beginning = beginning_regex.findall(ms_string)[0]
        ending = ending_regex.findall(ms_string)[0]
        # Get the times as strings of '_____' by themselves
        beginning = inside_regex.findall(beginning)[0][1:-2]
        ending = inside_regex.findall(ending)[0][1:-2]

        # If our time format is already pretty, we're done!
        if (not time_in_ms):
            return beginning, ending
        
        # Convert them into integer values, and then into seconds
        # The last 6 digits are decimals:
        beginning = int(beginning) // tick_rate
        ending = int(ending) // tick_rate
        # Convert into seconds, minutes, hours | Format: HH:MM:SS
        beginning = str(beginning // 3600) + ":" + str((beginning // 60) % 60) + ":" + str(beginning % 60)
        ending = str(ending // 3600) + ":" + str((ending // 60) % 60) + ":" + str(ending % 60)

        # We're done, return the strings
        return beginning, ending
    
    # Read all the files in a folder
    def read_all_in_folder(self, input_path = None, output_path = None, time_in_ms = False, verbose = False):
        if (input_path == None):
            input_path = input("Enter folder name: ")
        
        # Get all the files in the folder
        for filename in glob.glob(os.path.join(input_path, '*.xml')):
            self.read_subtitles(filename, output_path = output_path, time_in_ms = time_in_ms, verbose = verbose)