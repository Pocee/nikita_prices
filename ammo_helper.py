# -*- coding: utf-8 -*-
"""Helper functions for ammo command"""

from ammo_data import AMMO_DATA


def find_ammo_stats(name):
    """
    Find ammo stats by name (case-insensitive)
    Returns: (ammo_name, stats_dict) or (None, None)
    """
    name_lower = name.lower()
    
    # Try exact match first
    for key in AMMO_DATA:
        if key.lower() == name_lower:
            return key, AMMO_DATA[key]
    
    # Try partial match
    for key in AMMO_DATA:
        if name_lower in key.lower():
            return key, AMMO_DATA[key]
    
    return None, None


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
