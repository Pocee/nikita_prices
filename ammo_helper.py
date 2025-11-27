# -*- coding: utf-8 -*-
"""Helper functions for ammo command"""

from ammo_data import AMMO_DATA


def find_ammo_stats(name):
    """
    Find ammo stats by name (case-insensitive)
    Returns: list of tuples [(ammo_name, stats_dict), ...]
    Prioritizes: 1) Exact name start, 2) Exact word, 3) Prefix, 4) Partial
    """
    name_lower = name.lower()
    exact_name_matches = []  # "PS" matches "PS GZH" (name starts with search)
    exact_word_matches = []  # "PS" matches "PM PS GS PPO" (PS is a word)
    prefix_matches = []      # "PS" matches "PSV" (starts with PS)
    partial_matches = []     # "PS" matches "BPS" (contains PS)
    
    for key in AMMO_DATA:
        key_lower = key.lower()
        
        # Exact match
        if key_lower == name_lower:
            return [(key, AMMO_DATA[key])]
        
        # Split by space to get ammo name without caliber
        parts = key.split()
        if len(parts) > 1:
            ammo_name_only = ' '.join(parts[1:])
            ammo_words = ammo_name_only.split()
            
            # Check if ammo name starts with search term (e.g., "PS GZH" starts with "PS")
            if ammo_name_only.lower().startswith(name_lower + ' ') or ammo_name_only.lower() == name_lower:
                exact_name_matches.append((key, AMMO_DATA[key]))
                continue
            
            # Check if search term is an exact word match
            if any(word.lower() == name_lower for word in ammo_words):
                exact_word_matches.append((key, AMMO_DATA[key]))
                continue
            
            # Check if it starts with the search term
            if ammo_name_only.lower().startswith(name_lower):
                prefix_matches.append((key, AMMO_DATA[key]))
                continue
        
        # Partial match anywhere
        if name_lower in key_lower:
            partial_matches.append((key, AMMO_DATA[key]))
    
    # Return in priority order with length sorting within each tier
    exact_name_matches.sort(key=lambda x: len(x[0]))
    exact_word_matches.sort(key=lambda x: len(x[0]))
    prefix_matches.sort(key=lambda x: len(x[0]))
    partial_matches.sort(key=lambda x: len(x[0]))
    
    return exact_name_matches + exact_word_matches + prefix_matches + partial_matches


def format_armor_effectiveness(armor_list):
    """
    Format armor effectiveness as colored circles
    Returns: "🟢1 🟢2 🟢3 🟡4 🟢5 🔴6"
    
    Color coding based on shots to kill:
    - 🟢 Green (6-5): Effective
    - 🟡 Yellow (4): Medium
    - 🟠 Orange (3): Weak
    - 🔴 Red (2-1): Very weak
    - ⛔ Red/Stop (0): Ineffective
    """
    result = []
    
    for i, shots in enumerate(armor_list, 1):
        # Determine color based on shots to kill
        if not shots or shots == '' or shots == '-' or shots == '0':
            emoji = '⛔'  # Ineffective (Pure Red/Stop)
        else:
            try:
                shots_num = int(shots)
                if shots_num >= 6:
                    emoji = '🟢'  # Green - very effective
                elif shots_num == 5:
                    emoji = '🟢'  # Green - effective
                elif shots_num == 4:
                    emoji = '🟡'  # Yellow - medium
                elif shots_num == 3:
                    emoji = '🟠'  # Orange - weak
                elif shots_num >= 1:
                    emoji = '🔴'  # Red - very weak
                else:
                    emoji = '⛔'  # Ineffective
            except ValueError:
                emoji = '⚫'  # Black for invalid data
        
        result.append(f"{emoji}{i}")
    
    return " ".join(result)


def format_trader_info(buy_for_list):
    """
    Format trader purchase information
    Returns: list of formatted strings
    """
    traders = []
    flea = None
    
    for offer in buy_for_list:
        source = offer.get('source', '')
        vendor = offer.get('vendor', {})
        vendor_name = vendor.get('name', source)
        price = offer.get('price', 0)
        currency = offer.get('currency', 'RUB')
        price_rub = offer.get('priceRUB', price)
        
        if source == 'fleaMarket':
            flea = f"💰 Flea Market: {price_rub:,} ₽"
        else:
            # Trader offer
            level = vendor.get('minTraderLevel')
            task = vendor.get('taskUnlock')
            
            trader_str = f"🛒 {vendor_name}"
            if level:
                trader_str += f" (LL{level})"
            
            # Format price
            if currency == 'RUB':
                trader_str += f": {price:,} ₽"
            elif currency == 'USD':
                trader_str += f": ${price} (≈{price_rub:,} ₽)"
            elif currency == 'EUR':
                trader_str += f": €{price} (≈{price_rub:,} ₽)"
            
            if task:
                trader_str += f" [Quest: {task.get('name')}]"
            
            traders.append(trader_str)
    
    # Sort traders by price (cheapest first)
    result = sorted(traders)
    if flea:
        result.append(flea)
    
    return result


def get_ammo_by_caliber(caliber_search):
    """
    Get all ammo matching a caliber
    Returns: list of tuples [(full_name, stats_dict), ...]
    """
    caliber_lower = caliber_search.lower()
    matches = []
    
    for key, stats in AMMO_DATA.items():
        if caliber_lower in stats['caliber'].lower():
            matches.append((key, stats))
    
    # Sort by penetration (descending) for better overview
    matches.sort(key=lambda x: int(x[1]['pen']) if x[1]['pen'].isdigit() else 0, reverse=True)
    
    return matches


def format_ammo_compact(name, stats):
    """
    Format ammo info in a compact single line with fixed-width columns
    Returns: "Name      | D:49 P:44 | 🟢1 🟢2 🟢3 🟡4 🟢5 🔴6"
    """
    # Extract ammo name by removing the caliber prefix
    caliber = stats['caliber']
    if name.startswith(caliber):
        ammo_name = name[len(caliber):].strip()
    else:
        # Fallback: just take everything after first space
        ammo_name = ' '.join(name.split()[1:]) if len(name.split()) > 1 else name
    
    # Truncate and pad to fixed width (15 chars)
    if len(ammo_name) > 15:
        ammo_name = ammo_name[:12] + "..."
    ammo_name = ammo_name.ljust(15)
    
    # Format damage and pen with fixed width
    damage = str(stats['damage']).rjust(3)
    pen = str(stats['pen']).rjust(3)
    
    armor_str = format_armor_effectiveness(stats['armor'])
    
    # Put everything except emojis inside backticks for perfect alignment
    return f"`{ammo_name} | D:{damage} P:{pen}` {armor_str}"


def get_available_calibers():
    """Get list of all unique calibers in the database"""
    calibers = set()
    for stats in AMMO_DATA.values():
        calibers.add(stats['caliber'])
    return sorted(calibers)
