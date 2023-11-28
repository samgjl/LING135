# LING135
Python classes built to sift through OpenXML caption files for instances of targeted words/phrases, then analyze their use across gender and context.

## SubtitleReader class (subtitle_reader.py)
> Parses through a set of caption files for words/phrases specified by input file.
> Input file formatted as newline-separated values for each target word
> Output file is a CSV where each line is in the format of "timestamp, context"
> If specified, this class will convert ms to HH\MM\SS

## DataParser class (data_parser.py)
> Parses through CSV files and aggregates data across gender and context lines, as well as optional per-episode and per-name basis
> CSV input will be of the format "timestamp, word, contestant name, interview? (Y/N)"
