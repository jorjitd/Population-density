import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

data = pd.read_csv('Nepal_Data.csv')

# for population_data in data:
#     print(population_data)
    
data = data[['Name','Status','Population 2021']]
#renaming columns
data.rename(columns={'Population 2021': 'Population'}, inplace = True)

#Filter rows by value
data = data.loc[data['Status'] == 'District']

#Create an empty column
data['Districts2'] =''


#remove all english names in [] and put them in a new column
for index, row in data.iterrows():
    if '[' and ']' in row['Name']:
        start_index = row['Name'].find('[')
        end_index = row['Name'].find(']')
        data.loc[index, 'Districts2'] = data.loc[index]['Name'][start_index+1: end_index]
        
    else:
        data.loc[index, 'Districts2'] = data.loc[index]['Name']
        
        
#getting rid of unwanted columns like the origninal district name, 
#if its dristrict or not becasue theyre all districts, status


data = data[['Population', 'Districts2']]
data.rename(columns={'Districts2':'District'}, inplace = True)

#reading data from the shape file
nep_districts = gpd.read_file(r'C:\Users\jorji\.spyder-py3\NPL_adm\NPL_adm3.shp')
nep_districts = nep_districts[['NAME_3', 'geometry']]
nep_districts.rename(columns={'NAME_3': 'District'}, inplace = True)

#reprojecting to projected co-ordinate system
nep_districts.to_crs(epsg=32645, inplace = True)


#correction spellings

        
data.replace('Chitwan', 'Chitawan', inplace = True)
data.replace('Sindhupalchowk', 'Sindhupalchok', inplace = True)
data.replace('Tehrathum', 'Terhathum', inplace = True)
data.replace('Dodhara Chandani', 'Kanchanpur', inplace = True)
data.replace('Dang Deukhuri', 'Dang', inplace = True)
data.replace('East Rukum', 'Rukum', inplace = True)
data.replace('West Rukum', 'Rukum', inplace = True)
data.replace('Tanahun', 'Tanahu', inplace = True)
data.replace('Kapilvastu', 'Kapilbastu', inplace = True)
data.replace('Nawalparasi West', 'Nawalparasi', inplace = True)

for index, row in nep_districts['District'].items():
    if row in data['District'].tolist():
        pass
    else:
        print('The district ', row, 'is not in the population data list')

# Creating a new column and calculate the areas of the districts
nep_districts['area'] = nep_districts.area/1000000

# Do an attributes join
nep_districts = nep_districts.merge(data, on = 'District')

#create a population density colum
   

#nep_districts['Population']  = nep_districts['Population'].astype(float)



        
nep_districts['Population'] = nep_districts['Population'].astype(int)


#nep_districts['pop_den'] = nep_districts['Population'] /nep_districts['area']

# Plotting

#nep_districts.plot(column = 'pop_den', cmap = 'Spectral', legend = True)
#plt.savefig('Population_Density.jpg')