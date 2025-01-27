# # get the analysis.id from the bips csv output and search for the analysis.id in dps
# python extract_id.py \
#     -i restuls/bips_log.csv \
#     -o results/ids.txt

# write the output from a dps search 
# (by analysis id or executio id) to a file named by the analysis id
dps_log_dir="results/dps_logs"
if [ ! -d $dps_log_dir ]; then
    mkdir $dps_log_dir
fi

for i in $(cat results/ids.txt); do
    echo $i
    dps search \
        -m analysis-id=$i | tee $dps_log_dir/$i.json
done

# iterate through the dps logs and extract the data products
