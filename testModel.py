import pandas as pd
import pickle
modelName='modelGB.sav'
dataset=pd.read_csv('test.csv')
dataset=dataset.dropna()
header=dataset.columns[[54, 659, 870, 358, 657, 478, 66, 2, 138, 526, 90, 865, 590, 643, 145, 558, 62, 124, 427, 141, 359, 723, 147, 361, 436, 55, 142, 360, 917, 871, 525, 732, 543, 63, 428, 645, 650, 648, 284, 498, 355, 562, 948, 489, 65, 654, 856, 362, 868, 729, 1, 0, 869, 542, 550, 286, 46, 854, 39, 429, 128, 131, 14, 127, 136, 97, 534, 285, 216, 332, 726, 348, 798, 805, 731, 102, 640, 292, 524, 867, 221, 598, 214, 945, 610, 918, 554, 101, 208, 61, 218, 134, 279, 844, 553, 605, 133, 476, 53, 641, 730, 873, 426, 611, 636, 37, 773, 533, 932, 552, 864, 609, 425, 91, 287, 293, 10, 602, 777, 351, 135, 653, 557, 171, 276, 220, 490, 563, 722, 561, 724, 215, 787, 639, 477, 794, 420, 100, 265, 267, 947, 283, 538, 861, 497, 38, 50, 9, 855, 494, 139, 424, 212, 707, 125, 721, 52, 540, 781, 211, 790, 527, 795, 288, 778, 270, 779, 551, 876, 272, 866, 129, 935, 541, 860, 800, 277, 727, 36, 921, 352, 651, 939, 336, 354, 60, 845, 45, 274, 714, 680, 103, 555, 785, 363, 725, 209, 278, 433, 848, 207, 219, 793, 944, 728, 928, 591, 88, 263, 67, 273, 940, 608, 126, 665, 863, 518, 340, 194, 644, 711, 356, 434, 589, 851, 549, 342, 344, 198, 261, 89, 849, 151, 668, 266, 946, 717, 716, 780, 846]]
X=dataset[header]

loadModel=pickle.load(open(modelName,'rb'))
prediksi=loadModel.predict(X)
print(prediksi)


# kalkulasi
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
# simpan ke dataframe
data={'anger':anger,'joy':joy,'sad':sad,'fear':fear}
ser=pd.Series(data=data,index=['anger','joy','sad','fear'], )
ser.to_csv(r'simpan.csv',index=True,header=True)

print(type(data))
print(type(ser))

# kesimpulan
emosiKesimpulan=ser.idxmax()


