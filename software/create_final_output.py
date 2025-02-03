import argparse
import pandas as pd

def parse_args():
    parser = argparse.ArgumentParser(description='Create final output file to keep track of data from MYB run.')
    parser.add_argument('-u', '--unique', type=str, help='The unique set of data from GBQ search')
    parser.add_argument('-b', '--bips_input', type=str, help='The file used as input for BIPS')
    parser.add_argument('-l', '--bips_output', type=str, help='The output file from bips logs')
    parser.add_argument('-p', '--parsed_nohup', type=str, help='The parsed output file from MYB (parsedNoHup.out)')
    parser.add_argument('-c', '--combinedDataProdudcts', type=str, help='Combined data products file')
    parser.add_argument('-f', '--final_output', type=str, help='Output file')
    return parser.parse_args()

def main():
    args = parse_args()

    unique_orderhub_ids = args.unique
    bips_input = args.bips_input
    bips_output = args.bips_output
    parsed_nohup_output = args.parsed_nohup
    combined_data_products = args.combinedDataProdudcts
    final_output = args.final_output

    # this df contains ORDERHUB_ID on which we can join other dataframes
    unique_df = read_unique_input(unique_orderhub_ids)
    # this df contains ORDERHUB_ID on which we can join other dataframes
    bips_input_df = read_bips_input(bips_input)
    # JOIN the unique and both BIPS dataframes on orderhub_id
    joined_df_ohid = pd.merge(unique_df, bips_input_df, on='orderhub_id', how='left')

    # this df contains the ANALYSIS_ID and ORDERHUB_ID on which we can join other dataframes
    bips_output_df = read_bips_output(bips_output)
    # JOIN the joined_df_ohid and bips_output_df on orderhub_id (now we also have an analysis id)
    joined_df_ohid = pd.merge(joined_df_ohid, bips_output_df, on='orderhub_id', how='left')

    # this df contains rfnd-combined-myb-expression-features
    parsed_nohup_df = read_parsed_nohup_output(parsed_nohup_output)
    # this df contains dp_id=rfnd-combined-myb-expression-features
    combined_data_products_df = read_combined_output(combined_data_products)

    # join parsed_nohup_df and combined_data_products_df on rfnd-combined-myb-expression-features
    joined_df_myb_exp = pd.merge(parsed_nohup_df, combined_data_products_df, on='rfnd-combined-myb-expression-features', how='left')
    
    # combine the two joined df on analysis_id
    joined_df_anid = pd.merge(joined_df_ohid, joined_df_myb_exp, on='analysis_id', how='left')

    # reordered columns
    # 1. joined_df_anid['orderhub_id']
    # 2. joined_df_anid['analysis_id']
    # 3. remaining columns from joined_df_anid

    final_output_df = joined_df_anid[['orderhub_id', 'analysis_id'] + [col for col in joined_df_anid.columns if col not in ['orderhub_id', 'analysis_id']]]

    # write the merged dataframe to a csv file
    write_merged_df(final_output_df, final_output)
    
def read_unique_input(unique_orderhub_ids):
    '''
    Use pandas to read the unique file and store relevant information.

    @param unique_orderhub_ids: The file containing unique sample information
    '''
    # check if file exists, if not, exit with error
    try:
        with open(unique_orderhub_ids) as f:
            pass
        f.close()
    except FileNotFoundError:
        print(f"File {unique_orderhub_ids} not found.")
        exit(1)

    # read as a csv file and return the dataframe
    unique_df = pd.read_csv(unique_orderhub_ids)
    
    # remove analysis_id column--we get the analysis id from the bips output
    unique_df.drop('analysis_id', axis=1, inplace=True)

    # remove fastq_url column--we can get this from the bips input renamed correctly with gcs
    unique_df.drop('fastq_url', axis=1, inplace=True)

    # remove the 'orderhub_id'--we can get this from the bips input
    unique_df.drop('orderhub_id', axis=1, inplace=True)

    # remove the 'assay' column--we can get this from the bips input
    unique_df.drop('assay', axis=1, inplace=True)
    return unique_df


def read_bips_input(bips_input):
    '''
    Read the BIPS input file using pandas df.

    @param bips_input: The file containing the BIPS input
    '''
    # check if file exists, if not, exit with error
    try:
        with open(bips_input) as f:
            pass
        f.close()
    except FileNotFoundError:
        print(f"File {bips_input} not found.")
        exit(1)

    # read as a csv file and return the dataframe
    bips_df = pd.read_csv(bips_input)
    return bips_df


def read_bips_output(bips_output):
    '''
    Read the parsed csv file from bips output and get ONLY the analsis_id and orderhub_id.
    
    @param bips_output: 
    '''
    # check if file exists, if not, exit with error
    try:
        with open(bips_output) as f:
            pass
        f.close()
    except FileNotFoundError:
        print(f"File {bips_output} not found.")
        exit(1)

    # read as a csv file and return the dataframe
    bips_output_df = pd.read_csv(bips_output)
    # change the column name from "analysis.id" to "analysis_id"
    bips_output_df.rename(columns={'analysis.id': 'analysis_id'}, inplace=True)

    # only keep the 'analysis_id' and 'orderhub_id' columns
    bips_output_df = bips_output_df[['analysis_id', 'orderhub_id']]
    
    return bips_output_df

def read_parsed_nohup_output(parsed_nohup_output):
    '''
    Read the parsed output file from MYB.

    @param parsed_nohup_output: The parsed output file from MYB
    '''
    # check if file exists, if not, exit with error
    try:
        with open(parsed_nohup_output) as f:
            pass
        f.close()
    except FileNotFoundError:
        print(f"File {parsed_nohup_output} not found.")
        exit(1)

    # read as a csv file and return the dataframe
    parsed_nohup_df = pd.read_csv(parsed_nohup_output)
    return parsed_nohup_df

def read_combined_output(combined_data_products):
    '''
    Read the combined data products file.

    @param combined_data_products: The combined data products file
    '''
    # check if file exists, if not, exit with error
    try:
        with open(combined_data_products) as f:
            pass
        f.close()
    except FileNotFoundError:
        print(f"File {combined_data_products} not found.")
        exit(1)

    # read as a tsv file
    combined_df = pd.read_csv(combined_data_products, sep='\t')
    
    # rename "analysis_id" to "analysis_id_2"
    combined_df.rename(columns={'analysis_id': 'analysis_id_2'}, inplace=True)
    return combined_df

def write_merged_df(merged_df, 
                    output_csv):
    '''
    Write the merged dataframe to a csv file.
    '''
    merged_df.to_csv(output_csv, index=False)
    
if __name__ == '__main__':
    main()
