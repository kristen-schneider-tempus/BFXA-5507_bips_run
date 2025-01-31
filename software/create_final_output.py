import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Create final output file to keep track of data from MYB run.')
    parser.add_argument('-u', '--unique', type=str, help='The unique set of data from GBQ search')
    parser.add_argument('-b', '--bips_input', type=str, help='The file used as input for BIPS')
    parser.add_argument('-l', '--bips_output', type=str, help='Parsed BIPS output logs')
    parser.add_argument('-n', '--nohup_output', type=str, help='The parsed output file from MYB (parsedNoHup.out)')
    parser.add_argument('-c', '--combinedDataProdudcts', type=str, help='Combined data products file')
    parser.add_argument('-o', '--output', type=str, help='Output file')
    return parser.parse_args()

def main():
    args = parse_args()

    unique_orderhub_ids = args.unique
    bips_input = args.bips_input
    bips_output = args.bips_output
    nohup_output = args.nohup_output
    combined_data_products = args.combinedDataProdudcts
    final_output = args.output

    unique_ohid_info, unique_anid_info = read_unique_input(unique_orderhub_ids)
    bips_ohid_info = read_bips_input(bips_input)



def read_unique_input(unique_orderhub_ids):
    '''
    Read the unique file and store the information in a dictionary.

    @param unique_orderhub_ids: The file containing unique sample information
    @return unique_ohid_dict: A dictionary containing the unique orderhub ids as keys and the rest of the information as values
    @return unique_anid_dict: A dictionary containing the unique analysis ids as keys and the rest of the information as values
    '''

    # header in the unique file
    # analysis_id,isolate_id,orderhub_id,patient_id,run_id,assay,fastq_url  

    unique_ohid_dict = {}
    unique_anid_dict = {}

    with open(unique_orderhub_ids, 'r') as f:
        header = f.readline().strip().split(',')
        for line in f:
            line = line.strip().split(',')
            analysis_id = line[0]
            isolate_id = line[1]
            orderhub_id = line[2]
            patient_id = line[3]
            run_id = line[4]
            assay = line[5]
            fastq_url = line[6]

            unique_ohid_dict[orderhub_id] = [analysis_id, isolate_id, patient_id, run_id, assay, fastq_url]
            unique_anid_dict[analysis_id] = [isolate_id, orderhub_id, patient_id, run_id, assay, fastq_url]

    return ohid_dict, anid_dict

def read_bips_input(bips_input):
    '''
    Read the BIPS input file and store the information in a dictionary.

    @param bips_input: The file containing the BIPS input
    @return bips_dict: A dictionary containing the orderhub ids as keys and the rest of the information as values
    '''

    # header in the BIPS input file
    # orderhub_id,gcs_tumor_fastq_url,cancer_type,assay,analyte,match_type,intent

    bips_dict = {}

    with open(bips_input, 'r') as f:
        header = f.readline().strip().split(',')
        for line in f:
            line = line.strip().split(',')
            orderhub_id = line[0]
            gcs_tumor_fastq_url = line[1]
            cancer_type = line[2]
            assay = line[3]
            analyte = line[4]
            match_type = line[5]
            intent = line[6]

            bips_dict[orderhub_id] = [gcs_tumor_fastq_url, cancer_type, assay, analyte, match_type, intent]

    return bips_dict


