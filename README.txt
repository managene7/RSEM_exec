Quality_trimming

#load module
>module load adapterremoval

#check options
>python3 Automated_AdapterRemoval_py3_V1.0.py -help
_____________________________________________________________________________

Usage;

-help       	show option list
-include    	key words for filtering files to include 
-exclude    	key words for filtering files to exdlude (default is "")
-paired     	1: paired-end, 2: single-end (default is 1)
-cores      	number of cores for AdapterRemoval (default is 32)
_____________________________________________________________________________




#run pipeline
>python3 Automated_AdapterRemoval_py3_V1.0.py -include 600Mb -exclude .py -cores 32 -paired 1

Run RSEM 
#load modules
>module load rsem
>module load bowtie2
#or rsem and bowtie2 have to be installed.


#generate reference files for mapping
#rsem-prepare-reference --bowtie2 -gff3 (gff file name) (genome seq name) (genome seq ref name)
>rsem-prepare-reference --bowtie2 -gff3 TAIR10.gff TAIR10.fa TAIR10.fa.ref #example.

#check options for Automated RSEM code.
>python3 Automated_RSEM_py3_v1.0.py -help
_____________________________________________________________________________

Usage;

-help  	show option list
-include    	key words for filtering files to include 
-exclude   	key words for filtering files to exdlude (default is "")
-ref        	name of the reference file for bowtie mapping
-paired     	1: paired-end, 2: single-end (default is 1)
-cores      	number of cores for RSEM (default is 32)
_____________________________________________________________________________

#run pipeline
>python3 Automated_RSEM_py3_v1.0.py -include filtered -exclude rsem -cores 32 -ref  TAIR10.fa.ref -paired 1 #example




Parsing RSEM results

#check options
>python3 RSEM_parser_py3_v1.03.py -help
______________________________________________________________________________________________

Usage;

-help           	show option list
-include        	key words for filtering files to include 
-exclude      		key words for filtering files to exdlude (default is "")
-out            	output file name of output that you want to (option, default is "RSEM_result")
______________________________________________________________________________________________

#run RSEM result parser
python3 RSEM_parser_py3_v1.03.py -include isoforms.results -exclude gene.results -out test_results #example



