# BFXA-5507_bips_run
We need to evaluate the sre-rna-qc-summary-stats from 2 samples of rna.

To accomplish this task you will:


Use orderhubIDs to search for fastq files in bioinf-db

Use the fastq files as the inputs into bips

download and supply override csv to bips for workflow execution

collect execution information from log files

Use dps to search data products by name / data product ID to locate type=sre-rna-qc-summary-stat data products from the pipeline-name=jane-rna-expression 

write a python / shell / R script to combine and annotate the files such that you have a csv result
 

HOWTOs:


dps search -m analysis-id=ANALYSIS-ID -m type=… -m pipeline=…. 
 

Cleaned outcome annotation:

analysis-id,dataProductType,dataProductID

 

Data to search:

orderhub_id

24klbrrb

24igsasz

