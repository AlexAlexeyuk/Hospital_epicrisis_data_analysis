from temp import *


for file in list_of_files:
    try:
         with open(file, encoding='utf-8') as f:
                num = f.readline()
                file_ = f.read()
                ID_.append(ID((num)))
                tr.append(treatment((file_)))
                bir.append(born_adm_disch(file_)[0])
                ad.append(born_adm_disch(file_)[1])
                dis.append(born_adm_disch(file_)[2])
                dgs_.append(diagnosis_dirty((file_)))
                crp_.append(crp(''.join(file_.split())))
                sex_.append(gender(''.join(file_.split())))
                ldh_.append(ldh(file_))
                crea_.append(cre(file_))
                hgb_.append(hgb(file_))
                wbc_.append(wbc(file_))
                plt_.append(plt(file_))
    except:
        print(file)
        
data_dct = {'Platlets':plt_, 'Leucocytes': wbc_, 'Hemoglobin': hgb_,
           'Creatinine': crea_, 'LDG':ldh_, 'Gender':sex_, 'CRP':crp_,
           'Treatment':tr, 'Birthday': bir, 'Admission':ad,
           'Discharge':dis, 'ID':ID_, 'Diagnosis': dgs_}


dataFrame = pd.DataFrame(data_dct)

