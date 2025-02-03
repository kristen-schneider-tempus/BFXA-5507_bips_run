Table below in progress.

| PROCESS                  | DESCRIPTION                                                                                                                                                                                                 | HELPFUL SCRIPTS                       | INPUT                                                                 | OUTPUT                                                                                          | LINK                                                                                                      |
|--------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------|----------------------------------------------------------------------|-------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------|
| GBQ-search               | Search bioinf-db (via DataGrip or GoogleBigQuery) for a provided list of order hub IDs.                                                                                                                      | `orderuhub_bigquery.sql`, `gbq-code.ipynb`               | List of order hub IDs                                                | CSV with analysisID, isolateID, orderhubID, patientID, runID, assay, fastqURL                              |  [Google BigQuery Search](## Step 1: Look in bioinf_db for the orderhubIds of interest)                                                                                                         |
| ts_to_ts (TODO)          | Transfer data from prod to bet, if necessary.                                                                                                                                                               |                                      |                                                                      |                                                                                                             | Write script for this process                                                                             |
| unique                   | Parse the GBQ-search.output (CSV) for a unique set of samples to process.                                                                                                                                   | `filter_unique.sh`                     | GBQ-search.output (CSV)                                              | Similar to GBQ-search.output; but removed redundant samples. **DATA IN THIS FILE IS HELPFUL FOR FINAL SUMMARY FILE** |                                                                                                           |
| to_BIPS | Format the unique set of samples into a BIPs input format. Add an analyte column, change the fastq url column header, and optionally check the assay to assert that it matches the BIPs input format. | `transform_to_bips.sh`                           | unique.output (CSV) *see bips_input.csv example                      | BIPs input csv. **DATA IN THIS FILE IS HELPFUL FOR FINAL SUMMARY FILE**                                    | Generalize this workflow                                                                                   |
| run_BIPS (under maintenance) | Run BIPS with the properly formatted input CSV file from to_BIPS.output and a provided transform override.                                                                                              | `run_bips.sh`                          | to_BIPS.output transform_override_rnaonco…                           | BIPS_logs/ orderhubID_A.log orderhubID_B.log orderhubID_C.log …                                            | Generalize this workflow                                                                                   |
| parse_bips               | Parse the BIPS log files into one CSV with relevant information. The extracted fields from this step can be modified to include more, fewer, or different information.                                       | `parse_bips_log.py`                    | BIPS_logs/ orderhubID_A.log orderhubID_B.log orderhubID_C.log …      | parsed_bips.csv **DATA IN THIS FILE IS HELPFUL FOR FINAL SUMMARY FILE**                                    | Make this generalizable for more than one data product type (e.g. input of interesting data products)      |
| get_sample_ids           | Get a list of analysis (workflow) IDs from the parse_bips.csv file                                                                                                                                          | `extract_id.py`                        | parsed_bips.csv                                                     | sample_ids.csv                                                                                             |                                                                                                           |
| run_MYB                  | Execute MYB on the set of sample ID                                                                                                                                                                         | bioinf-myb-poison-exon-detection runFromSampleSheet.sh |                                                                      | nohup.out - JSON-esc output output.txt - analysis-id, dp-type, dp-id                                       |                                                                                                           |
| parse_nohup              | Get relevant information from nohup.out nexflowSessionID, sre_star_splice_junction (dp ID) sre_bam_rna_pseudobam (dp ID) sre_rna_qc_summary_stat (dp ID)                                                    | parseNoHupOut.sh                     | nohup.out                                                           | parsedNoHup.csv **DATA IN THIS FILE IS HELPFUL FOR FINAL SUMMARY FILE**                                    | Make this generalizable for more than one data product type (e.g. input of interesting data products)      |
| download_dp              | Get the nexflowSessionID from nohup.out DPS search using workflow-id=nexflowSessionID Download the dataproductID for rfnd-combined-myb-expression                                                           | parseSampleSheetouput.sh             | nohup.out dataProducts/                                              | dataProducts/ dataProductID_A.tsv(.gz) dataProductID_B.tsv(.gz) dataProductID_C.tsv(.gz) …                 | Make this generalizable for more than one data product type (e.g. input of interesting data products)      |
| concat_dp                | Take the information from each data product file and write them all with one header to the same output. Include the dataProductID to a column at the beginning for tracking.                                 | concatenateDataProducts.sh           | dataProducts/ dataProductID_A.tsv(.gz) dataProductID_B.tsv(.gz) dataProductID_C.tsv(.gz) … | combinedData.tsv **DATA IN THIS FILE IS HELPFUL FOR FINAL SUMMARY FILE**                                    |                                                                                                           |
| final_merge (under maintenance) | Create a final output file which includes information relevant to the entire run (e.g. order hub ID, analysis-id, analyte, …, dataProductID, etc.)                                                   | create_final_output.py               |                                                                      |                                                                                                             |                                                                                                           |


# BIPS run
[Link to jira ticket BFXA-5507](https://tempuslabs.atlassian.net/jira/software/c/projects/BFXA/boards/1249?assignee=712020%3Afe369597-023a-4144-a1f8-84df1cca7bd4&selectedIssue=BFXA-5606&useStoredSettings=true) 

## Step 1: Look in bioinf_db for the orderhubIds of interest
### Google BigQuery
Given a list of orderhub IDs, look in the bioinf_db for analysis IDs, fastq URLs, etc.
See `software/orderhub_bigquery.sql` for the same query as below.
```
SELECT distinct a.id as analysis_id, isolate_id, orderhub_id, patient_id, run_id, a.assay, fastq_url
FROM tl-zbxsrcj1dc7fc02q7htg.src_bioinformatics.analysis a
         join tl-zbxsrcj1dc7fc02q7htg.src_bioinformatics.analysis_run ar on ar.analysis_id = a.id
         join tl-zbxsrcj1dc7fc02q7htg.src_bioinformatics.analysis_isolate ai on ai.analysis_id = a.id
         join tl-zbxsrcj1dc7fc02q7htg.src_bioinformatics.analysis_output ao on ao.analysis_id = a.id
         join tl-zbxsrcj1dc7fc02q7htg.src_bioinformatics.workflow w on w.analysis_id = ao.analysis_id
where a.orderhub_id in ("24klbrrb","24igsasz","24jmbscz", ...)
```

## Step 2.1: Check if the samples exist in beta
Use the output from the Google BigQuery search to check if the samples exist in beta.
```
bash software/check_gcloud.sh 
    /path/to/GBQ_output.csv
```

## Step 2.2: ts to ts transfer if samples do not exist in beta
Use the output from the Google BigQuery search to transfer the samples from ts to ts if they do not exist in beta.
```
TODO: finish the script to transfer the samples from ts to ts
```

## Step 3: find unique set of samples with a given assay and analyte
Use the output from the Google BigQuery search to find the unique set of samples with a given assay and analyte.
```
bash software/filter_unique.sh 
    /path/to/GBQ_output.csv
    <assay>
    <analyte>
```
## Step 4: Transform the bioinf_db Google BigQuery (or DataGrip) to BIPS input
TODO: finish the script to transform the bioinf_db Google BigQuery (or DataGrip) to BIPS input
The output from the Google BigQuery search needs to be transformed into an acceptable format for BIPS as input. See example BIPS input [here](https://drive.google.com/drive/folders/1ppnUbq6udZSWzeRJ_zx5xv92QstRfC-3). 

```
python software/transform_to_bips.py 
    -i data/BFXA-5655/bquxjob_1d14aa3c_194a7ee210d_unique.csv 
    -o kristen_bips_input.csv 
    -l bet 
    -c "Adenoid Cystic Carcinoma" 
    -a RNA-onco.v1 
    -n rna 
    -m tumorOnly 
    -t rad
```

## Step 5: Run BIPs
[BIPS](https://docs.google.com/document/d/1VwEUHJdGHYeyPJwR0_43xiAnZmye46Vmo6CFVyXw7OQ/edit?tab=t.0) is a Tempus pipeline tool that is used to ...TODO
- Read more about BIPS [here](https://github.com/tempuslabs/bioinf-analysis-utils/tree/develop/doc/src/orch/bips_adapter).
- Find examples for BIPS input and transformoverride [here](https://drive.google.com/drive/folders/1TuARTyG3x3z9KszmUMZRuxvE5A1F6Wlc).
- Look in splunk [here](https://tempus.splunkcloud.com/en-US/app/search/transform_execution_and_logs_by_analysis_id?form.timespan.earliest=-24h&form.log_type_token=NOT%20loggerName%3Dtransformhub.lib.transform-harness.harness.transform-harness&form.log_type_token=NOT%20loggerName%3Dtransformhub.lib.dps.dps-provider&form.severity_token=level%3Ddebug&form.severity_token=level%3Dinfo&form.severity_token=level%3D%22warn*%22&form.severity_token=level%3Derror&form.selectedanalysisid=agkhkshxzjfn3gxvjcibo2ba5m) and [here](https://tempus.splunkcloud.com/en-US/app/search/cs_transformhub_transforms_by_execution_id?form.timespan.earliest=%40y&form.timespan.latest=now&form.log_type_token=NOT%20loggerName%3Dopt.tempus.transform.harness.node_modules.%40tempus.transformhub-tools.dist.lib.utils.performance-measures&form.log_type_token=NOT%20loggerName%3Dtransformhub.lib.dps.dps-provider&form.severity_token=level%3Derror&form.execution_id=d20178f7-0ac4-4611-8908-d8d86addc1c6) for more information about an BIPS run.

```
TODO: finish the script to runs bips
bash software/run_bips.sh
    -i orderhubIds.txt
    -o bips_output.csv
    -p bips_parameters.json
    -l path/to/bips_log_dir/
```
```
okta-personal-token get preview/sundial-staging
gcloud storage ls <gcsurl>
# might need to move into bioinf-analysis-utils/bioinf-analysis-utils-orch/
bips xxx-xxx-xxx-bips_input.csv
    --transform-override-csv transform_override_rnaonco_v140_val.csv
    --env staging
```

## Step 6: Convert BIPs output logs into a csv

# MYB_execution
[Link to jira ticket BFXA-5655](https://tempuslabs.atlassian.net/browse/BFXA-5655?atlOrigin=eyJpIjoiOTZmYTYwNmJjYmFjNDM1ZmE2OGM0YTVjMjY4YjcxZjciLCJwIjoiaiJ9)

[HOWTO execute xR IVD MYB-Mike Skaro](https://docs.google.com/spreadsheets/d/1oLOWrjKuH02oPkxUlfY7oEnN2jDbKNXWFIXBLEXbutM/edit?gid=0#gid=0)

[MYB-poison-exon-detecction Repository](https://github.com/tempuslabs/bioinf-myb-poison-exon-detection])

## Step 1: Get list of sample IDs from BIPS output csv
Use the output from the BIPS run to extract the sample IDs (analysis-id).
```
python software/extract_id
    -i bips_output.csv
    -o sample_ids.txt
```

## STEP 2:

```
nohup ./rp-flow/runFromSampleSheet.sh
    sample_ids.txt
    output.txt &
```

## Step 3: 
- Check the output.txt for `analysis-id,dataProductType,dataProductID`
- Check nohup.out for a series of JSON files concatenated between run status.
- !! Wait for MYB to complete running !!
### TODO: add which analysis-id to look for in output, nohub, and slack
- Check status on slack [`#rp-flow-nf-bet channel`](https://tempuslabs.enterprise.slack.com/archives/C078RJ27A1J).
- Check status in [GC Job List](https://console.cloud.google.com/batch/jobs?invt=AboP2g&project=tl-8ud1o1f9kjgpk29tjvkx&inv=1)). _I like to search for "myb-poison" in the search bar to find the jobs that I ran_.
- Connecting #rp-flow-nf-bet to job list to dps search...
---------------
-  Go to the job list and find the ID at the end of the Job name
- Go to #rp-flow-nf-bet and search for the ID (taskId)
- In the nohup.out file, there will be a session id associated with id / analysis-id


## Step 4: 
Parse nohup.out to get a list of `nextflowSessionId,rfnd-combined-myb-expression-features,sre_star_splice_junction,sre_expression_gene_normalized,sre_bam_rna_pseudobam,sre_rna_qc_summary_stat`.
```
./rp-flow/parseNoHup.sh
    nohup.out
    parsedNoHup.csv
```

## Step 5:
Download the data products matching `type=rfnd-combined-myb-expression-features`
```
mkdir dataProducts

./rp-flow/parseSampleSheetoutput.sh
    nohup.out

gunzip dataProducts/*.gz
```

Internally, `parseSampleSheetoutput.sh` is running:
```
# Get a list of unique nextflowSessionIds
nextflowSessionId="$(grep 'nextflowSessionId' $input_data | 
    cut -f 2 -d ":" | 
    tr -d ' ' | 
    tr -d '"' | 
    tr -d ',')"

# search for data product rfnd-combined-myb-expression-features by using the nexflowSessionId as the workflow
dataProductID="$(dps search --metadata workflow-id=$record -m type=rfnd-combined-myb-expression-features |
    grep '"id":' |
    head -n 1 |
    cut -f 2 -d ":" | 
    tr -d ' ' | 
    tr -d '"' | 
    tr -d ',')"

# download the data product by its id
dps download 
    --id $dataProductID 
    --download-dir "dataProducts/"
```

## Step 6:
Combine the `type=rfnd-combined-myb-expression-features` data products into a single file
```
./rp-flow/concatenateDataProducts.sh
    dataProducts/
```
`combinedData.tsv` should appear in working directory.