import argparse
import os
import numpy as np 
import pandas as pd
import nltk
import re
import math

def main():
    
    print ("")
    print ("preprocessing")
    print ("")
    
    
    
    help_str = """ preprocessing """
    
    ap = argparse.ArgumentParser(description=help_str)
    
    ap.add_argument("-i", "--input", default="./data_0_original/", help="***", type=str)

    ap.add_argument("-o", "--output", default="./data_1_preprocessing/", help="***", type=str)
    
    args = ap.parse_args()

    input_folder = args.input
    output_folder = args.output
    
    print ("input_folder: ", input_folder)
    print ("output_folder: ", output_folder)
    print ("")
    


    note_name_list = os.listdir(input_folder)

    print ("len(note_name_list): ", len(note_name_list))
    print ("")

    T = len(note_name_list)


    for t in range(T):
        
        if t%100 == 0:
            print (t)

        path1 = input_folder + note_name_list[t]

        f = open(path1, "r")

        line_list = f.readlines()

        N = len(line_list)

        result_note = list()

        for n in range(N):

            line = line_list[n]

            pattern = "[a-z]{2}[\`\~\!\@\#\$\%\^\&\(\)\_\[\]\{\}\|\;\'\'\:\"\"\,\.\?]?\d"

            finder = re.search(pattern, line)

            while finder:

                str_list = list(line)

                target_index= finder.span()[1]-1

                str_list.insert(target_index, " ")

                result_str = ''.join(str_list)

                line = result_str

                finder = re.search(pattern, line)

            result_line = line

            result_note.append(result_line)

        path2 = output_folder + note_name_list[t]

        f = open(path2, "w")
        f.writelines(result_note)
        f.close()


    print ("")
    print ("finish")
    print ("")
    
    

if __name__ == "__main__":
    main()
    







