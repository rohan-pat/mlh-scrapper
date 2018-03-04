import requests
from bs4 import BeautifulSoup
from collections import OrderedDict

r=requests.get("https://mlh.io/seasons/na-2018/events")
c=r.content
soup=BeautifulSoup(c,"html.parser")
#pg_nr=soup.find_all("a",{"class":"Page"})[-1].text

states = dict()
with open('us_states.txt', 'r') as f:
    no = 1
    while no <= 64:
        x = f.readline()
        x = x.strip().split(",")
        x[0] = x[0].strip()
        x[1] = x[1].strip()
        states[x[1]] = x[0]
        no += 1

print(states)

l=[]
#base_url= "https://mlh.io/"
#for page in range(0,int(pg_nr)*10,10):
#r=requests.get(base_url+str(page))
#c=r.content
#soup=BeautifulSoup(c,"html.parser")
all=soup.find_all("div",{"class":"event-wrapper"})
for item in all:
  d= OrderedDict()
  try:
      d["Name"]=item.find("h3",{"itemprop":"name"}).text
      # print(type(d["Name"]))
  except:
      d["Name"]=None
  try:
      d["startDate"]=item.find("meta",{"itemprop":"startDate"})["content"]
  except:
      d["startDate"]=None
  # print(d["startDate"])
  try:
      d["endDate"]=item.find("meta",{"itemprop":"endDate"})["content"]
  except:
      d["endDate"]=None
  # print(d["endDate"])
  try:
      d["Locality"]=item.find("span",{"itemprop":"addressLocality"}).text
  except:
      d["Locality"]=None
  try:
      d["State"]=item.find("span",{"itemprop":"addressRegion"}).text
  except:
      d["State"]=None
  l.append(d)

new_list = []
for d_dict in l:
    inner_list = list()
    for k, v in d_dict.items():
        if v == None:
            print("null value found!")
        if v in states:
            v = states[v]
        inner_list.append(v)
    new_list.append(tuple(inner_list))
# print(new_list)
print("length of new list ", len(new_list))
print("sample tuple is ", new_list[1])
# for i in range()

import MySQLdb as my
db = my.connect(host="webscrapper-instance.c2ay3hczfmtj.us-east-2.rds.amazonaws.com",
user="admin_webscrap",
passwd="password",
db="mlh_data"
)
cursor = db.cursor()

# for l in new_list:
sql = """insert into hackathon(Name, startDate, endDate, City, State) VALUES(%s, %s, %s, %s, %s)"""
number_of_rows = cursor.executemany(sql, new_list)

db.commit()
db.close()



#df=pandas.DataFrame(l)
#df.to_csv("output.csv")
