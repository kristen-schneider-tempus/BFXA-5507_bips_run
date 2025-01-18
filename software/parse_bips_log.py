import argparse
from collections import defaultdict
from datetime import datetime
import json
import numpy as np
import os
import pandas as pd
import sys

# TO EXTRACT:
    # executionArn
    # executionName
    # input.input.janeAdapter.assay
    # input.input.janeAdapter.analyte
    # input.input.janeAdapter.matchType
    # input.input.janeAdapter.cloudDestination
    # input.input.janeAdapter.assets.assetID
    # input.input.janeAdapter.assets.gcsurl
    # input.input.janeAdapter.assets.tissueClassification
    # input.input.janeAdapter.assets.tissueSource
    # input.input.janeAdapter.assets.tissueType
    # input.input.janeAdapter.assets.coverage
    # input.input.janeAdapter.orderhubItemId
    # input.input.janeAdapter.cancerCohort
    # input.input.janeAdapter.transformOverrides.* tuples: (workflow, transformID)
    # XXXX stateMachineArn XXXX
    # XXXX stateMachineName XXXX
    # analysis.id
    # analysis.assay
    # analysis.analyte
    # analysis.matchType
    # analysis.cancerCohort

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--orderhub_ids', type=str,
                        required=True, help='file with a list of orderhub ids')
    parser.add_argument('-l', '--logs_dir', type=str,
                        required=True, help='directory with BiPS logs')
    parser.add_argument('-o', '--output', type=str,
                        required=True, help='BiPS log JSON to CSV')
    return parser.parse_args()


def main():

    # get arguments
    args = get_args()
    orderhub_ids = args.orderhub_ids
    logs_dir = args.logs_dir
    output = args.output

    # get list of orderhub ids
    orderhub_id_list = get_orderhub_id_list(orderhub_ids)
    csv_dict = {}

    # iterate through bips logs for each orderhub id log file
    json_dict = defaultdict(dict)
    for orderhub_id in orderhub_id_list:
        log_file = os.path.join(logs_dir, orderhub_id + '.log')
        if os.path.exists(log_file):
            print('Processing log file: {}'.format(log_file))
            extracted_fields_headers, extracted_fields_values = parse_bips_log(log_file, orderhub_id)
            csv_dict[orderhub_id] = extracted_fields_values
        else:
            print('No log file for: {}'.format(log_file))

    # add 'orderhub_id' to the beginning of the headers
    extracted_fields_headers.insert(0, 'orderhub_id')
    # write parsed BiPS log data to a CSV file 
    write_to_csv(extracted_fields_headers,
                 csv_dict,
                 output)


def get_orderhub_id_list(orderhub_ids):
    '''
    Read in a file with a list of orderhub ids
    @param orderhub_ids: file with a list of orderhub ids
    @return orderhub_id_list: list of orderhub ids
    '''
    with open(orderhub_ids, 'r') as f:
        orderhub_id_list = f.read().splitlines()
    return orderhub_id_list

def parse_bips_log(bips_log_file,
                   orderhub_id):
    '''
    Parse a BiPS log file (JSON) 
    @param bips_log_file: BiPS log file (JSON)
    @param orderhub_id: orderhub id

    '''
    extracted_fields_headers = []
    extracted_fields_values = []

    df = pd.read_json(bips_log_file)
    
    # extract information from fields under input.input.janeAdapter
    input_input_janeAdapter = df['input']['input']['janeAdapter']
    for sub_category in input_input_janeAdapter:
        sub_category_value = input_input_janeAdapter[sub_category]

        # extract information from fields under input.input.janeAdapter.assets
        if sub_category == 'assets':
            for asset in sub_category_value:
                asset_id = asset['assetId']
                gcsurl = asset['gcsUrl']
                # remove "['" and "']" from gcsurl
                gcsurl = gcsurl.replace("['", "")
                gcsurl = gcsurl.replace("']", "")
                tissue_classification = asset['tissueClassification']
                tissue_source = asset['tissueSource']
                tissue_type = asset['tissueType']
                coverage = asset['coverage']
                extracted_fields_headers.append('assetID')
                extracted_fields_headers.append('gcsurl')
                extracted_fields_headers.append('tissueClassification')
                extracted_fields_headers.append('tissueSource')
                extracted_fields_headers.append('tissueType')
                extracted_fields_headers.append('coverage')
                extracted_fields_values.append(asset_id)
                extracted_fields_values.append(gcsurl)
                extracted_fields_values.append(tissue_classification)
                extracted_fields_values.append(tissue_source)
                extracted_fields_values.append(tissue_type)
                extracted_fields_values.append(coverage)
        
        elif sub_category == 'transformOverrides':
            for override_tuple in input_input_janeAdapter[sub_category]:
                override_workflow = override_tuple['workflow']
                override_transformId = override_tuple['transformId']
                extracted_fields_headers.append('transformOverrideWorkflow.' + override_workflow)
                extracted_fields_values.append(override_transformId)
        else:
            if sub_category == 'cloudDestination':
                sub_category_value = sub_category_value[0].replace("'", "")
                sub_category_value = sub_category_value[0].replace("'", "")
            
            extracted_fields_headers.append(sub_category)
            extracted_fields_values.append(sub_category_value)

    # # extract stateMachineArn and stateMachineName
    # stateMachineArn = df['stateMachineArn']
    # stateMachineName = df['stateMachineName']
    # extracted_fields_headers.append('stateMachineArn')
    # extracted_fields_headers.append('stateMachineName')
    # extracted_fields_values.append(stateMachineArn)
    # extracted_fields_values.append(stateMachineName)

    # extract information from fields under analysis
    analysis = df['analysis']
    extracted_fields_headers.append('analysis.id')
    extracted_fields_values.append(analysis['id'])
    extracted_fields_headers.append('analysis.assay')
    extracted_fields_values.append(analysis['assay'])
    extracted_fields_headers.append('analysis.analyte')
    extracted_fields_values.append(analysis['analyte'])
    extracted_fields_headers.append('analysis.matchType')
    extracted_fields_values.append(analysis['matchType'])
    extracted_fields_headers.append('analysis.cancerCohort')
    extracted_fields_values.append(analysis['cancerCohort'])

    # check that header and values have the same length
    if len(extracted_fields_headers) != len(extracted_fields_values):
        print('Error: extracted fields headers and values have different lengths')
        sys.exit(1)

    return extracted_fields_headers, extracted_fields_values

def write_to_csv(extracted_fields_headers,
                 csv_dict,
                 output):
    '''
    Write extracted fields to a CSV file
    @param headers: list of headers
    @param values: list of values
    @param output: output CSV file
    '''
    with open(output, 'w') as f:
        f.write(','.join(extracted_fields_headers) + '\n')
        print(','.join(extracted_fields_headers) + '\n')
        for orderhub_id in csv_dict:
            f.write(orderhub_id + ',')
            print(orderhub_id + ',')
            f.write(','.join([str(x) for x in csv_dict[orderhub_id]]) + '\n')
            print(','.join([str(x) for x in csv_dict[orderhub_id]]) + '\n')

if __name__ == '__main__':
    main()