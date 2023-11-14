# Cancer_Library_Data_Synthesize
- Authors : Won Seok Jang, Woo Seob Sim
- Objective : Generating synthetic data using Cancer Library Project data set.

## Synthesize Method
- Bayseian Network(BN) method is used for generating synthetic data.
- To guarantee privacy preserving, Laplace Differential Privacy(LDP) mechanism is applied.
- Synthesize codes are referenced from repository : https://github.com/DataResponsibly/DataSynthesizer

## Data Flow
- Using colon and lung cancer dataset in this project.
- Raw data had been constructed Realational DB format. So it must be pre-processed to first normal form (in this project, called 'D0').
- Synthetic Data S0 is generated after synthesize process and S0 is splited into original DB table form.
- Clinical quality check process is applied to each table seperately.

## Run code
0. Create virtual environment and install requirements.txt
1. Modify input/output path, some hyper-parameter(such as, epsilon for DP density) and data descriptions in config.yaml file
2. Run $sh ./produce_data to create S0 and restored DB form data
3. Run $sh ./postprocess.sh to drop incomplete value in each table
4. Run $sh ./QC_handling.sh to apply clinical quality check guide line
