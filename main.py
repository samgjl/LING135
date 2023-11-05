import subtitle_reader as sr
if __name__ == "__main__":
    # Intensifiers:
    reader = sr.SubtitleReader(filename = 'intensifiers.txt')
    reader.read_all_in_folder(input_path = "./input-files/", 
                              output_path = "./output-files/", 
                              time_in_ms = True, 
                              verbose = True)
    # Like:
    # reader = sr.SubtitleReader(filename = 'like.txt')
    # reader.read_all_in_folder(input_path = "./input-files/", 
    #                           output_path = "./output-files/", 
    #                           time_in_ms = True, 
    #                           verbose = True)
    
    # # The entire transcript:
    # reader = sr.SubtitleReader(filename = 'everything.txt')
    # reader.read_all_in_folder(input_path = "./input-files/", output_path = "./output-files/", time_in_ms = True)
