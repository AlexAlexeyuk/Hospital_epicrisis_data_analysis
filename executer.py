import os
import pandas as pd
import glob
import string
import nltk
import re



class Utils():
    root_directory = os.chdir('c:/Users/iZiPC.by/notebooks/parser/')# input path
    list_of_files = glob.glob('**/*.txt', recursive=True)
    invalid_parsing = []
    trash = ['Волковыск-1.txt','Волковыск.txt','Вороново-1.txt',
         'Вороново.txt', 'Черновик-1.txt', 'Черновик.txt']
    for file in list_of_files:
        try:
             with open(file, encoding='utf-8') as f:
                    num = f.readline()
                    file_ = f.read()
                    if num and file_:
                        pass
        except:
            invalid_parsing.append(file)
    for i in invalid_parsing:
        list_of_files.remove(i)
    for i in trash: 
        list_of_files.remove(i)


list_of_files = Utils.list_of_files


plt_ = []
wbc_ = []
hgb_ = []
crea_ = []
ldh_ = []
sex_ = []
crp_ = []
tr = []
bir = []
ad = []
dis = []
ID_ = []
dgs_ = []
rf_ = []
alt_ = []
ast_ = []
pct_ = []

def ID(num):
  """returns ID of the patient"""
  for i in num.split():
    for char in i.split():
        if char.isnumeric():
            try:
                return int(char)
            except:
                return 'None'
            
            
def treatment(file_):
  """ returns srting of remedies used for the patient """
  for line in file_.split('\n'):
    if re.search('лечение', line):  # Does the same thing as "if 'hello' in line:"
        return(line.replace('Проведенное лечение:', \
                            '').replace('ЛФК', '').replace('ФТЛ', ''))
    

def born_adm_disch(file_):
    """ finds all nessesary dates in the epicrisis"""
    pattern = re.compile("(\d{2}).(\d{2}).(\d{4})") # check all dates
    birthday, admission = pattern.findall(file_)[:2]
    discharging = pattern.findall(file_)[-1]
    try:
        return ':'.join(birthday), ':'.join(admission), ':'.join(discharging)
    except:
        return 'None'


pattern_diagnosis = ['Диагноз:','Диагноз клинический:','Диагноз', 'Д-з:',
                     "Диагноз заключительный:"]
def diagnosis_dirty(file_):
  int_ = 0
  for i in file_.split():
    int_ += 1
    if i in pattern_diagnosis:
      return file_.split()[int_+1:int_+40]    
  

def crp(file_):
  """returns all crp values"""
  file_= ''.join(file_.split())
  file_ = re.sub(r'[ЦСC]РБ|\w\D(реактив.|реакт.|реак.)белок', 'С-реактивныйбелок', file_)
  file_ = re.sub(r'\d{,2}\.\d\d\.\d{2,4}', '', file_)
  file_ = re.sub(r'[():]', '', file_)
  file_ = re.sub(r'(?<!С-реактивныйбелок)\d\d\.\d\d', '', file_)
  file_ = re.sub(r',', '.', file_)
  pattern_1 = re.compile(r'(?:\w\Dреактивныйбелок|\w\Dреактивныйбелокдо)(\d*\.\d+|\d+)')
  pattern_2 = pattern_1.findall(file_)
  try:
    if pattern_2:
      return pattern_2
    else:
      return 'None'
  except:
    pass


def gender(file_):
  file_ = file_.title()
  file_ = ''.join(file_.split())
  file_ = re.sub(r'Диагноз.*', '', file_)
  patt1 = re.compile(r'[А-Я](\w{,19}(\w|\ич))[А-Я]\w{,20}(вна)')
  patt2 = patt1.findall(file_)
  try:
    if patt2:
      return 'female'
    else:
      return 'male'
  except:
    pass
  

def ldh(file_):
  file_= ''.join(file_.split())
  file_ = file_.lower()
  file_ = re.sub(r'[():]', '', file_)
  file_ = re.sub(r'\d{,2}\.\d\d\.\d{2,4}', '', file_)
  file_ = re.sub(r'\wактатдегидрогеназ\w', 'лдг', file_)
  file_ = re.sub(r'(?<!лдг)\d\d\.\d\d', '', file_)
  patt1 = re.compile(r'(?<=лдг)\d{,4}')
  patt2 = patt1.findall(file_)
  try:
    if patt2:
      return patt2
    else:
      return 'None'
  except:
    pass



