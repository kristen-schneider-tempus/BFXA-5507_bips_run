bips_input_csv=$1
assay_type=$2
analyte_type=$3

id_col="orderhub_id"
asssay_col="assay"
analyte_col="analyte"

# make a unique output 
unique_output_csv=$(echo $bips_input_csv | sed 's/.csv/_unique.csv/g')

# check if bips_input_csv is a file
if [ ! -f $bips_input_csv ]; then
    echo "The input file does not exist"
    exit 1
fi

# for each record:
# 1. check if the record assay matches the assay_type
# 2. check if the record analyte matches the analyte_type
# 3. check if the record id is unique
# 4. write the record to the unique_output_csv

unique_id_list=()

# get the header
header=$(head -n 1 $bips_input_csv)
echo $header > $unique_output_csv

# get the column index of the id, assay, and analyte
id_col_index=$(echo $header | awk -F, -v col="$id_col" 'NR==1{for(i=1;i<=NF;i++)if($i==col)break; print i}')
assay_col_index=$(echo $header | awk -F, -v col="$asssay_col" 'NR==1{for(i=1;i<=NF;i++)if($i==col)break; print i}')
analyte_col_index=$(echo $header | awk -F, -v col="$analyte_col" 'NR==1{for(i=1;i<=NF;i++)if($i==col)break; print i}')

# get the unique records
awk -F, -v id_col_index="$id_col_index" -v assay_col_index="$assay_col_index" -v analyte_col_index="$analyte_col_index" -v id_col="$id_col" -v assay_type="$assay_type" -v analyte_col="$analyte_type" -v unique_output_csv="$unique_output_csv" '
    NR>1{
        if ($assay_col_index == assay_type && $analyte_col_index == analyte_type) {
            if (!($id_col_index in unique_id_list)) {
                unique_id_list[$id_col_index] = 1
                print $0 >> unique_output_csv
            }
        }
    }
' $bips_input_csv

# check if the unique_output_csv is empty
if [ $(wc -l $unique_output_csv | awk '{print $1}') -eq 1 ]; then
    echo "The unique output file is empty"
    exit 1
fi

