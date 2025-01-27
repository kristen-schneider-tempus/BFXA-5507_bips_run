import argparse
from collections import defaultdict
import json
import os
import pandas as pd


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--dps_log_dir', type=str,
                        required=True, help='dps log directory')
    parser.add_argument('-o', '--data_products', type=str,
                        required=True, help='data products for all the dps logs')
    return parser.parse_args()

def main():
    args = get_args()

    dps_log_dir = args.dps_log_dir
    out_csv = args.data_products

    data_products = get_data_product_for_dir(dps_log_dir)
    write_data_products(data_products,
                        out_csv)


    return 0

def get_data_product_for_dir(dps_log_dir):
    '''
    Get the data products for all the dps logs
    @param dps_log_dir: dps log directory
    @return data_products: data products for all the dps logs
    '''
    # {id: [workflow, data_product, version]}
    data_product_dict = defaultdict(list)
    if os.path.isdir(dps_log_dir):
        for id in os.listdir(dps_log_dir):
            if id.endswith('.json'):
                analysis_id = id.replace('.json', '')
                data_product_dict[analysis_id] = get_data_product(dps_log_dir, id)
    
    return data_product_dict

def get_data_product(dps_log_dir, id):
    '''
    Get the data product for the dps log
    @param dps_log_dir: dps log directory
    @param id: id of the dps log
    @return data_product: data product for the dps log
    '''
    id_json = os.path.join(dps_log_dir, id)
    json_data = json.load(open(id_json))
    data_product = []
    for object in json_data:
        analysis_id = object['metadata']['analysis-id']
        data_product_type = object['metadata']['type']
        # workflow_id = object['metadata']['workflow-id']
        try:
            workflow_name = object['metadata']['workflow-name'] # not all the objects have this key
        except KeyError:
            workflow_name = 'default (all)'
        pipeline_version = object['metadata']['pipeline-version']
        producing_software_product_version = object['metadata']['producing-software-product-version']
        
        data_product.append([analysis_id,
                            workflow_name,
                            data_product_type,
                            pipeline_version,
                            producing_software_product_version])
        
    return data_product

def write_data_products(data_products,
                        out_csv):
    '''
    Write the data products to a csv file
    @param data_products: data products for all the dps logs
    '''
    header=['analysis_id', 'workflow_name', 'data_product_type', 'pipeline_version', 'producing_software_product_version']
    o = open(out_csv, 'w')
    o.write(','.join(header))
    o.write('\n')
    for id in data_products:
        for object in data_products[id]:
            o.write(','.join(object))
            o.write('\n')


if __name__ == '__main__':
    main()