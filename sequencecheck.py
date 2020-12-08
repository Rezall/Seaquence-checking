import re 
import pdfplumber
import csv

args = []
parsed_cwl = []
sts_indxs = []
parsed_cwl = []
pings = []
seq_model = ["ADisch40","ADischs","BDisch40","BDischs","BLoads","BLoad40","ALoads","ALoad40"]
output = ["A Disch of 40'", "A Disch of 20'","B Disch of 40'","B Disch of 20'", "B Load of 20'", "B Load of 40'","A Load of 20'","A Load of 40'"]
act_model = []
sts_patternn = re.compile(3*"\w")
stsindex = []
singles_wi = []

#File importing ---------------------------

try : 
    with pdfplumber.open("CWL4.pdf") as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            for line in text.split('\n'):
                x = re.sub(' +', ' ',line)
                args.append(x.split(" "))
except:
    print("Error Loading CWL")

try :
    with open('singlesreport.csv', newline='') as csv_file:
        outputt = csv.reader(csv_file, delimiter=',')
        for x in outputt:
            if x[len(x)-1] != "91N050N":
                continue
            else:
                if x[2] == "Load":
                    if x[3][14] == "2":
                        singles_wi.append(x[3][9:12]+'l')
                else:
                    if x[3][15] == "2":
                        singles_wi.append(x[3][10:13]+'d')
except:
    print("Error loading WI")

for x in args:
    if x == [] or x[0] == "":
        continue
    elif x[0][2] != "A" and x[0][2] != "B":
        if x[0][:3] == "STS":
            sts_indxs.append(args.index(x))
        else:
            continue
    else:
        parsed_cwl.append(x)


#File parsing -------------------------------

for x in parsed_cwl:
    for i in range(len(x)):
        if  len(x[i]) > 3 :
            if x[i][-3] == "4":
                del x[i+1:]
                break
            elif x[i][-3] == "2":
                j = i+1
                while j < len(x):
                    if len(x[j]) > 5:
                        del x[j:]
                        break
                    else:
                        del x[j+2:]
                        break
                break
        else:
            continue

#Actual model parsing function -------------------------

bridged = []
bridged_indxs = []
expt = []
rslt = []
pings_split = []
wronged_singles = []


def parse_wq(x):
    counterr = 0
    if x[2][-3] == "2" and len(x) == 3:
        if x[1][:4] == 'Load':
            for y in singles_wi:
                if x[0] + 'l' == y:
                    counterr += 1
            if counterr == 0:
                wronged_singles.append(x[1]+" of single in bay "+ x[0][:3] + " is wrongly placed in single Q.")
            else:
                counterr == 0
        else:
            for y in singles_wi:
                if x[0] + 'd' == y:
                    counterr += 1
            if counterr == 0:
                wronged_singles.append(x[1]+" of single in bay "+ x[0][:3] + " is wrongly placed in single Q.")
            else:
                counterr == 0
    else:
        if x[2][-3] == "4":
            act_model.append(x[0][0:3]+x[1][:5]+"40")
        else:
            if len(x[3]) == 4:
                if int(x[-2][3])*2 != int(x[-3][:-4]):
                    if x[1][:4] == 'Load':
                            for y in singles_wi:
                                if x[0] + 'l' == y:
                                    counterr += 1
                            if int(x[-3][:-4]) == counterr:
                                pings_split.append(x[1]+" of single in bay "+ x[0][:3]+ " needs to be split")
                                counterr = 0
                            else:
                                wronged_singles.append(x[1]+" of single in bay "+ x[0][:3] + " is wrongly placed in twin Q.")
                                counterr = 0
                    else:
                            for y in singles_wi:
                                if x[0]+'d' == y:
                                    counterr += 1
                            if int(x[-3][:-4]) == counterr:
                                pings_split.append(x[1]+" of single in bay "+ x[0][:3]+ " needs to be split")
                                counterr = 0
                            else:
                                wronged_singles.append(x[1]+" of single in bay "+ x[0][:3] + " is wrongly placed in twin Q.")
                                counterr = 0

                a = str(int(x[0][:2]) + 1)
                
                if len(a) == 2:
                    act_model.append(a+x[0][2]+x[1][:5]+"s")
                else:
                    act_model.append("0"+a+x[0][2]+x[1][:5]+"s")
            else:
                if int(x[-2][3:])*2 != int(x[-3][:-4]):
                    if x[1][:4] == 'Load':
                            for y in singles_wi:
                                if x[0]+'l' == y:
                                    counterr += 1
                            if int(x[-3][:-4]) == counterr:
                                pings_split.append(x[1]+" of single in bay "+ x[0][:3]+ " needs to be split")
                                counterr = 0
                            else:
                                if str(int(x[0][:2])+2)+'l' not in singles_wi:
                                    pings_split.append(x[1]+" of single in bay "+ x[0][:3]+ " needs to be split")
                                    counterr = 0
                                else:
                                    wronged_singles.append(x[1]+" of single in bay "+ x[0][:3] + " is wrongly placed in twin Q.")
                                    counterr = 0
                    else:
                            for y in singles_wi:
                                if x[0]+'d' == y:
                                    counterr += 1
                            if int(x[-3][:-4]) == counterr:
                                pings_split.append(x[1]+" of single in bay "+ x[0][:3]+ " needs to be split")
                                counterr = 0
                            else:
                                wronged_singles.append(x[1]+" of single in bay "+ x[0][:3] + " is wrongly placed in twin Q.")
                                counterr = 0

                a = str(int(x[0][:2]) + 1)
                
                if len(a) == 2:
                        act_model.append(a+x[0][2]+x[1][:5]+"s")
                else:
                        act_model.append("0"+a+x[0][2]+x[1][:5]+"s")


