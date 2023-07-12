import splitfolders

input_folder="New_data"
output="New_data"

splitfolders.ratio(input_folder,output=output,seed=42,ratio=(0.8,0.1,0.1))