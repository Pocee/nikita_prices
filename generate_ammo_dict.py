import csv

# Read CSV and generate Python dict file
with open('ammo_stats.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    
    with open('ammo_data.py', 'w', encoding='utf-8') as out:
        out.write('# -*- coding: utf-8 -*-\n')
        out.write('# Ammo stats database - Auto-generated from CSV\n\n')
        out.write('AMMO_DATA = {\n')
        
        for row in reader:
            ammo_name = row['Munición']
            out.write(f'    {repr(ammo_name)}: {{\n')
            out.write(f'        "caliber": {repr(row["Calibre"])},\n')
            out.write(f'        "damage": {repr(row["Damage"])},\n')
            out.write(f'        "pen": {repr(row["Pen Value"])},\n')
            out.write(f'        "frag": {repr(row["Frag %"])},\n')
            out.write(f'        "recoil": {repr(row["Recoil"])},\n')
            out.write(f'        "accuracy": {repr(row["Accuracy"])},\n')
            out.write(f'        "speed": {repr(row["Speed (m/s)"])},\n')
            out.write(f'        "armor": [{repr(row["Class 1"])}, {repr(row["Class 2"])}, {repr(row["Class 3"])}, {repr(row["Class 4"])}, {repr(row["Class 5"])}, {repr(row["Class 6"])}]\n')
            out.write('    },\n')
        
        out.write('}\n')

print('Created ammo_data.py successfully!')
