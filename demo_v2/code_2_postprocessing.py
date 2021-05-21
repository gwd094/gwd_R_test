import argparse
import os
import numpy as np 
import pandas as pd
import nltk
import re
import math

def main():
    
    
    print ("")
    print ("postprocessing")
    print ("")
    
    
    
    help_str = """ postprocessing """
    
    ap = argparse.ArgumentParser(description=help_str)
    
    ap.add_argument("-i1", "--input_1", default="./data_1_preprocessing/", help="***", type=str)
    
    ap.add_argument("-i2", "--input_2", default="./data_2_philter/", help="***", type=str)

    ap.add_argument("-o", "--output", default="./data_3_post_processing/", help="***", type=str)
    
    ap.add_argument("-p", "--patient_name", default="None", help="***", type=str)
    
    args = ap.parse_args()

    input_1_folder = args.input_1
    input_2_folder = args.input_2
    output_folder = args.output
    patient_name_path = args.patient_name
    
    print ("input_1_folder: ", input_1_folder)
    print ("input_2_folder: ", input_2_folder)
    print ("output_folder: ", output_folder)
    print ("patient_name_path: ", patient_name_path)    
    print ("")
    
    

    note_name_list = os.listdir(input_1_folder)

    print ("len(note_name_list): ", len(note_name_list))
    print ("")
    
    keep_pattern_array = np.loadtxt("./keep_pattern_array.txt", delimiter = '\t', dtype = np.str)

    print ("keep_pattern_array.shape: ", keep_pattern_array.shape)
    print ("")
    
    remove_pattern_array = np.loadtxt("./remove_pattern_array.txt", delimiter = '\t', dtype = np.str)

    print ("remove_pattern_array.shape: ", remove_pattern_array.shape)
    print ("")
    
    age_pattern_array = np.loadtxt("./age_pattern_array.txt", delimiter = '\t', dtype = np.str)

    print ("age_pattern_array.shape: ", age_pattern_array.shape)
    print ("")
    
    
    
    if not patient_name_path == "None":
    
        df_pt_name = pd.read_csv(patient_name_path)  

        print ("df_pt_name.shape: ", df_pt_name.shape)
        print ("")

        first_name_list = df_pt_name["FirstName"]
        middle_name_list = df_pt_name["MiddleName"]
        last_name_list = df_pt_name["LastName"]


    T = len(note_name_list)

    for t in range(T):
        
        if t%100 == 0:
            print (t)

        
        path1 = input_1_folder + note_name_list[t]


        f1 = open(path1, "r")

        ori_line_list = f1.readlines()


        path2 = input_2_folder + note_name_list[t]


        f2 = open(path2, "r")

        philter_line_list = f2.readlines()
        
        
        
        
        if not patient_name_path == "None":
            
            first_name = first_name_list[t]
            middle_name = middle_name_list[t]
            last_name = last_name_list[t]


            name_list = list()

            name_list.append(first_name)
            name_list.append(last_name)
            name_list.append(first_name + " " + last_name)    
            name_list.append(last_name + ", " + first_name)
            name_list.append(first_name + " " + last_name) 


        N = len(ori_line_list)

        result_note = list()
        
        
        for n in range(N):
        
            ori_line = ori_line_list[n]
            philter_line = philter_line_list[n]

            # recover pattern

            for pattern in keep_pattern_array:

                finder_total = re.finditer(pattern, ori_line)

                for finder_i in finder_total:


                    ori_list = list(ori_line)
                    philter_list = list(philter_line)

                    target_str = philter_line[finder_i.span()[0]:finder_i.span()[1]]

                    if "*" in target_str:

                        philter_list[finder_i.span()[0]:finder_i.span()[1]] = ori_list[finder_i.span()[0]:finder_i.span()[1]]

                    philter_line = ''.join(philter_list) 


            # recover I ()


            finder_total = re.finditer("I \(.{1,30}\)", ori_line)

            for finder_i in finder_total:


                ori_list = list(ori_line)
                philter_list = list(philter_line)

                ori_list = list(ori_line)
                philter_list = list(philter_line)

                philter_list[finder_i.span()[0]] = ori_list[finder_i.span()[0]]

                for k in range(finder_i.span()[0]+1, finder_i.span()[1]):

                    if philter_list[k] == ' ' or  philter_list[k] == '(' or philter_list[k] == ')':
                        tem = 1

                    else:    
                        philter_list[k] = '*'




                philter_line = ''.join(philter_list) 




            finder_total = re.finditer("I;.{1,20}; MD", ori_line)

            for finder_i in finder_total:

                ori_list = list(ori_line)
                philter_list = list(philter_line)


                ori_list = list(ori_line)
                philter_list = list(philter_line)


                philter_list[finder_i.span()[0]] = ori_list[finder_i.span()[0]]

                for k in range(finder_i.span()[0]+1, finder_i.span()[1]-2):

                    if philter_list[k] == ' ' or  philter_list[k] == '(' or philter_list[k] == ')' or philter_list[k] == ';':
                        tem = 1

                    else:    
                        philter_list[k] = '*'




                philter_line = ''.join(philter_list) 





            # remove pattern

            for pattern in remove_pattern_array:

                finder_total = re.finditer(pattern, ori_line)

                for finder_i in finder_total:

                    ori_list = list(ori_line)
                    philter_list = list(philter_line)


                    target_str = philter_line[finder_i.span()[0]:finder_i.span()[1]]


                    for k in range(finder_i.span()[0],finder_i.span()[1]):

                        if not philter_list[k] == ' ':

                            philter_list[k] = '*'

                    philter_line = ''.join(philter_list) 








            # if age > 90: age = 90

            for pattern in age_pattern_array:

                finder_total = re.finditer(pattern, philter_line)

                for finder_i in finder_total:



                    age_str = philter_line[finder_i.span()[0]:finder_i.span()[1]]

                    age_str_0 = philter_line[finder_i.span()[0]:finder_i.span()[1]]


                    age_finder = re.search("\d+", age_str)



                    age = int(age_str[age_finder.span()[0]:age_finder.span()[1]])


                    if age > 90:

                        age_str = age_str.replace(str(age),"90")


                    philter_line = philter_line.replace(age_str_0, age_str)



            # re-check patient name:
            
            if not patient_name_path == "None":

                for name in name_list:

                    mask_str = "*"*len(name)

                    philter_line = philter_line.replace(name, mask_str)



            result_line = philter_line

            result_note.append(result_line)

        path3 = output_folder + note_name_list[t]

        f = open(path3, "w")
        f.writelines(result_note)
        f.close()


    print ("")
    print ("finish")
    print ("")
    
    

if __name__ == "__main__":
    main()
    







