main_dir=$1
bips_csv=$2
dps_log_dir=$3

# get the analysis.id from the bips csv output and search for the analysis.id in dps
python software/extract_id.py \
    -i $bips_csv \
    -o $main_dir/ids.txt

# write the output from a dps search 
# (by analysis id or executio id) to a file named by the analysis id

if [ ! -d $dps_log_dir ]; then
    mkdir $dps_log_dir
fi

for i in $(cat $main_dir/ids.txt); do
    echo $i
    dps search \
        -m analysis-id=$i | tee $dps_log_dir/$i.json
done

# iterate through the dps logs and extract the data products