def cre(file_):
  """Returns all creatinine values"""
  file_= ''.join(file_.split())  
  file_ = file_.lower()
  file_ = re.sub(r'[():]', '', file_)
  file_ = re.sub(r'\d{,2}\.\d\d\.\d{2,4}', '', file_)
  file_ = re.sub(r'(\wреатини\w|креатин|креат)(?![а-яА-Я,])', 'cre', file_)
  file_ = re.sub(r'(?<!cre)\d\d\.\d\d', '', file_)
  patt1 = re.compile(r'(?<=cre)\d{2,3}')
  patt2 = patt1.findall(file_)
  try:
    if patt2:
      return patt2
    else:
      return 'None'
  except:
    pass


def hgb(file_):
  """returns list of str with level of hemoglobin"""
  file_= ''.join(file_.split())  
  file_ = file_.lower()
  file_ = re.sub(r'[():]', '', file_)
  patt = re.compile(r'гемоглобин|гемогл|гб|гем')
  patt1 = re.sub(patt, r'hgb', file_)
  patt2 = re.compile(r'(?<=hgb)\d{2,3}')
  all_hgb = patt2.findall(patt1)
  try:
    if all_hgb:
      return all_hgb
    else:
      return 'None'
  except:
    pass


def wbc(file_):
  """returns list of str with level of wbc"""
  file_= ''.join(file_.split())
  file_ = file_.lower()
  file_ = re.sub(r'[():]', '', file_)
  file_ = re.sub(r'10(\*|[еe])9', '', file_)
  file_ = re.sub(r'\d{,2}\.\d\d\.\d{2,4}', '', file_)
  file_ = re.sub(r'\Dбщийанализкрови', 'оак', file_)
  file_ = re.sub(r'(?<=оак)гб\d*,', '', file_)
  file_ = re.sub(r',', '.', file_)
  patt1 = re.compile(r'(?<=оак|wbc)(?:л|лейкоцит\w)(\d*\.\d+|\d+)')
  all_wbc = patt1.findall(file_)
  try:
    if all_wbc:
      return all_wbc
    else:
      return 'None'
  except:
    pass


def plt(file_):
  """returns list of str with level of plt"""
  file_= ''.join(file_.split())
  file_ = file_.lower()
  file_ = re.sub(r'[():]', '', file_)
  file_ = re.sub(r'10(\*|[еe])9', '', file_)
  file_ = re.sub(r'\d{,2}\.\d\d\.\d{2,4}', '', file_)
  patt1 = re.compile(r'\wромбоцит\w|(?<![а-яА-Я])тр(?![а-яА-Я])')
  file_ = re.sub(patt1, r'plt', file_)
  file_ = re.sub(r'(?<!plt)\d\d\.\d\d', '', file_)
  patt2 = re.compile(r'(?<=plt)\d{3}')
  all_plt = patt2.findall(file_)
  try:
    if all_plt:
      return all_plt
    else:
      return 'None'
  except:
    pass


def rf(file_):
  file_= ''.join(file_.split())  
  file_ = re.sub(r'[а-яА-ЯёЁ]ДН[^Шш0-9]', 'ДН'.lower(), file_)
  file_ = re.sub(r'(?<=ДН)[1iI]{3}|[Шш]', '3', file_)
  file_ = re.sub(r'(?<=ДН)[1iI]{2}|1-2', '2', file_)
  file_ = re.sub(r'(?<=ДН)[оoОO]', '0', file_)
  patt1 = re.compile(r'(?<=ДН)\d')
  patt2 = patt1.findall(file_)
  try:
    if patt2:
      return patt2
    else:
      return 'None'  
  except:
      pass

def alt(file_):
  file_= ''.join(file_.split())
  file_ = file_.lower()
  file_ = re.sub(r'[():]', '', file_)
  file_ = re.sub(r'\d{,2}\.\d\d\.\d{2,4}', '', file_)
  file_ = re.sub(r'\wланинаминотрансфераз\w|алат', 'алт', file_)
  file_ = re.sub(r'(?<!алт)\d\d\.\d\d', '', file_)
  file_ = re.sub(r',', '.', file_) 
  patt1 = re.compile(r'(?<=алт)(\d*\.\d+|\d+)')
  patt2 = patt1.findall(file_)
  try:
    if patt2:
      return patt2
    else:
      return 'None'
  except:
    pass


def ast(file_):
  file_= ''.join(file_.split())
  file_ = file_.lower()
  file_ = re.sub(r'[():]', '', file_)
  file_ = re.sub(r'\d{,2}\.\d\d\.\d{2,4}', '', file_)
  file_ = re.sub(r'\wспартатаминотрансфераз\w|асат', 'аст', file_)
  file_ = re.sub(r'(?<!аст)\d\d\.\d\d', '', file_)
  file_ = re.sub(r',', '.', file_)
  patt1 = re.compile(r'(?<=аст)(\d*\.\d+|\d+)')
  patt2 = patt1.findall(file_)
  try:
    if patt2:
      return patt2
    else:
      return 'None'
  except:
    pass


