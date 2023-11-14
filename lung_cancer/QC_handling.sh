
#!/bin/bash

source ./bin/functions

#set_python_env
conda activate synthetic_data

echo "================ QC Handling ================="
python3 /home/dogu86/lung_synthesis/src/3_postprocess/QC_handling.py --epsilon 0.1 
echo "Epsilon 0.1 Done"
python3 /home/dogu86/lung_synthesis/src/3_postprocess/QC_handling.py --epsilon 1
echo "Epsilon 1 Done"
python3 /home/dogu86/lung_synthesis/src/3_postprocess/QC_handling.py --epsilon 10
echo "Epsilon 10 Done"
python3 /home/dogu86/lung_synthesis/src/3_postprocess/QC_handling.py --epsilon 100
echo "Epsilon 100 Done"
python3 /home/dogu86/lung_synthesis/src/3_postprocess/QC_handling.py --epsilon 1000
echo "Epsilon 1000 Done"