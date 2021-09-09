from tkinter import *
import subprocess
from tkinter import ttk


window = Tk()
window.eval('tk::PlaceWindow %s center' %window.winfo_toplevel())
window.title("SOFT AP")
window.geometry("380x200")


global drivers,TT,wifilist
global no_of_client_var

drivers=set()
wifilist={}
##FLAGS TO HIDE CONSOLE
##    TT=0X08000000
TT=0X00000008



def drivers_list():


    meta_data = subprocess.check_output(['netsh', 'wlan', 'show','drivers'],creationflags=TT)
    ## decoding meta data
    data = meta_data.decode('utf-8', errors ="backslashreplace")
    ## splitting data by line by line
    data = data.split('\n')
    tmp_driver=''

    for i in data:
        if "no wireless" in i:
            drivers.clear()
            print("cleared")
            return
    # find "All User Profile" in each item
        if "    Driver" in i:
            # item at index 1 will be the driver name
            tmp_driver=i.split(":")[1]
        
        if "Hosted network supported" in i :    
            # if found
            # split the item
            i = i.split(":")       
            # formatting the name
            if i[1] =="yes" or "Yes" or "YES":
                drivers.add(tmp_driver[1:-1])
            
def conn_wifi():
    meta_data = subprocess.check_output(['netsh', 'wlan', 'show','interface'],creationflags=TT)
    data = meta_data.decode('utf-8', errors ="backslashreplace")
    data = data.split('\n')
    tmp_wifi_name=''

    for i in data:
        if "no wireless" in i:
            wifilist.clear()
            print("cleared")
            return
        if "State" in i :    
            # if found
            # split the item
            i = i.split(":")
            # formatting the name
            tmp_state=i
        if ("Profile" in i) and (tmp_state[1] =="connected" or "Connected" or "CONNECTED"):
            tmp_wifi_name=i.split(":")[1]
            print(tmp_wifi_name)
            wifilist[tmp_wifi_name[1:-1]]=tmp_state
            
        
          
    
def update_driver_list():
    drivers_list()         
    print(drivers)
    if len(drivers)==0:
        drvrr.set("no adapter detected")
    else:
        try:
            drvrr['values']=drivers
            drvrr.current(0)
        except:
            drvrr.set("no adapter detected")
    conn_wifi()
    



def update_wifi():
    print("update wifi")
    
def start_command():
    print("start_command()")
    ssidd=ssid.get()
    pswrdd=pswrd.get()
##    aa=subprocess.check_output("netsh wlan set hostednetwork mode=allow ssid= "+ssidd +" key ="+ pswrdd,creationflags=TT)
##    print(aa)
    try:
        aa=subprocess.check_output(["netsh", "wlan", "set", "hostednetwork", "mode", "=", "allow", "ssid", "=",ssidd , "key", "=", pswrdd],creationflags=TT)
        
        print("ssid and password are set")
    except:
        print("error in setting ssid or password")
    try:
        subprocess.check_output(["netsh", "wlan", "start", "hostednetwork"],creationflags=TT)
        print("hotspot / soft__ap started")
    except:
        print("error in starting ap")   
    s_status_var.set("Connected")
    
def stop_command():
    try:
        subprocess.check_output(["netsh", "wlan", "stop", "hostednetwork"],creationflags=TT)
        print("hotspot / soft__ap stoped")
    except:
        print("error in stopping ap")
    s_status_var.set("Not Connected")
def no_clients():
    print("in no of clients")
    
    try:
        cmdd='netsh wlan show hostednetwork | findstr /i /c:"number of clients"'
        meta_data=subprocess.Popen(cmdd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).communicate()[0]
        data = meta_data.decode('utf-8', errors ="backslashreplace")
        data = data.split('\n')

        for i in data:
           if "Number of clients " in i:
                # item at index 1 will be the driver name
                no_of_clients=i.split(":")[1]
        print(no_of_clients)
        no_of_client_var.set(no_of_clients)
        print("no_of_clients printed")
    except:
        print("no_of_clients not printed")

##def clients():
##    print("clients")
def test_command():
    no_clients()
'''main'''
frame=LabelFrame(window,text="********",padx=3,pady=3)
frame.pack(padx=5,pady=5)

driver=Label(frame,text="Connected drivers")
driver.grid(row=0,column=0)
driver_list=StringVar()
drvrr = ttk.Combobox(frame,textvariable=driver_list,width=30)
drvrr.grid(row=0,column=2)

refresh_driver=Button(frame,text='f5',width=4,command=update_driver_list)
refresh_driver.grid(row=0,column=3)
update_driver_list()

#Combobox
wifi_l=Label(frame,text="WiFi name")
wifi_l.grid(row=1,column=0)
wifi_name_var=StringVar()
wifi_ll = ttk.Label(frame,textvariable=wifi_name_var,width=30)
wifi_ll.grid(row=1,column=2)


ssid_l = Label(frame,text="SSID")
ssid_l.grid(row=2,column=0)
pswrd_l = Label(frame,text="Password")
pswrd_l.grid(row=3,column=0)

ssid=StringVar()
ssid_e = Entry(frame,textvariable=ssid,width=30)
ssid_e.grid(row=2,column=2)

pswrd=StringVar()
ssid_e = Entry(frame,textvariable=pswrd,show="*",width=30)
ssid_e.grid(row=3,column=2)


start=Button(frame,text='START',width=8,command=start_command)
start.grid(row=5,column=0)
stop=Button(frame,text='STOP',width=8,command=stop_command)
stop.grid(row=5,column=2)

test=Button(frame,text='f55',width=8,command=test_command)
test.grid(row=7,column=3)

no_client_l = Label(frame,text="No of clients")
no_client_l.grid(row=6,column=0)
no_of_client_var=StringVar()
no_client_ll = Label(frame,textvariable=no_of_client_var,width=30)
no_client_ll.grid(row=6,column=2)


sframe=LabelFrame(window,padx=2)
sframe.pack(side="bottom")
##sframe.pack_propagate(0)
##LabelFrame.rowconfigure(window,0,weight=1)
s_title=Label(sframe,text="Status : ",width=10)
s_title.grid(row=0,column=0,sticky="w")

s_status_var=StringVar()
s_status=Label(sframe,textvariable=s_status_var,width=28)
s_status.grid(row=0,column=1,sticky="w")


ssid.set("dharma")
pswrd.set("12345678")
no_clients()

##print(list(wifilist))
try:
    wifi_name_var.set(list(wifilist)[0])
    s_status_var.set("Connected")
##wifi_status_var.set(wifilist["WiFi"])
except:
    wifi_name_var.set("Not connected")
    s_status_var.set("Not Connected")

#s_status_var.set("dsasd")
##start_command()

window.bind('<Return>',lambda x: start_command())
window.mainloop()
