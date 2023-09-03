import tkinter as tk
from tkinter import ttk,messagebox

from PIL import ImageTk,Image

import threading
import time
import csv
import datetime

import pandas as pd
import pickle

from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import ThreadingOSCUDPServer

from EEG_generate_training_matrix import gen_training_matrix

namaFile='uji/uji-predict-0.csv'
ip="0.0.0.0"
port=5000
tp9=0
tp10=0
af7=0
af8=0
au=0

waktuRekam=5
def tampilanAwal():
    global frameAktual
    frameAktual.pack_forget()
    frameAwal.pack()
    frameAktual=frameAwal
    
    labelWelcome=ttk.Label(frameAwal,text="Selamat Datang",font=("Arial",20,))
    labelWelcome.grid(row=0,column=0, columnspan=2, padx=0, pady=25)
    
    labelKeterangan=ttk.Label(frameAwal,text="Silahkan klik tombol Berikut untuk melanjutkan menggunakan aplikasi ",font=("Arial",14),anchor="center")
    labelKeterangan.grid(row=1,column=0, columnspan=2,padx=0)
    labelKeterangan1=ttk.Label(frameAwal,text="dan klik tombol Tutup jika ingin menutup aplikasi",font=("Arial",14),anchor="center")
    labelKeterangan1.grid(row=2,column=0, columnspan=2,padx=0)
    
    tombolTutup=ttk.Button(frameAwal,text="Tutup",command=window.destroy)
    tombolTutup.grid(row=3,column=0,pady=120)
    
    tombolBerikut=ttk.Button(frameAwal,text="Berikut",command=lambda:tampilIsiData())
    tombolBerikut.grid(row=3,column=1)
    
    
    
def tampilIsiData():
    global frameAktual
    frameAktual.pack_forget()
    frameIsiData.pack()
    frameAktual=frameIsiData
    labelJudul=ttk.Label(frameIsiData,text="Silahkan isi data siswa", font=("Arial",14))
    labelJudul.grid(row=0,column=0,padx=5,pady=25,columnspan=2)
    
    global inputNama
    labelIsiNama=ttk.Label(frameIsiData,text="Nama :")
    labelIsiNama.grid(row=1,column=0,sticky='w')
    inputNama=ttk.Entry(frameIsiData,width=23)
    inputNama.grid(row=1,column=1,pady=15 )
    
    global comboSex
    labelIsiSex=ttk.Label(frameIsiData,text="Jenis Kelamin :")
    labelIsiSex.grid(row=2,column=0,sticky='w')
    comboSex=ttk.Combobox(frameIsiData)
    comboSex['values']=('Laki-Laki','Perempuan')
    comboSex.grid(row=2,column=1,pady=15)
    
    global inputSekolah
    labelSekolah=ttk.Label(frameIsiData,text="Asal Sekolah :")
    labelSekolah.grid(row=3,column=0,sticky='w')
    inputSekolah=ttk.Entry(frameIsiData,width=23)
    inputSekolah.grid(row=3,column=1,pady=15)
    
    tombolSebelum=ttk.Button(frameIsiData,text="Sebelumnya",command=lambda:tampilanAwal())
    tombolSebelum.grid(row=4,column=0,sticky='w',pady=40)
    
    tombolBerikut=ttk.Button(frameIsiData,text="Berikut",command=lambda:tampilPetunjuk())
    tombolBerikut.grid(row=4,column=1,sticky='e')
    
