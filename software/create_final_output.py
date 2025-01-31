import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Create final output file to keep track of data from MYB run.')
    parser.add_argument('-u', '--unique', type=str, help='The unique set of data from GBQ search')
    parser.add_argument('-b', '--bips_input', type=str, help='The file used as input for BIPS')
    parser.add_argument('-l', '--bips_output', type=str, help='Parsed BIPS output logs')
    parser.add_argument('-n', '--nohup_output', type=str, help='The parsed output file from MYB (parsedNoHup.out)')
    parser.add_argument('-c', '--combinedDataProdudcts', type=str, help='Combined data products file')
    parser.add_argument('-o', '--output', type=str, help='Output file')
    return parser.parse_args()

def main():
    args = parse_args()

    unique_orderhub_ids = args.unique
    bips_input = args.bips_input
    bips_output = args.bips_output
    nohup_output = args.nohup_output
    combined_data_products = args.combinedDataProdudcts
    final_output = args.output

    unique_ohid_info, unique_anid_info = read_unique_file(unique_orderhub_ids)




def read_unique_file(unique_orderhub_ids):
    '''
    Read the unique file and store the information in a dictionary.

    @param unique_orderhub_ids: The file containing unique sample information
    @return ohid_dict: A dictionary containing the unique orderhub ids as keys and the rest of the information as values
    @return anid_dict: A dictionary containing the unique analysis ids as keys and the rest of the information as values
    '''

    # header in the unique file
    # analysis_id,isolate_id,orderhub_id,patient_id,run_id,assay,fastq_url  

    ohid_dict = {}
    anid_dict = {}

    with open(unique_orderhub_ids, 'r') as f:
        header = f.readline().strip().split(',')
        for line in f:
            line = line.strip().split(',')
            analysis_id = line[0]
            isolate_id = line[1]
            orderhub_id = line[2]
            patient_id = line[3]
            run_id = line[4]
            assay = line[5]
            fastq_url = line[6]

            ohid_dict[orderhub_id] = [analysis_id, isolate_id, patient_id, run_id, assay, fastq_url]
            anid_dict[analysis_id] = [isolate_id, orderhub_id, patient_id, run_id, assay, fastq_url]

    return ohid_dict, anid_dict


    


