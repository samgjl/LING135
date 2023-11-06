class DataParser:
    def __init__(self, data):
        pass

    def parse(self, file_path, men = [], women = []):
        # Reas the file:
        file = open(file_path, 'r')
        data = file.read()
        file.close()
        
        # Split the data:
        data = data.split('\n')
        data = [x.split(',') for x in data]

        # Parse:
        words_totals = {}
        words_by_cast = {}
        words_by_interview = {}

        for line in data:
            # If the data is unfilled / 'N/A' was entered:
            if (len(line) < 3):
                continue
            
            # Data sorting:
            word = "".join([char if char.isalpha() else "" for char in line[0].lower()])
            contestant = line[1]
            interview = line[2]

            # Totals over words:
            if (word not in words_totals):
                words_totals[word] = 1
            else:
                words_totals[word] += 1
            
            # Totals over each contestant:
            if (contestant not in words_by_cast):
                words_by_cast[contestant] = {}
            elif (word not in words_by_cast[contestant]):
                words_by_cast[contestant][word] = 0
            words_by_cast[contestant][word] += 1
            words_by_cast[contestant]['total'] += 1

            # Totals over each interview:
            if (word not in words_by_interview):
                words_by_interview[word] = {}
            elif (interview not in words_by_interview[word]):
                words_by_interview[word][interview] = 0
            words_by_interview[word][interview] += 1







