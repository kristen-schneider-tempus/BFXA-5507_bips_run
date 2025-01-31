import argparse
import pandas as pd

def parse_args():
    parser = argparse.ArgumentParser(description='Create final output file to keep track of data from MYB run.')
    parser.add_argument('-u', '--unique', type=str, help='The unique set of data from GBQ search')
    parser.add_argument('-b', '--bips_input', type=str, help='The file used as input for BIPS')
    parser.add_argument('-o', '--nohup_output', type=str, help='The output file from MYB (output.txt)')
    parser.add_argument('-p', '--parsed_nohup', type=str, help='The parsed output file from MYB (parsedNoHup.out)')
    parser.add_argument('-c', '--combinedDataProdudcts', type=str, help='Combined data products file')
    parser.add_argument('-f', '--final_output', type=str, help='Output file')
    return parser.parse_args()

def main():
    args = parse_args()

    unique_orderhub_ids = args.unique
    bips_input = args.bips_input
    nohup_output = args.nohup_output
    parsed_nohup_output = args.nohup_output
    combined_data_products = args.combinedDataProdudcts
    final_output = args.output

    # this df contains orderhub ids AND analysis IDS
    unique_df = read_unique_input(unique_orderhub_ids)
    # this df contains only orderhub ids
    bips_input_df = read_bips_input(bips_input)

    # join the unique and both BIPS dataframes on orderhub_id
    joined_df = pd.merge(unique_df, bips_input_df, on='orderhub_id', how='left')


    nohup_output_df = read_nohup_output(nohup_output)
    # this df contains 
    parsed_nohup_df = read_nohup_output(parsed_nohup_output)
    
    # this df contains nextflowSessionID AND 

    
    # write the merged dataframe to a csv file
    write_merged_df(joined_df, final_output)
    
   

def read_unique_input(unique_orderhub_ids):
    '''
    Use pandas to read the unique file and store the information

    @param unique_orderhub_ids: The file containing unique sample information
    '''
    unique_df = pd.read_csv(unique_orderhub_ids)
    return unique_df


def read_bips_input(bips_input):
    '''
    Read the BIPS input file using pandas df.

    @param bips_input: The file containing the BIPS input
    '''
    bips_df = pd.read_csv(bips_input)
    return bips_df


def read_nohup_output(nohup_output):
    '''
    Read the parsed output file from MYB.

    @param nohup_output: The parsed output file from MYB
    '''
    nohup_df = pd.read_csv(nohup_output)
    return nohup_df

def write_merged_df(merged_df, 
                    output_csv):
    '''
    Write the merged dataframe to a csv file.
    '''
    merged_df.to_csv(output_csv, index=False)
    
if __name__ == '__main__':
    main()
