unique_samples=$1
bips_input=$2
bips_output=$3
parsed_nohup_output=$4
combined_output=$5
final_output=$6

# get the orderhub_ids and anlaysis ids from the unique samples file

# find index of the orderhub_id and analysis_id in the bips_input file (csv)
orderhub_id_index=$(head -n 1 $unique_samples | tr ',' '\n' | grep -n "orderhub_id" | cut -d: -f1)
analysis_id_index=$(head -n 1 $unique_samples | tr ',' '\n' | grep -n "analysis_id" | cut -d: -f1)

echo "orderhub_id_index: $orderhub_id_index"
echo "analysis_id_index: $analysis_id_index"

# get the orderhub_ids and analysis ids from the unique samples file
orderhub_ids=$(tail -n +2 $unique_samples | cut -d, -f$orderhub_id_index)
analysis_ids=$(tail -n +2 $unique_samples | cut -d, -f$analysis_id_index)

# for each orderhub_id get the record in the bips input file and save it as a tmp record

