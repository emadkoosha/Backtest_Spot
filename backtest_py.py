from talib import MA_Type
import talib
data["BB_lower"]=0
upper, middle, lower = talib.BBANDS(data["close"], matype=MA_Type.T3)
data["BB_lower"]=lower
data["Slpercentage"]=(data["close"]/data["BB_lower"])-1
#Back Test
f = data
capital = 150
lpp = 0.02 #percentage of your capital thath you lose in each trade
lppd = capital*lpp # loss per position
slp = 0.1 #  set stp loss by percentage
tpp=1  # set tp by percentage
commissionfee = 0.002 #fee
# scorelimit = 0.8

# lable=signal
backtestnew = f
backtestnew['Label'] = pd.to_numeric(backtestnew['signal'])
#TP and sl
backtestnew['TP'] = 0
backtestnew['SL'] = 0

#cal return daily
backtestnew['ProfLoss'] = 0
backtestnew['ProfLoss'] = (backtestnew['close']-backtestnew['close'].shift(1))/backtestnew['close'].shift(1)

# start Buy/Hold/TP/SL/Close
backtestnew['condition'] = '0'
i=1
for i in range(len(backtestnew)):
   if (backtestnew.iloc[i-1, backtestnew.columns.get_loc('Label')]==0) and (backtestnew.iloc[i, backtestnew.columns.get_loc('Label')]==1): #scorelimit jash injast
    backtestnew.iloc[i, backtestnew.columns.get_loc('TP')]=backtestnew.iloc[i, backtestnew.columns.get_loc('close')]*(1+tpp)
    backtestnew.iloc[i, backtestnew.columns.get_loc('condition')]='Buy'
    backtestnew.iloc[i, backtestnew.columns.get_loc('SL')]=backtestnew.iloc[i, backtestnew.columns.get_loc('close')]*(1-backtestnew.columns.get_loc('Slpercentage'))
   elif  ((backtestnew.iloc[i-1, backtestnew.columns.get_loc('Label')]==1) and (backtestnew.iloc[i, backtestnew.columns.get_loc('Label')]==0)):
      backtestnew.iloc[i, backtestnew.columns.get_loc('condition')]='Close'
   elif ((backtestnew.iloc[i-1, backtestnew.columns.get_loc('Label')]==1) and (backtestnew.iloc[i, backtestnew.columns.get_loc('Label')]==1)):
      backtestnew.iloc[i, backtestnew.columns.get_loc('condition')]='Hold'


for j in range(len(backtestnew)):
  if (backtestnew.iloc[j, backtestnew.columns.get_loc('condition')]=='Hold') or (backtestnew.iloc[j, backtestnew.columns.get_loc('condition')]=='Close') :
    backtestnew.iloc[j, backtestnew.columns.get_loc('TP')]=backtestnew.iloc[j-1, backtestnew.columns.get_loc('TP')]
    backtestnew.iloc[j, backtestnew.columns.get_loc('SL')]=backtestnew.iloc[j-1, backtestnew.columns.get_loc('SL')]


backtestnew['conditionfinal'] = '0'
for k in range(len(backtestnew)):
  if k<=(len(backtestnew)-2):
    if (backtestnew.iloc[k, backtestnew.columns.get_loc('condition')]=='Buy') or (backtestnew.iloc[k, backtestnew.columns.get_loc('condition')]=='Close') :
     backtestnew.iloc[k, backtestnew.columns.get_loc('conditionfinal')] = backtestnew.iloc[k, backtestnew.columns.get_loc('condition')]
    elif(backtestnew.iloc[k, backtestnew.columns.get_loc('condition')]=='Hold'):
       if backtestnew.iloc[k+1, backtestnew.columns.get_loc('high')]>backtestnew.iloc[k, backtestnew.columns.get_loc('TP')]:
          backtestnew.iloc[k, backtestnew.columns.get_loc('conditionfinal')]='Tp'
       elif backtestnew.iloc[k+1, backtestnew.columns.get_loc('low')]<backtestnew.iloc[k, backtestnew.columns.get_loc('SL')]:   
          backtestnew.iloc[k, backtestnew.columns.get_loc('conditionfinal')]='Sl'      
       else:
          backtestnew.iloc[k, backtestnew.columns.get_loc('conditionfinal')] = backtestnew.iloc[k, backtestnew.columns.get_loc('condition')]

