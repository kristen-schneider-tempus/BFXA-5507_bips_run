# BFXA-5507_bips_run
[Link to jira ticket](https://tempuslabs.atlassian.net/jira/software/c/projects/BFXA/boards/1249?assignee=712020%3Afe369597-023a-4144-a1f8-84df1cca7bd4&selectedIssue=BFXA-5606&useStoredSettings=true) 

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
    /paht/to/GBQ_output.csv
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
    /paht/to/GBQ_output.csv
    <assay>
    <analyte>
```
## Step 4: Transform the bioinf_db Google BigQuery (or DataGrip) to BiPS input
TODO: finish the script to transform the bioinf_db Google BigQuery (or DataGrip) to BiPS input
The output from the Google BigQuery search needs to be transformed into an acceptable format for BiPS as input. See example BiPS input [here](https://drive.google.com/drive/folders/1ppnUbq6udZSWzeRJ_zx5xv92QstRfC-3). 

```
python transform_bips_input.py
    - i TODO
    - o TODO
    - ... TODO
```

## Step 5: Run BiPS
[BiPS](https://docs.google.com/document/d/1VwEUHJdGHYeyPJwR0_43xiAnZmye46Vmo6CFVyXw7OQ/edit?tab=t.0) is a Tempus pipeline tool that is used to ...TODO
- Read more about BiPS [here](https://github.com/tempuslabs/bioinf-analysis-utils/tree/develop/doc/src/orch/bips_adapter).
- Find examples for BiPS input and transformoverride [here](https://drive.google.com/drive/folders/1TuARTyG3x3z9KszmUMZRuxvE5A1F6Wlc).
- Look in splunk [here](https://tempus.splunkcloud.com/en-US/app/search/transform_execution_and_logs_by_analysis_id?form.timespan.earliest=-24h&form.log_type_token=NOT%20loggerName%3Dtransformhub.lib.transform-harness.harness.transform-harness&form.log_type_token=NOT%20loggerName%3Dtransformhub.lib.dps.dps-provider&form.severity_token=level%3Ddebug&form.severity_token=level%3Dinfo&form.severity_token=level%3D%22warn*%22&form.severity_token=level%3Derror&form.selectedanalysisid=agkhkshxzjfn3gxvjcibo2ba5m) and [here](https://tempus.splunkcloud.com/en-US/app/search/cs_transformhub_transforms_by_execution_id?form.timespan.earliest=%40y&form.timespan.latest=now&form.log_type_token=NOT%20loggerName%3Dopt.tempus.transform.harness.node_modules.%40tempus.transformhub-tools.dist.lib.utils.performance-measures&form.log_type_token=NOT%20loggerName%3Dtransformhub.lib.dps.dps-provider&form.severity_token=level%3Derror&form.execution_id=d20178f7-0ac4-4611-8908-d8d86addc1c6) for more information about an BiPS run.

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

## Step 6: Conver BiPS output logs into a csv

# BFXA-562_MYB_execution
[Link to jira ticket](https://tempuslabs.atlassian.net/browse/BFXA-5655?atlOrigin=eyJpIjoiOTZmYTYwNmJjYmFjNDM1ZmE2OGM0YTVjMjY4YjcxZjciLCJwIjoiaiJ9)
[HOWTO execute xR IVD MYB-Mike Skaro](https://docs.google.com/spreadsheets/d/1oLOWrjKuH02oPkxUlfY7oEnN2jDbKNXWFIXBLEXbutM/edit?gid=0#gid=0)

[MYB-poison-exon-detecction Repository](https://github.com/tempuslabs/bioinf-myb-poison-exon-detection])

## Step 1: Get list of sample IDs from BiPS output csv
Use the output from the BiPS run to extract the sample IDs (analysis-id).
```
python software/extract_id
    -i bips_output.csv
    -o sample_ids.txt
```

## STEP 2:

```
nohup ./rp-flow/runFromSampleSheet.sh
    sameple_ids.txt
    output.txt &
```

## Step 3: 
- Check the output.txt for `analysis-id,dataProductType,dataProductID`
- Check nohup.out for a series of JSON files concatenated between run status.
- !! Wait for MYB to complete running !!
### TODO: add which analysis-id to look for in output, nohub, and slack
- Check status on slack [`#rp-flow-nf-bet channel`](https://tempuslabs.enterprise.slack.com/archives/C078RJ27A1J).
- Check status in [GC Job List](https://console.cloud.google.com/batch/jobs?invt=AboEhQ&project=tl-8ud1o1f9kjgpk29tjvkx))

## Step 4: 
```
mkdir dataProducts
./rp-flow/parseSampleSheetoutput.sh 
    nohup.out
gunzip dataProducts/*.gz
./rp-flow/concatenateDataProducts.sh
    dataProducts/
```
`combinedData.tsv` should appear in working directory.

