import sys
sys.path.append(r'C:\Python24\Lib')

import subprocess
import re

import clr

clr.AddReference("System.Drawing")
clr.AddReference("System.Windows.Forms")

from System.Text import Encoding
from System.Drawing import Point, Size
from System.Windows.Forms import Application, Button, Form, TextBox, GroupBox, CheckBox, Label, MessageBox, ScrollBars, FormStartPosition
class PythonAPP(Form):

    def __init__(self):
        self.Text = 'Ping & Traceroute & ARP & Netstat'
        startPosition = FormStartPosition()
        self.StartPosition = startPosition.CenterScreen
        #self.Height = 500
        #self.Width = 500       
        self.MaximizeBox = False
        self.MinimumSize = Size(910,570)
        self.MaximumSize = Size(910,570)
        #TextBox Panel Wyswietlacz
        #self.utf = UTF8Encoding()
        scrollBars = ScrollBars()
        
        self.GrupaPing = GroupBox()
        self.GrupaPing.Text = "Parametry Ping"
        self.GrupaPing.Size = Size(150,220)
        self.GrupaPing.Location = Point(5, 5)
        #self.GrupaPing.Parent = self

        self.Hostlb = Label()
        self.Hostlb.Size = Size(32,20)
        self.Hostlb.Location = Point(17, 27)
        self.Hostlb.Text = "Host: "

        self.ParamPinglb = Label()
        self.ParamPinglb.Size = Size(80,20)
        self.ParamPinglb.Location = Point(17, 47)
        self.ParamPinglb.Text = "Parametry:"

        self.ChbLiczbaPakietow = CheckBox()
        self.ChbLiczbaPakietow.Checked = False
        self.ChbLiczbaPakietow.Text = "-n:"
        self.ChbLiczbaPakietow.Location = Point(17, 80)

        self.ChbPakiWielkoscetow = CheckBox()
        self.ChbPakiWielkoscetow.Checked = False
        self.ChbPakiWielkoscetow.Text = "-l:"
        self.ChbPakiWielkoscetow.Location = Point(17, 117)

        self.ChbTTL = CheckBox()
        self.ChbTTL.Checked = False
        self.ChbTTL.Text = "-i:"
        self.ChbTTL.Location = Point(17, 155)

        self.pingNtb = TextBox()
        self.pingNtb.Height = 30
        self.pingNtb.Width = 50
        self.pingNtb.Location = Point(52,83)

        self.pingLtb = TextBox()
        self.pingLtb.Height = 30
        self.pingLtb.Width = 50
        self.pingLtb.Location = Point(52,120)

        self.pingIttl = TextBox()
        self.pingIttl.Height = 30
        self.pingIttl.Width = 50
        self.pingIttl.Location = Point(52,158)

        self.Hosttb = TextBox()
        self.Hosttb.Location = Point(52, 25)
        self.Hosttb.Height = 30
        self.Hosttb.Width = 90
        self.Hosttb.Text = "8.8.8.8"

        self.pingNlb = Label()
        self.pingNlb.Size = Size(100,20)
        self.pingNlb.Location = Point(15, 65)
        self.pingNlb.Text = "Liczba pakietow:"

        self.pingLlb = Label()
        self.pingLlb.Size = Size(110,20)
        self.pingLlb.Location = Point(15, 102)
        self.pingLlb.Text = "Wielkosc pakietow:"

        self.pingIlb = Label()
        self.pingIlb.Size = Size(100,20)
        self.pingIlb.Location = Point(15, 140)
        self.pingIlb.Text = "Czas wygasniecia:"

        self.count = 0

        button = Button()
        button.Text = "Ping !"
        button.Size = Size(130,30)
        button.Location = Point(15, 185)

        button.Click += self.buttonPressed

        self.GrupaTracert = GroupBox()
        self.GrupaTracert.Text = "Parametry Traceroute"
        self.GrupaTracert.Size = Size(150,150)
        self.GrupaTracert.Location = Point(5, 225)

        self.ParamTraclb = Label()
        self.ParamTraclb.Size = Size(80,40)
        self.ParamTraclb.Location = Point(17, 270)
        self.ParamTraclb.Text = "Limit liczby przeskokow:"

        self.Host1lb = Label()
        self.Host1lb.Size = Size(32,20)
        self.Host1lb.Location = Point(17, 248)
        self.Host1lb.Text = "Host: "

        self.HostTractb = TextBox()
        self.HostTractb.Location = Point(52, 245)
        self.HostTractb.Height = 30
        self.HostTractb.Width = 90
        self.HostTractb.Text = "8.8.8.8"

        self.LimitTractb = TextBox()
        self.LimitTractb.Location = Point(52, 309)
        self.LimitTractb.Height = 30
        self.LimitTractb.Width = 60
        self.LimitTractb.Text = "30"

        self.ChLimitPrzeskokow = CheckBox()
        self.ChLimitPrzeskokow.Checked = False
        self.ChLimitPrzeskokow.Text = "-h: "
        self.ChLimitPrzeskokow.Location = Point(17, 308)

        self.count = 0

        button1 = Button()
        button1.Text = "Tracert !"
        button1.Size = Size(130,30)
        button1.Location = Point(15, 335)

        button1.Click += self.button1Pressed

        self.GrupaARP = GroupBox()
        self.GrupaARP.Text = "Parametry ARP"
        self.GrupaARP.Size = Size(150,150)
        self.GrupaARP.Location = Point(5, 375)

        self.ParamA = Label()
        self.ParamA.Size = Size(70,30)
        self.ParamA.Location = Point(17, 395)
        self.ParamA.Text = "Wyswietlenie tablicy ARP:"

        self.ParamV = Label()
        self.ParamV.Size = Size(70,40)
        self.ParamV.Location = Point(17, 435)
        self.ParamV.Text = "Wyswietlenie pelnej tablicy ARP:"

        self.ChA = CheckBox()
        self.ChA.Checked = True
        self.ChA.Enabled = False
        self.ChA.Size = Size(37,20)
        self.ChA.Text = "-a"
        self.ChA.Location = Point(115, 400)

        self.ChV = CheckBox()
        self.ChV.Checked = False
        self.ChV.Size = Size(37,20)
        self.ChV.Text = "-v"
        self.ChV.Location = Point(115, 440)

        self.count = 0

        button2 = Button()
        button2.Text = "ARP !"
        button2.Size = Size(130,30)
        button2.Location = Point(15, 485)

        button2.Click += self.button2Pressed

        self.GrupaNET = GroupBox()
        self.GrupaNET.Text = "Parametry Netstat"
        self.GrupaNET.Size = Size(155,260)
        self.GrupaNET.Location = Point(735, 5)

        self.ParamAnetstat = Label()
        self.ParamAnetstat.Size = Size(90,50)
        self.ParamAnetstat.Location = Point(745,20)
        self.ParamAnetstat.Text = "Wszystkie aktywne polaczenia:"

        self.ChAnetstat = CheckBox()
        self.ChAnetstat.Checked = False
        self.ChAnetstat.Size = Size(37,20)
        self.ChAnetstat.Text = "-a"
        self.ChAnetstat.Location = Point(845,30)

        self.ParamE = Label()
        self.ParamE.Size = Size(90,50)
        self.ParamE.Location = Point(745,60)
        self.ParamE.Text = "Statystyki sieci Ethernet:"

        self.ChE = CheckBox()
        self.ChE.Checked = False
        self.ChE.Size = Size(37,20)
        self.ChE.Text = "-e"
        self.ChE.Location = Point(845,65)

        self.ParamF = Label()
        self.ParamF.Size = Size(90,50)
        self.ParamF.Location = Point(745, 90)
        self.ParamF.Text = "Nazwy domen adresow obcych:"

        self.ChF = CheckBox()
        self.ChF.Checked = False
        self.ChF.Size = Size(37,20)
        self.ChF.Text = "-f"
        self.ChF.Location = Point(845, 100)

        self.ParamO = Label()
        self.ParamO.Size = Size(90,50)
        self.ParamO.Location = Point(745, 127)
        self.ParamO.Text = "Identyfikator polaczenia:"

        self.ChO = CheckBox()
        self.ChO.Checked = False
        self.ChO.Size = Size(37,20)
        self.ChO.Text = "-o"
        self.ChO.Location = Point(845, 130)

        self.ParamR = Label()
        self.ParamR.Size = Size(90,50)
        self.ParamR.Location = Point(745,165)
        self.ParamR.Text = "Tabele routingu:  "

        self.ChR = CheckBox()
        self.ChR.Checked = False
        self.ChR.Size = Size(37,20)
        self.ChR.Text = "-r"
        self.ChR.Location = Point(845, 165)

        self.ParamS = Label()
        self.ParamS.Size = Size(90,50)
        self.ParamS.Location = Point(745, 185)
        self.ParamS.Text = "Statystyka protokolow:  "

        self.ChS = CheckBox()
        self.ChS.Checked = False
        self.ChS.Size = Size(37,20)
        self.ChS.Text = "-s"
        self.ChS.Location = Point(845, 195)

        self.count = 0

        button3 = Button()
        button3.Text = "Netstat !"
        button3.Size = Size(130,30)
        button3.Location = Point(745,225)

        button3.Click += self.button3Pressed

        self.ipconfig = GroupBox()
        self.ipconfig.Text = "IPconfig"
        self.ipconfig.Size = Size(155,260)
        self.ipconfig.Location = Point(735,265)
     
        self.ParamPodst = Label()
        self.ParamPodst.Size = Size(80,50)
        self.ParamPodst.Location = Point(745,290)
        self.ParamPodst.Text = "IP dane podstawowe: "

        self.ChPod = CheckBox()
        self.ChPod.Checked = False
        self.ChPod.Size = Size(63,30)
        self.ChPod.Text = "ipconfig"
        self.ChPod.Location = Point(820,288)

        self.ParamALL = Label()
        self.ParamALL.Size = Size(80,50)
        self.ParamALL.Location = Point(745,320)
        self.ParamALL.Text = "IP dane szczegolowe: "

        self.ChAll = CheckBox()
        self.ChAll.Checked = False
        self.ChAll.Size = Size(50,30)
        self.ChAll.Text = "all"
        self.ChAll.Location = Point(820,322)

        self.ParamRelease = Label()
        self.ParamRelease.Size = Size(80,50)
        self.ParamRelease.Location = Point(745,350)
        self.ParamRelease.Text = "Zwolnienie adresów IPv4: "

        self.ChRelease = CheckBox()
        self.ChRelease.Checked = False
        self.ChRelease.Size = Size(67,30)
        self.ChRelease.Text = "release"
        self.ChRelease.Location = Point(820,352)

        self.ParamRenew = Label()
        self.ParamRenew.Size = Size(80,50)
        self.ParamRenew.Location = Point(745,380)
        self.ParamRenew.Text = "Odnowienie adresów IPv4: "

        self.ChRenew = CheckBox()
        self.ChRenew.Checked = False
        self.ChRenew.Size = Size(67,30)
        self.ChRenew.Text = "renev"
        self.ChRenew.Location = Point(820,382)

        self.ParamDisplaydns = Label()
        self.ParamDisplaydns.Size = Size(80,50)
        self.ParamDisplaydns.Location = Point(745,415)
        self.ParamDisplaydns.Text = "Pokaż wpisy DNS: "

        self.ChDisplaydns = CheckBox()
        self.ChDisplaydns.Checked = False
        self.ChDisplaydns.Size = Size(62,30)
        self.ChDisplaydns.Text = "displaydns"
        self.ChDisplaydns.Location = Point(820,417)

        self.ParamFlushdns = Label()
        self.ParamFlushdns.Size = Size(80,50)
        self.ParamFlushdns.Location = Point(745,445)
        self.ParamFlushdns.Text = "Czysc wpisy DNS: "

        self.ChFlushdns = CheckBox()
        self.ChFlushdns.Checked = False
        self.ChFlushdns.Size = Size(67,30)
        self.ChFlushdns.Text = "flushdns"
        self.ChFlushdns.Location = Point(820,447)

        self.count = 0

        button4 = Button()
        button4.Text = "Ipconfig !"
        button4.Size = Size(130,30)
        button4.Location = Point(745,485)

        button4.Click += self.button4Pressed

        #Okno niezale¿ne
        self.Wyswietlacz = TextBox()
        self.Wyswietlacz.Location = Point(159, 10)
        self.Wyswietlacz.Height = 515
        self.Wyswietlacz.Width = 570
        self.Wyswietlacz.Multiline = True
        self.Wyswietlacz.ScrollBars = scrollBars.Both
        self.Wyswietlacz.ScrollBars = scrollBars.Vertical

        #Pierwsza grupa#
        self.Controls.Add(self.Hostlb)
        self.Controls.Add(self.pingIttl)
        self.Controls.Add(self.pingNtb)
        self.Controls.Add(self.pingLtb)
        self.Controls.Add(self.ParamPinglb)
        self.Controls.Add(self.ChbTTL)
        self.Controls.Add(self.ChbLiczbaPakietow)
        self.Controls.Add(self.ChbPakiWielkoscetow)
        self.Controls.Add(self.pingIlb)
        self.Controls.Add(self.pingLlb) 
        self.Controls.Add(self.pingNlb)      
        self.Controls.Add(self.Hosttb)
        self.Controls.Add(button)
        self.Controls.Add(self.GrupaPing)
        #Druga grupa#
        self.Controls.Add(button1)
        self.Controls.Add(self.LimitTractb)
        self.Controls.Add(self.HostTractb)    
        self.Controls.Add(self.ChLimitPrzeskokow)
        self.Controls.Add(self.Host1lb)
        self.Controls.Add(self.ParamTraclb)
        self.Controls.Add(self.GrupaTracert)
        #Trzecia grupa#
        self.Controls.Add(button2)
        self.Controls.Add(self.ChA)
        self.Controls.Add(self.ChV)
        self.Controls.Add(self.ParamA)
        self.Controls.Add(self.ParamV)
        self.Controls.Add(self.GrupaARP)
        #Czwarta grupa#
        self.Controls.Add(button3)
        self.Controls.Add(self.ChAnetstat)
        self.Controls.Add(self.ChF)
        self.Controls.Add(self.ChE)
        self.Controls.Add(self.ChO)   
        self.Controls.Add(self.ChR) 
        self.Controls.Add(self.ChS)
        self.Controls.Add(self.ParamS)  
        self.Controls.Add(self.ParamR)
        self.Controls.Add(self.ParamO)
        self.Controls.Add(self.ParamF)
        self.Controls.Add(self.ParamE)             
        self.Controls.Add(self.ParamAnetstat)
        self.Controls.Add(self.GrupaNET)
        #Wyswietlacz#
        self.Controls.Add(self.Wyswietlacz)
        #Piata grupa#
        self.Controls.Add(button4)
        self.Controls.Add(self.ChFlushdns)
        self.Controls.Add(self.ChDisplaydns)
        self.Controls.Add(self.ChRenew)
        self.Controls.Add(self.ChRelease)
        self.Controls.Add(self.ChAll)
        self.Controls.Add(self.ChPod)
        self.Controls.Add(self.ParamFlushdns)
        self.Controls.Add(self.ParamDisplaydns)
        self.Controls.Add(self.ParamRenew)
        self.Controls.Add(self.ParamRelease)
        self.Controls.Add(self.ParamALL)
        self.Controls.Add(self.ParamPodst)
        self.Controls.Add(self.ipconfig)
     
        
    def buttonPressed(self, sender, args):

        self.Wyswietlacz.Text = "Czekaj wykonuje polecenie..."
        host = self.Hosttb.Text
        L = "-l "
        L1 = self.pingLtb.Text
        N = "-n " 
        N1 = self.pingNtb.Text
        i = "-i " 
        i1 = self.pingIttl.Text

        
        if self.ChbLiczbaPakietow.Checked == True & self.ChbPakiWielkoscetow.Checked == True:
                    ping = subprocess.Popen(["ping", host , N, N1, L, L1],stdout = subprocess.PIPE,stderr = subprocess.PIPE)
                    out, error = ping.communicate()
                    self.Wyswietlacz.Text = out
                    self.pingNtb.Text = ""
                    self.pingLtb.Text = ""
                    self.ChbLiczbaPakietow.Checked = False
                    self.ChbPakiWielkoscetow.Checked = False
                    return  

        if self.ChbLiczbaPakietow.Checked == True & self.ChbPakiWielkoscetow.Checked == True & self.ChbTTL.Checked == True:
                    ping = subprocess.Popen(["ping", host , N, N1, L, L1, i, i1],stdout = subprocess.PIPE,stderr = subprocess.PIPE)
                    out, error = ping.communicate()
                    self.Wyswietlacz.Text = out
                    self.pingNtb.Text = ""
                    self.pingLtb.Text = ""
                    self.pingIttl.Text = ""
                    self.ChbLiczbaPakietow.Checked = False
                    self.ChbPakiWielkoscetow.Checked = False
                    self.ChbTTL.Checked = False
                    return
                        

        if self.ChbPakiWielkoscetow.Checked == True:
                    ping = subprocess.Popen(["ping", host , L, L1],stdout = subprocess.PIPE,stderr = subprocess.PIPE)                
                    out, error = ping.communicate()
                    self.Wyswietlacz.Text = out 
                    self.pingNtb.Text = ""
                    self.ChbPakiWielkoscetow.Checked = False
                    return

        if self.ChbLiczbaPakietow.Checked == True:
                    ping = subprocess.Popen(["ping", host , N, N1],stdout = subprocess.PIPE,stderr = subprocess.PIPE)
                    out, error = ping.communicate()
                    self.Wyswietlacz.Text = out
                    self.pingLtb.Text = ""
                    self.ChbLiczbaPakietow.Checked = False
                    return

        if self.ChbTTL.Checked == True:
                    ping = subprocess.Popen(["ping", host, i, i1],stdout = subprocess.PIPE,stderr = subprocess.PIPE)
                    out, error = ping.communicate()
                    self.Wyswietlacz.Text = out
                    self.pingIttl.Text = ""
                    self.ChbTTL.Checked = False
                    return

        else:
                    ping = subprocess.Popen(["ping", host],stdout = subprocess.PIPE,stderr = subprocess.PIPE)
                    out, error = ping.communicate()
                    self.Wyswietlacz.Text = out
                    return


    def button1Pressed(self, sender, args):

        self.Wyswietlacz.Text = "Czekaj wykonuje polecenie..."
        host = self.HostTractb.Text
        H = "-h "
        H1 = self.LimitTractb.Text

        if self.ChLimitPrzeskokow.Checked == True:
                    tracert = subprocess.Popen(["tracert",H,H1,host],stdout = subprocess.PIPE,stderr = subprocess.PIPE)
                    out, error = tracert.communicate()
                    self.Wyswietlacz.Text = out
                    self.LimitTractb.Text = "30"
                    self.ChLimitPrzeskokow.Checked = False                  
                    return
        else:
                    tracert = subprocess.Popen(["tracert", host],stdout = subprocess.PIPE,stderr = subprocess.PIPE)
                    out, error = tracert.communicate()
                    self.Wyswietlacz.Text = out
                    return

    def button2Pressed(self, sender, args):

        self.Wyswietlacz.Text = "Czekaj wykonuje polecenie..."
        A = "-a"
        V = "-v"

        if self.ChA.Checked == True & self.ChV.Checked:
                    arp = subprocess.Popen(["arp",A,V],stdout = subprocess.PIPE,stderr = subprocess.PIPE)
                    out, error = arp.communicate()
                    self.Wyswietlacz.Text = out
                    self.ChV.Checked = False
                    return
        else:
                    arp = subprocess.Popen(["arp",A],stdout = subprocess.PIPE,stderr = subprocess.PIPE)
                    out, error = arp.communicate()
                    self.Wyswietlacz.Text = out

    def button3Pressed(self, sender, args):

        self.Wyswietlacz.Text = "Czekaj wykonuje polecenie..."
        Anetstat = "-a"
        F = "-f"
        E = "-e"
        O = "-o"
        S = "-s"
        R = "-r"        

        if self.ChAnetstat.Checked == True:
                    netstat = subprocess.Popen(["netstat",Anetstat],stdout = subprocess.PIPE,stderr = subprocess.PIPE)
                    out, error = netstat.communicate()
                    self.Wyswietlacz.Text = out
                    self.ChAnetstat.Checked = False
                    return
        if self.ChF.Checked == True:
                    netstat = subprocess.Popen(["netstat",F],stdout = subprocess.PIPE,stderr = subprocess.PIPE)
                    out, error = netstat.communicate()
                    self.Wyswietlacz.Text = out
                    self.ChF.Checked = False
                    return
        if self.ChE.Checked == True:
                    netstat = subprocess.Popen(["netstat",E],stdout = subprocess.PIPE,stderr = subprocess.PIPE)
                    out, error = netstat.communicate()
                    self.Wyswietlacz.Text = out
                    self.ChE.Checked = False
                    return
        if self.ChO.Checked == True:
                    netstat = subprocess.Popen(["netstat",O],stdout = subprocess.PIPE,stderr = subprocess.PIPE)
                    out, error = netstat.communicate()
                    self.Wyswietlacz.Text = out
                    self.ChO.Checked = False
                    return
        if self.ChS.Checked == True:
                    netstat = subprocess.Popen(["netstat",S],stdout = subprocess.PIPE,stderr = subprocess.PIPE)
                    out, error = netstat.communicate()
                    self.Wyswietlacz.Text = out
                    self.ChS.Checked = False
                    return
        if self.ChR.Checked == True:
                    netstat = subprocess.Popen(["netstat",R],stdout = subprocess.PIPE,stderr = subprocess.PIPE)
                    out, error = netstat.communicate()
                    self.Wyswietlacz.Text = out
                    self.ChR.Checked = False
                    return
        else:
                    netstat = subprocess.Popen(["netstat"],stdout = subprocess.PIPE,stderr = subprocess.PIPE)
                    out, error = netstat.communicate()
                    self.Wyswietlacz.Text = out
                    return

    def button4Pressed(self, sender, args):

        self.Wyswietlacz.Text = "Czekaj wykonuje polecenie..."
        all = "/all"
        Release = "/release"
        Renew = "/renew"
        DisplayDNS = "/displaydns"
        FlushDNS = "/flushdns"        

        if self.ChPod.Checked == True:
                    ipconfig = subprocess.Popen(["ipconfig"],stdout = subprocess.PIPE,stderr = subprocess.PIPE)
                    out, error = ipconfig.communicate()
                    self.Wyswietlacz.Text = out
                    self.ChPod.Checked = False
                    return
        if self.ChAll.Checked == True:
                    ipconfig = subprocess.Popen(["ipconfig", all],stdout = subprocess.PIPE,stderr = subprocess.PIPE)
                    out, error = ipconfig.communicate()
                    self.Wyswietlacz.Text = out
                    self.ChAll.Checked = False
                    return
        if self.ChRelease.Checked == True:
                    ipconfig = subprocess.Popen(["ipconfig", Release],stdout = subprocess.PIPE,stderr = subprocess.PIPE)
                    out, error = ipconfig.communicate()
                    self.Wyswietlacz.Text = out
                    self.ChRelease.Checked = False
                    return
        if self.ChRenew.Checked == True:
                    MessageBox.Show("Operacja jest najczesciej czasochłonna")
                    ipconfig = subprocess.Popen(["ipconfig", Renew],stdout = subprocess.PIPE,stderr = subprocess.PIPE)
                    out, error = ipconfig.communicate()
                    self.Wyswietlacz.Text = out
                    self.ChRenew.Checked = False
                    return
        if self.ChDisplaydns.Checked == True:
                    ipconfig = subprocess.Popen(["ipconfig", DisplayDNS],stdout = subprocess.PIPE,stderr = subprocess.PIPE)
                    out, error = ipconfig.communicate()
                    self.Wyswietlacz.Text = out
                    self.ChDisplaydns.Checked = False
                    return
        if self.ChFlushdns.Checked == True:
                    ipconfig = subprocess.Popen(["ipconfig", FlushDNS],stdout = subprocess.PIPE,stderr = subprocess.PIPE)
                    out, error = ipconfig.communicate()
                    self.Wyswietlacz.Text = out
                    self.ChFlushdns.Checked = False
                    return
        else:
                    ipconfig = subprocess.Popen(["ipconfig"],stdout = subprocess.PIPE,stderr = subprocess.PIPE)
                    out, error = ipconfig.communicate()
                    self.Wyswietlacz.Text = out
                    return

#MessageBox.Show(MessageBoxButtons.OK ,"W przypadku wybrania opcji -t prosze nie wybierac innej z opcji", MessageBoxIcon.Information)

form = PythonAPP()
Application.Run(form)