#tp and sl
backtestnew['conditionfinalf'] = backtestnew['conditionfinal']
i=1
for i in range(len(backtestnew)):
 if i<  (len(backtestnew)-2):
   if( (backtestnew.iloc[i, backtestnew.columns.get_loc('conditionfinalf')]=='Tp' and  backtestnew.iloc[i-1, backtestnew.columns.get_loc('conditionfinalf')]=='Hold') or(backtestnew.iloc[i, backtestnew.columns.get_loc('conditionfinalf')]=='Tp' and  backtestnew.iloc[i-1, backtestnew.columns.get_loc('conditionfinalf')]=='Buy') ):
     c=i
     while backtestnew.iloc[c, backtestnew.columns.get_loc('conditionfinalf')]!='Close' and c<(len(backtestnew)-1):
        backtestnew.iloc[c, backtestnew.columns.get_loc('conditionfinalf')]=0
        backtestnew.iloc[i, backtestnew.columns.get_loc('conditionfinalf')]='Tp'
        c=c+1
     if backtestnew.iloc[c, backtestnew.columns.get_loc('conditionfinalf')]=='Close':backtestnew.iloc[c, backtestnew.columns.get_loc('conditionfinalf')]=0
   elif((backtestnew.iloc[i, backtestnew.columns.get_loc('conditionfinalf')]=='Sl' and  backtestnew.iloc[i-1, backtestnew.columns.get_loc('conditionfinalf')]=='Hold') or(backtestnew.iloc[i, backtestnew.columns.get_loc('conditionfinalf')]=='Sl' and  backtestnew.iloc[i-1, backtestnew.columns.get_loc('conditionfinalf')]=='Buy')):
     c=i
     while backtestnew.iloc[c, backtestnew.columns.get_loc('conditionfinalf')]!='Close' and c< (len(backtestnew)-2):
        backtestnew.iloc[c, backtestnew.columns.get_loc('conditionfinalf')]=0
        backtestnew.iloc[i, backtestnew.columns.get_loc('conditionfinalf')]='Sl'
        c=c+1

     if backtestnew.iloc[c, backtestnew.columns.get_loc('conditionfinalf')]=='Close':backtestnew.iloc[c, backtestnew.columns.get_loc('conditionfinalf')]=0
# finish  Buy/Hold/TP/SL/Close - ba sotoon conditionfinalf kar   
#-----------------------------------------------------------------------------------------------
#start position size adding   
backtestnew['PositionSize'] = 0
for kx in range(len(backtestnew)):
   if backtestnew.iloc[kx, backtestnew.columns.get_loc('conditionfinalf')] == 'Buy' or backtestnew.iloc[kx, backtestnew.columns.get_loc('conditionfinalf')] == 'Hold' or backtestnew.iloc[kx, backtestnew.columns.get_loc('conditionfinalf')] == 'Sl' or backtestnew.iloc[kx, backtestnew.columns.get_loc('conditionfinalf')] == 'Tp' or backtestnew.iloc[kx, backtestnew.columns.get_loc('conditionfinalf')] == 'Close' :
      backtestnew.iloc[kx, backtestnew.columns.get_loc('PositionSize')] = (capital * lpp)/slp
#end position size adding

# return per trade
backtestnew['CallReturn'] = 0
for kx in range(len(backtestnew)):
   if backtestnew.iloc[kx, backtestnew.columns.get_loc('conditionfinalf')] == 'Hold' or backtestnew.iloc[kx, backtestnew.columns.get_loc('conditionfinalf')] == 'Sl' or backtestnew.iloc[kx, backtestnew.columns.get_loc('conditionfinalf')] == 'Tp' or backtestnew.iloc[kx, backtestnew.columns.get_loc('conditionfinalf')] == 'Close' :
      backtestnew.iloc[kx, backtestnew.columns.get_loc('CallReturn')] = backtestnew.iloc[kx, backtestnew.columns.get_loc('ProfLoss')]
backtestnew['CallReturn2'] = 0  
for kx in range(len(backtestnew)):
 if kx>0: 
  if backtestnew.iloc[kx, backtestnew.columns.get_loc('CallReturn')] != 0:
   backtestnew.iloc[kx, backtestnew.columns.get_loc('CallReturn2')] = backtestnew.iloc[kx-1, backtestnew.columns.get_loc('CallReturn2')]+backtestnew.iloc[kx, backtestnew.columns.get_loc('CallReturn')]

backtestnew['ReturnTrade'] = 0
for kx in range(len(backtestnew)):
 if kx>0:
  if backtestnew.iloc[kx, backtestnew.columns.get_loc('conditionfinalf')]=='Tp' :
   backtestnew.iloc[kx, backtestnew.columns.get_loc('ReturnTrade')] =tpp-commissionfee
  elif backtestnew.iloc[kx, backtestnew.columns.get_loc('conditionfinalf')]=='Sl':
   backtestnew.iloc[kx, backtestnew.columns.get_loc('ReturnTrade')] =-(slp+commissionfee)
  elif backtestnew.iloc[kx, backtestnew.columns.get_loc('conditionfinalf')]=='Close':
   backtestnew.iloc[kx, backtestnew.columns.get_loc('ReturnTrade')] = backtestnew.iloc[kx, backtestnew.columns.get_loc('CallReturn2')]-commissionfee