def tampilPetunjuk():
    if inputNama.get()=="" or inputSekolah.get()=="" or comboSex.get()=="" :
        messagebox.showerror("Error", "Data Masih ada yang kosong")
        tampilIsiData()
    else :
        global frameAktual
        frameAktual.pack_forget()
        framePetunjuk.pack()
        frameAktual=framePetunjuk
            
        labelPetunjuk=ttk.Label(framePetunjuk,text="Ikuti Petunjuk Berikut",font=("Arial",14))
        labelPetunjuk.grid(row=0,column=0,columnspan=2,pady=25)
        
        label1=ttk.Label(framePetunjuk,text="1. Nyalakan Muse2 Headset",font=('Arial',11))
        label1.grid(row=1,column=0,columnspan=2,pady=3,sticky='w')
        
        label2=ttk.Label(framePetunjuk,text="2. Hubungkan Muse2 Headset dengan aplikasi Mind Monitor pada Smartphone",font=('Arial',11))
        label2.grid(row=2,column=0,columnspan=2,pady=3,sticky='w')
        
        label3=ttk.Label(framePetunjuk,text="3. Pasangkan Muse2 Headset pada siswa sesuai gambar dibawah berikut",font=('Arial',11),)
        label3.grid(row=3,column=0,columnspan=2,pady=3,sticky='w')
        
        label4=ttk.Label(framePetunjuk,text="4. Pastikan Aplikasi Mind Monitor dalam 1 jaringan yang sama dengan Laptop/PC yang digunakan",font=('Arial',11))
        label4.grid(row=5,column=0,columnspan=2,pady=3,sticky='w')
        
        label5=ttk.Label(framePetunjuk,text="5. Tekan tombol streaming pada aplikasi Mind Monitor",font=('Arial',11))
        label5.grid(row=6,column=0,columnspan=2,pady=3,sticky='w')
        
        gambar=Image.open('img/petunjuk.png')
        foto=ImageTk.PhotoImage(gambar)
        
        label=ttk.Label(framePetunjuk,image=foto)
        label.image=foto
        label.grid(row=4,column=0,sticky='w',padx=23)
        
        tombolSebelum=ttk.Button(framePetunjuk,text="Sebelumnya",command=lambda:tampilIsiData())
        tombolSebelum.grid(row=7,column=0,pady=50,sticky='w' )
        
        tombolBerikut=ttk.Button(framePetunjuk,text="Berikut", command=lambda:tampilRekamEEG())
        tombolBerikut.grid(row=7,column=1,sticky='e')
    
def tampilRekamEEG():
    global frameAktual
    frameAktual.pack_forget()
    frameRekamEEG.pack()
    frameAktual=frameRekamEEG
        
    labelHeader=ttk.Label(frameRekamEEG,text="Prediksi Emosi",font=("Arial",14))
    labelHeader.grid(row=0,column=0,columnspan=2,pady=25)
    
    labelPetunjuk1=ttk.Label(frameRekamEEG,text="1.Untuk memprediksi Emosi, tekan tombol Prediksi",font=('Arial',11))
    labelPetunjuk1.grid(row=1,column=0,columnspan=2,pady=3,sticky='w')
    labelPetunjuk2=ttk.Label(frameRekamEEG,text="2.Mohon gerakan kepala dibatasi pada saat proses prediksi, karena akan mengganggu sinyal yang direkam.",font=('Arial',11))
    labelPetunjuk2.grid(row=2,column=0,columnspan=2,pady=3,sticky='w')
    
    tombolSebelum=ttk.Button(frameRekamEEG,text="Sebelumnya",command=lambda:tampilPetunjuk())
    tombolSebelum.grid(row=3,column=0,pady=50,sticky='w' )
    
    global tombolMulai
    tombolMulai=ttk.Button(frameRekamEEG,text="Mulai", command=lambda:mulai())
    tombolMulai.grid(row=3, column=0, columnspan=2, pady=10)
    
    global labelEmosi
    labelEmosi=ttk.Label(frameRekamEEG)
    
    
    
def mulai():
    
    labelEmosi.config(state=tk.DISABLED)
    tombolMulai.config(state=tk.DISABLED, text="Menunggu selama "+ str(waktuRekam) +" detik")
    thread=threading.Thread(target=fungsiBacaEEG)
    thread.start()
    checkThread(thread)
    
def checkThread(thread):
    if thread.is_alive():
        window.after(500,lambda:checkThread(thread))
    else:
        tombolMulai.config(state=tk.NORMAL,text="Mulai")

def fungsiBacaEEG():
    global listJoin
    listJoin=[]
    dispatcher=Dispatcher()
    dispatcher.map("/muse/eeg",eeg_handler)
    
    global server
    server=ThreadingOSCUDPServer((ip,port),dispatcher)
    print("Listening on UDP port "+str(port))
    
    threading.Thread(target=startServer).start()
    threading.Thread(target=writeCSV).start()
    time.sleep(waktuRekam)
    threading.Thread(target=stopServer).start()
    print("selesai rekam")
    try:
        buatDataset()
        prediksi()
    except:
        messagebox.showinfo("Informasi","Terjadi Kesalahan, Silahkan Coba Lagi")
    
    

def startServer():
    server.serve_forever(poll_interval=0.5)

def stopServer():
    server.shutdown()
    server.server_close()
    
def eeg_handler( address, *args):
    data=[]
    global tp9,tp10,af7,af8,au
    tp9,af7,af8,tp10,au=args
    
    timeStamps=time.time()
    data=list(args)
    data.insert(0,timeStamps)
    listJoin.append(data)
    
