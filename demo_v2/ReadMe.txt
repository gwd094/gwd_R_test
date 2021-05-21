
Step 1:

python code_1_preprocessing.py -i ./data_0_original/ -o ./data_1_preprocessing/

Step 2:

python main.py -i ./data_1_preprocessing/ -o ./data_2_philter/ -f ./configs/philter_delta.json --prod=True --outputformat "asterisk"

Step 3:

if we have no patient name list

python code_2_postprocessing.py -i1 ./data_1_preprocessing/ -i2 ./data_2_philter/ -o ./data_3_post_processing/


if we have patient name list

python code_2_postprocessing.py -i1 ./data_1_preprocessing/ -i2 ./data_2_philter/ -o ./data_3_post_processing/ -p ./patient_name_array.csv


