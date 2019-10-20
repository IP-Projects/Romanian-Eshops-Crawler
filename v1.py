import random
import time
import urllib.request
import csv
import re
from bs4 import BeautifulSoup




def startProgram():
    reqheaders = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'
    }
    # getEmagLaptops('https://www.emag.ro/laptopuri/p',24,reqheaders)
    # getPCGarageLaptops('https://www.pcgarage.ro/notebook-laptop/pagina',45,reqheaders)
    getCelRoLaptops('http://www.cel.ro/laptop-laptopuri/0a-',28,reqheaders)

 

def getEmagLaptops(url,maxPage,reqheaders):
    for index in range(1,maxPage + 1):
        site= url + str(index) + '/c'
        req = urllib.request.Request(site, headers=reqheaders)
        try:
            page = urllib.request.urlopen(req)
            soup = BeautifulSoup(page, 'html.parser')
            data = soup.findAll('a',attrs={'class':'thumbnail-wrapper js-product-url'})
            for link in data:
                characteristicsList = getEmagCharacteristics(link['href'],reqheaders)
                name = link.find('div').find('img')['alt']
                list = ['Emag',name,link['href']] + characteristicsList
                for i in range(0,len(list)):
                    # print(list[i])
                    list[i] = list[i].replace("®","")
                    list[i] = list[i].replace("™","")
                    # print(list[i])
                csvFileWriter.writerow(list)
                # break
        except Exception as e:
            print("An exception occurred")
            print (e)


def getEmagCharacteristics(url,reqheaders):
    req = urllib.request.Request(url, headers=reqheaders)
    try:
        page = urllib.request.urlopen(req)
    except Exception as e:
        print("An exception occurred")
        print (e)
        return []
    soup = BeautifulSoup(page, 'html.parser')
    price = soup.find('p',attrs={'class':'product-new-price'}).renderContents().decode("utf-8").strip().split('<')[0]
    price = price.replace('.','')

    producatorProcesor = ''
    famlilieProcesor=''
    modelProcesor = ''
    arhitectura = ''
    nrNuclee = ''
    diagonalaDisplay=''
    formatDisplay =''
    tehnologieDisplay='' # ips, tn
    rezolutiedisplay='' #fHD, uhd
    capacitateRam=''
    frecventaRam =''
    tipStocare = ''
    capacitateStocare=''
    tipPlacaVideo='' 
    chipsetVideo='' #seria placa video
    modelVideo=''

    data = soup.findAll('td')
    for i in range(0,len(data)):
        data[i] =  data[i].renderContents().decode("utf-8").strip()
    for i in range(0,len(data)) :
        if data[i] == 'Producator procesor':
            producatorProcesor = data[i+1]
        if data[i] == 'Tip procesor':
            famlilieProcesor = data[i+1]
        if data[i] == 'Model procesor':
            modelProcesor = data[i+1]
        if data[i] == 'Arhitectura':
            arhitectura = data[i+1]
        if data[i] == 'Numar nuclee':
            nrNuclee = data[i+1]
        if data[i] == 'Diagonala display':
            diagonalaDisplay = data[i+1]
            diagonalaDisplay = diagonalaDisplay.replace(" inch","")
        if data[i] == 'Format display':
            formatDisplay = data[i+1]
        if data[i] == 'Tehnologie display':
            if("IPS" in data[i+1]):
                tehnologieDisplay = "IPS"
            else:
                tehnologieDisplay = data[i+1]
        if data[i] == 'Rezolutie':
            rezolutiedisplay = data[i+1]
        if data[i] == 'Capacitate memorie':
            capacitateRam = data[i+1]
        if data[i] == 'Frecventa':
            frecventaRam = data[i+1]
        if data[i] == 'Tip stocare':
            tipStocare = data[i+1]
        if data[i] == 'Capacitate stocare':
            capacitateStocare = data[i+1]
        if data[i] == 'Tip placa video':
            tipPlacaVideo = data[i+1]
        if data[i] == 'Chipset video':
            if("Intel" in data[i+1]):
                chipsetVideo = "Intel"
            if('nVidia' in data[i+1]):
                chipsetVideo = "nVidia"
            if('AMD' in data[i+1]):
                chipsetVideo = "AMD"
            # chipsetVideo = data[i+1]
            # chipsetVideo.replace(" GeForce","")
            # chipsetVideo.replace(" GTX","")
        if data[i] == 'Model placa video':
            modelVideo = data[i+1]
            modelVideo = modelVideo.replace("GeForce","")

    return [price,producatorProcesor,famlilieProcesor,modelProcesor,arhitectura,nrNuclee,diagonalaDisplay,formatDisplay,tehnologieDisplay,rezolutiedisplay,capacitateRam,frecventaRam,tipStocare,capacitateStocare,tipPlacaVideo,chipsetVideo,modelVideo]



