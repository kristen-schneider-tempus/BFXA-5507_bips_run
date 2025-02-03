import argparse
import pandas as pd

BIPS_FIELDS=['orderhub_id',
             'gcs_tumor_fastq_url',
             'cancer_type',
             'assay',
             'analyte',
             'match_type',
             'intent']

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str,
                        required=True, help='GBQ output')
    parser.add_argument('-o', '--output', type=str,
                        required=True, help='bips input format')
    parser.add_argument('-l', '--location', type=str,
                        required=True, help='location of the fastq files (e.g. prd, beta, etc.)')
    parser.add_argument('-c', '--cancer_type', type=str,
                        required=True, help='cancer type (ex. "Adenoid Cystic Carcinoma")')
    parser.add_argument('-a', '--assay', type=str,
                        required=True, help='assay type (ex. "RNA-onco.v1, RS.v2")')
    parser.add_argument('-n', '--analyte', type=str,
                        required=True, help='analyte type (ex. "rna")')
    parser.add_argument('-m', '--match_type', type=str,
                        required=True, help='match type (ex. "tumorOnly")')
    parser.add_argument('-t', '--intent', type=str,
                        required=True, help='intent (ex. "rad")')

    return parser.parse_args()

def main():

    # get required arguments
    args = get_args()
    sql_output_file = args.input
    bips_input_file = args.output
    location = args.location
    cancer_type = args.cancer_type
    assay = args.assay
    analyte = args.analyte
    match_type = args.match_type
    intent = args.intent

    # read the sql output file
    sql_df = read_sql_output(sql_output_file,
                             location,
                             assay)
    
    # create the bips input file
    create_bips_input(sql_df,
                        cancer_type,
                        assay,
                        analyte,
                        match_type,
                        intent,
                        bips_input_file)

def read_sql_output(sql_output_file,
                    location,
                    assay):
    '''
    Read the sql output file and return a dataframe with the data.

    @param sql_output_file: The file containing the sql output
    @return sql_df: The dataframe with the sql output
    '''
    # check if file exists, if not, exit with error
    try:
        with open(sql_output_file) as f:
            pass
        f.close()
    except FileNotFoundError:
        print(f"File {sql_output_file} not found.")
        exit(1)

    # read as a csv file and return the dataframe
    sql_df = pd.read_csv(sql_output_file)

    # rename 'fastq_url' to 'gcs_tumor_fastq_url'
    sql_df.rename(columns={'fastq_url': 'gcs_tumor_fastq_url'}, inplace=True)
    # change location in the fastq url from 'prd' to the location provided
    sql_df['gcs_tumor_fastq_url'] = sql_df['gcs_tumor_fastq_url'].str.replace('prd', location)

    # replace the assay column with the assay type provided
    sql_df['assay'] = assay

    return sql_df

def create_bips_input(sql_df,
                        cancer_type,
                        assay,
                        analyte,
                        match_type,
                        intent,
                        bips_input_file):
        '''
        Create the bips input file from the sql output.
    
        @param sql_df: The dataframe with the sql output
        @param cancer_type: The cancer type
        @param assay: The assay type
        @param analyte: The analyte type
        @param match_type: The match type
        @param intent: The intent
        @param bips_input_file: The file to write the bips input

        '''

        # add the cancer type, assay, match type, and intent to the dataframe
        sql_df['cancer_type'] = cancer_type
        sql_df['assay'] = assay
        sql_df['analyte'] = analyte
        sql_df['match_type'] = match_type
        sql_df['intent'] = intent

        # Write the df in order:
        # orderhub_id,gcs_tumor_fastq_url,cancer_type,assay,analyte,match_type,intent
        sql_df.to_csv(bips_input_file, index=False, columns=BIPS_FIELDS)
    

if __name__ == '__main__':
    main()