backtestnew['PNL'] = 0
for kx in range(len(backtestnew)):
  backtestnew.iloc[kx, backtestnew.columns.get_loc('PNL')] = backtestnew.iloc[kx, backtestnew.columns.get_loc('ReturnTrade')]*backtestnew.iloc[kx, backtestnew.columns.get_loc('PositionSize')]

backtestnew['Balance'] = 0
for kx in range(len(backtestnew)):
 if kx==0:
  backtestnew.iloc[kx, backtestnew.columns.get_loc('Balance')] = capital
 else: backtestnew.iloc[kx, backtestnew.columns.get_loc('Balance')]=backtestnew.iloc[kx-1, backtestnew.columns.get_loc('Balance')]+backtestnew.iloc[kx, backtestnew.columns.get_loc('PNL')]

backtestnew['CX'] = 0
for kx in range(len(backtestnew)):
 if backtestnew.iloc[kx, backtestnew.columns.get_loc('PNL')]<0:
  backtestnew.iloc[kx, backtestnew.columns.get_loc('CX')]=1
                  
backtestnew['CL'] = 0
if kx>0:
 for kx in range(len(backtestnew)):
  if backtestnew.iloc[kx, backtestnew.columns.get_loc('PNL')]>0:
   backtestnew.iloc[kx, backtestnew.columns.get_loc('CL')]=0
  elif backtestnew.iloc[kx, backtestnew.columns.get_loc('CX')]==1:
   backtestnew.iloc[kx, backtestnew.columns.get_loc('CL')]=backtestnew.iloc[kx, backtestnew.columns.get_loc('CX')]+backtestnew.iloc[kx-1, backtestnew.columns.get_loc('CL')]
  else: backtestnew.iloc[kx, backtestnew.columns.get_loc('CL')]=backtestnew.iloc[kx-1, backtestnew.columns.get_loc('CL')]
                                                                                       
backtestnew['FakeSL'] = 0
if kx>0:
 for kx in range(len(backtestnew)):
  if backtestnew.iloc[kx, backtestnew.columns.get_loc('conditionfinalf')]=='Sl':
   backtestnew.iloc[kx, backtestnew.columns.get_loc('FakeSL')]=1

backtestnew['ReturnBTC'] = 0
if kx>0:
 for kx in range(len(backtestnew)):
  backtestnew.iloc[kx, backtestnew.columns.get_loc('ReturnBTC')]=(backtestnew.iloc[kx, backtestnew.columns.get_loc('close')]/backtestnew.iloc[kx-1, backtestnew.columns.get_loc('close')])-1

backtestnew['ReturnRobot'] = 0
if kx>0:
 for kx in range(len(backtestnew)):
  if backtestnew.iloc[kx, backtestnew.columns.get_loc('PNL')]!=0:
   backtestnew.iloc[kx, backtestnew.columns.get_loc('ReturnRobot')]=(backtestnew.iloc[kx, backtestnew.columns.get_loc('Balance')]/backtestnew.iloc[kx-1, backtestnew.columns.get_loc('Balance')])-1

backtestnew['ReturnBtcCum'] = 0
if kx>0:
 for kx in range(len(backtestnew)):
  backtestnew.iloc[kx, backtestnew.columns.get_loc('ReturnBtcCum')]=backtestnew.iloc[kx-1, backtestnew.columns.get_loc('ReturnBtcCum')]+backtestnew.iloc[kx, backtestnew.columns.get_loc('ReturnBTC')]

backtestnew['ReturnRobotCum'] = 0
if kx>0:
 for kx in range(len(backtestnew)):
  backtestnew.iloc[kx, backtestnew.columns.get_loc('ReturnRobotCum')]=backtestnew.iloc[kx-1, backtestnew.columns.get_loc('ReturnRobotCum')]+backtestnew.iloc[kx, backtestnew.columns.get_loc('ReturnRobot')]
                              
backtestnew['DD'] = 0
for kx in range(len(backtestnew)):
 if kx>0:
  if backtestnew.iloc[kx, backtestnew.columns.get_loc('ReturnRobot')]<=0:
   if backtestnew.iloc[kx, backtestnew.columns.get_loc('ReturnRobot')]==0:
    backtestnew.iloc[kx, backtestnew.columns.get_loc('DD')]=backtestnew.iloc[kx-1, backtestnew.columns.get_loc('DD')]
   else: backtestnew.iloc[kx, backtestnew.columns.get_loc('DD')]=backtestnew.iloc[kx-1, backtestnew.columns.get_loc('DD')]+backtestnew.iloc[kx, backtestnew.columns.get_loc('ReturnRobot')]