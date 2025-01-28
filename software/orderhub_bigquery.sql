-- Google BigQuery code to parse the bioinf-db data for a given list of orderhub_ids
SELECT distinct a.id as analysis_id, isolate_id, orderhub_id, patient_id, run_id, a.assay, fastq_url
FROM tl-zbxsrcj1dc7fc02q7htg.src_bioinformatics.analysis a
         join tl-zbxsrcj1dc7fc02q7htg.src_bioinformatics.analysis_run ar on ar.analysis_id = a.id
         join tl-zbxsrcj1dc7fc02q7htg.src_bioinformatics.analysis_isolate ai on ai.analysis_id = a.id
         join tl-zbxsrcj1dc7fc02q7htg.src_bioinformatics.analysis_output ao on ao.analysis_id = a.id
         join tl-zbxsrcj1dc7fc02q7htg.src_bioinformatics.workflow w on w.analysis_id = ao.analysis_id
where a.orderhub_id in ("24jmbscz","24klbrrb","24igsasz")