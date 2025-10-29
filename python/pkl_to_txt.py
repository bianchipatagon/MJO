import pickle
import pandas as pd



with open('/home/emi/Dropbox/DTEC/MJO/merra/data/sitio_0.pkl', 'rb') as file:
    data0 = pickle.load(file)
with open('/home/emi/Dropbox/DTEC/MJO/merra/data/sitio_1.pkl', 'rb') as file:
    data1 = pickle.load(file)
with open('/home/emi/Dropbox/DTEC/MJO/merra/data/sitio_2.pkl', 'rb') as file:
    data2 = pickle.load(file)

cld_uru = pd.DataFrame()
cld_arg = pd.DataFrame()
cld_chi = pd.DataFrame()

cld_uru = data0 
cld_arg = data1
cld_chi = data2 

cld_uru.to_csv('urucld.csv', index=True, header=True) 
cld_arg.to_csv('argcld.csv', index=True, header=True) 
cld_chi.to_csv('chicld.csv', index=True, header=True) 
