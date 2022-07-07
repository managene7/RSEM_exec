#________________ option parse _______________________________
import sys 

args = sys.argv[1:]

option_dict={'-infilter':"",'-exfilter':"","-out":"RSEM_result","-exclude":""}
for i in range(len(args)):
    if args[i].startswith("-"):
        try:
            option_dict[args[i]]=args[i+1]
        except:
            if args[0]=="-help":
                print ("""
______________________________________________________________________________________________

Usage;

-help           show option list
-include        key words for filtering files to include 
-exclude        key words for filtering files to exdlude (default is "")
-out            output file name of output that you want to (option, default is "RSEM_result")
______________________________________________________________________________________________
""")
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
    print ("Filtered files are:\n", exfiltered)
    return exfiltered

def main():
    infilter_cont=option_dict['-include']
    exfilter_cont=option_dict['-exclude']

    filtered=file_list(infilter_cont,exfilter_cont)

    import os
    import csv
    n=0

    seq_list=[]
    transcript_list=[]
    init=0
    cont_dic={} # {transcript:[count,tpm, fpkm]}
    for f in filtered:
        n=n+1
        f_open=open(f,'r')
        sub_cont_dic={}
        while 1:
            line=f_open.readline().strip()
            if line=="":
                break
            else:
                line=line.split()
                if line[0]!="transcript_id":
                    transcript=line[0].split("_")[0]
                    if init==0:
                        transcript_list.append(transcript)
                        
                    sub_cont_dic[transcript]=[line[4],line[5],line[6]]
        init=1
        seq_name=f.split("_")[0]+"_"+f.split("_")[1]+"_"+f.split("_")[2]
        seq_list.append(seq_name)
        cont_dic[seq_name]=sub_cont_dic
    seq_list.sort()


    count_dic={}
    tpm_dic={}
    fpkm_dic={}
    for t_id in transcript_list:
        count_dic[t_id]=[]
        tpm_dic[t_id]=[]
        fpkm_dic[t_id]=[]
        for seq in seq_list:
            #print (t_id)
            #print (cont_dic[seq][t_id])
            count_dic[t_id].append(cont_dic[seq][t_id][0])
            tpm_dic[t_id].append(cont_dic[seq][t_id][1])
            fpkm_dic[t_id].append(cont_dic[seq][t_id][2])
    count_csv=csv.writer(open(option_dict['-out']+"_Count_all.csv",'w', newline=""))
    TPM_csv=csv.writer(open(option_dict['-out']+"_TPM_all.csv",'w', newline=""))
    FPKM_csv=csv.writer(open(option_dict['-out']+"_FPKM_all.csv",'w', newline=""))

    #print (count_dic)
    #print (list(["Transcript ID"])+seq_list)
    count_csv.writerow(list(["Transcript ID"])+seq_list)
    TPM_csv.writerow(list(["Transcript ID"])+seq_list)
    FPKM_csv.writerow(list(["Transcript ID"])+seq_list)

    for transcript_id in transcript_list:
        count_csv.writerow(list([transcript_id])+count_dic[transcript_id])
        TPM_csv.writerow(list([transcript_id])+tpm_dic[transcript_id])
        FPKM_csv.writerow(list([transcript_id])+fpkm_dic[transcript_id])

if __name__ == '__main__':
    main()    





