import pickle

# Replace 'path_to_your_file.pkl' with the actual path to your PKL file
file_path = '/home/emi/Dropbox/DTEC/MJO/datos/ajuste/dem0_arg.pkl'

# Open the file in binary mode and load the data
with open(file_path, 'rb') as file:
    data = pickle.load(file)

# Now 'data' contains the deserialized Python object
print(data['dem0'])
data['dem0'].to_csv('/home/emi/Dropbox/DTEC/MJO/datos/ajuste/demARG.csv',float_format='%6.1f')
