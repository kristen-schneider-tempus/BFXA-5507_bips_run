unique_samples=$1
bips_input=$2
bips_output=$3
nohup_output=$4
combined_output=$5
final_output=$6

# get the orderhub_ids and anlaysis ids from the unique samples file

# find index of the orderhub_id and analysis_id in the bips_input file
orderhub_id_index=$(head -n 1 $bips_input | tr '\t' '\n' | grep -n "orderhub_id" | cut -d ":" -f 1)
analysis_id_index=$(head -n 1 $bips_input | tr '\t' '\n' | grep -n "analysis_id" | cut -d ":" -f 1)

echo "orderhub_id_index: $orderhub_id_index"
echo "analysis_id_index: $analysis_id_index"