for i in range(int(sts_indxs[0]), len(sts_indxs)):
    bridged.append(int(parsed_cwl[int(sts_indxs[i]) - i - 1][0][:2]))
    bridged_indxs.append(parsed_cwl.index(parsed_cwl[int(sts_indxs[i]) - i - 1]))


for i in range(len(parsed_cwl)):
    if i not in expt : 
        expt += [i]
        for k in range(len(bridged)):
            if int(parsed_cwl[i][0][:2]) == bridged[k] or abs(int(parsed_cwl[i][0][:2]) - bridged[k]) == 1 :
                for j in range(bridged_indxs[k], len(parsed_cwl)):
                    if abs(int(parsed_cwl[j][0][:2]) - int(parsed_cwl[i][0][:2])) <= 1 and j not in expt:
                        expt += [j]
                        parse_wq(parsed_cwl[j])
        parse_wq((parsed_cwl[i]))

#Report creation  ---------------------------------

reslt = []
calc = []
L = 0
errors = 1
report = []


while L < len(act_model)-1:
    reslt.append(act_model[L])
    for l in range(L+1,len(act_model)):
        if act_model[L][:2] == act_model[l][:2]:
            reslt.append(act_model[l])
        else:
            break
    for x in reslt:
        calc.append(seq_model.index(x[2:]))
    for i in range(len(calc)):
        for j in range(i+1,len(calc)):
            if calc[i]>calc[j]:
                report.append("Sequencing Error N°"+str(errors)+": "+x[:2]+str(output[calc[j]])+" must be before "+x[:2] +str(output[calc[i]]))
                errors += 1
                break
    reslt = []
    calc = []
    L = l

#Report output --------------------------------------

singles = 1
singles_split = 1
wronged = 1

if errors > 0 :
    print('-----------------')
    print("Errors Report")
    print('-----------------')
    for x in report :
        print(x)
else:
    if len(pings_split)> 0 or len(wronged_singles)> 0:
        print("Sequencing well done, Please check Singles Report")
    else:
        print("Sequencing well done")

if len(pings_split)>0:
    print('-----------------')
    print('Split Singles Report')
    print('-----------------')
    for x in pings_split:
        print("Single split N°"+str(singles_split)+": "+x)
        singles_split += 1

if len(wronged_singles) > 0:
    print('-----------------')
    print('Wrong single bay')
    print('-----------------')
    for x in wronged_singles:
        print("Single N°"+str(wronged)+": "+x)
        wronged += 1