def pct(file_):
  file_= ''.join(file_.split())
  file_ = file_.lower()
  file_ = re.sub(r'(?<=\,\d)\,|\.\d{2}\.\d\d\.\d{2,4}.', '', file_)
  file_ = re.sub(r'\d{,2}\.\d\d\.\d{2,4}(\.|)', '', file_)
  file_ = re.sub(r'[–-]|[():<>=]', '', file_)
  file_ = re.sub(r'менее', '', file_)
  file_ = re.sub(r'от', '', file_)
  file_ = re.sub(r'(\wрокальцитони\w|прокальцитон|прокальцит|прокальц|рст)(?![а-яА-Я,])', 'pct', file_)
  file_ = re.sub(r',', '.', file_)
  patt1 = re.compile(r'(?<=pct)(\d*\.\d+|\d+)')
  patt2 = patt1.findall(file_)
  try:
    if patt2:
      return patt2
    else:
      return 'None'
  except:
    pass



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
                crp_.append(crp(file_))
                sex_.append(gender(file_))
                ldh_.append(ldh(file_))
                crea_.append(cre(file_))
                hgb_.append(hgb(file_))
                wbc_.append(wbc(file_))
                plt_.append(plt(file_))
                rf_.append(rf(file_))
                alt_.append(alt(file_))
                ast_.append(ast(file_))
                pct_.append(pct(file_))
    except:
        print('stp')
        

rfl = []
for i in rf_:
    if i:
        rfl.append(max(i))
    else:
        rfl.append('None')
        
        
        
diagnosis_cleaned =  []
for diagnos in dgs_:
    try:
        diagnosis_cleaned.append(' '.join(diagnos))
    except:
        diagnosis_cleaned.append('None')
        
        
        
PUNCT_TO_REMOVE = string.punctuation
def remove_punctuation(text):
    """custom function to remove the punctuation"""
    return text.translate(str.maketrans('', '', PUNCT_TO_REMOVE))





list_wo_punct = []
for sent in diagnosis_cleaned:
    try:
        sent = remove_punctuation(sent.lower())
        list_wo_punct.append(sent)
    except:
        pass
    
    
covid_list = []    
for sent in list_wo_punct:
    pattern = re.sub(r'covid19', 'covid', sent )
    pattern = re.sub(r'коронавирусная', 'covid', pattern)
    pattern = re.sub(r'короновирусная', 'covid', pattern)
    pattern = re.sub(r'b342', 'covid', pattern)
    pattern = re.sub(r'sarscov2', 'covid', pattern)
    pattern = re.sub(r'торсков2', 'covid', pattern)
    pattern_1 = re.compile(r'covid')
    patt_2 = re.search(pattern_1, pattern)
    #patt_2 = pattern_1.findall(''.join(pattern.split()))
    try:
        covid_list.append(patt_2)
    except:
        pass
    
    
  
pn_list = []
for sent in list_wo_punct:
    pattern = re.sub(r'пневмония', 'J18', sent )
    pattern = re.sub(r'пне...ния', 'J18', pattern)
    pattern = re.sub(r'внегоспитальная', 'J18', pattern)
    pattern = re.sub(r'внебольничная', 'J18', pattern)
    #pattern = re.sub(r'sarscov2', 'covid', pattern)
    #pattern = re.sub(r'торсков2', 'covid', pattern)
    pattern_1 = re.compile(r'J18')
    patt_2 = re.search(pattern_1, pattern)
    #patt_2 = pattern_1.findall(''.join(pattern.split()))
    try:
        pn_list.append(patt_2)
    except:
        pass  
    
    
p = []

for i in pn_list:
    if not i:
        p.append(0)
    else:
        p.append(1)
        
        
c =[]
for i in covid_list:
    if not i:
        c.append(0)
    else:
        c.append(1)        
        
        
        

data_dct = {'Platlets':plt_, 'Leucocytes': wbc_, 'Hemoglobin': hgb_,
           'Creatinine': crea_, 'LDG':ldh_, 'Gender':sex_, 'CRP':crp_,
            'Treatment':tr, 'Birthday': bir, 'Admission':ad,
            'Discharge':dis, 'ID':ID_, 'Diagnosis': list_wo_punct,
            'COVID-19': c, 'Pneumonia': p, 'RF': rfl, "ALT": alt_, "AST": ast_, "Procalcitonine": pct_ }
        


dataFrame = pd.DataFrame(data_dct)


dataFrame.head(5)

dataFrame.to_csv('Data7.csv')
