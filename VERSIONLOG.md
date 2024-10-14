# Scilifelab_epps Version Log

## 20241014.1

For AVITI manifest generation: make PhiX manifest variant, fix udf typo, remove unused func, clarify var names

## 20241011.1

New project validator EPP

## 20241009.1

Improve AVITI run manifest generation with sample-level settings. No longer produce submanifests.

## 20241006.2

Improve aviti run parameter parser

## 20241006.1

Fix issue with empty Aviti runmanifest results in Lane nr 0

## 20241002.1

Fix bug with index checker EPP with preset index sets

## 20241001.1

Update index checker EPP to capture invalid bases

## 20240930.1

For AVITI manifest generation, assume idx2 > 12 cycles and no idx2 parsed means idx2 is UMI and add Ns to manifest.

## 20240925.1

Add 10X steps to comments-to-running-notes config.

## 20240924.2

Update method for fetching AVITI stats in the BCL conversion step

## 20240924.1

Fix bug with data type in frag_an_driver_gen

## 20240920.1

New EPP for parsing VC100 CSV file

## 20240913.1

Generate composite run manifests for AVITI based on index lengths.

## 20240912.3

Fix bugs with EPP in the BCL conversion step

## 20240912.2

Support AVITI protocols for lobgook and comments_to_RN

## 20240912.1

Update AVITI run stats parser to handle multiple lanes

## 20240910.5

Fix simple naming bug.

## 20240910.4

Fix bug causing MinKNOW ss generation to fail for single samples w. label.

## 20240910.3

Add logbook for PromethION and MinION.

## 20240910.2

Support both single lane and dual lane of AVITI flowcell
Decide whether to include PhiX based on lane level UDF

## 20240910.1

Downprioritize column 3 of PromethION (used by CG), when running script to suggest ports.

## 20240909.1

Fix bug with zika module import cont; Change project format for AVITI run manifest

## 20240902.4

Also include Project name and sequencing setup in AVITI run manifest for PhiX

## 20240902.3

Include Project name and sequencing setup in AVITI run manifest

## 20240902.2

Ruff format

## 20240902.1

Fix bug with zika module import

## 20240901.1

Fix bug with AVITI process

## 20240830.2

Make ONT volume calculations script case-agnostic for concentration units.

## 20240830.1

When parsing Anglerfish results, upload the Anglerfish .csv dataframe to the LIMS step.

## 20240826.1

Add script for AVITI run manifest generation, re-organize repo to follow best-practice modularization and implement EPP wrapper.

## 20240823.2

Add function to fetch sample-level Q30 for AVITI

## 20240823.1

Support AVITI in the BCL conversion step

## 20240822.1

New EPP scripts for parsing AVITI run parameters and stats

## 20240816.1

Set up fixed-volume pooling by Zika for no-QC libraries.

## 20240815.1

Support Illumina DNA No-QC protocol

## 20240701.1

Improve pipreqs comparison script in CI

## 20240624.1

Fix bug to accommodate truseq single idx when writing Anglerfish samplesheet

## 20240617.1

Change pattern to run mypy for entire dir regardless of file depth.

## 20240612.1

Skip warning message for distance of special indexes

## 20240610.1

When parsing ONT sequencing libraries, use database queries to link pool samples to their respective labels.

## 20240530.1

Support VC100 in logbook

## 20240527.1

Generate Anglerfish samplesheet post database sync and name after run.

## 20240523.1

Upgrade index orientation checker to handle swapped indexes

## 20240521.2

Bugfix comparative assertion in Anglerfish parsing.

## 20240521.1

Skip special indexes for index orientation checker

## 20240508.2

For ONT samplesheet generation, accommodate kits with included barcodes.

## 20240508.1

Refactor step and UDF instrument for Amplification and Purification

## 20240506.2

Use different functions for moving MinKNOW samplesheet to ngi-nas-ns.

## 20240506.1

Update instrument logbook and running notes config to new ONT QC workflow.

## 20240503.1

Fix bug that Check Index Distance Log is not correctly attached

## 20240502.1

Fix running notes configuration for last PR.

## 20240502.1

Major ONT update and new module 'calc_from_args' for generalized calculations.

## 20240429.1

Add TAKARA_8nt_UDI and TruSeqUDv2-UDI for index checking

## 20240425.1

Close psycopg2 connections when query is done

## 20240423.1

Update the multiplication factor for total Lysate

## 20240422.2

Update GHA script to check VERSIONLOG.md diff to compare the latest PR-commit to the latest upstream/master commit instead of the commit at the base of the PR-branch.

## 20240422.1

Fix bug that seq_platform cannot be fetched when sample ID is in a wrong format

