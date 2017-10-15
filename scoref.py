# -*- coding: utf-8 -*-
#!/usr/bin/env python
from Tkinter import *
import time, os, pygame, httplib, sys, msql, datetime, json
os.system('rm /var/tmp/database.msql')
try:
  import urllib.request as url
except ImportError:
    import urllib
msql.connect('/var/tmp/database.msql')
msql.execute('CREATE TABLE canlisonuclar (ID:id, Code:Int, DT:Text, ATTR:Text, HTTR:Text, AMS:Int, HMS:Int, AIY:Int, HIY:Int, STL:Text, STATE:Text, LIG:Text, AG:Text, HG:Text)')
date = str(datetime.datetime.now())[0:10].split('-')
datenow = date[0] +'-'+ date[1] +'-'+ date[2]
clock = str(datetime.datetime.now()).split(' ')[0:5]
AMS, HMS = -1,-1
AIY, HIY = -1,-1
geometry = ['CENTER']
color = {'Goal':'LIMEGREEN', 'Font':'Ubuntu 9', 'Maç Sonucu':'red', 'Lig':'white',
         'Devre Arası':'yellow', 'Başlamadı':'brown', 'IYLABEL':'gray', 'background':'black',
         'Oynanıyor':'green', 'Saat':'white', 'GM':'orange', 'Ertelendi':'pink',
         'ATTR':'gray', 'HTTR':'gray', 'wraplength':600} #Renk font size değerlerini değiştirerek uygulamayı özelleştirebilirsin.
enabled = {'Saat':1, 'Code':1, 'STL':0, 'ATTR':1, 'LIG':0,
           'HTTR':1, 'MS':1, 'IY':1} # Eğer etiketi ekranda görmek istemiyorsan değerini {0} yapmalısın. Bu özellik {Saat Code STL IY LIG} için uygulanabilir.
def hide_command(event):
    windows.state("withdrawn")
def center_geometry(event):
    windows.geometry('{}x{}-{}+{}'.format(str(frame1.winfo_width()), str(windows.winfo_height()) , windows.winfo_screenwidth()/2-frame1.winfo_width()/2, 0))
    geometry.append('CENTER')
