import csv

# Read CSV and generate Python dict file
# Using municiones_completas.csv directly as source of truth
with open('municiones_completas.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader) # Skip header
    
    with open('ammo_data.py', 'w', encoding='utf-8') as out:
        out.write('# -*- coding: utf-8 -*-\n')
        out.write('# Ammo stats database - Auto-generated from CSV\n\n')
        out.write('AMMO_DATA = {\n')
        
        for row in reader:
            if not row or len(row) < 10:
                continue
                
            # Basic fields (Always at fixed positions)
            caliber = row[0]
            ammo_name = row[1]
            # Skip Buy/Sell (2, 3)
            damage = row[4]
            pen = row[5]
            frag = row[6]
            
            # Dynamic fields (Read from end)
            # Last 6 are armor classes
            armor = row[-6:]
            
            # 7th from end is Speed
            speed = row[-7]
            
            # Recoil/Accuracy are in between if they exist
            # Standard row has 17 cols, Short row has 14
            recoil = "N/A"
            accuracy = "N/A"
            
            if len(row) >= 16:
                recoil = row[7] # Usually after Frag
                accuracy = row[8]
            
            # Create key with caliber + ammo name
            full_key = f"{caliber} {ammo_name}"
            
            out.write(f"    {repr(full_key)}: {{\n")
            out.write(f"        'caliber': {repr(caliber)},\n")
            out.write(f"        'damage': {repr(damage)},\n")
            out.write(f"        'pen': {repr(pen)},\n")
            out.write(f"        'frag': {repr(frag)},\n")
            out.write(f"        'recoil': {repr(recoil)},\n")
            out.write(f"        'accuracy': {repr(accuracy)},\n")
            out.write(f"        'speed': {repr(speed)},\n")
            out.write(f"        'armor': {repr(armor)}\n")
            out.write("    },\n")
        
        out.write('}\n')

print('Created ammo_data.py successfully!')