def writeCSV():
    fieldnames=["timestamps","tp9","af7","af8","tp10","right aux"]
    start=time.time()
    
    with open(namaFile,'w',newline='')as csvFile:
        csvWriter=csv.DictWriter(csvFile,fieldnames=fieldnames)
        csvWriter.writeheader()
    
    while True:
        # print(tp9,' ',af7,' ',af8,' ',tp10)
        if tp9!=0 and tp10!=0 and af7!=0 and af8!=0:
            
            with open(namaFile,'a',newline='') as csvFile:
                str_waktu=time.time()
                csvWriter=csv.DictWriter(csvFile,fieldnames=fieldnames)
                info={
                    "timestamps":str_waktu,
                    "tp9":tp9,
                    "af7":af7,
                    "af8":af8,
                    "tp10":tp10,
                    "right aux":au
                }
                
                csvWriter.writerow(info)
            time.sleep(0.0001)
            elapse=str_waktu-start
            print(elapse)
            if (elapse>=waktuRekam):
                break

def buatDataset():
    inputDirectory='uji/'
    outputFile='test.csv'
    gen_training_matrix(inputDirectory,outputFile,cols_to_ignore=-1)

def prediksi():
    modelName='modelGB.sav'
    dataset=pd.read_csv('test.csv')
    dataset=dataset.dropna()
    header=dataset.columns[[54,659,870,358,657,478,66,2,138,526,90,865,590,643,558,145,124,62,427,141,359,723,147,361,436,55,142,360,917,525,871,732,428,63,543,650,645,648,284,498,562,355,654,65,948,489,856,542,362,868,729,0,46,1,869,550,286,854,128,14,429,39,131,136,127,534,97,726,285,216,332,348,524,640,102,798,805,731,53,598,221,292,554,610,553,867,208,279,214,61,945,918,101,641,218,605,134,844,730,133,476,426,636,873,932,611,773,37,10,425,609,533,552,602,864,777,351,91,287,293,135,557,653,490,171,563,724,276,220,477,561,722,787,215,639,283,497,420,861,794,947,100,265,139,267,212,538,125,38,45,9,50,494,790,855,721,424,707,540,129,52,36,921,211,288,935,781,779,795,60,778,527,876,551,270,800,785,272,727,608,866,277,541,860,845,555,274,352,651,714,939,336,278,363,354,209,433,680,848,644,940,725,591,793,103,928,728,207,273,219,263,944,711,665,356,549,863,88,194,67,89,126,518,340,98,851,344,589,266,434,342,872,668,780,334]]
    
    X=dataset[header]
    
    loadModel=pickle.load(open(modelName,'rb'))
    prediksi=loadModel.predict(X)
    print(prediksi)
    
    anger=0
    joy=0
    sad=0
    fear=0
    
    for emosi in prediksi:
        if emosi == 'anger':
            anger +=1
        elif emosi == 'joy':
            joy +=1
        elif emosi =='sad':
            sad +=1
        elif emosi =='fear':
            fear +=1
            
    data={'anger':anger,'joy':joy,'sad':sad,'fear':fear}
    ser=pd.Series(data=data,index=['anger','joy','sad','fear'])

    print(ser)
    # kesimpulan
    emosiKesimpulan=ser.idxmax()        
    print(emosiKesimpulan)
    if emosiKesimpulan=='anger':
        gambarEmosi=Image.open('img/anger.png')
    elif emosiKesimpulan=='joy':
        gambarEmosi=Image.open('img/joy.png')
    elif emosiKesimpulan=='sad':
        gambarEmosi=Image.open('img/sad.png')
    elif emosiKesimpulan=='fear':
        gambarEmosi=Image.open('img/fear.png')
        
    fotoEmosi=ImageTk.PhotoImage(gambarEmosi)
    
    global labelEmosi
    labelEmosi=ttk.Label(frameRekamEEG,image=fotoEmosi)
    labelEmosi.image=fotoEmosi
    labelEmosi.grid(row=4,column=0, columnspan=2,pady=10)
    simpanDataCSV(emosiKesimpulan)
    
def simpanDataCSV(emosi):
    with open('dataemosi.csv','a',newline='')as f:
        writer=csv.writer(f,lineterminator='\n')
        data=[datetime.datetime.now(),inputNama.get(),comboSex.get(),inputSekolah.get(),emosi]
        writer.writerow(data)
    
window=tk.Tk()
window.geometry("800x500")
window.resizable(False,False)
window.title("Aplikasi Pendeteksi Emosi")

frameAwal=tk.Frame(window)
frameAwal.pack()

frameIsiData=tk.Frame(window)
framePetunjuk=tk.Frame(window)
frameRekamEEG=tk.Frame(window)



frameAktual=frameAwal

tampilanAwal()

window.mainloop()