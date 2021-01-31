import os
import pandas as pd
import glob
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
  int_=0
  for i in file_.split():
    int_ += 1
    if i in pattern_diagnosis:
      return file_.split()[int_+1:int_+40]    
  

def crp(file_):
  """returns all crp values"""
  pattern = re.sub(r'[ЦСC]РБ', 'С-реактивныйбелок', file_)
  pattern_1 = re.compile(r'(?:\w\Dреактивныйбелок|\w\Dреактивныйбелокдо)\
                         (\d*.\d+|\d+)')
  pattern_2 = pattern_1.findall(''.join(pattern.split()))
  try:
    return pattern_2
  except:
    return 'None'


def gender(file_):
  patt1 = re.compile(r'(?<=Ф.И.О:)[А-Я]\w{,20}[А-Я]\w{,20}(вич)')
  patt2 = patt1.findall(file_)
  try:
    if patt2:
      return 'male'
    else:
      return 'female'
  except:
      pass
  

def ldh(file_):
  file_ = file_.lower()
  file_ = re.sub(r'[():]', '', file_)
  file_ = re.sub(r'\d\d\.\d\d\.\d{2,4}', '', file_)
  file_ = re.sub(r'\wактатдегидрогеназ\w', 'лдг', file_)
  patt1 = re.compile(r'(?<=лдг)\d{,4}')
  patt2 = patt1.findall(''.join(file_.split()))
  try:
    if patt2:
      return patt2
    else:
      return 'None'
  except:
    pass



def cre(file_):
  """Returns all creatinine values"""
  file_ = file_.lower()
  file_ = re.sub(r'[():]', '', file_)
  file_ = re.sub(r'\d\d\.\d\d\.\d{2,4}', '', file_)
  file_ = re.sub(r'(\wреатини\w|креатин|креат)(?![а-яА-Я,])', 'cre', file_)
  patt1 = re.compile(r'(?<=cre)\d{,3}')
  patt2 = patt1.findall(''.join(file_.split()))
  try:
    if patt2:
      return patt2
    else:
      return 'None'
  except:
    pass


def hgb(file_):
  """returns list of str with level of hemoglobin"""
  file_ = file_.lower()
  file_ = re.sub(r'[():]', '', file_)
  patt = re.compile(r'гемоглобин|гемогл|гб|гем')
  patt1 = re.sub(patt, r'hgb', file_)
  patt2 = re.compile(r'(?<=hgb)\d{2,3}')
  all_hgb = patt2.findall(''.join(patt1.split()))
  try:
    if all_hgb:
      return all_hgb
    else:
      return 'None'
  except:
    pass


def wbc(file_):
  """returns list of str with level of wbc"""
  file_ = file_.lower()
  patt1 = re.sub(r'[():]', '', file_)
  patt1 = re.sub(r'10(\*|[еe])9', '', patt1)
  patt1 = re.sub(r'\Dбщийанализкрови', 'оак', patt1) 
  patt2 = re.sub(r'(?<=оак)\d\d.\d\d.\d{2,4}|(?<=оак)\d\d.\d\d', '', patt1)
  patt3 = re.compile(r'(?<=оак|wbc)(?:л|лейкоцит\w)(\d*.\d+|\d+)')
  all_wbc = patt3.findall(''.join(patt2.split()))
  try:
    if all_wbc:
      return all_wbc
    else:
      return 'None'
  except:
    pass


def plt(file_):
  """returns list of str with level of plt"""
  file_ = file_.lower()
  file_ = re.sub(r'[():]', '', file_)
  file_ = re.sub(r'10(\*|[еe])9', '', file_)
  patt2 = re.compile(r'(?:\wромбоцит\w|тр)')
  patt1 = re.sub(patt2, '', file_)
  patt1 = ''.join(patt1.split())
  patt2 = re.compile(r'(?<=plt)\d{3}')
  all_plt = patt2.findall(patt1)
  try:
    if all_plt:
      return all_plt
    else:
      return 'None'
  except:
    pass