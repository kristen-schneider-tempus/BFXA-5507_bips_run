#!/bin/bash

# Kristen Schneider
# Date: 2025-01-18
# Purpose: Run a full BIPS analysis from start to finish

# # PREREQUISITES ##
# - Use Google BigQuery to get the full BIPS dataset
# - Transform the dataset to a format that can be used by the BIPS analysis

## TODO JSON INPUT NOT WORKING
# # Input file (JSON)
# bips_run_config_json="/Users/kristen.schneider/Research/unattached_tickets/BFXA-5507_bips_run/data/example/full_input.json"
# # Extract necessary data from input JSON file
# orderhub_ids_txt=$(jq '.input.orderhub_ids' $bips_run_config_json)
# echo $orderhub_ids_txt

# INPUT FILES
orderhub_ids_txt="/Users/kristen.schneider/Research/unattached_tickets/BFXA-5507_bips_run/data/orderhub_ids.txt"
bips_logs="/Users/kristen.schneider/Research/unattached_tickets/BFXA-5507_bips_run/results/log/"
parse_bips_log_py="/Users/kristen.schneider/Research/unattached_tickets/BFXA-5507_bips_run/software/parse_bips_log.py"

# OUTPUT FILES
run_ids_txt="/Users/kristen.schneider/Research/unattached_tickets/BFXA-5507_bips_run/results/run_ids.txt"
data_products_dir="/Users/kristen.schneider/Research/unattached_tickets/BFXA-5507_bips_run/results/data_products/"

# 1. Run the BIPS analysis
# TODO echo "Running BIPS analysis"

# 2. Get the analysis ID or execution ID from the BiPS log file
echo "Getting the analysis ID or execution ID from the BiPS log file"
# clear contents of run_ids.txt
> $run_ids_txt
# for a list of orderhub_ids, get the analysis_id or execution_id
while IFS= read -r orderhub_id; do
    orderhub_id_log="${bips_logs}${orderhub_id}.log"
    # run parse_bips_log_py.py get_run_id on the log file
    echo "Getting the run ID for orderhub_id: $orderhub_id"
    python $parse_bips_log_py "run_id" $orderhub_id_log "analysis" $run_ids_txt
done < $orderhub_ids_txt

# 3. Get data products for the analysis ID or execution ID
echo "Getting data products for the run IDs"
# check if the run_ids.txt file is empty
if [ -s $run_ids_txt ]; then
    # for a list of run_ids, get the data products
    while IFS= read -r run_id; do
        # run parse_bips_log_py.py get_data_products on the log file
        echo "Getting the data products for run ID: $run_id"
    done < $run_ids_txt
else
    echo "No run IDs found in the log files"
fi