def right_geometry(event): 
    windows.geometry('{}x{}-{}+{}'.format(str(frame1.winfo_width()), str(windows.winfo_height()) , +30, +0))
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
        if len(STL) == 0 : STL = 'Oynaniyor'
        T = data['result'][OnlineIddaa]['ES']
        if str(Code) in sys.argv[1:]:
            if len(GOALS) is not 0:
                for SCORE in GOALS:
                    print Code, SCORE['PIN'], SCORE['TS'], SCORE['T'], SCORE['P'], SCORE['M']
                    if SCORE['TS'] is 1:
                        if SCORE['T'] is 1 or SCORE['T'] is 4 or SCORE['T'] is 2 or SCORE['T'] is 3:
                            HG = HG + str(SCORE['P'].encode('Utf-8')+':'+SCORE['M'].encode('Utf-8')+',')
                    if SCORE['TS'] is 2:
                        if SCORE['T'] is 1 or SCORE['T'] is 4 or SCORE['T'] is 2 or SCORE['T'] is 3:
                            AG = AG + str(SCORE['P'].encode('Utf-8')+':'+SCORE['M'].encode('Utf-8')+',')
            if len(T) is 0: #Başlamayan maçlar
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

            string = {'Code':Code, 'DT':DT, 'ATTR':ATTR, 'HTTR':HTTR, 'AMS':AMS, 'HMS':HMS, 'AIY':AIY, 'HIY':HIY, 'STL':STL, 'STATE':'', 'LIG':LIG, 'AG':AG, 'HG':HG}
            
            if truefalse(Code) == False:
                msql.execute('INSERT INTO canlisonuclar ROW (Code, DT, ATTR, HTTR, AMS, HMS, AIY, HIY, STL, STATE, LIG, AG, HG) NOT (Code)', string['Code'], string['DT'], string['ATTR'], string['HTTR'], string['AMS'], string['HMS'], string['AIY'], string['HIY'], string['STL'], string['STATE'], string['LIG'], string['AG'], string['HG'])
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
    if enabled['STL'] is 0:
        Label(frame0,text='Devre Arası',bg=color['background'],fg=color['Devre Arası'],
              anchor=NW,justify=LEFT,font=(color['Font'])).grid(row=1,column=1, sticky=W) 
        Label(frame0,text='Maç Sonucu',bg=color['background'],fg=color['Maç Sonucu'],
              anchor=NW,justify=LEFT,font=(color['Font'])).grid(row=1,column=2, sticky=W) 
        Label(frame0,text='Oynanıyor',bg=color['background'],fg=color['Oynanıyor'],
              anchor=NW,justify=LEFT,font=(color['Font'])).grid(row=1,column=3, sticky=W) 
        Label(frame0,text='Başlamadı',bg=color['background'],fg=color['Başlamadı'],
              anchor=NW,justify=LEFT,font=(color['Font'])).grid(row=1,column=4, sticky=W) 
    Label(frame2,text='',bg=color['background'],fg='yellow',anchor=NW,justify=LEFT,font=(color['Font'])).grid(row=1,column=1, sticky=W) 
    for id in range(1, msql.count('canlisonuclar')+1, +1):
        for c in range(1, 15):
            truefalse_goal = msql.gets('canlisonuclar', id)[10]
            if c is 2 and enabled['Code'] is 1:
                if msql.gets('canlisonuclar', id)[9] == 'Maç Sonucu':
                    LBL_CODE = Label(frame1,text=msql.gets('canlisonuclar',id)[1],bg=color['background'],fg=color['Maç Sonucu'],anchor=NW,justify=LEFT,font=(color['Font'])).grid(row=id,column=c, sticky=W) 
                elif msql.gets('canlisonuclar', id)[9] == 'Devre Arası':
                    LBL_CODE = Label(frame1,text=msql.gets('canlisonuclar', id)[1],bg=color['background'],fg=color['Devre Arası'], anchor=NW, justify=LEFT, font=(color['Font'])).grid(row=id, column=c, sticky=W) 
                elif msql.gets('canlisonuclar', id)[9] == 'Başlamadı.':
                    LBL_CODE = Label(frame1,text=msql.gets('canlisonuclar', id)[1],bg=color['background'],fg=color['Başlamadı'], anchor=NW, justify=LEFT, font=(color['Font'])).grid(row=id, column=c, sticky=W) 
                elif msql.gets('canlisonuclar', id)[9] == 'Ertelendi':
                    LBL_CODE = Label(frame1,text=msql.gets('canlisonuclar', id)[1],bg=color['background'],fg=color['Ertelendi'], anchor=NW, justify=LEFT, font=(color['Font'])).grid(row=id, column=c, sticky=W) 
                else:
                    LBL_CODE = Label(frame1,text=msql.gets('canlisonuclar', id)[1],bg=color['background'],fg=color['Oynanıyor'], anchor=NW, justify=LEFT, font=(color['Font'])).grid(row=id, column=c, sticky=W)  
            if c is 1 and enabled['Saat'] is 1:
                LBL_CLOCK = Label(frame1,text=msql.gets('canlisonuclar', id)[2],bg=color['background'],fg=color['Saat'], anchor=NW, justify=LEFT, font=(color['Font'])).grid(row=id, column=c, sticky=W) 
            if c is 3 and enabled['STL'] is 1:
                if msql.gets('canlisonuclar', id)[9] == 'Maç Sonucu':
                    LBL_STL = Label(frame1,text=msql.gets('canlisonuclar', id)[9] + ' ',bg=color['background'],fg=color['Maç Sonucu'], anchor=NW, justify=LEFT, font=(color['Font'])).grid(row=id, column=c, sticky=W) 
                elif msql.gets('canlisonuclar', id)[9] == 'Devre Arası':
                    LBL_STL = Label(frame1,text=msql.gets('canlisonuclar', id)[9] + ' ',bg=color['background'],fg=color['Devre Arası'], anchor=NW, justify=LEFT, font=(color['Font'])).grid(row=id, column=c, sticky=W)
                elif msql.gets('canlisonuclar', id)[9] == 'Başlamadı.':
                    LBL_STL = Label(frame1,text=msql.gets('canlisonuclar', id)[9] + ' ',bg=color['background'],fg=color['Başlamadı'], anchor=NW, justify=LEFT, font=(color['Font'])).grid(row=id, column=c, sticky=W)
                elif msql.gets('canlisonuclar', id)[9] == 'Ertelendi':
                    LBL_STL = Label(frame1,text=msql.gets('canlisonuclar', id)[9],bg=color['background'],fg=color['Ertelendi'], anchor=NW, justify=LEFT, font=(color['Font'])).grid(row=id, column=c, sticky=W) 
                else:
                    LBL_STL = Label(frame1,text=msql.gets('canlisonuclar', id)[9] + ' ',bg=color['background'],fg=color['Oynanıyor'], anchor=NW, justify=LEFT, font=(color['Font'])).grid(row=id, column=c, sticky=W)
            if c is 4 and enabled['LIG'] is 1:
                LBL_LIG = Label(frame1,text=msql.gets('canlisonuclar', id)[11],bg=color['background'],fg=color['Lig'], anchor=NW, justify=LEFT, font=(color['Font'])).grid(row=id, column=c, sticky=W)
            if c is 5:
                if truefalse_goal == 'HIY' or truefalse_goal == 'HMS':
                    LBL_HTTR = Label(frame1, text=msql.gets('canlisonuclar', id)[4],bg=color['background'],fg=color['Goal'],anchor=NW,justify=LEFT,font=(color['Font'])).grid(row=id, column=c, sticky=E)
                    msql.UPDATE_(id, 'canlisonuclar', 'STATE', '')
                else:
                    beta, test = '', msql.gets('canlisonuclar', id)[-1].split(',')[0:-1]
                    for minute in test:
                        beta = beta +' '+ minute.split(':')[1]
                    if len(beta) < 2:
                        LBL_HTTR = Label(frame1, text=msql.gets('canlisonuclar', id)[4],bg=color['background'], fg=color['HTTR'], anchor=NW, justify=LEFT, font=(color['Font'])).grid(row=id, column=c, sticky=E)
                    else:
                        LBL_HTTR = Label(frame1, text=str('('+beta+') ')+msql.gets('canlisonuclar', id)[4],bg=color['background'], fg=color['HTTR'], anchor=NW, justify=LEFT, font=(color['Font'])).grid(row=id, column=c, sticky=E)      
            if c is 6:
                LBL_SCORE_HMS = Label(frame1, text=msql.gets('canlisonuclar', id)[6],bg=color['background'], fg='white', anchor=NW, justify=LEFT, font=(color['Font'])).grid(row=id, column=c, sticky=E) 
            if c is 7:
                Label(frame1, text= '-',bg=color['background'], fg='gray', anchor=NW, justify=LEFT, font=(color['Font'])).grid(row=id, column=c, sticky=W) 
            if c is 8:
                LBL_SCORE_AMS = Label(frame1, text=msql.gets('canlisonuclar', id)[5],bg=color['background'], fg='white', anchor=NW, justify=LEFT, font=(color['Font'])).grid(row=id, column=c, sticky=E)         
            if c is 9:
                if truefalse_goal == 'AIY' or truefalse_goal == 'AMS': 
                    LBL_ATTR = Label(frame1, text=msql.gets('canlisonuclar', id)[3],bg=color['background'], fg=color['Goal'], anchor=NW, justify=LEFT, font=(color['Font'])).grid(row=id, column=c, sticky=W) 
                    msql.UPDATE_(id, 'canlisonuclar', 'STATE', '')
                else:
                    beta, test = '', msql.gets('canlisonuclar', id)[-2].split(',')[0:-1]
                    for minute in test:
                        beta = beta +' '+ minute.split(':')[1]
                    if len(beta) < 2:
                        LBL_ATTR = Label(frame1, text=msql.gets('canlisonuclar', id)[3],bg=color['background'],fg=color['ATTR'],anchor=NW,justify=LEFT, font=(color['Font'])).grid(row=id, column=c, sticky=W) 
                    else:
                        LBL_ATTR = Label(frame1, text=msql.gets('canlisonuclar', id)[3] + str(' ('+beta+')'),bg=color['background'], fg=color['ATTR'], anchor=NW, justify=LEFT, font=(color['Font'])).grid(row=id, column=c, sticky=W)                     
            if c is 10:
                continue
                beta, test = '', msql.gets('canlisonuclar', id)[-2].split(',')[0:-1]
                for minute in test:
                    beta = beta +' '+ minute.split(':')[1]
                Label(frame1,text=beta,bg=color['background'],fg=color['GM'], anchor=NW, justify=LEFT, font=('Verdana 6')).grid(row=id, column=c, sticky=W)
            if c is 11 and enabled['IY'] is 1:
                LBL_AIY = Label(frame1, text='  IY',bg=color['background'],fg=color['IYLABEL'],anchor=NW,justify=LEFT,font=(color['Font'])).grid(row=id, column=c, sticky=E) 
            if c is 12 and enabled['IY'] is 1:
                LBL_SCORE_HIY = Label(frame1,text=msql.gets('canlisonuclar', id)[8],bg=color['background'],fg='white',anchor=NW,justify=LEFT,font=(color['Font'])).grid(row=id, column=c, sticky=E) 
            if c is 13 and enabled['IY'] is 1:
                Label(frame1,text='-',bg=color['background'], fg='gray',anchor=NW, justify=LEFT, font=(color['Font'])).grid(row=id, column=c, sticky=E) 
            if c is 14 and enabled['IY'] is 1:
                LBL_SCORE_AIY = Label(frame1, text=msql.gets('canlisonuclar', id)[7],bg=color['background'], fg='white', anchor=NW, justify=LEFT, font=(color['Font'])).grid(row=id, column=c, sticky=E) 
        frame1.update()
    hide = Label(frame3, text=' HIDE ',bg=color['background'],fg='orange', anchor=E, justify=LEFT, 
            font=('Verdana 6'))
    hide.bind('<Button-1>', hide_command)
    hide.grid(row=1, column=1, sticky=E)
    center =Label(frame3, text=' C ',bg=color['background'],fg='gray', anchor=E, justify=LEFT, 
            font=('Verdana 6'))
    center.bind('<Button-1>', center_geometry)
    center.grid(row=1, column=2, sticky=E)
    right = Label(frame3, text=' R ',bg=color['background'],fg='gray', anchor=E, justify=LEFT, 
            font=('Verdana 6'))
    right.bind('<Button-1>', right_geometry)
    right.grid(row=1, column=3, sticky=E)
    frame3.update()
    if goal_ is True:
        goal()
    if geometry[-1] != 'CENTER':
        windows.geometry('{}x{}-{}+{}'.format(str(frame1.winfo_width()+10), str(windows.winfo_height()) , +30, +0))
    else:
        windows.geometry('{}x{}-{}+{}'.format(str(frame1.winfo_width()+10), str(windows.winfo_height()) , windows.winfo_screenwidth()/2-frame1.winfo_width()/2, 0))
    windows.after(60000, program) #LOOP
windows = Tk()
windows.attributes('-alpha', 0.8)
windows.configure(background=color['background'])
windows.overrideredirect(1)
frame0 = Frame(padx=5, pady=5, bg=color['background'])
frame0.pack()
frame1 = Frame(padx=10, pady=10, bg=color['background'])
frame1.pack()
frame2 = Frame(padx=1, pady=2, bg=color['background'])
frame2.pack()
frame3 = Frame(padx=10, pady=10, bg=color['background'])
frame3.pack(side=RIGHT)
program() #START
windows.mainloop()
