import argparse

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--bips_csv', type=str,
                        required=True, help='csv file with selected output from bips logs')
    parser.add_argument('-o', '--ids_txt', type=str,
                        required=True, help='analysis or execution ids')
    return parser.parse_args()

def main():
    args = get_args()

    bips_csv = args.bips_csv
    ids_txt = args.ids_txt

    analysis_id_idx, execution_id_idx = get_ids_idx(bips_csv)
    if analysis_id_idx == -1 and execution_id_idx == -1:
        print('No analysis.id or execution.id found in the csv file')
        return 1
    
    if analysis_id_idx != -1:
        print('Found analysis.id in the csv file. Writing to output file.')
        ids = get_ids(bips_csv, analysis_id_idx)
        with open(ids_txt, 'w') as f:
            for id in ids:
                f.write(id + '\n')

    if execution_id_idx != -1:
        print('Found execution.id in the csv file. Writing to output file.')
        ids = get_ids(bips_csv, execution_id_idx)
        with open(ids_txt, 'a') as f:
            for id in ids:
                f.write(id + '\n')
    
    return 0

def get_ids_idx(bips_csv):
    '''
    Get the index of the id_type in the bips_csv
    @param bips_csv: csv file with selected output from bips logs
    @return ids_idx: index of the id_type in the bips_csv
    '''
    analysis_id = 'analysis.id'
    analysis_id_idx = -1
    execution_id = 'execution.id'
    execution_id_idx = -1

    with open(bips_csv, 'r') as f:
        headers = f.readline().strip().split(',')
        try :
            analysis_id_idx = headers.index(analysis_id)
        except ValueError:
            pass
        try:
            execution_id_idx = headers.index(execution_id)
        except ValueError:
            pass

    return analysis_id_idx, execution_id_idx

def get_ids(bips_csv,
            id_idx):
    '''
    Get the ids from the bips_csv according to the id_idx
    @param bips_csv: csv file with selected output from bips logs
    @param id_idx: index of the id_type in the bips_csv
    @return ids: list of ids
    '''
    ids = []
    with open(bips_csv, 'r') as f:
        f.readline()
        for line in f:
            ids.append(line.strip().split(',')[id_idx])
    return ids


if __name__ == '__main__':
    main()