def getPCGarageLaptops(url,maxPage,reqheaders):
    for index in range(1,maxPage + 1):
        
        site= url + str(index) + '/'
        req = urllib.request.Request(site, headers=reqheaders)
        try:
            page = urllib.request.urlopen(req)
            soup = BeautifulSoup(page, 'html.parser')
            data = soup.findAll('div',attrs={'class':'pb-name'})
            for div in data:
                link = div.find('a')
                characteristicsList = getPCGarageCharacteristics(link['href'],reqheaders)
                name = link['title']
                list = ['PCGarage',name,link['href']] + characteristicsList
                for i in range(0,len(list)):
                    # print(list[i])
                    list[i] = list[i].replace("®","")
                    list[i] = list[i].replace("™","")
                    # print(list[i])
                csvFileWriter.writerow(list)
                # break
        except Exception as e:
            print("An exception occurred")
            print (e)


def getPCGarageCharacteristics(url,reqheaders):
    req = urllib.request.Request(url, headers=reqheaders)
    try:
        page = urllib.request.urlopen(req)
    except Exception as e:
        print("An exception occurred")
        print (e)
        return []
    soup = BeautifulSoup(page, 'html.parser')
    price = soup.find('meta',attrs={'itemprop':'price'})['content'].strip().split('.')[0]

    producatorProcesor = ''
    famlilieProcesor=''
    modelProcesor = ''
    arhitectura = ''
    nrNuclee = ''
    diagonalaDisplay=''
    formatDisplay =''
    tehnologieDisplay='' # ips, tn
    rezolutiedisplay='' #fHD, uhd
    capacitateRam=''
    frecventaRam =''
    tipStocare = ''
    capacitateStocare=''
    tipPlacaVideo='' 
    chipsetVideo='' #seria placa video
    modelVideo=''

    data = soup.find('table', attrs={'class':'specs-table'}).findAll('td')
    # print(data)
    for i in range(0,len(data)):
        data[i] =  data[i].renderContents().decode("utf-8").strip()
    for i in range(0,len(data)) :
        if data[i] == 'Producator':
            producatorProcesor = data[i+1]
        if data[i] == 'Familie':
            if('i3' in data[i+1]):
                famlilieProcesor = 'i3'
            if('i5' in data[i+1]):
                famlilieProcesor = 'i5'
            if('i7' in data[i+1]):
                famlilieProcesor = 'i7'
            if('i3','i5','i7' not in data[i+1]):
                famlilieProcesor = data[i+1]
        if data[i] == 'Model' and data[i+2] == "Nucleu":
            modelProcesor = data[i+1]
        if data[i] == 'Nucleu':
            arhitectura = data[i+1]
        if data[i] == 'Numar nuclee':
            nrNuclee = data[i+1]
        if data[i] == 'Diagonala':
            diagonalaDisplay = data[i+1]
            diagonalaDisplay = diagonalaDisplay.replace(" inch","")
        if data[i] == 'Format':
            formatDisplay = data[i+1]
        if data[i] == 'Tehnologie ecran':
            if("IPS" in data[i+1]):
                tehnologieDisplay = "IPS"
            else:
                tehnologieDisplay = data[i+1]
        if data[i] == 'Rezolutie':
            rezolutiedisplay = data[i+1]
            rezolutiedisplay = rezolutiedisplay.replace(" pixeli","")
        if data[i] == 'Capacitate':
            capacitateRam = data[i+1]
        if data[i] == 'Frecventa':
            frecventaRam = data[i+1]
        if data[i] == 'Capacitate HDD':
            tipStocare = tipStocare + 'HDD'
            capacitateStocare = capacitateStocare + data[i+1]
        if data[i] == 'Capacitate SSD':
            if "HDD" in tipStocare:
                tipStocare = tipStocare + "+" + 'SSD'
                capacitateStocare = capacitateStocare + "+" + data[i+1]
            else:
                tipStocare = tipStocare + 'SSD'
                capacitateStocare = capacitateStocare + data[i+1]
        if data[i] == 'Placa video':
            tipPlacaVideo = data[i+1]
        if data[i] == 'Producator chipset':
            # chipsetVideo = data[i+1]
            if("Intel" in data[i+1]):
                chipsetVideo = "Intel"
            if('nVidia' in data[i+1]):
                chipsetVideo = "nVidia"
            if('AMD' in data[i+1]):
                chipsetVideo = "AMD"
        if data[i] == 'Model' and data[i+2] == "Memorie dedicata":
            modelVideo = data[i+1]
            modelVideo = modelVideo.replace("GeForce","")

    return [price,producatorProcesor,famlilieProcesor,modelProcesor,arhitectura,nrNuclee,diagonalaDisplay,formatDisplay,tehnologieDisplay,rezolutiedisplay,capacitateRam,frecventaRam,tipStocare,capacitateStocare,tipPlacaVideo,chipsetVideo,modelVideo]