def read_bips_output(bips_output):
    '''
    Read the BIPS output file and store the information in a dictionary.

    @param bips_output: The file containing the BIPS output
    @return bips_output_ohid_dict: A dictionary containing the orderhub ids as keys and the rest of the information as values
    @return bips_output_anid_dict: A dictionary containing the analysis ids as keys and the rest of the information as values
    '''

    # header in the BIPS output file
        # orderhub_id,assay,analyte,matchType,cloudDestination,assetID,
        # gcsurl,tissueClassification,tissueSource,tissueType,coverage,
        # intent,orderLabId,patientId,orderhubId,orderhubItemId,urgency,
        # cancerCohort,cancerCohorts,isControl,controlSampleType,
        # assayVersion,flowCellId,isolateId,sampleClass,tumorPercentage,
        # transformOverrideWorkflow.altered_splicing,
        # transformOverrideWorkflow.expression_quant,
        # transformOverrideWorkflow.gene_quant,
        # transformOverrideWorkflow.gep_interpretation,
        # transformOverrideWorkflow.ihc_er_prediction,
        # transformOverrideWorkflow.ihc_pr_prediction,
        # transformOverrideWorkflow.rna_exp_alignment,
        # transformOverrideWorkflow.rna_fusion_align,
        # transformOverrideWorkflow.rna_fusion_annot,
        # transformOverrideWorkflow.rna_fusion_char,
        # transformOverrideWorkflow.rna_fusion_mojo,
        # transformOverrideWorkflow.rna_fusion_star,
        # transformOverrideWorkflow.rna_qc,
        # transformOverrideWorkflow.rna_qc_aggregate,
        # transformOverrideWorkflow.umi_deduplication,
        # analysis.id,analysis.assay,analysis.analyte,
        # analysis.matchType,analysis.cancerCohort

    bips_output_ohid_dict = {}
    bips_output_anid_dict = {}

    with open(bips_output, 'r') as f:
        header = f.readline().strip().split(',')
        for line in f:
            line = line.strip().split(',')
            orderhub_id = line[0]
            assay = line[1]
            analyte = line[2]
            matchType = line[3]
            cloudDestination = line[4]
            assetID = line[5]
            gcsurl = line[6]
            tissueClassification = line[7]
            tissueSource = line[8]
            tissueType = line[9]
            coverage = line[10]
            intent = line[11]
            orderLabId = line[12]
            patientId = line[13]
            orderhubId = line[14]
            orderhubItemId = line[15]
            urgency = line[16]
            cancerCohort = line[17]
            cancerCohorts = line[18]
            isControl = line[19]
            controlSampleType = line[20]
            assayVersion = line[21]
            flowCellId = line[22]
            isolateId = line[23]
            sampleClass = line[24]
            tumorPercentage = line[25]
            altered_splicing = line[26]
            expression_quant = line[27]
            gene_quant = line[28]
            gep_interpretation = line[29]
            ihc_er_prediction = line[30]
            ihc_pr_prediction = line[31]
            rna_exp_alignment = line[32]
            rna_fusion_align = line[33]
            rna_fusion_annot = line[34]
            rna_fusion_char = line[35]
            rna_fusion_mojo = line[36]
            rna_fusion_star = line[37]
            rna_qc = line[38]
            rna_qc_aggregate = line[39]
            umi_deduplication = line[40]
            analysis_id = line[41]
            analysis_assay = line[42]
            analysis_analyte = line[43]
            analysis_matchType = line[44]
            analysis_cancerCohort = line[45]

            bips_output_ohid_dict[orderhub_id] = [assay, analyte, matchType, cloudDestination,
                                                   assetID, gcsurl, tissueClassification, tissueSource,
                                                     tissueType, coverage, intent, orderLabId, patientId,
                                                       orderhubId, orderhubItemId, urgency, cancerCohort,
                                                         cancerCohorts, isControl, controlSampleType,
                                                           assayVersion, flowCellId, isolateId, sampleClass,
                                                             tumorPercentage, altered_splicing,
                                                               expression_quant, gene_quant, gep_interpretation,
                                                                 ihc_er_prediction, ihc_pr_prediction, rna_exp_alignment,
                                                                   rna_fusion_align, rna_fusion_annot, rna_fusion_char,
                                                                     rna_fusion_mojo, rna_fusion_star, rna_qc, rna_qc_aggregate,
                                                                       umi_deduplication, analysis_id, analysis_assay, analysis_analyte,
                                                                         analysis_matchType, analysis_cancerCohort]
            
            bips_output_anid_dict[analysis_id] = [orderhub_id, assay, analyte, matchType, cloudDestination,
                                                   assetID, gcsurl, tissueClassification, tissueSource,
                                                     tissueType, coverage, intent, orderLabId, patientId,
                                                       orderhubId, orderhubItemId, urgency, cancerCohort,
                                                         cancerCohorts, isControl, controlSampleType,
                                                           assayVersion, flowCellId, isolateId, sampleClass,
                                                             tumorPercentage, altered_splicing,
                                                               expression_quant, gene_quant, gep_interpretation,
                                                                 ihc_er_prediction, ihc_pr_prediction, rna_exp_alignment,
                                                                   rna_fusion_align, rna_fusion_annot, rna_fusion_char,
                                                                     rna_fusion_mojo, rna_fusion_star, rna_qc, rna_qc_aggregate,
                                                                       umi_deduplication, analysis_assay, analysis_analyte,
                                                                         analysis_matchType, analysis_cancerCohort]
            
    return bips_output_ohid_dict, bips_output_anid_dict

    


