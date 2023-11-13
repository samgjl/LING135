import re, json
import os, glob

class DataParser:
    def __init__(self, men = [], women = []):
        self.use_gender = False
        if (men != [] and women != []):
            self.men = men
            self.women = women
            self.use_gender = True

    def parse(self, file_path, men = [], women = [], output_path = "output.csv"):
        # Reas the file:
        file = open(file_path, 'r')
        data = file.read()
        file.close()
        
        # Split the data:
        data = data.split('\n')
        data = [x.split(',')[1:] for x in data] # remove the first column (time)

        # Parse:
        words_totals = {}
        words_by_cast = {}
        words_by_gender = {"Men" : {"Interview" : 0,
                                     "Public" : 0,
                                     "Total" : 0},
                           "Women" : {"Interview" : 0,
                                       "Public" : 0,
                                       "Total" : 0},
                            "Total": {}
                           }
        useless_data_points = 0
        intensifiers_by_gender = {
            "Men" : {
                        "so" : 0,
                        "very" : 0, 
                        "really" : 0,
                    },
            "Women" : {
                        "so" : 0,
                        "very" : 0, 
                        "really" : 0,
                    },
        }

        for line in data:
            # If the data is unfilled / 'N/A' was entered:
            if (line[1][0] == 'N'):
                useless_data_points += 1
                continue
            
            # Data sorting:
            word = "".join([char if char.isalpha() else "" for char in line[0].lower()])
            contestant = line[1]
            interview = line[2]

            # Totals over words:
            if (word not in words_totals):
                words_totals[word] = {
                    'Total' : 0,
                    "Interview" : 0,
                    "Public" : 0
                    }
            words_totals[word]['Total'] += 1
            if (interview[0].lower() == 'y'):
                words_totals[word]['Interview'] += 1
            else:
                words_totals[word]['Public'] += 1
            
            # Totals over each contestant:
            if (contestant not in words_by_cast):
                words_by_cast[contestant] = {
                    'Total': 0,
                    'Interview': 0,
                    'Public': 0
                    }
            if (word not in words_by_cast[contestant]):
                words_by_cast[contestant][word] = 0
            words_by_cast[contestant][word] += 1
            words_by_cast[contestant]['Total'] += 1
            if (interview[0].lower() == 'y'):
                words_by_cast[contestant]['Interview'] += 1
            else:
                words_by_cast[contestant]['Public'] += 1


        # Gendered intensifiers by intensifier:
        
        # Gendered totals:
        if (self.use_gender):
            man_regex = re.compile(r'm.n', re.IGNORECASE)
            woman_regex = re.compile(r'wom.n', re.IGNORECASE)
            for person in words_by_cast:
                if (person in self.men or len(man_regex.findall(person)) > 0):
                    # gendered contexts:
                    words_by_gender["Men"]['Interview'] += words_by_cast[person]['Interview']
                    words_by_gender["Men"]['Public'] += words_by_cast[person]['Public']
                    words_by_gender["Men"]['Total'] += words_by_cast[person]['Total']
                    # Totals:
                    for word in ["so", "very", "really"]:
                        intensifiers_by_gender["Men"][word] += words_by_cast[person][word] if word in words_by_cast[person] else 0  # NOT SUSTAINABLE
                elif (person in self.women or len(woman_regex.findall(person)) > 0):
                    #gendered contexts:
                    words_by_gender['Women']['Interview'] += words_by_cast[person]['Interview']
                    words_by_gender["Women"]["Public"] += words_by_cast[person]['Public']
                    words_by_gender["Women"]["Total"] += words_by_cast[person]['Total']
                    # Totals:
                    for word in ["so", "very", "really"]:
                        intensifiers_by_gender["Women"][word] += words_by_cast[person][word] if word in words_by_cast[person] else 0 # NOT SUSTAINABLE
                else:
                    print("missed", person)
            # Overall totals:
            words_by_gender["Total"]["Total"] = words_by_gender["Men"]["Total"] + words_by_gender["Women"]["Total"]
            words_by_gender["Total"]["Interview"] = words_by_gender["Men"]["Interview"] + words_by_gender["Women"]["Interview"]
            words_by_gender["Total"]["Public"] = words_by_gender["Men"]["Public"] + words_by_gender["Women"]["Public"]          

        self.write_csv(path =                output_path, 
                       words_totals =        words_totals, 
                       words_by_gender =     words_by_gender, 
                       words_by_cast =       words_by_cast)

        file = open(output_path[:-3] + "out", 'w')
        file.write("<words_totals>" + str(words_totals) + "</words_totals>\n")
        file.write("<words_by_cast>" + str(words_by_cast) + "</words_by_cast>\n")
        file.write("<useless_data_points>" + str(useless_data_points) + "</useless_data_points>\n")
        if self.use_gender:
            file.write("<words_by_gender>" + str(words_by_gender) + "</words_by_gender>\n")
            file.write("<intensifier_by_gender>" + str(intensifiers_by_gender) + "</intensifier_by_gender>\n")
        file.close()

    def write_csv(self, path = "output.csv", words_by_cast = {}, words_by_gender = {}, words_totals = {}, useless_data_points = None):
        # WRITING TO FILE
        file = open(path, 'w')

        # Write the totals by word:
        file.write("Word, Interview, Public, Total\n")
        total = 0
        for word in words_totals:
            total += words_totals[word]['Total']
            file.write(" '" + word + "', " +
                       str(words_totals[word]['Interview']) + ", " +
                       str(words_totals[word]['Public']) + ", " +
                       str(words_totals[word]['Total']) + "\n")
        file.write(f'Overall, {total}\n')
        if (useless_data_points != None):
            file.write(f'(unused points), {useless_data_points}\n')
        file.write('\n')

        # Write the totals by cast:
        file.write("Words by Cast Member\n")
        for person in words_by_cast:
            file.write(person + '\n')
            for subkey in words_by_cast[person]:
                if (subkey not in ['Total', 'Public', 'Interview']):
                    file.write(" , " + subkey + ', ' + str(words_by_cast[person][subkey]) + '\n')
            file.write(f" , Interview, {words_by_cast[person]['Interview']}\n" +
                       f" , Public, {words_by_cast[person]['Public']}\n" + 
                       f"Total, {words_by_cast[person]['Total']}\n\n"
                    )
        if (self.use_gender):
            file.write("Totals by Gender\n")
            for gender in words_by_gender:
                file.write(gender + '\n')
                for context in words_by_gender[gender]:
                    file.write(f" , {context}, {words_by_gender[gender][context]}\n")

        file.close()

    def wrangle_all(self, path = ""):
        words_by_totals = []
        overall_totals = {}
        wbt_regex = re.compile(r'<words_totals>.*?</words_totals>', re.DOTALL)
        words_by_cast = []
        overall_cast = {}
        wbc_regex = re.compile(r'<words_by_cast>.*?</words_by_cast>', re.DOTALL)
        words_by_gender = []
        overall_gender = {}
        wbg_regex = re.compile(r'<words_by_gender>.*?</words_by_gender>', re.DOTALL)
        useless_data_points = 0
        useless_regex = re.compile(r'<useless_data_points>.*?</useless_data_points>', re.DOTALL)
        intra = re.compile(r'>.*?<', re.DOTALL)
        int_by_gender = re.compile(r'<intensifier_by_gender>.*?</intensifier_by_gender>', re.DOTALL)
        intensifiers_by_gender = []
        gender_intensifiers = {}

        for filename in glob.glob(os.path.join(path, '*.out')):
            file = open(filename, 'r')
            data = file.read()
            file.close()
            # By totals:
            wbt = intra.findall(wbt_regex.findall(data)[0])[0][1:-1]
            words_by_totals.append(json.loads(wbt.replace("'", '"'))) # Add the dict to the list
            # By cast:
            wbc = intra.findall(wbc_regex.findall(data)[0])[0][1:-1]
            words_by_cast.append(json.loads(wbc.replace("'", '"'))) # Add the dict to the list
            # By gender:
            wbg = intra.findall(wbg_regex.findall(data)[0])[0][1:-1]
            words_by_gender.append(json.loads(wbg.replace("'", '"'))) # Add the dict to the list
            # Useless data points:
            udp = intra.findall(useless_regex.findall(data)[0])[0][1:-1]
            useless_data_points += int(udp)
            # Intensifier types by gender:
            ibg = intra.findall(int_by_gender.findall(data)[0])[0][1:-1]
            intensifiers_by_gender.append(json.loads(ibg.replace("'", '"')))
        
        # Totals:
        for dictionary in words_by_totals:
            # This is a dictionary of words:
            for word in dictionary:
                if (word not in overall_totals):
                    overall_totals[word] = dictionary[word]
                else:
                    for context in dictionary[word]:
                        if (context not in overall_totals[word]):
                            overall_totals[word][context] = dictionary[word][context]
                        else:
                            overall_totals[word][context] += dictionary[word][context]
        
        # Cast:
        for dictionary in words_by_cast:
            # This is a dictionary of cast members:
            for cast_member in dictionary:
                if (cast_member not in overall_cast):
                    overall_cast[cast_member] = dictionary[cast_member]
                else:
                    for context in dictionary[cast_member]:
                        if (context not in overall_cast[cast_member]):
                            overall_cast[cast_member][context] = dictionary[cast_member][context]
                        else:
                            overall_cast[cast_member][context] += dictionary[cast_member][context]
        
        # Gender:
        if self.use_gender:
            for dictionary in words_by_gender:
                for gender in dictionary:
                    if (gender not in overall_gender):
                        overall_gender[gender] = dictionary[gender]
                    else:
                        for context in dictionary[gender]:
                            if (context not in overall_gender[gender]):
                                overall_gender[gender][context] = dictionary[gender][context]
                            else:
                                overall_gender[gender][context] += dictionary[gender][context]

            for dictionary in intensifiers_by_gender: # dictionary of intensifiers
                for gender in dictionary: # Men / Women
                    if (gender not in gender_intensifiers):
                        gender_intensifiers[gender] = dictionary[gender]
                    else:
                        for context in dictionary[gender]: # Word
                            if (context not in gender_intensifiers[gender]):
                                gender_intensifiers[gender][context] = dictionary[gender][context]
                            else:
                                gender_intensifiers[gender][context] += dictionary[gender][context]
        
        # Quick extra write! (for intensifier use by gender)
        f = open(path + "gendered_intensifiers.csv", 'w')
        f.write("Totals by Gender\n")
        for gender in ["Men", "Women"]:
            f.write(gender + '\n')
            for context in gender_intensifiers[gender]:
                f.write(f" , {context}, {gender_intensifiers[gender][context]}\n")
        f.close()
        
        self.write_csv(path = path + "overall.csv",
                       words_totals=overall_totals, 
                       words_by_cast=overall_cast,
                       words_by_gender=overall_gender,
                       useless_data_points=useless_data_points)

        file.close()