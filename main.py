import subtitle_reader as sr
import data_parser as dp
import os, glob

if __name__ == "__main__":
    # Intensifiers:
    reader = sr.SubtitleReader(filename = 'intensifiers.txt')
    reader.read_all_in_folder(input_path = "./input-files/", 
                              output_path = "./output-files/", 
                              time_in_ms = True, 
                              verbose = True)
    
    men =   ["Jeremiah", "James", "Tre", "Connor", "Carrington", "Johnny", "Calvin", "Caleb", "Matthew"]
    women = [ "Cely", "Moira", "Justine", "Kaitlynn", "Mackenzie", "Kierstan", "Rachel", "Lauren", "Arielle"]
    parser = dp.DataParser(men = men, women = women)

    for filename in glob.glob(os.path.join("./round-two-input/", '*.csv')):
        parser.parse(filename, output_path = "./round-two-output/" + filename.split("\\")[-1][0:-4] + ".csv")
    parser.wrangle_all(path ="./round-two-output/")