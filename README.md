# BFXA-5507_bips_run
[Link to jira ticket](https://tempuslabs.atlassian.net/jira/software/c/projects/BFXA/boards/1249?assignee=712020%3Afe369597-023a-4144-a1f8-84df1cca7bd4&selectedIssue=BFXA-5606&useStoredSettings=true) 

## Step 1: Look in bioinf_db for the orderhubIds of interest
### GOOGLE BIGQUERY
```
SELECT distinct a.id as analysis_id, isolate_id, orderhub_id, patient_id, run_id, a.assay, fastq_url
FROM tl-zbxsrcj1dc7fc02q7htg.src_bioinformatics.analysis a
         join tl-zbxsrcj1dc7fc02q7htg.src_bioinformatics.analysis_run ar on ar.analysis_id = a.id
         join tl-zbxsrcj1dc7fc02q7htg.src_bioinformatics.analysis_isolate ai on ai.analysis_id = a.id
         join tl-zbxsrcj1dc7fc02q7htg.src_bioinformatics.analysis_output ao on ao.analysis_id = a.id
         join tl-zbxsrcj1dc7fc02q7htg.src_bioinformatics.workflow w on w.analysis_id = ao.analysis_id
where a.orderhub_id in ("24klbrrb","24igsasz","24jmbscz")
```

## Step 2: Transform the bioinf_db Google BigQuery (or DataGrip) to BiPS input
The output from the Google BigQuery search needs to be transformed into an acceptable format for BiPS as input. See example BiPS input [here](/Users/kristen.schneider/Research/unattached_tickets/BFXA-5507_bips_run/data/bips_input/bips_input.csv)

```
python transform_bips_input.py
    - i TODO
    - o TODO
    - ... TODO
```

## Step 3: Run BiPS
[BiPS](https://docs.google.com/document/d/1VwEUHJdGHYeyPJwR0_43xiAnZmye46Vmo6CFVyXw7OQ/edit?tab=t.0) is a Tempus pipeline tool that is used to ...TODO
Read more about BiPS [here](https://github.com/tempuslabs/bioinf-analysis-utils/tree/develop/doc/src/orch/bips_adapter). Look in splunk [here](https://tempus.splunkcloud.com/en-US/app/search/transform_execution_and_logs_by_analysis_id?form.timespan.earliest=-24h&form.log_type_token=NOT%20loggerName%3Dtransformhub.lib.transform-harness.harness.transform-harness&form.log_type_token=NOT%20loggerName%3Dtransformhub.lib.dps.dps-provider&form.severity_token=level%3Ddebug&form.severity_token=level%3Dinfo&form.severity_token=level%3D%22warn*%22&form.severity_token=level%3Derror&form.selectedanalysisid=agkhkshxzjfn3gxvjcibo2ba5m) and [here](https://tempus.splunkcloud.com/en-US/app/search/cs_transformhub_transforms_by_execution_id?form.timespan.earliest=%40y&form.timespan.latest=now&form.log_type_token=NOT%20loggerName%3Dopt.tempus.transform.harness.node_modules.%40tempus.transformhub-tools.dist.lib.utils.performance-measures&form.log_type_token=NOT%20loggerName%3Dtransformhub.lib.dps.dps-provider&form.severity_token=level%3Derror&form.execution_id=d20178f7-0ac4-4611-8908-d8d86addc1c6) for more information about an BiPS run.

```
TODO: finish the com
bash run_bips.sh
    -i orderhubIds.txt
    -o bips_output.csv
    -p bips_parameters.json
    -l path/to/bips_log_dir/
```
```
okta-personal-token get preview/sundial-staging
gcloud storage ls gs://tl-bet-sequencer-output-fastq-us/20250109-054454-352503-f79c61425a11/24-D67015_RSQ1.tar.gz
bips xxx-xxx-xxx-bips_input_manual.csv
    --transform-override-csv transform_override_rnaonco_v140_val.csv
    --env staging
```

## Step 4: Parse the BiPS log file
The BiPS log file is a JSON file that contains information about the BiPS run. The log file is generated by the BiPS software and contains information about the BiPS run, such as the analysis id, the parameters used, and the output files generated.

```
python parse_bips_log.py
    -i data/example/example_orderhubIds.txt
    -l data/example/example_bips_log.csv
    -o data/example/exaample_bips_log.csv
```

## Step 5: use dps search data products by name to locate type=sre-rna-qc-summary-stat data products from the pipeline-name=jane-rna-expression
```
dps search
    -m analysis-id=ANALYSIS-ID
    -m type=sre-rna-qc-summary-stat
    -m pipeline=jane-rna-expression…
```