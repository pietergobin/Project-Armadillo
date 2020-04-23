
import radiology_functions as f
j=0
waarde2 = 100

while j <1000000:
    j+=1
    waarde = f.normal_distributions(10,1)
    if(waarde < waarde2):
        waarde2 = waarde

print(waarde2)
