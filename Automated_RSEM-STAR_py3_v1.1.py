

"""
Created on Mon Jan 18 17:41:10 2021

@author: minkj
"""
#________________ option parse _______________________________
import sys 

args = sys.argv[1:]

option_dict={'-cores':"32",'-paired':"1", '-exclude':"",'-ref':""}
for i in range(len(args)):
    if args[i].startswith("-"):
        try:
            option_dict[args[i]]=args[i+1]
        except:
            if args[0]=="-help":
                print ("""
_____________________________________________________________________________

Usage;

-help       show option list
-include    key words for filtering files to include 
-exclude    key words for filtering files to exdlude (default is "")
-ref        name of the reference file for bowtie mapping
-paired     1: paired-end, 2: single-end (default is 1)
-cores      number of cores for RSEM (default is 32)
_____________________________________________________________________________
""")

                quit()
if option_dict['-ref']=="":
    print ("Please enter the name of reference file for bowtie mapping.")
    quit()


def file_list(infilter, exfilter): #inputs are string
    import os
    f_list=os.listdir('.')
    infiltered=list(filter(lambda x: infilter in x, f_list))
    if option_dict["-exclude"]=="":
        exfiltered=infiltered
    else:
        exfiltered=list(filter(lambda x: exfilter not in x, infiltered))
    exfiltered.sort()
    print ("\n\nFiltered file list:\n", exfiltered)
    return exfiltered

def seq_pairing(filtered_files): # input is list
    n=0
    paired_list=[]
    infile=filtered_files
    #infile.sort()
    print (infile)
    infile_len=len(infile)
    for k in range(int(len(infile)/2)):
        #print (n)
        f1=infile[n]
        f2=infile[n+1]
        n=n+2

        f1_list=list(f1)
        f2_list=list(f2)
        if len(f1_list)==len(f2_list):
            #diff=0
            for k in range(len(f1_list)):
                if f1_list[k]!=f2_list[k]:
                    if f1_list[k] in ["1","2"] and f2_list[k] in ["1","2"]:
                        diff="paired"
                    else:
                        diff="error"
            if diff=="paired":
                paired_list.append((f1,f2))
            else:
                print ("\n\n", f1,"    and    ", f2,"   are compared.")
                print ("Error occurred in pairing.. \nF and R names must be same except for the distinguishing number, 1 and 2.")
                quit()

        else:
            print ("\n\n", f1,"    and    ", f2,"   are compared.")
            print ("Error occurred in pairing.. \nF and R names must be same except for the distinguishing number, 1 and 2.")
            quit()

    return paired_list

def main():
    infilter_cont=option_dict["-include"]
    exfilter_cont=option_dict["-exclude"]

    filtered=file_list(infilter_cont,exfilter_cont)
    import os
    if option_dict['-paired']=="1":
        paired=seq_pairing(filtered)
        n=0
        for tuple_file in paired:
            print (tuple_file)
            n=n+1
            print (str(n)+"/"+str(len(paired)), tuple_file[0], tuple_file[1],"<=== rsem running.....\n\n")
            run_RSEM=os.system("rsem-calculate-expression -p %s --paired-end --star --estimate-rspd --append-names --output-genome-bam %s %s %s %s" % (option_dict['-cores'], tuple_file[0], tuple_file[1], option_dict['-ref'], tuple_file[0]+"--"+tuple_file[1]+"_rsem_output.txt"))

    elif option_dict['-paired']=="2":
        #filtered.sort()
        n=0
        for file in filtered:
            n=n+1
            print (str(n)+"/"+str(len(filtered)), file,"<=== rsem running.....\n\n") 
            run_RSEM=os.system("rsem-calculate-expression -p %s --star --estimate-rspd --append-names --output-genome-bam %s %s %s" % (option_dict['-cores'], file, option_dict['-ref'], file+"_rsem_output.txt"))

    print ("Completed!!")

if __name__=="__main__":
    main()
