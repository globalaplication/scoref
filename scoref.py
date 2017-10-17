# -*- coding: utf-8 -*-
#!/usr/bin/env python
#https://i.hizliresim.com/zJn7PB.png
from Tkinter import *
import time, os, pygame, httplib, sys, msql, datetime, json
os.system('rm /var/tmp/database.msql')
try:
  import urllib.request as url
except ImportError:
    import urllib
msql.connect('/var/tmp/database.msql')
msql.execute('CREATE TABLE canlisonuclar (ID:id, Code:Int, DT:Text, ATTR:Text, HTTR:Text, AMS:Int, HMS:Int, AIY:Int, HIY:Int, STL:Text, STATE:Text, TV:Text, LIG:Text, DEVRE:Int, AG:Text, HG:Text)')
date = str(datetime.datetime.now())[0:10].split('-')
datenow = date[0] +'-'+ date[1] +'-'+ date[2]
clock = str(datetime.datetime.now()).split(' ')[0:5]
AMS, HMS = -1,-1
AIY, HIY = -1,-1
geometry = ['CENTER']
color = {'Goal':'LIMEGREEN', 'Font':'Ubuntu 9', 'Maç Sonucu':'red', 'Lig':'white', 'IYSCORE':'white', 'MSSCORE':'white',
         'Devre Arası':'yellow', 'Başlamadı':'brown', 'IYLABEL':'DIMGRAY', 'background':'black','Oynanıyor':'green', 'Saat':'FLORALWHITE', 
         'GM':'orange', 'Ertelendi':'pink', 'TV':'white','ATTR':'DIMGRAY', 'HTTR':'DIMGRAY', 'exit_bg':'#1c1c1c', 'exit_fg':'gray', 'select_bg':'FLORALWHITE','select_fg':'black','title_bg':'#1c1c1c', 'title_fg':'gray', 'hide':'orange', 'C':'gray', 'R':'gray'} #Renk font size değerlerini değiştirerek uygulamayı özelleştirebilirsin.
enabled = {'Saat':1, 'Code':1, 'STL':0, 'ATTR':1, 'LIG':0,
           'HTTR':1, 'MS':1, 'IY':1, 'TV':1, 'STATE':True} # Eğer etiketi ekranda görmek istemiyorsan değerini {0} yapmalısın. Bu özellik {Saat Code STL IY LIG STATE} için uygulanabilir.
def exit_(event):
    windows.destroy()
def live_soccer(event):
    print 'http://www.xsportv2.com/canli.html'
def hide_command(event):
    windows.state("withdrawn")
def center_geometry(event):
    windows.geometry('{}x{}-{}+{}'.format(str(frame1.winfo_width()+10), str(windows.winfo_height()) , windows.winfo_screenwidth()/2-(frame1.winfo_width()+10)/2, 0))
    geometry.append('CENTER')
def right_geometry(event): 
    windows.geometry('{}x{}-{}+{}'.format(str(frame1.winfo_width()+10), str(windows.winfo_height()) , +30, +0))
    geometry.append('RIGHT')
def goal():
    windows.state("normal")
    pygame.init()
    pygame.mixer.music.load('golsesi.ogg')
    pygame.mixer.music.play()
def truefalse(code): #kayitlimi?
    code = int(code)
    codetf = []
    for canlisonuclar in range(1, msql.count('canlisonuclar')+1, +1):
        if code == int(msql.gets('canlisonuclar', canlisonuclar)[1]):
            codetf.append(True)
            break
    if True in codetf:
        return True
    else:
        return False