## 20240417.1

Update lane yield thresholds for NovaSeqXPlus 1.5B and 25B FC

## 20240415.1

Upgrade index checker for finlib to check index orientations

## 20240411.1

Fix bug with plate well index

## 20240409.1

Fix issue that sys stderr blocks a step to be completed

## 20240407.1

Add Genstat URL in running notes

## 20240407.1

Add lane yield threshold for NovaSeqXPlus 25B FC

## 20240325.1

Upgrade index_placement_checker to check expected index position

## 20240320.4

Enable index_distance_checker to catch case that one sample with multiple indexes

## 20240320.3

Enable index_placement_checker to verify index set

## 20240320.2

Improve warning messages for index_distance_checker

## 20240320.1

Add cDNA QC in comments_to_running_notes

## 20240319.1

New EPP for checking index placement for inhouse workset

## 20240318.1

Add lane yield threshold for NovaSeqXPlus 1.5B FC

## 20240315.2

ruff format linting

## 20240315.1

Handle special cases for Miseq samplesheet

## 20240307.1

Add PCR machine as UDF to "CytAssist Probe Release and Extension".

## 20240305.1

Add CytAssist electronic logbook.

## 20240229.2

Add PCR instrument logbook automation for Visium CytAssist protocol steps.

## 20240229.1

Add Biomek to "Selection, cDNA Synthesis and Library Construction" step.

## 20240215.1

Treat RAD-seq as regular pooling step, requested by Hamid.

## 20240208.1

In Anglerfish parsing, only try to assign barcode-specific UDFs for barcoded samples.

## 20240130.1

Handle Anglerfish result parsing for runs W/O ONT barcodes

## 20240126.1

Discover latest anglerfish run even if embedded in subdir of run dir

## 20240122.1

Enable copy_field_art2samp to copy values from Aggregate QC steps

## 20230111.1

Add CI-check to see versionlog is updated for a given pull request

## 20231220.1

Fix bug with verify index EPP

## 20231219.1

Fix bug that log is missing with index checker

## 20231214.1

Always have chemistry as amplicon for Miseq samplesheet

## 20231213.3

Fix BioAnalyzer EPP to expect row-wise samples instead of column-wise. Associated with deviation #211.

## 20231213.2

Expand 10X and SS3 indexes for MiSeq samplesheet

## 20231213.1

Fix MiSeq samplesheet generator to include options for custom primers

## 20231212.1

Enable Attaching xml files for MiSeq

## 20231201.1

Change MiSeq samplesheet to new version

## 20231120.1

Fix change in flowcell mode name that is related with control software upgrade

## 20231117.1

Re-write EPP for parsing Anglerfish results.

## 20231106.1

Fix error for RAD-seq prep pooling.

## 20231102.1

Improve logging for Zika normalization and improve docs for Zika utils func.

## 20231102.1

Implement script parse_ba_results.py.

## 20231031.1

Change Tecan instrument into UDF for logbook

## 20231027.1

Fix bug with multiple Tos breaking sendmail

## 20231025.2

Refactor UDF names for library prep amount

## 20231025.1

Remove obsoleted EPP scripts

## 20231019.1

Remove HiSeq and HiSeqX from demux EPP scripts

## 20231011.4

Add support for Illumina DNA PCR-free protocol

## 20231011.3

Update Anglerfish SS generation to accomodate 10X indices.

## 20231011.2

Change lane yield threshold for NovaSeqXPlus 10B

## 20231011.1

Change lane yield threshold for NextSeq P3

## 20231009.1

Remove special rule for no-depletion in bravo_csv

## 20230928.2

Fix parent in running notes in comments_to_running_notes

## 20230928.1

Fix couchdb conflict error with running notes

## 20230927.1

Fix bug with datatime in make_running_note_from_workset

## 20230925.1

Bugfix ONT process started runs

## 20230914.1

Replace mfs with ngi-nas-ns

## 20230828.2

Update Qubit EPP scripts to handle FLEX file format

## 20230828.1

Use the longer read for demux threshold

## 20230821.1

Fix bug that control has no project id in index checker

## 20230814.1

Enable "ONT Start Sequencing v2.0" for running notes script.

## 20230726.2

Refactor index_distance_checker

## 20230726.1

Add function to verify if sample name matches project id in index_distance_checker

## 20230718.2

Add NovaSeqXPlus in sequencing step list for readscount

## 20230718.1

Add function to verify sample name format in index_distance_checker

## 20230714.1

Accomodate Anglerfish samplesheet generation w/o any ONT barcodes.

## 20230712.1

Fix fatal error for ONT EPP by updating names of module resource.

## 20230711.2

