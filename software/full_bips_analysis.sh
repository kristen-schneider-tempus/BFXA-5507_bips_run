# 0. Use Google BigQuery to get the full BIPS dataset
# 0. Transform the dataset to a format that can be used by the BIPS analysis

input_json="/Users/kristen.schneider/Research/unattached_tickets/BFXA-5507_bips_run/data/example/full_input.json"
# 1. Run the BIPS analysis
echo "Running BIPS analysis"
jq '.input.bips_input' $input_json