def program():
    global goal_
    goal_=False
    url = 'https://www.nesine.com/iddaa/IddaaResultsData?BetType=1&OnlyLive=0&Date='+datenow+'&League=&FilterType=init'
    source = urllib.urlopen(url)
    data = json.load(source)
    for OnlineIddaa in range(0, len(data['result']), +1):
        Code, DT = int(data['result'][OnlineIddaa]['C']), str(data['result'][OnlineIddaa]['DT'])
        HTTR, ATTR = str(data['result'][OnlineIddaa]['HTTR'].encode('Utf-8')), str(data['result'][OnlineIddaa]['ATTR'].encode('Utf-8'))
        ES = data['result'][OnlineIddaa]['ES']
        STL = str(data['result'][OnlineIddaa]['STL'].encode('Utf-8')) #Text
        DT =  data['result'][OnlineIddaa]['DT']
        LIG = data['result'][OnlineIddaa]['L'].encode('Utf-8')
        GOALS, AG, HG = data['result'][OnlineIddaa]['ME'], '',''
        TV = data['result'][OnlineIddaa]['TV']
        if TV is None or len(TV) is 0: TV = ''
        else: TV = '(TV)'
        if len(STL) == 0 : STL = 'Oynaniyor'
        T = data['result'][OnlineIddaa]['ES']
        if str(Code) in sys.argv[1:]:
            if len(T) is 1:
                DEVRE = 1
            else:
                DEVRE = 2
            if len(GOALS) is not 0:
                for SCORE in GOALS:
                    if SCORE['TS'] is 1:
                        if SCORE['T'] is 1 or SCORE['T'] is 4 or SCORE['T'] is 2 or SCORE['T'] is 3:
                            HG = HG + str(SCORE['P'].encode('Utf-8')+':'+SCORE['M'].encode('Utf-8')+',')
                    if SCORE['TS'] is 2:
                        if SCORE['T'] is 1 or SCORE['T'] is 4 or SCORE['T'] is 2 or SCORE['T'] is 3:
                            AG = AG + str(SCORE['P'].encode('Utf-8')+':'+SCORE['M'].encode('Utf-8')+',')
            if len(T) is 0:
                AIY = -1
                HIY = -1
                AMS = AIY
                HMS = HIY
            if len(T) is 1:
                AIY = int(T[1-1]['A'])
                HIY = int(T[1-1]['H'])
                AMS = AIY
                HMS = HIY
            if len(T) is 3:
                AIY = int(T[2-1]['A']) #T1
                HIY = int(T[2-1]['H']) #T1
                AMS = int(T[3-1]['A']) #T2
                HMS = int(T[3-1]['H']) #T2
            if len(T) is 2:
                AIY = int(T[2-1]['A'])
                HIY = int(T[2-1]['H'])
                AMS = int(T[1-1]['A'])
                HMS = int(T[1-1]['H'])

            string = {'Code':Code, 'DT':DT, 'ATTR':ATTR, 'HTTR':HTTR, 'AMS':AMS, 'HMS':HMS, 'AIY':AIY, 'HIY':HIY, 'STL':STL, 'STATE':'', 'TV':TV, 'LIG':LIG, 'DEVRE':DEVRE, 'AG':AG, 'HG':HG}
            
            if truefalse(Code) == False:
                msql.execute('INSERT INTO canlisonuclar ROW (Code, DT, ATTR, HTTR, AMS, HMS, AIY, HIY, STL, STATE, TV, LIG, DEVRE, AG, HG) NOT (Code)', string['Code'], string['DT'], string['ATTR'], string['HTTR'], string['AMS'], string['HMS'], string['AIY'], string['HIY'], string['STL'], string['STATE'], string['TV'], string['LIG'], string['DEVRE'], string['AG'], string['HG'])
                msql.update()
            else:
                for id in range(1, msql.count('canlisonuclar')+1, +1):  #'KAYITLI-TRUE'
                    db_Code = msql.gets('canlisonuclar', id)[1]
                    if db_Code == Code:
                        db_DT, db_STL = msql.gets('canlisonuclar', id)[2], msql.gets('canlisonuclar', id)[9]         
                        db_ATTR, db_HTTR = msql.gets('canlisonuclar', id)[3], msql.gets('canlisonuclar', id)[4]      
                        db_AMS, db_HMS = msql.gets('canlisonuclar', id)[5], msql.gets('canlisonuclar', id)[6] 
                        db_AIY, db_HIY = msql.gets('canlisonuclar', id)[7], msql.gets('canlisonuclar', id)[8]
                        db_AG, db_HG = msql.gets('canlisonuclar', id)[-2], msql.gets('canlisonuclar', id)[-1]
                        if db_AG != string['AG']:
                            msql.UPDATE_(id, 'canlisonuclar', 'AG', string['AG'])
                        if db_HG != string['HG']:
                            msql.UPDATE_(id, 'canlisonuclar', 'HG', string['HG'])
                        if  db_STL != STL:
                            windows.state("normal")
                            msql.UPDATE_(id, 'canlisonuclar', 'STL', STL)
                            msql.UPDATE_(id, 'canlisonuclar', 'STATE', 'STL')
                        if  db_AIY is not AIY:
                            msql.UPDATE_(id, 'canlisonuclar', 'AIY', AIY)
                            msql.UPDATE_(id, 'canlisonuclar', 'STATE', 'AIY')
                            goal_=True
                        if  db_HIY is not HIY:
                            msql.UPDATE_(id, 'canlisonuclar', 'HIY', HIY)
                            msql.UPDATE_(id, 'canlisonuclar', 'STATE', 'HIY')
                            goal_=True
                        if  db_AMS is not AMS:
                            msql.UPDATE_(id, 'canlisonuclar', 'AMS', AMS)
                            msql.UPDATE_(id, 'canlisonuclar', 'STATE', 'AMS')
                            goal_=True
                        if  db_HMS is not HMS:
                            msql.UPDATE_(id, 'canlisonuclar', 'HMS', HMS)
                            msql.UPDATE_(id, 'canlisonuclar', 'STATE', 'HMS')
                            goal_=True
    exit =Label(frame0,text=' x ',bg=color['exit_bg'],fg=color['exit_fg'],
              anchor=E,justify=LEFT,font=('Verdana', 9, 'bold'))
    exit.grid(row=1,column=1, sticky=E)
    exit.bind('<Button-1>', exit_)
    Label(frame0,bg=color['background'],fg=color['title_fg'],
              anchor=E,justify=LEFT,font=('Verdana', 9, 'bold')).grid(row=1,column=2, sticky=E)
    title = Label(frame0,text='Canlı Maç Sonuçları  ',bg=color['title_bg'],fg=color['title_fg'],
              anchor=E,justify=LEFT,font=('Ubuntu', 9, 'bold')).grid(row=1,column=3, sticky=E)
    frame0.update()
    if enabled['STL'] is 1:
        Label(frame5, text='DA',bg=color['background'],fg=color['Devre Arası'], 
              anchor=E, justify=RIGHT, font=('Verdana 7')).grid(row=1, column=1, sticky=E) 
        Label(frame5, text='MS',bg=color['background'],fg=color['Maç Sonucu'], 
              anchor=E, justify=RIGHT, font=('Verdana 7')).grid(row=1, column=2, sticky=E) 
        Label(frame5, text='OY',bg=color['background'],fg=color['Oynanıyor'], 
              anchor=E, justify=RIGHT, font=('Verdana 7')).grid(row=1, column=3, sticky=E) 
        Label(frame5, text='BSL',bg=color['background'],fg=color['Başlamadı'], 
              anchor=E, justify=RIGHT, font=('Verdana 7')).grid(row=1, column=4, sticky=E) 
    for id in range(1, msql.count('canlisonuclar')+1, +1):
        for c in range(1, 22):
            truefalse_goal = msql.gets('canlisonuclar', id)[10]
            HMS, AMS = msql.gets('canlisonuclar', id)[6], msql.gets('canlisonuclar', id)[5]
            HIY, AIY = msql.gets('canlisonuclar', id)[8], msql.gets('canlisonuclar', id)[7]
            db_DEVRE = msql.gets('canlisonuclar', id)[13]
            DEVRE_1 = HIY + AIY
            DEVRE_2 = AMS + HMS
            if db_DEVRE is 1:
                TG = DEVRE_1
            else:
                TG = DEVRE_2
            if c is 5 and enabled['TV'] is 1:
                LBL_TV = Label(frame1,text=msql.gets('canlisonuclar',id)[11],bg=color['background'],fg=color['TV'],anchor=NW,justify=LEFT,font=('Verdana 5'))
                LBL_TV.grid(row=id,column=c, sticky=W)
                LBL_TV.bind('<Button-1>', live_soccer)
            if c is 4 and enabled['Code'] is 1:
                if msql.gets('canlisonuclar', id)[9] == 'Maç Sonucu':
                    LBL_CODE = Label(frame1,text=msql.gets('canlisonuclar',id)[1],bg=color['background'],fg=color['Maç Sonucu'],anchor=NW,justify=LEFT,
                                     font=(color['Font'])).grid(row=id,column=c, sticky=W) 
                elif msql.gets('canlisonuclar', id)[9] == 'Devre Arası':
                    LBL_CODE = Label(frame1,text=msql.gets('canlisonuclar', id)[1],bg=color['background'],fg=color['Devre Arası'], anchor=NW, justify=LEFT, 
                                     font=(color['Font'])).grid(row=id, column=c, sticky=W) 
                elif msql.gets('canlisonuclar', id)[9] == 'Başlamadı.':
                    LBL_CODE = Label(frame1,text=msql.gets('canlisonuclar', id)[1],bg=color['background'],fg=color['Başlamadı'], anchor=NW, justify=LEFT, 
                                     font=(color['Font'])).grid(row=id, column=c, sticky=W) 
                elif msql.gets('canlisonuclar', id)[9] == 'Ertelendi':
                    LBL_CODE = Label(frame1,text=msql.gets('canlisonuclar', id)[1],bg=color['background'],fg=color['Ertelendi'], anchor=NW, justify=LEFT, 
                                     font=(color['Font'])).grid(row=id, column=c, sticky=W) 
                else:
                    LBL_CODE = Label(frame1,text=msql.gets('canlisonuclar', id)[1],bg=color['background'],fg=color['Oynanıyor'], anchor=NW, justify=LEFT, 
                                     font=(color['Font'])).grid(row=id, column=c, sticky=W)  
            if c is 1 and enabled['Saat'] is 1:
                LBL_CLOCK = Label(frame1,text=msql.gets('canlisonuclar', id)[2],bg=color['background'],fg=color['Saat'], anchor=NW, justify=LEFT, 
                                  font=(color['Font'])).grid(row=id, column=c, sticky=W) 
            if c is 3 and enabled['STL'] is 1:
                if msql.gets('canlisonuclar', id)[9] == 'Maç Sonucu':
                    LBL_STL = Label(frame1,text=msql.gets('canlisonuclar', id)[9] + ' ',bg=color['background'],fg=color['Maç Sonucu'], anchor=NW, justify=LEFT, 
                                    font=(color['Font'])).grid(row=id, column=c, sticky=W) 
                elif msql.gets('canlisonuclar', id)[9] == 'Devre Arası':
                    LBL_STL = Label(frame1,text=msql.gets('canlisonuclar', id)[9] + ' ',bg=color['background'],fg=color['Devre Arası'], anchor=NW, justify=LEFT, 
                                    font=(color['Font'])).grid(row=id, column=c, sticky=W)
                elif msql.gets('canlisonuclar', id)[9] == 'Başlamadı.':
                    LBL_STL = Label(frame1,text=msql.gets('canlisonuclar', id)[9] + ' ',bg=color['background'],fg=color['Başlamadı'], anchor=NW, justify=LEFT, 
                                    font=(color['Font'])).grid(row=id, column=c, sticky=W)
                elif msql.gets('canlisonuclar', id)[9] == 'Ertelendi':
                    LBL_STL = Label(frame1,text=msql.gets('canlisonuclar', id)[9],bg=color['background'],fg=color['Ertelendi'], anchor=NW, justify=LEFT, 
                                    font=(color['Font'])).grid(row=id, column=c, sticky=W) 
                else:
                    LBL_STL = Label(frame1,text=msql.gets('canlisonuclar', id)[9] + ' ',bg=color['background'],fg=color['Oynanıyor'], anchor=NW, justify=LEFT, 
                                    font=(color['Font'])).grid(row=id, column=c, sticky=W)
            if c is 2 and enabled['LIG'] is 1:
                LBL_LIG = Label(frame1,text=msql.gets('canlisonuclar', id)[12],bg=color['background'],fg=color['Lig'], anchor=NW, justify=LEFT, 
                                font=(color['Font'])).grid(row=id, column=c, sticky=W)
            if c is 6:
                if truefalse_goal == 'HIY' or truefalse_goal == 'HMS':
                    LBL_HTTR = Label(frame1, text=msql.gets('canlisonuclar', id)[4],bg=color['background'],fg=color['Goal'],anchor=NW,justify=LEFT,
                                     font=(color['Font'])).grid(row=id, column=c, sticky=E)
                    msql.UPDATE_(id, 'canlisonuclar', 'STATE', '')
                else:
                    beta, test = '', msql.gets('canlisonuclar', id)[-1].split(',')[0:-1]
                    for minute in test:
                        beta = beta +' '+ minute.split(':')[1]
                    if len(beta) < 2:
                        LBL_HTTR = Label(frame1, text=msql.gets('canlisonuclar', id)[4],bg=color['background'], fg=color['HTTR'], anchor=NW, justify=LEFT, 
                                         font=(color['Font'])).grid(row=id, column=c, sticky=E)
                    else:
                        LBL_HTTR = Label(frame1, text=str('('+beta+') ')+msql.gets('canlisonuclar', id)[4],bg=color['background'], fg=color['HTTR'], anchor=NW, justify=LEFT, font=(color['Font'])).grid(row=id, column=c, sticky=E)      
            if c is 7:
                if msql.gets('canlisonuclar', id)[6] is -1: #or db_DEVRE is 1
                    beta = '' 
                else: 
                    beta = msql.gets('canlisonuclar', id)[6]
                LBL_SCORE_HMS = Label(frame1, text=beta,bg=color['background'], fg=color['MSSCORE'], anchor=NW, justify=LEFT, 
                                      font=(color['Font'])).grid(row=id, column=c, sticky=E) 
            if c is 8:
                Label(frame1, text= '-',bg=color['background'], fg='gray', anchor=NW, justify=LEFT, font=(color['Font'])).grid(row=id, column=c, sticky=W) 
            if c is 9:
                if msql.gets('canlisonuclar', id)[5] is -1: #or db_DEVRE is 1
                    beta = '' 
                else: 
                    beta = msql.gets('canlisonuclar', id)[5]
                LBL_SCORE_AMS = Label(frame1, text=beta,bg=color['background'], fg=color['MSSCORE'], anchor=NW, justify=LEFT, 
                                      font=(color['Font'])).grid(row=id, column=c, sticky=E)         
            if c is 10:
                if truefalse_goal == 'AIY' or truefalse_goal == 'AMS': 
                    LBL_ATTR = Label(frame1, text=msql.gets('canlisonuclar', id)[3],bg=color['background'], fg=color['Goal'], anchor=NW, justify=LEFT, 
                                     font=(color['Font'])).grid(row=id, column=c, sticky=W) 
                    msql.UPDATE_(id, 'canlisonuclar', 'STATE', '')
                else:
                    beta, test = '', msql.gets('canlisonuclar', id)[-2].split(',')[0:-1]
                    for minute in test:
                        beta = beta +' '+ minute.split(':')[1]
                    if len(beta) < 2:
                        LBL_ATTR = Label(frame1, text=msql.gets('canlisonuclar', id)[3],bg=color['background'],fg=color['ATTR'],anchor=NW,justify=LEFT, 
                                         font=(color['Font'])).grid(row=id, column=c, sticky=W) 
                    else:
                        LBL_ATTR = Label(frame1, text=msql.gets('canlisonuclar', id)[3] + str(' ('+beta+')'),bg=color['background'], fg=color['ATTR'], anchor=NW, justify=LEFT, font=(color['Font'])).grid(row=id, column=c, sticky=W)                     
            if c is 11:
                continue
                beta, test = '', msql.gets('canlisonuclar', id)[-2].split(',')[0:-1]
                for minute in test:
                    beta = beta +' '+ minute.split(':')[1]
                Label(frame1,text=beta,bg=color['background'],fg=color['GM'], anchor=NW, justify=LEFT, font=('Verdana 6')).grid(row=id, column=c, sticky=W)
            if c is 12 and enabled['IY'] is 1:
                LBL_AIY = Label(frame1, text='  IY',bg=color['background'],fg=color['IYLABEL'],anchor=NW,justify=LEFT,
                                font=(color['Font'])).grid(row=id, column=c, sticky=E) 
            if c is 13 and enabled['IY'] is 1:
                if msql.gets('canlisonuclar', id)[8] is -1:
                    beta = '-'
                else:
                    beta = msql.gets('canlisonuclar', id)[8]
                LBL_SCORE_HIY = Label(frame1,text=beta,bg=color['background'],fg=color['IYSCORE'],anchor=NW,justify=LEFT,
                                      font=(color['Font'])).grid(row=id, column=c, sticky=E) 
            if c is 14 and enabled['IY'] is 1:
                Label(frame1,text='-',bg=color['background'], fg='gray',anchor=NW, justify=LEFT, font=(color['Font'])).grid(row=id, column=c, sticky=E) 
            if c is 15 and enabled['IY'] is 1:
                if msql.gets('canlisonuclar', id)[7] is -1:
                    beta = '-' 
                else: 
                    beta = msql.gets('canlisonuclar', id)[7]
                LBL_SCORE_AIY = Label(frame1, text=beta,bg=color['background'], fg=color['IYSCORE'], anchor=NW, justify=LEFT, 
                                      font=(color['Font'])).grid(row=id, column=c, sticky=E) 
            if c is 16 and (HMS is not -1 and AMS is not -1) and enabled['STATE'] is True:
                Label(frame1,text='   ', bg=color['background'], fg='DIMGRAY', anchor=NW, justify=LEFT, 
                      font=(color['Font'])).grid(row=id, column=c, sticky=E)
            if c is 17 and (HMS is not -1 and AMS is not -1) and enabled['STATE'] is True:
                if HMS > AMS and db_DEVRE is 2:
                    LBL_MS_1 = Label(frame1,text='MS 1',bg=color['select_bg'], fg=color['select_fg'], anchor=NW, justify=LEFT, 
                                 font=(color['Font'])).grid(row=id, column=c, sticky=E)
                elif HMS > AMS and db_DEVRE is 1:
                    LBL_MS_1 = Label(frame1,text='         ',bg=color['select_bg'], fg=color['select_fg'], anchor=NW, justify=LEFT, 
                                 font=(color['Font'])).grid(row=id, column=c, sticky=E)
            if c is 17  and (HMS is not -1 and AMS is not -1) and enabled['STATE'] is True:
                if HMS is AMS and db_DEVRE is 2:
                    LBL_MS_0 = Label(frame1,text='MS 0',bg=color['select_bg'], fg=color['select_fg'], anchor=NW, justify=LEFT, 
                                 font=(color['Font'])).grid(row=id, column=c, sticky=E)
                elif HMS is AMS and db_DEVRE is 1:
                    LBL_MS_0 = Label(frame1,text='         ',bg=color['select_bg'], fg=color['select_fg'], anchor=NW, justify=LEFT, 
                                 font=(color['Font'])).grid(row=id, column=c, sticky=E)
            if c is 17 and ( HMS is not -1 and AMS is not -1) and enabled['STATE'] is True:
                if HMS < AMS and db_DEVRE is 2:
                    LBL_MS_2 = Label(frame1,text='MS 2',bg=color['select_bg'], fg=color['select_fg'], anchor=NW, justify=LEFT, 
                                 font=(color['Font'])).grid(row=id, column=c, sticky=E)
                elif HMS < AMS and db_DEVRE is 1: 
                    LBL_MS_2 = Label(frame1,text='         ',bg=color['select_bg'], fg=color['select_fg'], anchor=NW, justify=LEFT, 
                                 font=(color['Font'])).grid(row=id, column=c, sticky=E)
            if c is 18 and (HIY is not -1 and AIY is not -1) and enabled['STATE'] is True:
                Label(frame1,bg=color['background'], fg='DIMGRAY', anchor=NW, justify=LEFT, font=(color['Font'])).grid(row=id, column=c, sticky=E)
            if c is 19 and (HIY is not -1 and AIY is not -1) and enabled['STATE'] is True:
                if HIY > AIY:
                    LBL_IY_1 = Label(frame1,text='IY 1',bg=color['select_bg'], fg=color['select_fg'], anchor=NW, justify=LEFT, 
                                 font=(color['Font'])).grid(row=id, column=c, sticky=E)
            if c is 19 and (HIY is not -1 and AIY is not -1) and enabled['STATE'] is True:
                if HIY is AIY:
                    LBL_IY_0 = Label(frame1,text='IY 0',bg=color['select_bg'], fg=color['select_fg'], anchor=NW, justify=LEFT, 
                                 font=(color['Font'])).grid(row=id, column=c, sticky=E)
            if c is 19 and (HIY is not -1 and AIY is not -1) and enabled['STATE'] is True:
                if HIY < AIY:
                    LBL_IY_2 = Label(frame1,text='IY 2',bg=color['select_bg'], fg=color['select_fg'], anchor=NW, justify=LEFT, 
                                 font=(color['Font'])).grid(row=id, column=c, sticky=E)
            if c is 20 and (HIY is not -1 and AIY is not -1) and enabled['STATE'] is True:
                Label(frame1,bg=color['background'], fg='DIMGRAY', anchor=NW, justify=LEFT, font=(color['Font'])).grid(row=id, column=c, sticky=E)
            if c is 21 and (HIY is not -1 and AIY is not -1) and enabled['STATE'] is True:
                if db_DEVRE is 1:
                    LBL_TG = Label(frame1,text='TG '+str(TG),bg=color['select_bg'], fg=color['select_fg'], anchor=NW, justify=LEFT, 
                                font=(color['Font'])).grid(row=id, column=c, sticky=E)
                else:
                    LBL_TG = Label(frame1,text='TG '+str(TG),bg=color['select_bg'], fg=color['select_fg'], anchor=NW, justify=LEFT, 
                                font=(color['Font'])).grid(row=id, column=c, sticky=E)
                    
      
    frame1.update()
    hide = Label(frame3, text=' HIDE ',bg=color['background'],fg=color['hide'], anchor=E, justify=LEFT, 
            font=('Verdana 6'))
    hide.bind('<Button-1>', hide_command)
    hide.grid(row=1, column=1, sticky=E)
    center =Label(frame3, text=' C ',bg=color['background'],fg=color['C'], anchor=E, justify=LEFT, 
            font=('Verdana 6'))
    center.bind('<Button-1>', center_geometry)
    center.grid(row=1, column=2, sticky=E)
    right = Label(frame3, text=' R ',bg=color['background'],fg=color['R'], anchor=E, justify=LEFT, 
            font=('Verdana 6'))
    right.bind('<Button-1>', right_geometry)
    right.grid(row=1, column=3, sticky=E)
    frame3.update()
    if goal_ is True:
        goal()
    if geometry[-1] != 'CENTER':
        windows.geometry('{}x{}-{}+{}'.format(str(frame1.winfo_width()+10), str(windows.winfo_height()) , +30, +0))
    else:
        windows.geometry('{}x{}-{}+{}'.format(str(frame1.winfo_width()+10), str(windows.winfo_height()) , windows.winfo_screenwidth()/2-(frame1.winfo_width()+10)/2, 0))
    windows.after(60000, program) #LOOP
windows = Tk()
windows.attributes('-alpha', 0.8)
windows.configure(background=color['background'])
windows.overrideredirect(1)
frame0 = Frame(padx=3, pady=1, bg='black')
frame0.pack(fill=X)
frame1 = Frame(padx=10, pady=10, bg=color['background'])
frame1.pack()
frame3 = Frame(padx=10, pady=10, bg=color['background'])
frame3.pack(side=RIGHT)
frame5 = Frame(padx=15, pady=10, bg=color['background'])
frame5.pack(side=LEFT)
program()
windows.mainloop()