def getCelRoLaptops(url,maxPage,reqheaders):
    for index in range(1,maxPage + 1):
        
        site= url + str(index) + '/'
        req = urllib.request.Request(site, headers=reqheaders)
        try:
            page = urllib.request.urlopen(req)
            soup = BeautifulSoup(page, 'html.parser')
            data = soup.findAll('a',attrs={'class':'productListing-data-b product_link product_name'})
            for a in data:
                characteristicsList = getCelRoCharacteristics(a['href'],reqheaders)
                name = a.find('span',attrs={'itemprop':'name'}).text
                list = ['CelRo',name,a['href']] + characteristicsList
                for i in range(0,len(list)):
                    # print(list[i])
                    list[i] = list[i].replace("®","")
                    list[i] = list[i].replace("™","")
                    # print(list[i])
                csvFileWriter.writerow(list)
                # break
        except Exception as e:
            print("An exception occurred")
            print (e)


def getCelRoCharacteristics(url,reqheaders):
    req = urllib.request.Request(url, headers=reqheaders)
    try:
        page = urllib.request.urlopen(req)
    except Exception as e:
        print("An exception occurred")
        print (e)
        return []
    soup = BeautifulSoup(page, 'html.parser')
    price = soup.find('span',attrs={'itemprop':'price'}).text.strip()

    producatorProcesor = ''
    famlilieProcesor=''
    modelProcesor = ''
    arhitectura = ''
    nrNuclee = ''
    diagonalaDisplay=''
    formatDisplay =''
    tehnologieDisplay='' # ips, tn
    rezolutiedisplay='' #fHD, uhd
    capacitateRam=''
    frecventaRam =''
    tipStocare = ''
    capacitateStocare=''
    tipPlacaVideo='' 
    chipsetVideo='' #seria placa video
    modelVideo=''

    data = soup.findAll('td')
    # print(data)
    for i in range(0,len(data)):
        data[i] =  data[i].renderContents().decode("utf-8").strip()
        data[i] = data[i].replace("<div>","")
        data[i] = data[i].replace("</div>","")
    for i in range(0,len(data)) :
        if data[i] == 'Model Procesor:':
            if("Intel" in data[i+1]):
                producatorProcesor = "Intel"
            if('AMD' in data[i+1]):
                producatorProcesor = "AMD"
            data[i+1] = data[i+1].replace("®","")
            data[i+1] = data[i+1].replace("™","")
            data[i+1] = data[i+1].replace("-"," ")
            data[i+1] = data[i+1].replace(data[i+5],"").strip()
            modelProcesor = data[i+1]
        if data[i] == 'Procesor:':
            if('i3' in data[i+1]):
                famlilieProcesor = 'i3'
            elif('i5' in data[i+1]):
                famlilieProcesor = 'i5'
            elif('i7' in data[i+1]):
                famlilieProcesor = 'i7'
            else:
                famlilieProcesor = data[i+1]
            print(famlilieProcesor)
        if data[i] == 'Platforma Procesor:':
            arhitectura = data[i+1]
        if data[i] == 'Diagonala LCD:':
            diagonalaDisplay = data[i+1]
            diagonalaDisplay = diagonalaDisplay.replace(" inch","")
        if data[i] == 'Tip display:':
            if("IPS" in data[i+1]):
                tehnologieDisplay = "IPS"
            if('FullHD' in data[i+1]):
                formatDisplay = 'Full HD'
            if('UltraHD' in data[i+1]):
                formatDisplay = 'Ultra HD'
        if data[i] == 'Rezolutie optima:':
            rezolutiedisplay = data[i+1]
            rezolutiedisplay = rezolutiedisplay.replace(" pixeli","")
        if data[i] == 'Memorie standard:':
            capacitateRam = data[i+1]
        if data[i] == 'Frecventa Memorie RAM:':
            frecventaRam = data[i+1]
        if data[i] == 'Capacitate HDD:':
            tipStocare = data[i+1]
        if data[i] == 'Tip unitate stocare:':
                tipStocare = data[i+1]
        if data[i] == 'Chipset video:':
            if("Intel" in data[i+1]):
                chipsetVideo = "Intel"
                tipPlacaVideo = 'Integrata'
            if('NVIDIA' in data[i+1]):
                chipsetVideo = "nVidia"
                tipPlacaVideo = 'Dedicata'
                modelVideo = data[i+1].replace('NVIDIA(R) GeForce(R) ','')[0:8]
                modelVideo = data[i+1].replace('NVIDIA GeForce ','')[0:8]
            if('nVidia' in data[i+1]):
                chipsetVideo = "nVidia"
                tipPlacaVideo = 'Dedicata'
                modelVideo = data[i+1].replace('nVidia GeForce ','')[0:8]
            if('AMD' in data[i+1]):
                chipsetVideo = "AMD"
                tipPlacaVideo = 'Dedicata'
                modelVideo = data[i+1]
        if data[i] == 'Model' and data[i+2] == "Memorie dedicata":
            modelVideo = data[i+1]
            modelVideo = modelVideo.replace("GeForce","")

    return [price,producatorProcesor,famlilieProcesor,modelProcesor,arhitectura,nrNuclee,diagonalaDisplay,formatDisplay,tehnologieDisplay,rezolutiedisplay,capacitateRam,frecventaRam,tipStocare,capacitateStocare,tipPlacaVideo,chipsetVideo,modelVideo]




file = open('index.csv', mode='w',newline='')
csvFileWriter = csv.writer(file, delimiter=',')
csvFileWriter.writerow(['Shop','Name','Link','Price','Producator procesor','Tip procesor','Model Procesor','Arhitectura','Numar nuclee','Diagonala display','Format display','Tehnologie display','Rezolutie','Capacitate Ram','Frecventa Ram','Tip stocare','Capacitate stocare','Tip placa video','Chipset video','Model placa video'])
startProgram()