Fix unwarranted error message when moving files to external storage by using a different shutil function. Likely issue with Python <3.8.

## 20230711.1

When calculating amounts in QC, populate both "Amount (ng)" and "Amount (fmol)", if possible. Useful for LIMSing nanopore samples.

## 20230630.2

Implement ONT and Anglerfish samplesheet generation for MinION QC.

## 20230630.1

Config updates and minor fixes from live testing the NovaSeqXPlus sequencing protocol on dummy samples on LIMS Prod.

## 20230622.1

Bugfix for deviation 173. Differentiate metadata paths for Illumina instruments.

## 20230615.1

Put generated ONT samplesheets on ngi-nas-ns instead of mfs.

## 20230613.1

Rework zika_utils.format_worklist() split transfers logic to prevent the post-split volume from ending up as less than what is allowed by the instrument.

## 20230602.1

Rename utils module to epp_utils to avoid name collision with native Python module and fix bug causing fatal error for Zika pooling.

## 20230529.1

Assign step (accidentally omitted from PR #150) to RN config.

## 20230525.1

Live troubleshooting of ONT EPPs upon deployment of new workflow to LIMS prod.

## 20230329.1

Improve modularity and readability of ONT EPP script names and contents. Also implement changes requested during live testing.

## 20230313.1

Deploy validation 23_02_zika_codebase_revamp to replace accredited codebase for pooling using Mosquito X1.

## 20230306.2

Update control lists and fetch run recipe from project for samplesheet generator

## 20230306.1

Replace formula used for ng -> molar conversion.

## 20230227.1

Improvements and bugfixes on ONT EPPs.

## 20230224.2

Add four new EPPs related to the updated ONT workflow deploying shortly.

## 20230224.1

Update after live troubleshooting of new Zika pooling code. Fix faulty variable name and improve error logging.

## 20230222.1

Support nM as a valid conc unit for Aggregate QC DNA and RNA

## 20230213.1

Differentiate Zika normalization parameters for Amplicon workflow plate set-up. Unlike QIAseq and SMARTer it should use customer metrics and a lower minimum volume.

## 20230209.1

Enable verify index and placement epp for checking wrong well format

## 20230207.1

Update 20230130.2, correct the volume and conc information that is fetched and support both nM and ng/ul pooling. General updates to make the code simpler and more maintainable.

## 20230130.2

zika_refactoring
Add re-factored pooling code for Zika. Re-route to the new code ONLY for RAD-seq pooling (non-accredited). Accredited operations will run on the old code, for now.

## 20230130.1

Convert 10X dual index 2 to RC for MiSeq

## 20230128.1

Update index_checker EPP to support SMARTSEQ3 indexes

## 20230126.1

Fix issue with NaN values for fragment analyzer results

## 20230123.1

Fix bug that manual in UDF instrument is recorded in logbook

## 20230116.1

Refactor EPP scripts for qc_amount_calculation

## 20221215.1

When writing the Zika deck layout in a worklist comment, omit all commas, to prevent the line from being cut-off.

## 20221123.1

New EPP for calculating cell or nuclei conc for the new 10X Chromium workflow

## 20221122.1

Also support two new UDFs for the QIAseq miRNA and Amplicon workflows for Bravo

## 20221121.1

Large update in functionality of Zika code. Accomodate two new UDFs and enable usage in the non-validated methods SMARTer PicoRNA, QIAseq miRNA and amplicon normalization.

## 20221116.2

Refactor of the default_bravo and calc_vol functions for bravo_csv to include two new UDFs

## 20221116.1

Update amount taken and total volume for bravo_csv

## 20221109.1

Implement Zika for QIAseq setup and start refactoring Zika code into separate files zika.py and zika_methods.py

## 20221011.1

Fix bug that manual in UDF instrument is recorded in logbook

## 20220914.1

Multiple EPP changes to support the OmniC protocol v2.0

## 20220909.1

Handle special characters in PCs name

## 20220907.1

Add more optional keys for Aggregate QC

## 20220904.1

Add PromethION Sequencing in comments_to_running_notes

## 20220902.2

Fix bug with index checker with submitted container info for inhouse libraries

## 20220902.1

New EPP for copying input UDF to output

## 20220831.1

For MiSeq samplesheet, replace Experiment Name with Flowcell ID

## 20220804.1

Add new control types for samplesheet generator

## 20220722.1

Upgrade index checker to throw error for bad format indexes

## 20220718.1

Fix bug with manage_demux_stats that noindex case cannot be handled for NextSeq

## 20220709.2

Upgrade index checker for checking sample placement

## 20220709.1

Fix issue that record changes EPP cannot handle controls

## 20220708.1

Refactor index checker for better handling of smartseq indexes

## 20220707.1

Write verify indexes comments to running notes

## 20220706.1

Upgrade index checker for verifying finished library projects

## 20220701.1

Fix bug with single read MiSeq run for illumina_run_parameter_parser

## 20220630.1

Make a new logbook EPP based on Google service account

## 20220629.1

Support Biomek for logbook

## 20220628.1

Remove workset tag for CaliperGX in comments_to_running_notes

## 20220616.1

Fix path of QC_criteria.json

## 20220615.1

Update statusdb URL to use https

## 20220608.1

Fix index distance checker for cases that one sample with multiple indexes

## 20220606.1

Fix samplesheet generator for cases that one sample with multiple indexes

## 20220602.1

Rename FC and cartridge UDFs for NextSeq and add NextSeq 2000 P1

## 20220506.1

Take 2uL sample for low pipetting volume cases for the SMARTer Pico RNA workflows

## 20220503.1

Include controls in samplesheet for MiSeq, NextSeq and NovaSeq

## 20220428.1

Enable illumina_run_parameter_parser for parsing run stats for NovaSeq

## 20220427.1

Support 10X SI-TS indexes

## 20220415.2

New EPP for summarizing Aggregate QC stats into running notes, stats for QC metrics

## 20220415.1

New EPP for summarizing Aggregate QC stats into running notes

## 20220412.1

Refactor 10X index pattern names

## 20220409.1

Do not convert index 2 for finished library samples for MiSeq

## 20220407.1

New index handling method for samplesheet generator

## 20220313.1

Update illumina_run_parameter_parser for handling MiSeq run without index cycles

## 20220304.1

Multiple EPP changes to support the new OmniC protocol

## 20220301.1

Support Mosquito for logbook

## 20220222.1

Return message when no issue detected for index checker

## 20220221.2

Refactor index checker to support 10X indexes

## 20220221.1

New EPP for checking index distance

## 20220217.1

Update illumina_run_parameter_parser for parsing run stats for MiSeq

## 20220215.1

Put back Workflow for samplesheet generator for MiSeq

## 20220211.1

Replace UDF for samplesheet generator for MiSeq

## 20220202.1

Update to send email to proj coord when a running note is written from LIMS

## 20211104.1

Update samplesheet generator to handle non-QC Minion sequencing step

## 20211027.1

Remove FastQ path from MinION samplesheet

## 20211025.2

Bravo CSV EPP for new library normalization and pooling steps

## 20211025.1

EPP support for new library normalization and pooling steps

## 20211021.1

Show ERROR messages when pool volume is too high

## 20211013.1

Support selectable Fragment Analyzer for logbook

## 20211011.1

Update anglerfish results parser to support outputfile with new format

## 20211007.1

Support fmol amount calculation

## 20210930.1

Fix bug with control samples for bravo_csv

## 20210920.1

Exclude RNA no depletion protocol from volume adjustment

## 20210910.1

Update bravo_csv to support volume adjustment for high conc samples

## 20210809.1

Update threshold of max undet per lane percentage for demux step

## 20210702.1

Upgrade EPPs to support the new ONT protocol

## 20210617.1

Support additional 10X index types in samplesheet generator
Update 10X index list

## 20210615.1

Support DV200 for Caliper result parser

## 20210603.1

Allow empty path for Minion QC

## 20210531.1

Fix bug with MiSeq in samplesheet generator

## 20210528.1

Better sort functions for bravo csv and samplesheet

## 20210525.2

Fix issue with error message

## 20210525.1

Add fragment analyzer protocols in comments_to_running_notes

## 20210520.1

Upgrade EPPs to support the new QIAseq miRNA protocol

## 20210519.1

Fix bug with None type comparison in copy_qubit.py

## 20210511.1

Update obtain_customer_cc.py to support custom volume

## 20210503.1

Update scripts for parsing fragment analyzer result files

## 20210419.1

Port scripts to python 3

## 20210414.1

Update illumina_run_parameter_parser for parsing run stats

## 20210410.1

Update samplesheet generator to handle blanks in sample index

## 20210409.2

Update EPP for parsing run info for NextSeq 2000, MiSeq and NovaSeq

## 20210409.1

Update EPP for parsing run info for both NextSeq 2000 and MiSeq

## 20210408.1

New EPP for parsing run info for NextSeq 2000

## 20210313.1

Support additional 10X index types in samplesheet generator
Update 10X index list

## 20210226.1

Change plate name to plate id for Bravo CSV for qPCR

## 20210224.2

Add new EPP for aliquoting samples for qPCR steps

## 20210224.1

Setup VERSIONLOG.md
