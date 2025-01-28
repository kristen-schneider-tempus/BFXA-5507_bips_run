# TODO step 1: run the bioinf-db to bips input script once it's more robust

# step 2: run bips
input_bips_csv=$1
transform_override_csv=$2

bips $input_bips_csv
    --transform-override-csv $transform_override_csv
    --env staging
    # --log_dir /Users/kristen.schneider/Research/unattached_tickets/BFXA-5507_bips_run/results/log
