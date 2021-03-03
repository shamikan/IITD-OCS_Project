from django.shortcuts import render
import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup
# Create your views here.

list1=['google','microsoft','facebook']
list_final=[]

baseurl="https://github.com/"
s=HTMLSession()

class Node:
    def __init__(self,name,link,f_count):
        self.name=name
        self.link=link
        self.f_count=f_count

list_final=[]
def getData(url):
    r=s.get(url)
    soup= BeautifulSoup(r)
    return soup

def getNextPage(soup,p):
    page=soup.find_all('div',{'class':'paginate-container d-none d-md-flex flex-md-justify-center'})
    if not page.find('span',{'class':'next_page disabled'}):
        url='https://github.com/'+p+(page.find('a'))['href']
        return url
    else:
        return 


def getURLlist(url,org):
    url_list=[]
    while True:
        soup=getData(url)
        url=getNextPage(soup,org)
        if not url:
            break
        url_list.append(url)
    return url_list

def getNameFork(url_list):
    for urli in url_list:
        soup=getData(urli)
        name=[]
        rep_link=[]
        count=[]

        for x in soup.find_all('a',{'class':'d-inline-block'}):
            name.append(x)
        
        for x in soup.find_all('a',href=True):
            rep_link.append(baseurl+x['href'])

        for x in soup.find_all('a',{'class':'muted-link mr-3'}):
            count.append(x)

        for i in range(len(name)):
            n=Node(name[i],rep_link[i],count[i])
            list_final.append(n)

    return list_final


def index(request):
    if request.method=='POST':
        org=request.POST.get('Organisation')
        n=request.POST.get('N')
        m=request.POST.get('M')

        #list1=['google','microsoft','facebook']
        #baseurl="https://github.com/"+list1[org]
        p=getURLlist(baseurl,list1[org])
        q=getNameFork(p)
        l1=[]
        l2=[]
        l3=[]
        for i in n:
            eman=q[i].name
            knil=q[i].link
            tnuoc_f=q[i].f_count
            l1.append(eman)
            l2.append(knil)
            l3.append(tnuoc_f)
            
            
    context={
            'list1':l1,
            'list2':l2,
            'list3':l3,
    }
    templates='Fetch/html/index.html'
    return render(request,templates,context)
