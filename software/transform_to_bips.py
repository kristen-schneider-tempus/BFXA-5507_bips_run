import argparse
import pandas as pd

BIPS_FIELDS=['orderhub_id',
             'gcs_tumor_fastq_url',
             'cancer_type',
             'assay',
             'analyte',
             'match_type',
             'intent',
             'control_sample_type']

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str, required=True)
    parser.add_argument('-o', '--output', type=str, required=True)
    parser.add_argument('-n', '--num_records', type=int, required=True)
    parser.add_argument('-ohid', '--orderhub_id', type=str, required=False, default='')
    parser.add_argument('-fq', '--gcs_tumor_fastq_url', type=str, required=False, default='')
    parser.add_argument('-cncr', '--cancer_type', type=str, required=False, default='Tumor of Unknown Origin')
    parser.add_argument('-as', '--assay', type=str, required=False, default='')
    parser.add_argument('-an', '--analyte', type=str, required=False, default='rna')
    parser.add_argument('-mt', '--match_type', type=str, required=False, default='tumor_only')
    parser.add_argument('-int', '--intent', type=str, required=False, default='rad')
    parser.add_argument('-cst', '--control_sample_type', type=str, required=False, default='')
    return parser.parse_args()

def main():

    # get required arguments
    args = get_args()
    # REQUIRED
    sql_output_file = args.input
    bips_input_file = args.output
    num_records = args.num_records

    # SUPPLEMENT
    user_input = {bf:'' for bf in BIPS_FIELDS}
    user_input['ohid'] = args.orderhub_id
    user_input['fq'] = args.gcs_tumor_fastq_url
    user_input['cncr'] = args.cancer_type
    user_input['as'] = args.assay
    user_input['an'] = args.analyte
    user_input['mt'] = args.match_type
    user_input['int'] = args.intent
    user_input['cst'] = args.control_sample_type

    # get fields from the sql query
    input_file_field_dict = get_bioinfdb_query_data(sql_output_file,
                                                     ',') 

    # fill output dict with input data + added fields
    bips_output_dict = fill_bips_data(input_file_field_dict,
                                      user_input,
                                      num_records)
    
    # write output bips file
    write_output_bips(bips_input_file,
                      bips_output_dict,
                      num_records)

def get_bioinfdb_query_data(bioinf_db_csv,
                             delim):
    '''
    Read in a SQL query output file and return a dictionary with 
    the fields included in the header + the entries.
    @param input bioinf_db_csv: SQL query output
    @param input delim: file delimeter
    @param return field_dict: list of fields from SQL query
    '''

    # TODO: make it so that only unique IDs are included

    field_dict = dict()

    f = open(bioinf_db_csv, 'r')
    header = f.readline()
    header_list_ = header.strip().split(delim)
    header_list = []
    
    # change fastq_url --> gcs_tumor_fastq_url
    for h in header_list_:
        if 'fastq_url' in h:
            header_list.append('gcs_tumor_fastq_url')
        else: header_list.append(h) 
    
    for line in f:
        L = line.strip().split(delim)
        for field_data in L:
            field_idx = L.index(field_data)
            field_header = header_list[field_idx]
            try:
                field_dict[field_header].append(field_data)
            except KeyError:
                field_dict[field_header] = [field_data]
    f.close()
    return field_dict

def fill_bips_data(input_file_field_dict,
                   user_input,
                   num_records):
    '''
    create a dict data structure with keys in the BIPS input
    from the SQL input file. if the input file does not include some
    fields, look in the user fields (args)
    @param input_file_field_dict:
    @param user_input:
    @return bips_output_dict: 
    '''
    bips_output_dict = dict()
    for i, bf in enumerate(BIPS_FIELDS):
        try:
            # get field data from input file
            bips_output_dict[bf] = input_file_field_dict[bf]
        except KeyError:
            # need to get field data from cli args
            match bf:
                case 'orederhub_id':
                    cli_input = [user_input['ohid']] * num_records   ## TODO: this might be required
                case 'gcs_tumor_fastq_url':
                    cli_input = [user_input['fq']] * num_records      ## TODO: this might be required
                case 'cancer_type':
                    cli_input = [user_input['cncr']] * num_records
                case 'assay':
                    cli_input = [user_input['as']] * num_records
                case 'analyte':
                    cli_input = [user_input['an']] * num_records
                case 'match_type':
                    cli_input = [user_input['mt']] * num_records
                case 'intent':
                    cli_input = [user_input['int']] * num_records
                case 'control_sample_type':
                    cli_input = [user_input['cst']] * num_records
            bips_output_dict[bf] = cli_input

            print('no field in input file for:', bf)

    return bips_output_dict

def write_output_bips(bips_input_file,
                      bips_output_dict,
                      num_records): 
    '''
    Writes out a file which can be used as input for BIPS.
    @param bips_input_file: output file path
    @param bips_output_dict: dictionary containing BIPS data
    @param num_records: number of records to write
    '''  
    # write out to a bips_input file
    o = open(bips_input_file, 'w')
    # writing BIPS header
    for i, bf in enumerate(BIPS_FIELDS):
        if i == 0:
            o.write(bf)
        else:
            o.write(',' + bf)
    o.write('\n')
    
    # writing a field information for each record
    for r in range(num_records):
        record_string = ''
        for i_, bf_ in enumerate(BIPS_FIELDS):
            if i_ == 0:
                record_string += bips_output_dict[bf_][r]
            else:
                record_string += ',' + bips_output_dict[bf_][r]
        o.write(record_string + '\n')

if __name__ == '__main__':
    main()