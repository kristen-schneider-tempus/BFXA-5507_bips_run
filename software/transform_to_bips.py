import argparse
import pandas as pd

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str, required=True)
    parser.add_argument('-o', '--output', type=str, required=True)
    parser.add_argument('-f', '--fields', type=str, required=False)
    return parser.parse_args()

def main():
    x = 'hello world'
    print(x)

    # get arguments
    args = get_args()
    sql_input = args.input
    bips_output = args.output
    sql_fields = args.fields

    # get fields from the sql query
    sql_file_fields = get_bioinfdb_query_fields(sql_input, ',')

    # fill in whichever fields are not part of the file input
    # use user input for this

    # # write out to a bips_input file
    # o = open(bips_output, 'w')
    # o.write()

    

def get_bioinfdb_query_fields(bioinf_db_csv, delim):
    '''
    Read in a SQL query output file and return the fields included in the header.
    @param input bioinf_db_csv: SQL query output
    @param input delim: file delimeter
    @param return field_list: list of fields from SQL query
    '''
    f = open(bioinf_db_csv, 'r')
    header = f.readline()
    field_list = header.strip().split(delim)
    f.close()
    return field_list


if __name__ == '__main__':
    main()