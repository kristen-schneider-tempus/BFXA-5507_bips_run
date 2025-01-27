# for the list of files from the BiPS query, check if it is already in beta
# if not, a ts-to-ts transfer is needed

GoogleBQcsv=$1
echo "The input file is: " $GoogleBQcsv
# check if GoogleBQcsv is a file
if [ ! -f $GoogleBQcsv ]; then
    echo "The input file does not exist"
    exit 1
fi
fastq_column_title="fastq_url"

# Get the fastq URLs from the Google BigQuery CSV
fastq_urls=$(awk -F, -v col="$fastq_column_title" 'NR==1{for(i=1;i<=NF;i++)if($i==col)break} {print $i}' $GoogleBQcsv | tail -n +2)

# replace 'prd' with 'bet' in the fastq URLs
fastq_urls=$(echo $fastq_urls | sed 's/prd/bet/g')

# Check if the file exists in the GCS bucket
for fq in $fastq_urls; do
    if [ $(gcloud storage ls $fq | wc -l) -gt 0 ]; then
        # do nothing
        x=0
        echo "PASS"
    else
        echo "The file: " $fq
        echo "Does not exist in the Google Cloud Storage and needs to be transferred" 
        exit 1
    fi
done