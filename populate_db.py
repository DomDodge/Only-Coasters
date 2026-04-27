import sqlite3
from datetime import datetime

def populate_lagoon_refined():
    conn = sqlite3.connect('database_new.db')
    cursor = conn.cursor()
    current_year = datetime.now().year

    # 1. Manufacturers
    mfg_data = [
        ('Lagoon (In-house)', 1886),
        ('Schwarzkopf', 1960),
        ('Zierer', 1930),
        ('Maurer AG', 1876),
        ('Vekoma', 1926),
        ('ART Engineering', 2002),
        ('John A. Miller', 1920)
    ]
    
    mfg_map = {}
    for name, year in mfg_data:
        cursor.execute("INSERT INTO manufacturers (name, year_founded) VALUES (?, ?)", (name, year))
        mfg_map[name] = cursor.lastrowid

    # 2. Lagoon Park
    cursor.execute('''
        INSERT INTO parks (name, owned_by, year_opened, visitors_per_year, visitors_per_day, location)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', ("Lagoon", "Freed Family", 1886, 1500000, 10000, "Farmington, Utah"))
    lagoon_id = cursor.lastrowid

    # 3. Refined Coaster Data
    # Schema Order: name, type, model, mfg_id, height, speed, length, year_opened, year_closed, operating, SBNO, removed, park_id, RPH, thrill, inversions, wait, restriction, duration, lift_launch, cost, drop_angle, age
    coasters = [
        ('Cannibal', 'Steel', 'Hypercoaster', 'Lagoon (In-house)', 208, 70, 2735, 2015, None, 1, 0, 0, 1200, 'high', 4, '60 mins', 48, '2:30', 'Elevator Lift', 22000000, 116),
        ('Colossus the Fire Dragon', 'Steel', 'Double Looper', 'Schwarzkopf', 85, 52, 2850, 1983, None, 1, 0, 0, 1400, 'high', 2, '30 mins', 48, '2:00', 'Lift', 4000000, 45),
        ('Wicked', 'Steel', 'Launch Coaster', 'Zierer', 110, 55, 2050, 2007, None, 1, 0, 0, 900, 'high', 1, '45 mins', 46, '2:00', 'Launch', 10000000, 90),
        ('Roller Coaster', 'Wood', 'Classic', 'John A. Miller', 62, 45, 2500, 1921, None, 1, 0, 0, 1000, 'medium', 0, '40 mins', 46, '2:00', 'Lift', 75000, 45),
        ('Primordial', 'Steel', '3D Interactive', 'ART Engineering', 84, 40, 1968, 2023, None, 1, 0, 0, 800, 'medium', 0, '90 mins', 36, '5:00', 'Lift', 20000000, 0),
        ('Spider', 'Steel', 'Spinning', 'Maurer AG', 49, 37, 1391, 2003, None, 1, 0, 0, 800, 'medium', 0, '50 mins', 42, '1:30', 'Lift', 4000000, 45),
        ('Wild Mouse', 'Steel', 'Wild Mouse', 'Maurer AG', 49, 28, 1213, 1998, None, 1, 0, 0, 800, 'medium', 0, '45 mins', 42, '1:30', 'Lift', 3000000, 45),
        ('Bombora', 'Steel', 'Family', 'Lagoon (In-house)', 55, 31, 1100, 2011, None, 1, 0, 0, 900, 'low', 0, '30 mins', 36, '1:30', 'Lift', 5000000, 30),
        ('Bat', 'Steel', 'Suspended Family', 'Vekoma', 65, 26, 1122, 2005, None, 1, 0, 0, 650, 'low', 0, '40 mins', 42, '1:30', 'Lift', 2500000, 20),
        ('Jet Star 2', 'Steel', 'Compact', 'Schwarzkopf', 44, 31, 1920, 1976, 2025, 0, 0, 1, 700, 'medium', 0, None, 44, '1:30', 'Lift', 1500000, 45),
        ('Puff the Little Fire Dragon', 'Steel', 'Kiddie', 'Zierer', 13, 15, 197, 1985, None, 1, 0, 0, 400, 'kiddie', 0, '15 mins', 36, '0:45', 'Lift', 250000, 15)
    ]

    for c in coasters:
        (name, c_type, model, mfg_name, h, s, l, yr, yr_c, active, sbno, rem, 
         rph, thrill, inv, wait, restrict, dur, lift, cost, drop) = c
        
        age = current_year - yr
        
        cursor.execute('''
            INSERT INTO rollercoasters (
                name, type, model, manufacturer_id, height, speed, length, 
                year_opened, year_closed, currently_operating, SBNO, removed, park_id, 
                riders_per_hour, thrill_level, inversions, avg_wait_time, 
                height_restriction, ride_duration, lift_or_launch, cost, 
                drop_angle_in_degrees, age
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            name, c_type, model, mfg_map[mfg_name], h, s, l, 
            yr, yr_c, active, sbno, rem, lagoon_id, 
            rph, thrill, inv, wait, restrict, dur, lift, cost, drop, age
        ))

    conn.commit()
    conn.close()
    print("Database updated with accurate Lagoon stats and new schema.")

def populate_cedar_point():
    conn = sqlite3.connect('database_new.db')
    cursor = conn.cursor()
    current_year = datetime.now().year

    # 1. Insert Manufacturers (using IF NOT EXISTS logic via SELECT)
    mfg_data = [
        ('Bolliger & Mabillard', 1988),
        ('Intamin', 1967),
        ('Arrow Dynamics', 1946),
        ('Rocky Mountain Construction', 2001),
        ('Dinn Corporation', 1983),
        ('Zamperla', 1966),
        ('Philadelphia Toboggan Coasters', 1904)
    ]
    
    mfg_map = {}
    for name, year in mfg_data:
        # Check if exists first to avoid duplicates if run multiple times
        cursor.execute("SELECT manufacturer_id FROM manufacturers WHERE name = ?", (name,))
        result = cursor.fetchone()
        if result:
            mfg_map[name] = result[0]
        else:
            cursor.execute("INSERT INTO manufacturers (name, year_founded) VALUES (?, ?)", (name, year))
            mfg_map[name] = cursor.lastrowid

    # 2. Insert Cedar Point
    cursor.execute('''
        INSERT INTO parks (name, owned_by, year_opened, visitors_per_year, visitors_per_day, location)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', ("Cedar Point", "Six Flags", 1870, 3440000, 25000, "Sandusky, Ohio"))
    cp_id = cursor.lastrowid

    # 3. Cedar Point Coaster Data (Includes Operating and Removed)
    # Schema Order: name, type, model, mfg, h, s, l, yr_open, yr_closed, operating, SBNO, removed, RPH, thrill, inv, wait, restriction, duration, lift_launch, cost, drop_angle
    coasters = [
        # --- OPERATING COASTERS ---
        ('Millennium Force', 'Steel', 'Giga Coaster', 'Intamin', 310, 93, 6595, 2000, None, 1, 0, 0, 1200, 'high', 0, '60 mins', 48, '2:20', 'Cable Lift', 25000000, 80),
        ('Maverick', 'Steel', 'Blitz Coaster', 'Intamin', 105, 70, 4000, 2007, None, 1, 0, 0, 1200, 'high', 2, '75 mins', 52, '2:30', 'Launch', 21000000, 95),
        ('Steel Vengeance', 'Steel', 'IBox Track', 'Rocky Mountain Construction', 205, 74, 5740, 2018, None, 1, 0, 0, 1200, 'high', 4, '90 mins', 52, '2:30', 'Lift', 23000000, 90),
        ('GateKeeper', 'Steel', 'Wing Coaster', 'Bolliger & Mabillard', 170, 67, 4164, 2013, None, 1, 0, 0, 1710, 'high', 6, '30 mins', 52, '2:40', 'Lift', 30000000, 78),
        ('Magnum XL-200', 'Steel', 'Hyper Coaster', 'Arrow Dynamics', 205, 72, 5106, 1989, None, 1, 0, 0, 2000, 'high', 0, '20 mins', 48, '2:00', 'Lift', 8000000, 60),
        ('Raptor', 'Steel', 'Inverted Coaster', 'Bolliger & Mabillard', 137, 57, 3790, 1994, None, 1, 0, 0, 1600, 'high', 6, '45 mins', 54, '2:15', 'Lift', 11500000, 45),
        ('Rougarou', 'Steel', 'Floorless Coaster', 'Bolliger & Mabillard', 145, 60, 3900, 2015, None, 1, 0, 0, 1800, 'high', 4, '15 mins', 54, '2:15', 'Lift', None, 52),
        ('Top Thrill 2', 'Steel', 'Lightning', 'Zamperla', 420, 120, 3422, 2024, None, 1, 0, 0, 1000, 'high', 0, '120 mins', 52, '2:00', 'LSM Launch', None, 90),
        ('Blue Streak', 'Wood', 'Out and Back', 'Philadelphia Toboggan Coasters', 78, 40, 2558, 1964, None, 1, 0, 0, 1400, 'medium', 0, '15 mins', 48, '1:45', 'Lift', 200000, 45),
        ('Wild Mouse', 'Steel', 'Twister Freeform', 'Zamperla', 52, 35, 1312, 2023, None, 1, 0, 0, 600, 'medium', 0, '45 mins', 42, '1:30', 'Lift', None, 45),
        
        # --- REMOVED / REPLACED COASTERS ---
        ('Mean Streak', 'Wood', 'Wooden Coaster', 'Dinn Corporation', 161, 65, 5427, 1991, 2016, 0, 0, 1, 1600, 'high', 0, None, 48, '3:15', 'Lift', 7500000, 65),
        ('Disaster Transport', 'Steel', 'Space Diver', 'Intamin', 63, 40, 1932, 1990, 2012, 0, 0, 1, 1800, 'medium', 0, None, 46, '2:30', 'Lift', 4000000, 45),
        ('Mantis', 'Steel', 'Stand-Up Coaster', 'Bolliger & Mabillard', 145, 60, 3900, 1996, 2014, 0, 0, 1, 1800, 'high', 4, None, 54, '2:15', 'Lift', 12000000, 52),
        ('Top Thrill Dragster', 'Steel', 'Accelerator Coaster', 'Intamin', 420, 120, 2800, 2003, 2021, 0, 0, 1, 1000, 'high', 0, None, 52, '0:30', 'Hydraulic Launch', 25000000, 90),
        ('Wicked Twister', 'Steel', 'Twisted Impulse Coaster', 'Intamin', 215, 72, 2700, 2002, 2021, 0, 0, 1, 1000, 'high', 0, None, 52, '0:40', 'LIM Launch', 9000000, 90)
    ]

    # Dictionary to keep track of inserted coaster names and their IDs
    coaster_id_map = {}

    for c in coasters:
        (name, c_type, model, mfg_name, h, s, l, yr_open, yr_closed, active, sbno, rem, 
         rph, thrill, inv, wait, restrict, dur, lift, cost, drop) = c
        
        age = current_year - yr_open
        
        cursor.execute('''
            INSERT INTO rollercoasters (
                name, type, model, manufacturer_id, height, speed, length, 
                year_opened, year_closed, currently_operating, SBNO, removed, park_id, 
                riders_per_hour, thrill_level, inversions, avg_wait_time, 
                height_restriction, ride_duration, lift_or_launch, cost, 
                drop_angle_in_degrees, age
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            name, c_type, model, mfg_map[mfg_name], h, s, l, 
            yr_open, yr_closed, active, sbno, rem, cp_id, 
            rph, thrill, inv, wait, restrict, dur, lift, cost, drop, age
        ))
        
        # Store the ID for the replacement logic later
        coaster_id_map[name] = cursor.lastrowid

    # 4. Map Replacements 
    # Key: The old coaster that was removed. Value: The new coaster that replaced it.
    replacements = {
        "Mean Streak": "Steel Vengeance",
        "Disaster Transport": "GateKeeper",
        "Mantis": "Rougarou",
        "Top Thrill Dragster": "Top Thrill 2",
        "Wicked Twister": "Wild Mouse" # Replaced by the Grand Pavilion / Wild Mouse area
    }

    # 5. Update the replaced_by_id foreign key
    for old_coaster, new_coaster in replacements.items():
        if old_coaster in coaster_id_map and new_coaster in coaster_id_map:
            old_id = coaster_id_map[old_coaster]
            new_id = coaster_id_map[new_coaster]
            
            cursor.execute('''
                UPDATE rollercoasters 
                SET replaced_by_id = ? 
                WHERE rollercoaster_id = ?
            ''', (new_id, old_id))

    conn.commit()
    conn.close()
    print("Cedar Point data (with legacy coasters and replacements) successfully added.")

def populate_magic_mountain():
    conn = sqlite3.connect('database_new.db')
    cursor = conn.cursor()
    current_year = datetime.now().year

    # 1. Insert Manufacturers (Safe check logic)
    mfg_data = [
        ('Bolliger & Mabillard', 1988),
        ('Intamin', 1967),
        ('Arrow Dynamics', 1946),
        ('Rocky Mountain Construction', 2001),
        ('Premier Rides', 1994),
        ('Giovanola', 1880),
        ('Great Coasters International', 1994),
        ('Schwarzkopf', 1960),
        ('International Amusement Devices', 1946),
        ('Dinn Corporation', 1983)
    ]
    
    mfg_map = {}
    for name, year in mfg_data:
        cursor.execute("SELECT manufacturer_id FROM manufacturers WHERE name = ?", (name,))
        result = cursor.fetchone()
        if result:
            mfg_map[name] = result[0]
        else:
            cursor.execute("INSERT INTO manufacturers (name, year_founded) VALUES (?, ?)", (name, year))
            mfg_map[name] = cursor.lastrowid

    # 2. Insert Six Flags Magic Mountain
    cursor.execute('''
        INSERT INTO parks (name, owned_by, year_opened, visitors_per_year, visitors_per_day, location)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', ("Six Flags Magic Mountain", "Six Flags", 1971, 3360000, 15000, "Valencia, California"))
    sfmm_id = cursor.lastrowid

    # 3. SFMM Coaster Data
    # Format: name, type, model, mfg, h, s, l, yr_open, yr_closed, active, sbno, rem, rph, thrill, inv, wait, restriction, duration, lift_launch, cost, drop_angle
    coasters = [
        # --- OPERATING COASTERS ---
        ('Twisted Colossus', 'Steel', 'IBox Track', 'Rocky Mountain Construction', 121, 57, 4990, 2015, None, 1, 0, 0, 1080, 'high', 2, '60 mins', 48, '3:40', 'Lift', None, 80),
        ('X2', 'Steel', '4th Dimension Coaster', 'Arrow Dynamics', 175, 76, 3610, 2002, None, 1, 0, 0, 1000, 'high', 2, '90 mins', 48, '2:00', 'Lift', 46000000, 88), # Cost includes original X plus X2 revamp
        ('Tatsu', 'Steel', 'Flying Coaster', 'Bolliger & Mabillard', 170, 62, 3602, 2006, None, 1, 0, 0, 1400, 'high', 4, '75 mins', 54, '2:00', 'Lift', 21000000, 62),
        ('Superman: Escape from Krypton', 'Steel', 'Reverse Freefall Coaster', 'Intamin', 415, 100, 1315, 1997, None, 1, 0, 0, 1050, 'high', 0, '45 mins', 48, '0:28', 'LSM Launch', 20000000, 90),
        ('Wonder Woman Flight of Courage', 'Steel', 'Raptor Track', 'Rocky Mountain Construction', 131, 58, 3300, 2022, None, 1, 0, 0, 800, 'high', 3, '60 mins', 48, '2:00', 'Lift', None, 87),
        ('Full Throttle', 'Steel', 'Sky Rocket III', 'Premier Rides', 160, 70, 2200, 2013, None, 1, 0, 0, 800, 'high', 2, '60 mins', 54, '1:30', 'LSM Launch', None, 90), # Has a drop off the loop
        ('Goliath', 'Steel', 'Mega Coaster', 'Giovanola', 235, 85, 4500, 2000, None, 1, 0, 0, 1600, 'high', 0, '45 mins', 48, '3:00', 'Lift', 30000000, 61),
        ('West Coast Racers', 'Steel', 'Magnetic Launch Coaster', 'Premier Rides', 66, 55, 4000, 2020, None, 1, 0, 0, 800, 'high', 4, '45 mins', 54, '2:50', 'LSM Launch', None, 45),
        ('Batman: The Ride', 'Steel', 'Inverted Coaster', 'Bolliger & Mabillard', 105, 50, 2693, 1994, None, 1, 0, 0, 1400, 'high', 5, '30 mins', 54, '2:00', 'Lift', 8000000, 50),
        ("Riddler's Revenge", 'Steel', 'Stand-Up Coaster', 'Bolliger & Mabillard', 156, 65, 4370, 1998, None, 1, 0, 0, 1610, 'high', 6, '30 mins', 54, '3:00', 'Lift', 14000000, 52),
        ('Scream', 'Steel', 'Floorless Coaster', 'Bolliger & Mabillard', 150, 63, 3985, 2003, None, 1, 0, 0, 1440, 'high', 7, '15 mins', 54, '3:00', 'Lift', None, 50),
        ('Viper', 'Steel', 'Custom Looping Coaster', 'Arrow Dynamics', 188, 70, 3830, 1990, None, 1, 0, 0, 1700, 'high', 7, '10 mins', 54, '2:30', 'Lift', 12000000, 55),
        ('Revolution', 'Steel', 'Looping Coaster', 'Schwarzkopf', 113, 45, 3457, 1976, None, 1, 0, 0, 1200, 'medium', 1, '20 mins', 48, '2:15', 'Lift', 3000000, 45),
        ('Ninja', 'Steel', 'Suspended Coaster', 'Arrow Dynamics', 60, 55, 2700, 1988, None, 1, 0, 0, 1600, 'medium', 0, '20 mins', 42, '1:30', 'Lift', None, 45),
        ('Apocalypse', 'Wood', 'Wooden Coaster', 'Great Coasters International', 98, 50, 2887, 2009, None, 1, 0, 0, 1000, 'medium', 0, '30 mins', 48, '2:30', 'Lift', 10000000, 52),
        ('Gold Rusher', 'Steel', 'Mine Train', 'Arrow Dynamics', 70, 35, 2590, 1971, None, 1, 0, 0, 1750, 'medium', 0, '10 mins', 48, '2:30', 'Lift', None, 45),

        # --- REMOVED / REPLACED COASTERS ---
        ('Colossus', 'Wood', 'Racing Coaster', 'International Amusement Devices', 125, 62, 4325, 1978, 2014, 0, 0, 1, 2600, 'high', 0, None, 48, '2:30', 'Lift', 2500000, 50),
        ('Psyclone', 'Wood', 'Wooden Coaster', 'Dinn Corporation', 95, 50, 2970, 1991, 2006, 0, 0, 1, 1200, 'medium', 0, None, 48, '2:00', 'Lift', None, 53),
        ('Green Lantern: First Flight', 'Steel', 'ZacSpin', 'Intamin', 107, 37, 825, 2011, 2019, 0, 0, 1, 800, 'high', 0, None, 52, '1:15', 'Lift', 7000000, 90)
    ]

    coaster_id_map = {}

    for c in coasters:
        (name, c_type, model, mfg_name, h, s, l, yr_open, yr_closed, active, sbno, rem, 
         rph, thrill, inv, wait, restrict, dur, lift, cost, drop) = c
        
        age = current_year - yr_open
        
        # Check if cost or drop is None to avoid inserting the string "None"
        cursor.execute('''
            INSERT INTO rollercoasters (
                name, type, model, manufacturer_id, height, speed, length, 
                year_opened, year_closed, currently_operating, SBNO, removed, park_id, 
                riders_per_hour, thrill_level, inversions, avg_wait_time, 
                height_restriction, ride_duration, lift_or_launch, cost, 
                drop_angle_in_degrees, age
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            name, c_type, model, mfg_map[mfg_name], h, s, l, 
            yr_open, yr_closed, active, sbno, rem, sfmm_id, 
            rph, thrill, inv, wait, restrict, dur, lift, cost, drop, age
        ))
        
        coaster_id_map[name] = cursor.lastrowid

    # 4. Map Replacements 
    replacements = {
        "Colossus": "Twisted Colossus",
        "Psyclone": "Apocalypse",
        "Green Lantern: First Flight": "Wonder Woman Flight of Courage"
    }

    # 5. Update the replaced_by_id foreign key
    for old_coaster, new_coaster in replacements.items():
        if old_coaster in coaster_id_map and new_coaster in coaster_id_map:
            old_id = coaster_id_map[old_coaster]
            new_id = coaster_id_map[new_coaster]
            
            cursor.execute('''
                UPDATE rollercoasters 
                SET replaced_by_id = ? 
                WHERE rollercoaster_id = ?
            ''', (new_id, old_id))

    conn.commit()
    conn.close()
    print("Six Flags Magic Mountain data successfully added.")

def populate_busch_gardens_tampa():
    conn = sqlite3.connect('database_new.db')
    cursor = conn.cursor()
    current_year = datetime.now().year

    # 1. Insert Manufacturers (Safe check logic)
    # Including new ones like Mack Rides, while reusing B&M, Intamin, etc.
    mfg_data = [
        ('Bolliger & Mabillard', 1988),
        ('Intamin', 1967),
        ('Rocky Mountain Construction', 2001),
        ('Mack Rides', 1780),
        ('Schwarzkopf', 1960),
        ('Great Coasters International', 1994),
        ('Arrow Dynamics', 1946),
        ('Maurer AG', 1876),
        ('Zierer', 1930)
    ]
    
    mfg_map = {}
    for name, year in mfg_data:
        cursor.execute("SELECT manufacturer_id FROM manufacturers WHERE name = ?", (name,))
        result = cursor.fetchone()
        if result:
            mfg_map[name] = result[0]
        else:
            cursor.execute("INSERT INTO manufacturers (name, year_founded) VALUES (?, ?)", (name, year))
            mfg_map[name] = cursor.lastrowid

    # 2. Insert Busch Gardens Tampa Bay
    cursor.execute('''
        INSERT INTO parks (name, owned_by, year_opened, visitors_per_year, visitors_per_day, location)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', ("Busch Gardens Tampa Bay", "United Parks & Resorts", 1959, 4100000, 11200, "Tampa, Florida"))
    bgt_id = cursor.lastrowid

    # 3. BGT Coaster Data
    # Format: name, type, model, mfg, h, s, l, yr_open, yr_closed, active, sbno, rem, rph, thrill, inv, wait, restriction, duration, lift_launch, cost, drop_angle
    coasters = [
        # --- OPERATING COASTERS ---
        ('Iron Gwazi', 'Steel', 'IBox Track', 'Rocky Mountain Construction', 206, 76, 4075, 2022, None, 1, 0, 0, 1050, 'high', 2, '75 mins', 48, '1:50', 'Lift', None, 91),
        ('SheiKra', 'Steel', 'Dive Coaster', 'Bolliger & Mabillard', 200, 70, 3188, 2005, None, 1, 0, 0, 1500, 'high', 1, '45 mins', 54, '2:20', 'Lift', 13500000, 90),
        ('Montu', 'Steel', 'Inverted Coaster', 'Bolliger & Mabillard', 150, 60, 3983, 1996, None, 1, 0, 0, 1710, 'high', 7, '30 mins', 54, '3:00', 'Lift', None, 50),
        ('Kumba', 'Steel', 'Sitting Coaster', 'Bolliger & Mabillard', 143, 60, 3977, 1993, None, 1, 0, 0, 1700, 'high', 7, '15 mins', 54, '2:54', 'Lift', None, 55),
        ('Cheetah Hunt', 'Steel', 'Blitz Coaster', 'Intamin', 102, 60, 4429, 2011, None, 1, 0, 0, 1370, 'high', 1, '60 mins', 48, '3:30', 'LSM Launch', None, 50),
        ("Cobra's Curse", 'Steel', 'Spinning Coaster', 'Mack Rides', 70, 40, 2100, 2016, None, 1, 0, 0, 1000, 'medium', 0, '45 mins', 42, '3:30', 'Elevator Lift', None, 45),
        ('Phoenix Rising', 'Steel', 'Family Inverted Coaster', 'Bolliger & Mabillard', 80, 44, 1831, 2024, None, 1, 0, 0, 800, 'medium', 0, '45 mins', 42, '2:00', 'Lift', None, 45),
        ('Air Grover', 'Steel', 'Force', 'Zierer', 24, 22, 623, 2010, None, 1, 0, 0, 500, 'kiddie', 0, '15 mins', 38, '1:00', 'Lift', None, 30),

        # --- REMOVED / REPLACED COASTERS ---
        ('Gwazi', 'Wood', 'Wooden Coaster', 'Great Coasters International', 105, 51, 7000, 1999, 2015, 0, 0, 1, 1000, 'high', 0, None, 48, '2:30', 'Lift', 10000000, 50), # Length is combined for both tracks
        ('Sand Serpent', 'Steel', 'Wild Mouse', 'Maurer AG', 45, 28, 1213, 2004, 2023, 0, 0, 1, 600, 'medium', 0, None, 46, '1:30', 'Lift', None, 45),
        ('Scorpion', 'Steel', 'Silverarrow', 'Schwarzkopf', 60, 50, 1817, 1980, 2024, 0, 0, 1, 900, 'medium', 1, None, 42, '1:30', 'Lift', None, 45),
        ('Python', 'Steel', 'Custom Looping Coaster', 'Arrow Dynamics', 70, 50, 1200, 1976, 2006, 0, 0, 1, 1000, 'medium', 2, None, 48, '1:30', 'Lift', None, 45)
    ]

    coaster_id_map = {}

    for c in coasters:
        (name, c_type, model, mfg_name, h, s, l, yr_open, yr_closed, active, sbno, rem, 
         rph, thrill, inv, wait, restrict, dur, lift, cost, drop) = c
        
        age = current_year - yr_open
        
        cursor.execute('''
            INSERT INTO rollercoasters (
                name, type, model, manufacturer_id, height, speed, length, 
                year_opened, year_closed, currently_operating, SBNO, removed, park_id, 
                riders_per_hour, thrill_level, inversions, avg_wait_time, 
                height_restriction, ride_duration, lift_or_launch, cost, 
                drop_angle_in_degrees, age
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            name, c_type, model, mfg_map[mfg_name], h, s, l, 
            yr_open, yr_closed, active, sbno, rem, bgt_id, 
            rph, thrill, inv, wait, restrict, dur, lift, cost, drop, age
        ))
        
        coaster_id_map[name] = cursor.lastrowid

    # 4. Map Replacements 
    replacements = {
        "Gwazi": "Iron Gwazi",
        "Sand Serpent": "Phoenix Rising" # Phoenix Rising was built in the Pantopia footprint left by Sand Serpent
    }

    # 5. Update the replaced_by_id foreign key
    for old_coaster, new_coaster in replacements.items():
        if old_coaster in coaster_id_map and new_coaster in coaster_id_map:
            old_id = coaster_id_map[old_coaster]
            new_id = coaster_id_map[new_coaster]
            
            cursor.execute('''
                UPDATE rollercoasters 
                SET replaced_by_id = ? 
                WHERE rollercoaster_id = ?
            ''', (new_id, old_id))

    conn.commit()
    conn.close()
    print("Busch Gardens Tampa Bay data successfully added.")

def populate_busch_gardens_williamsburg():
    conn = sqlite3.connect('database_new.db')
    cursor = conn.cursor()
    current_year = datetime.now().year

    # 1. Insert Manufacturers (Safe check logic)
    mfg_data = [
        ('Bolliger & Mabillard', 1988),
        ('Intamin', 1967),
        ('Arrow Dynamics', 1946),
        ('Premier Rides', 1994),
        ('Great Coasters International', 1994),
        ('Zierer', 1930),
        ('Schwarzkopf', 1960)
    ]
    
    mfg_map = {}
    for name, year in mfg_data:
        cursor.execute("SELECT manufacturer_id FROM manufacturers WHERE name = ?", (name,))
        result = cursor.fetchone()
        if result:
            mfg_map[name] = result[0]
        else:
            cursor.execute("INSERT INTO manufacturers (name, year_founded) VALUES (?, ?)", (name, year))
            mfg_map[name] = cursor.lastrowid

    # 2. Insert Busch Gardens Williamsburg
    cursor.execute('''
        INSERT INTO parks (name, owned_by, year_opened, visitors_per_year, visitors_per_day, location)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', ("Busch Gardens Williamsburg", "United Parks & Resorts", 1975, 2800000, 10000, "Williamsburg, Virginia"))
    bgw_id = cursor.lastrowid

    # 3. BGW Coaster Data
    # Format: name, type, model, mfg, h, s, l, yr_open, yr_closed, active, sbno, rem, rph, thrill, inv, wait, restriction, duration, lift_launch, cost, drop_angle
    coasters = [
        # --- OPERATING COASTERS ---
        ('Alpengeist', 'Steel', 'Inverted Coaster', 'Bolliger & Mabillard', 195, 67, 3828, 1997, None, 1, 0, 0, 1820, 'high', 6, '30 mins', 54, '3:10', 'Lift', 20000000, None),
        ("Apollo's Chariot", 'Steel', 'Hyper Coaster', 'Bolliger & Mabillard', 170, 73, 4882, 1999, None, 1, 0, 0, 1750, 'high', 0, '20 mins', 52, '2:15', 'Lift', 20000000, 65),
        ('DarKoaster', 'Steel', 'Family Straddle Coaster', 'Intamin', 20, 36, 2454, 2023, None, 1, 0, 0, 1000, 'medium', 0, '60 mins', 48, '1:30', 'LSM Launch', None, None),
        ('Griffon', 'Steel', 'Dive Coaster', 'Bolliger & Mabillard', 205, 71, 3108, 2007, None, 1, 0, 0, 1400, 'high', 2, '25 mins', 54, '3:00', 'Lift', 15600000, 90),
        ('InvadR', 'Wood', 'Wooden Coaster', 'Great Coasters International', 74, 48, 2118, 2017, None, 1, 0, 0, 800, 'medium', 0, '45 mins', 46, '1:30', 'Lift', 15000000, 56),
        ('Loch Ness Monster', 'Steel', 'Custom Looping Coaster', 'Arrow Dynamics', 130, 60, 3240, 1978, None, 1, 0, 0, 1200, 'high', 2, '20 mins', 48, '2:10', 'Lift', 2500000, 55),
        ('Pantheon', 'Steel', 'LSM Launch Coaster', 'Intamin', 178, 73, 3328, 2022, None, 1, 0, 0, 1050, 'high', 2, '60 mins', 52, '2:00', 'LSM Launch', None, 95),
        ('Tempesto', 'Steel', 'Sky Rocket II', 'Premier Rides', 150, 62, 863, 2015, None, 1, 0, 0, 600, 'high', 1, '45 mins', 54, '0:55', 'LSM Launch', None, None),
        ('Verbolten', 'Steel', 'Elevated Seating Coaster', 'Zierer', 88, 53, 2835, 2012, None, 1, 0, 0, 1200, 'medium', 0, '45 mins', 48, '3:20', 'LSM Launch', 51000000, 88),
        ("Grover's Alpine Express", 'Steel', 'Force', 'Zierer', 24, 22, 600, 2009, None, 1, 0, 0, 500, 'kiddie', 0, '15 mins', 38, '1:00', 'Lift', None, 30),

        # --- REMOVED / REPLACED COASTERS ---
        ('Big Bad Wolf', 'Steel', 'Suspended Coaster', 'Arrow Dynamics', 100, 48, 2800, 1984, 2009, 0, 0, 1, 1300, 'medium', 0, None, 42, '3:00', 'Lift', 3800000, None),
        ('Drachen Fire', 'Steel', 'Custom Looping Coaster', 'Arrow Dynamics', 150, 60, 3550, 1992, 1998, 0, 0, 1, 1200, 'high', 6, None, 48, '3:00', 'Lift', 4000000, None), # Stood SBNO until 2002, closed in 98
        ('Wild Maus', 'Steel', 'Wild Mouse', 'Schwarzkopf', 46, 28, 1500, 1996, 2003, 0, 0, 1, 900, 'medium', 0, None, 46, '1:30', 'Lift', None, None)
    ]

    coaster_id_map = {}

    for c in coasters:
        (name, c_type, model, mfg_name, h, s, l, yr_open, yr_closed, active, sbno, rem, 
         rph, thrill, inv, wait, restrict, dur, lift, cost, drop) = c
        
        age = current_year - yr_open
        
        cursor.execute('''
            INSERT INTO rollercoasters (
                name, type, model, manufacturer_id, height, speed, length, 
                year_opened, year_closed, currently_operating, SBNO, removed, park_id, 
                riders_per_hour, thrill_level, inversions, avg_wait_time, 
                height_restriction, ride_duration, lift_or_launch, cost, 
                drop_angle_in_degrees, age
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            name, c_type, model, mfg_map[mfg_name], h, s, l, 
            yr_open, yr_closed, active, sbno, rem, bgw_id, 
            rph, thrill, inv, wait, restrict, dur, lift, cost, drop, age
        ))
        
        coaster_id_map[name] = cursor.lastrowid

    # 4. Map Replacements 
    replacements = {
        "Big Bad Wolf": "Verbolten" # Verbolten occupies the exact footprint and reuses the same final drop trench to the river
    }

    # 5. Update the replaced_by_id foreign key
    for old_coaster, new_coaster in replacements.items():
        if old_coaster in coaster_id_map and new_coaster in coaster_id_map:
            old_id = coaster_id_map[old_coaster]
            new_id = coaster_id_map[new_coaster]
            
            cursor.execute('''
                UPDATE rollercoasters 
                SET replaced_by_id = ? 
                WHERE rollercoaster_id = ?
            ''', (new_id, old_id))

    conn.commit()
    conn.close()
    print("Busch Gardens Williamsburg data successfully added.")

def populate_seaworld_orlando():
    conn = sqlite3.connect('database_new.db')
    cursor = conn.cursor()
    current_year = datetime.now().year

    # 1. Insert Manufacturers (Safe check logic)
    mfg_data = [
        ('Bolliger & Mabillard', 1988),
        ('Premier Rides', 1994),
        ('Mack Rides', 1780),
        ('Zierer', 1930)
    ]
    
    mfg_map = {}
    for name, year in mfg_data:
        cursor.execute("SELECT manufacturer_id FROM manufacturers WHERE name = ?", (name,))
        result = cursor.fetchone()
        if result:
            mfg_map[name] = result[0]
        else:
            cursor.execute("INSERT INTO manufacturers (name, year_founded) VALUES (?, ?)", (name, year))
            mfg_map[name] = cursor.lastrowid

    # 2. Insert SeaWorld Orlando
    cursor.execute('''
        INSERT INTO parks (name, owned_by, year_opened, visitors_per_year, visitors_per_day, location)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', ("SeaWorld Orlando", "United Parks & Resorts", 1973, 4600000, 12600, "Orlando, Florida"))
    swo_id = cursor.lastrowid

    # 3. SWO Coaster Data
    # Format: name, type, model, mfg, h, s, l, yr_open, yr_closed, active, sbno, rem, rph, thrill, inv, wait, restriction, duration, lift_launch, cost, drop_angle
    coasters = [
        # --- OPERATING COASTERS ---
        ('Mako', 'Steel', 'Hyper Coaster', 'Bolliger & Mabillard', 200, 73, 4760, 2016, None, 1, 0, 0, 1680, 'high', 0, '45 mins', 54, '3:00', 'Lift', None, 73),
        ('Kraken', 'Steel', 'Floorless Coaster', 'Bolliger & Mabillard', 153, 65, 4177, 2000, None, 1, 0, 0, 1500, 'high', 7, '30 mins', 54, '2:02', 'Lift', None, None),
        ('Manta', 'Steel', 'Flying Coaster', 'Bolliger & Mabillard', 140, 56, 3359, 2009, None, 1, 0, 0, 1500, 'high', 4, '60 mins', 54, '2:35', 'Lift', None, None),
        ('Pipeline: The Surf Coaster', 'Steel', 'Surf Coaster', 'Bolliger & Mabillard', 110, 60, 2950, 2023, None, 1, 0, 0, 1200, 'high', 1, '45 mins', 54, '1:50', 'LSM Launch', None, None),
        ('Ice Breaker', 'Steel', 'Sky Rocket', 'Premier Rides', 93, 52, 1900, 2022, None, 1, 0, 0, 800, 'medium', 0, '45 mins', 48, '1:30', 'LSM Launch', None, 100), # 100-degree beyond-vertical spike
        ('Penguin Trek', 'Steel', 'Family Coaster', 'Bolliger & Mabillard', 65, 43, 3020, 2024, None, 1, 0, 0, 1000, 'medium', 0, '60 mins', 42, '2:00', 'LSM Launch', None, None),
        ('Journey to Atlantis', 'Steel', 'Water Coaster', 'Mack Rides', 60, 40, 1800, 1998, None, 1, 0, 0, 1400, 'medium', 0, '45 mins', 42, '5:54', 'Lift', None, None),
        ("Super Grover's Box Car Derby", 'Steel', 'Force', 'Zierer', 24, 22, 600, 2006, None, 1, 0, 0, 500, 'kiddie', 0, '15 mins', 38, '1:00', 'Lift', None, None)
    ]

    coaster_id_map = {}

    for c in coasters:
        (name, c_type, model, mfg_name, h, s, l, yr_open, yr_closed, active, sbno, rem, 
         rph, thrill, inv, wait, restrict, dur, lift, cost, drop) = c
        
        age = current_year - yr_open
        
        cursor.execute('''
            INSERT INTO rollercoasters (
                name, type, model, manufacturer_id, height, speed, length, 
                year_opened, year_closed, currently_operating, SBNO, removed, park_id, 
                riders_per_hour, thrill_level, inversions, avg_wait_time, 
                height_restriction, ride_duration, lift_or_launch, cost, 
                drop_angle_in_degrees, age
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            name, c_type, model, mfg_map[mfg_name], h, s, l, 
            yr_open, yr_closed, active, sbno, rem, swo_id, 
            rph, thrill, inv, wait, restrict, dur, lift, cost, drop, age
        ))
        
        coaster_id_map[name] = cursor.lastrowid

    # 4. Map Replacements (Empty because SeaWorld Orlando has zero removed coasters!)
    replacements = {}

    # 5. Update the replaced_by_id foreign key (this will safely bypass since the dict is empty)
    for old_coaster, new_coaster in replacements.items():
        if old_coaster in coaster_id_map and new_coaster in coaster_id_map:
            old_id = coaster_id_map[old_coaster]
            new_id = coaster_id_map[new_coaster]
            
            cursor.execute('''
                UPDATE rollercoasters 
                SET replaced_by_id = ? 
                WHERE rollercoaster_id = ?
            ''', (new_id, old_id))

    conn.commit()
    conn.close()
    print("SeaWorld Orlando data successfully added.")

def populate_seaworld_san_diego():
    conn = sqlite3.connect('database_new.db')
    cursor = conn.cursor()
    current_year = datetime.now().year

    # 1. Insert Manufacturers (Safe check logic)
    # Introducing Skyline Attractions for the defunct Tidal Twister
    mfg_data = [
        ('Bolliger & Mabillard', 1988),
        ('Intamin', 1967),
        ('Premier Rides', 1994),
        ('Mack Rides', 1780),
        ('Skyline Attractions', 2014)
    ]
    
    mfg_map = {}
    for name, year in mfg_data:
        cursor.execute("SELECT manufacturer_id FROM manufacturers WHERE name = ?", (name,))
        result = cursor.fetchone()
        if result:
            mfg_map[name] = result[0]
        else:
            cursor.execute("INSERT INTO manufacturers (name, year_founded) VALUES (?, ?)", (name, year))
            mfg_map[name] = cursor.lastrowid

    # 2. Insert SeaWorld San Diego
    cursor.execute('''
        INSERT INTO parks (name, owned_by, year_opened, visitors_per_year, visitors_per_day, location)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', ("SeaWorld San Diego", "United Parks & Resorts", 1964, 4000000, 10900, "San Diego, California"))
    swsd_id = cursor.lastrowid

    # 3. SWSD Coaster Data
    # Format: name, type, model, mfg, h, s, l, yr_open, yr_closed, active, sbno, rem, rph, thrill, inv, wait, restriction, duration, lift_launch, cost, drop_angle
    coasters = [
        # --- OPERATING COASTERS ---
        ('Arctic Rescue', 'Steel', 'Family Launch Coaster', 'Intamin', 30, 40, 2800, 2023, None, 1, 0, 0, 1000, 'medium', 0, '45 mins', 48, '1:15', 'Tire Launch', None, None),
        ('Emperor', 'Steel', 'Dive Coaster', 'Bolliger & Mabillard', 153, 60, 2411, 2022, None, 1, 0, 0, 1200, 'high', 3, '45 mins', 52, '1:35', 'Lift', None, 90),
        ('Electric Eel', 'Steel', 'Sky Rocket II', 'Premier Rides', 150, 62, 863, 2018, None, 1, 0, 0, 600, 'high', 1, '30 mins', 54, '0:55', 'LSM Launch', None, None),
        ('Manta', 'Steel', 'Launched Coaster', 'Mack Rides', 30, 43, 2800, 2012, None, 1, 0, 0, 1400, 'high', 0, '45 mins', 48, '1:40', 'LSM Launch', None, None),
        ('Journey to Atlantis', 'Steel', 'Water Coaster', 'Mack Rides', 95, 42, 0, 2004, None, 1, 0, 0, 1900, 'medium', 0, '30 mins', 42, '5:00', 'Elevator/Lift', None, None),

        # --- REMOVED / REPLACED COASTERS ---
        ('Tidal Twister', 'Steel', 'Skywarp Horizon', 'Skyline Attractions', 22, 30, 320, 2019, 2023, 0, 0, 1, 600, 'medium', 1, None, 48, '2:42', 'Drive Tires', None, None)
    ]

    coaster_id_map = {}

    for c in coasters:
        (name, c_type, model, mfg_name, h, s, l, yr_open, yr_closed, active, sbno, rem, 
         rph, thrill, inv, wait, restrict, dur, lift, cost, drop) = c
        
        age = current_year - yr_open
        
        cursor.execute('''
            INSERT INTO rollercoasters (
                name, type, model, manufacturer_id, height, speed, length, 
                year_opened, year_closed, currently_operating, SBNO, removed, park_id, 
                riders_per_hour, thrill_level, inversions, avg_wait_time, 
                height_restriction, ride_duration, lift_or_launch, cost, 
                drop_angle_in_degrees, age
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            name, c_type, model, mfg_map[mfg_name], h, s, l, 
            yr_open, yr_closed, active, sbno, rem, swsd_id, 
            rph, thrill, inv, wait, restrict, dur, lift, cost, drop, age
        ))
        
        coaster_id_map[name] = cursor.lastrowid

    # 4. Map Replacements (Empty because Tidal Twister was removed without a direct coaster replacement)
    replacements = {}

    # 5. Update the replaced_by_id foreign key
    for old_coaster, new_coaster in replacements.items():
        if old_coaster in coaster_id_map and new_coaster in coaster_id_map:
            old_id = coaster_id_map[old_coaster]
            new_id = coaster_id_map[new_coaster]
            
            cursor.execute('''
                UPDATE rollercoasters 
                SET replaced_by_id = ? 
                WHERE rollercoaster_id = ?
            ''', (new_id, old_id))

    conn.commit()
    conn.close()
    print("SeaWorld San Diego data successfully added.")

def populate_great_adventure():
    conn = sqlite3.connect('database_new.db')
    cursor = conn.cursor()
    current_year = datetime.now().year

    # 1. Insert Manufacturers
    mfg_data = [
        ('Bolliger & Mabillard', 1988),
        ('Intamin', 1967),
        ('Rocky Mountain Construction', 2001),
        ('Arrow Dynamics', 1946),
        ('Mack Rides', 1780),
        ('Vekoma', 1926),
        ('Premier Rides', 1994),
        ('Togo', 1935)
    ]
    
    mfg_map = {}
    for name, year in mfg_data:
        cursor.execute("SELECT manufacturer_id FROM manufacturers WHERE name = ?", (name,))
        result = cursor.fetchone()
        if result:
            mfg_map[name] = result[0]
        else:
            cursor.execute("INSERT INTO manufacturers (name, year_founded) VALUES (?, ?)", (name, year))
            mfg_map[name] = cursor.lastrowid

    # 2. Insert Six Flags Great Adventure
    cursor.execute('''
        INSERT INTO parks (name, owned_by, year_opened, visitors_per_year, visitors_per_day, location)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', ("Six Flags Great Adventure", "Six Flags", 1974, 3400000, 15000, "Jackson, New Jersey"))
    sfga_id = cursor.lastrowid

    # 3. SFGA Coaster Data
    coasters = [
        # --- OPERATING COASTERS ---
        ('El Toro', 'Wood', 'Prefabricated Wood', 'Intamin', 181, 76, 4400, 2006, None, 1, 0, 0, 1200, 'high', 0, '60 mins', 48, '1:42', 'Cable Lift', 25000000, 76),
        ('Nitro', 'Steel', 'Hyper Coaster', 'Bolliger & Mabillard', 230, 80, 5394, 2001, None, 1, 0, 0, 1600, 'high', 0, '45 mins', 54, '2:20', 'Lift', 20000000, None),
        ('Jersey Devil Coaster', 'Steel', 'Raptor Track', 'Rocky Mountain Construction', 130, 58, 3000, 2021, None, 1, 0, 0, 1000, 'high', 3, '60 mins', 48, '2:00', 'Lift', None, 87),
        ('Medusa', 'Steel', 'Floorless Coaster', 'Bolliger & Mabillard', 142, 61, 3985, 1999, None, 1, 0, 0, 1350, 'high', 7, '30 mins', 54, '3:15', 'Lift', None, None),
        ('Batman: The Ride', 'Steel', 'Inverted Coaster', 'Bolliger & Mabillard', 105, 50, 2693, 1993, None, 1, 0, 0, 1400, 'high', 5, '20 mins', 54, '2:00', 'Lift', None, None),
        ('Superman: Ultimate Flight', 'Steel', 'Flying Coaster', 'Bolliger & Mabillard', 106, 51, 2759, 2003, None, 1, 0, 0, 1500, 'high', 2, '60 mins', 54, '2:35', 'Lift', None, None),
        ('The Flash: Vertical Velocity', 'Steel', 'Super Boomerang', 'Vekoma', 142, 59, 1414, 2024, None, 1, 0, 0, 800, 'high', 0, '45 mins', 48, '1:30', 'LSM Launch', None, None),
        ('Runaway Mine Train', 'Steel', 'Mine Train', 'Arrow Dynamics', 60, 38, 2500, 1974, None, 1, 0, 0, 1200, 'medium', 0, '15 mins', 44, '2:30', 'Lift', None, None),
        ('The Dark Knight', 'Steel', 'Wild Mouse', 'Mack Rides', 45, 28, 1213, 2008, None, 1, 0, 0, 800, 'medium', 0, '30 mins', 42, '2:00', 'Lift', 7500000, None),

        # --- REMOVED / REPLACED COASTERS ---
        ('Kingda Ka', 'Steel', 'Strata Coaster', 'Intamin', 456, 128, 3118, 2005, 2024, 0, 0, 1, 1400, 'high', 0, None, 54, '0:28', 'Hydraulic Launch', 25000000, 90),
        ('Green Lantern', 'Steel', 'Stand-Up Coaster', 'Bolliger & Mabillard', 154, 63, 4155, 2011, 2024, 0, 0, 1, 1400, 'high', 5, None, 54, '2:30', 'Lift', None, None),
        ('Great American Scream Machine', 'Steel', 'Custom Looping Coaster', 'Arrow Dynamics', 173, 68, 3800, 1989, 2010, 0, 0, 1, 1500, 'high', 7, None, 54, '2:20', 'Lift', 4000000, None),
        ('Viper', 'Steel', 'Sitting Coaster', 'Togo', 88, 50, 1670, 1995, 2001, 0, 0, 1, 1000, 'medium', 2, None, 54, '1:40', 'Lift', None, None),
        ('Batman & Robin: The Chiller', 'Steel', 'LIM Shuttle Loop', 'Premier Rides', 200, 65, 1139, 1997, 2007, 0, 0, 1, 1360, 'high', 0, None, 54, '0:45', 'LIM Launch', None, None)
    ]

    coaster_id_map = {}

    for c in coasters:
        (name, c_type, model, mfg_name, h, s, l, yr_open, yr_closed, active, sbno, rem, 
         rph, thrill, inv, wait, restrict, dur, lift, cost, drop) = c
        
        age = current_year - yr_open
        
        cursor.execute('''
            INSERT INTO rollercoasters (
                name, type, model, manufacturer_id, height, speed, length, 
                year_opened, year_closed, currently_operating, SBNO, removed, park_id, 
                riders_per_hour, thrill_level, inversions, avg_wait_time, 
                height_restriction, ride_duration, lift_or_launch, cost, 
                drop_angle_in_degrees, age
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            name, c_type, model, mfg_map[mfg_name], h, s, l, 
            yr_open, yr_closed, active, sbno, rem, sfga_id, 
            rph, thrill, inv, wait, restrict, dur, lift, cost, drop, age
        ))
        
        coaster_id_map[name] = cursor.lastrowid

    # 4. Map Replacements
    replacements = {
        "Great American Scream Machine": "Green Lantern",
        "Viper": "El Toro"
    }

    # 5. Update the replaced_by_id foreign key
    for old_coaster, new_coaster in replacements.items():
        if old_coaster in coaster_id_map and new_coaster in coaster_id_map:
            old_id = coaster_id_map[old_coaster]
            new_id = coaster_id_map[new_coaster]
            
            cursor.execute('''
                UPDATE rollercoasters 
                SET replaced_by_id = ? 
                WHERE rollercoaster_id = ?
            ''', (new_id, old_id))

    conn.commit()
    conn.close()
    print("Six Flags Great Adventure data successfully updated and added.")

def populate_fiesta_texas():
    conn = sqlite3.connect('database_new.db')
    cursor = conn.cursor()
    current_year = datetime.now().year

    # 1. Insert Manufacturers (Safe check logic)
    mfg_data = [
        ('Bolliger & Mabillard', 1988),
        ('Rocky Mountain Construction', 2001),
        ('Premier Rides', 1994),
        ('S&S - Sansei Technologies', 1994),
        ('Vekoma', 1926),
        ('Arrow Dynamics', 1946),
        ('Gerstlauer', 1982),
        ('Skyline Attractions', 2014),
        ('Roller Coaster Corporation of America', 1979)
    ]
    
    mfg_map = {}
    for name, year in mfg_data:
        cursor.execute("SELECT manufacturer_id FROM manufacturers WHERE name = ?", (name,))
        result = cursor.fetchone()
        if result:
            mfg_map[name] = result[0]
        else:
            cursor.execute("INSERT INTO manufacturers (name, year_founded) VALUES (?, ?)", (name, year))
            mfg_map[name] = cursor.lastrowid

    # 2. Insert Six Flags Fiesta Texas
    cursor.execute('''
        INSERT INTO parks (name, owned_by, year_opened, visitors_per_year, visitors_per_day, location)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', ("Six Flags Fiesta Texas", "Six Flags", 1992, 2500000, 10000, "San Antonio, Texas"))
    sfft_id = cursor.lastrowid

    # 3. SFFT Coaster Data
    # Format: name, type, model, mfg, h, s, l, yr_open, yr_closed, active, sbno, rem, rph, thrill, inv, wait, restriction, duration, lift_launch, cost, drop_angle
    coasters = [
        # --- OPERATING COASTERS ---
        ('Iron Rattler', 'Steel', 'IBox Track', 'Rocky Mountain Construction', 171, 70, 3266, 2013, None, 1, 0, 0, 1080, 'high', 1, '45 mins', 48, '1:52', 'Lift', 10000000, 81),
        ('Superman: Krypton Coaster', 'Steel', 'Floorless Coaster', 'Bolliger & Mabillard', 168, 70, 4025, 2000, None, 1, 0, 0, 1600, 'high', 6, '30 mins', 54, '2:35', 'Lift', None, None),
        ('Wonder Woman Golden Lasso Coaster', 'Steel', 'Raptor Track', 'Rocky Mountain Construction', 113, 52, 1800, 2018, None, 1, 0, 0, 600, 'high', 3, '60 mins', 48, '1:00', 'Lift', None, 90),
        ("Dr. Diabolical's Cliffhanger", 'Steel', 'Dive Coaster', 'Bolliger & Mabillard', 150, 60, 2501, 2022, None, 1, 0, 0, 1200, 'high', 2, '45 mins', 52, '1:00', 'Lift', None, 95),
        ('Poltergeist', 'Steel', 'LIM Spaghetti Bowl', 'Premier Rides', 78, 60, 2705, 1999, None, 1, 0, 0, 900, 'high', 4, '30 mins', 54, '1:15', 'LIM Launch', None, None),
        ('Batman: The Ride', 'Steel', '4D Free Spin', 'S&S - Sansei Technologies', 120, 38, 1017, 2015, None, 1, 0, 0, 720, 'high', 6, '45 mins', 48, '1:00', 'Vertical Lift', None, 90),
        ('Goliath', 'Steel', 'Inverted Coaster', 'Bolliger & Mabillard', 105, 50, 2693, 2008, None, 1, 0, 0, 1400, 'high', 5, '30 mins', 54, '2:00', 'Lift', None, None),
        ('Boomerang', 'Steel', 'Boomerang', 'Vekoma', 116, 47, 935, 1999, None, 1, 0, 0, 760, 'high', 6, '20 mins', 48, '1:48', 'Lift', None, None),
        ('Road Runner Express', 'Steel', 'Mine Train', 'Arrow Dynamics', 73, 35, 2400, 1997, None, 1, 0, 0, 1200, 'medium', 0, '15 mins', 42, '2:24', 'Lift', None, None),
        ('Pandemonium', 'Steel', 'Spinning Coaster', 'Gerstlauer', 43, 31, 1351, 2007, None, 1, 0, 0, 800, 'medium', 0, '30 mins', 42, '1:51', 'Lift', None, None),
        ('Kid Flash Cosmic Coaster', 'Steel', "P'Sghetti Bowl", 'Skyline Attractions', 30, 36, 1158, 2023, None, 1, 0, 0, 800, 'medium', 0, '30 mins', 36, '1:00', 'Drive Tires', None, None),

        # --- REMOVED / REPLACED COASTERS ---
        ('The Rattler', 'Wood', 'Wooden Coaster', 'Roller Coaster Corporation of America', 179, 65, 5080, 1992, 2012, 0, 0, 1, 1200, 'high', 0, None, 48, '2:26', 'Lift', None, 61),
        ("Joker's Revenge", 'Steel', 'Hurricane', 'Vekoma', 79, 40, 1600, 1996, 2001, 0, 0, 1, 800, 'medium', 3, None, 48, '1:45', 'Lift', None, None)
    ]

    coaster_id_map = {}

    for c in coasters:
        (name, c_type, model, mfg_name, h, s, l, yr_open, yr_closed, active, sbno, rem, 
         rph, thrill, inv, wait, restrict, dur, lift, cost, drop) = c
        
        age = current_year - yr_open
        
        cursor.execute('''
            INSERT INTO rollercoasters (
                name, type, model, manufacturer_id, height, speed, length, 
                year_opened, year_closed, currently_operating, SBNO, removed, park_id, 
                riders_per_hour, thrill_level, inversions, avg_wait_time, 
                height_restriction, ride_duration, lift_or_launch, cost, 
                drop_angle_in_degrees, age
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            name, c_type, model, mfg_map[mfg_name], h, s, l, 
            yr_open, yr_closed, active, sbno, rem, sfft_id, 
            rph, thrill, inv, wait, restrict, dur, lift, cost, drop, age
        ))
        
        coaster_id_map[name] = cursor.lastrowid

    # 4. Map Replacements
    replacements = {
        "The Rattler": "Iron Rattler"
    }

    # 5. Update the replaced_by_id foreign key
    for old_coaster, new_coaster in replacements.items():
        if old_coaster in coaster_id_map and new_coaster in coaster_id_map:
            old_id = coaster_id_map[old_coaster]
            new_id = coaster_id_map[new_coaster]
            
            cursor.execute('''
                UPDATE rollercoasters 
                SET replaced_by_id = ? 
                WHERE rollercoaster_id = ?
            ''', (new_id, old_id))

    conn.commit()
    conn.close()
    print("Six Flags Fiesta Texas data successfully added.")

def populate_knotts_berry_farm():
    conn = sqlite3.connect('database_new.db')
    cursor = conn.cursor()
    current_year = datetime.now().year

    # 1. Insert Manufacturers (Safe check logic)
    mfg_data = [
        ('Custom Coasters International', 1991),
        ('Intamin', 1967),
        ('Bolliger & Mabillard', 1988),
        ('Gerstlauer', 1982),
        ('Zamperla', 1966),
        ('Mack Rides', 1780),
        ('Zierer', 1930),
        ('Schwarzkopf', 1960),
        ('Vekoma', 1926),
        ('Togo', 1935),
        ('Arrow Dynamics', 1946),
        ('Bradley and Kaye', 1946)
    ]
    
    mfg_map = {}
    for name, year in mfg_data:
        cursor.execute("SELECT manufacturer_id FROM manufacturers WHERE name = ?", (name,))
        result = cursor.fetchone()
        if result:
            mfg_map[name] = result[0]
        else:
            cursor.execute("INSERT INTO manufacturers (name, year_founded) VALUES (?, ?)", (name, year))
            mfg_map[name] = cursor.lastrowid

    # 2. Insert Knott's Berry Farm
    # Note: Owned by Six Flags Entertainment Corporation post-2024 Cedar Fair merger
    cursor.execute('''
        INSERT INTO parks (name, owned_by, year_opened, visitors_per_year, visitors_per_day, location)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', ("Knott's Berry Farm", "Six Flags Entertainment Corporation", 1920, 3800000, 10400, "Buena Park, California"))
    kbf_id = cursor.lastrowid

    # 3. KBF Coaster Data
    coasters = [
        # --- OPERATING / SBNO COASTERS ---
        ('GhostRider', 'Wood', 'Wooden Coaster', 'Custom Coasters International', 118, 56, 4533, 1998, None, 1, 0, 0, 1600, 'high', 0, '60 mins', 48, '2:40', 'Lift', 17000000, 51),
        ('Xcelerator', 'Steel', 'Accelerator Coaster', 'Intamin', 205, 82, 2202, 2002, None, 1, 0, 0, 1330, 'high', 0, '60 mins', 54, '1:02', 'Hydraulic Launch', 13000000, 90),
        ('Silver Bullet', 'Steel', 'Inverted Coaster', 'Bolliger & Mabillard', 146, 55, 3125, 2004, None, 1, 0, 0, 1300, 'high', 6, '45 mins', 54, '2:10', 'Lift', 16000000, None),
        ('HangTime', 'Steel', 'Infinity Coaster', 'Gerstlauer', 150, 57, 2198, 2018, None, 1, 0, 0, 800, 'high', 5, '45 mins', 48, '1:30', 'Vertical Lift', None, 96),
        ('Pony Express', 'Steel', 'Motocoaster', 'Zamperla', 44, 38, 1300, 2008, None, 1, 0, 0, 900, 'medium', 0, '30 mins', 48, '0:36', 'Flywheel Launch', 9000000, None),
        ('Sierra Sidewinder', 'Steel', 'Spinning Coaster', 'Mack Rides', 62, 37, 1411, 2007, None, 1, 0, 0, 800, 'medium', 0, '45 mins', 42, '2:00', 'Lift', None, None),
        ('Coast Rider', 'Steel', 'Wild Mouse', 'Mack Rides', 52, 37, 1339, 2013, None, 1, 0, 0, 1000, 'medium', 0, '30 mins', 44, '2:30', 'Lift', None, None),
        ('Jaguar!', 'Steel', 'Tivoli', 'Zierer', 40, 35, 2602, 1995, None, 1, 0, 0, 1200, 'medium', 0, '30 mins', 48, '2:00', 'Lift', None, None),
        ("Snoopy's Tenderpaw Twister Coaster", 'Steel', 'Family Coaster', 'Zamperla', 16, 15, 390, 2024, None, 1, 0, 0, 400, 'kiddie', 0, '15 mins', 36, '1:00', 'Drive Tires', None, None),
        ("Montezooma's Revenge", 'Steel', 'Shuttle Loop', 'Schwarzkopf', 148, 55, 800, 1978, None, 0, 1, 0, 1300, 'high', 1, None, 48, '0:36', 'Flywheel Launch', None, None), # Set to SBNO (active=0, SBNO=1)

        # --- REMOVED / REPLACED COASTERS ---
        ('Boomerang', 'Steel', 'Boomerang', 'Vekoma', 116, 47, 935, 1990, 2017, 0, 0, 1, 760, 'high', 6, None, 48, '1:48', 'Lift', None, None),
        ('Windjammer Surf Racers', 'Steel', 'Racing Coaster', 'Togo', 54, 40, 2145, 1997, 2000, 0, 0, 1, 1000, 'medium', 1, None, 48, '1:30', 'Lift', None, None),
        ('Corkscrew', 'Steel', 'Corkscrew', 'Arrow Dynamics', 70, 46, 1250, 1975, 1989, 0, 0, 1, 1000, 'medium', 2, None, 48, '1:10', 'Lift', None, None),
        ('Timberline Twister', 'Steel', 'Kiddie Coaster', 'Bradley and Kaye', 30, 22, 480, 1983, 2023, 0, 0, 1, 400, 'kiddie', 0, None, 36, '1:00', 'Lift', None, None)
    ]

    coaster_id_map = {}

    for c in coasters:
        (name, c_type, model, mfg_name, h, s, l, yr_open, yr_closed, active, sbno, rem, 
         rph, thrill, inv, wait, restrict, dur, lift, cost, drop) = c
        
        age = current_year - yr_open
        
        cursor.execute('''
            INSERT INTO rollercoasters (
                name, type, model, manufacturer_id, height, speed, length, 
                year_opened, year_closed, currently_operating, SBNO, removed, park_id, 
                riders_per_hour, thrill_level, inversions, avg_wait_time, 
                height_restriction, ride_duration, lift_or_launch, cost, 
                drop_angle_in_degrees, age
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            name, c_type, model, mfg_map[mfg_name], h, s, l, 
            yr_open, yr_closed, active, sbno, rem, kbf_id, 
            rph, thrill, inv, wait, restrict, dur, lift, cost, drop, age
        ))
        
        coaster_id_map[name] = cursor.lastrowid

    # 4. Map Replacements
    replacements = {
        "Corkscrew": "Boomerang",
        "Boomerang": "HangTime",
        "Windjammer Surf Racers": "Xcelerator",
        "Timberline Twister": "Snoopy's Tenderpaw Twister Coaster"
    }

    # 5. Update the replaced_by_id foreign key
    for old_coaster, new_coaster in replacements.items():
        if old_coaster in coaster_id_map and new_coaster in coaster_id_map:
            old_id = coaster_id_map[old_coaster]
            new_id = coaster_id_map[new_coaster]
            
            cursor.execute('''
                UPDATE rollercoasters 
                SET replaced_by_id = ? 
                WHERE rollercoaster_id = ?
            ''', (new_id, old_id))

    conn.commit()
    conn.close()
    print("Knott's Berry Farm data successfully added.")

def populate_hersheypark():
    conn = sqlite3.connect('database_new.db')
    cursor = conn.cursor()
    current_year = datetime.now().year

    # 1. Insert Manufacturers (Safe check logic)
    mfg_data = [
        ('Intamin', 1967),
        ('Bolliger & Mabillard', 1988),
        ('Rocky Mountain Construction', 2001),
        ('Great Coasters International', 1994),
        ('Philadelphia Toboggan Coasters', 1904),
        ('Schwarzkopf', 1960),
        ('Arrow Dynamics', 1946),
        ('Vekoma', 1926),
        ('Mack Rides', 1780),
        ('Maurer Rides', 1993),
        ('Zamperla', 1966),
        ('Setpoint', 1992)
    ]
    
    mfg_map = {}
    for name, year in mfg_data:
        cursor.execute("SELECT manufacturer_id FROM manufacturers WHERE name = ?", (name,))
        result = cursor.fetchone()
        if result:
            mfg_map[name] = result[0]
        else:
            cursor.execute("INSERT INTO manufacturers (name, year_founded) VALUES (?, ?)", (name, year))
            mfg_map[name] = cursor.lastrowid

    # 2. Insert Hersheypark
    cursor.execute('''
        INSERT INTO parks (name, owned_by, year_opened, visitors_per_year, visitors_per_day, location)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', ("Hersheypark", "Hershey Entertainment & Resorts Company", 1906, 3300000, 10500, "Hershey, Pennsylvania"))
    hp_id = cursor.lastrowid

    # 3. Hersheypark Coaster Data
    # Format: name, type, model, mfg, h, s, l, yr_open, yr_closed, active, sbno, rem, rph, thrill, inv, wait, restriction, duration, lift_launch, cost, drop_angle
    coasters = [
        # --- OPERATING COASTERS ---
        ('Candymonium', 'Steel', 'Hyper Coaster', 'Bolliger & Mabillard', 210, 76, 4636, 2020, None, 1, 0, 0, 1600, 'high', 0, '60 mins', 54, '2:26', 'Lift', 25000000, 77),
        ('Skyrush', 'Steel', 'Wing Coaster', 'Intamin', 200, 75, 3600, 2012, None, 1, 0, 0, 1350, 'high', 0, '45 mins', 54, '1:03', 'Cable Lift', 25000000, 85),
        ('Storm Runner', 'Steel', 'Accelerator Coaster', 'Intamin', 150, 72, 2600, 2004, None, 1, 0, 0, 1200, 'high', 3, '45 mins', 54, '0:50', 'Hydraulic Launch', 12500000, 90),
        ('Fahrenheit', 'Steel', 'Vertical Lift Coaster', 'Intamin', 121, 58, 2700, 2008, None, 1, 0, 0, 850, 'high', 6, '60 mins', 54, '1:25', 'Vertical Lift', 12100000, 97),
        ("Wildcat's Revenge", 'Steel', 'IBox Track', 'Rocky Mountain Construction', 140, 62, 3510, 2023, None, 1, 0, 0, 1050, 'high', 4, '60 mins', 48, '2:36', 'Lift', None, 82),
        ('Great Bear', 'Steel', 'Inverted Coaster', 'Bolliger & Mabillard', 90, 58, 3150, 1998, None, 1, 0, 0, 1300, 'high', 4, '45 mins', 54, '2:55', 'Lift', 13000000, None),
        ('Lightning Racer', 'Wood', 'Racing Coaster', 'Great Coasters International', 90, 51, 3393, 2000, None, 1, 0, 0, 2000, 'high', 0, '20 mins', 48, '2:20', 'Lift', 12500000, None),
        ('Comet', 'Wood', 'Wooden Coaster', 'Philadelphia Toboggan Coasters', 84, 50, 3360, 1946, None, 1, 0, 0, 1000, 'medium', 0, '45 mins', 42, '1:45', 'Lift', None, 47),
        ('Superdooperlooper', 'Steel', 'Custom Looping Coaster', 'Schwarzkopf', 75, 45, 2614, 1977, None, 1, 0, 0, 1100, 'medium', 1, '20 mins', 42, '1:45', 'Lift', 3000000, None),
        ('Laff Trakk', 'Steel', 'Spinning Coaster', 'Maurer Rides', 50, 40, 1400, 2015, None, 1, 0, 0, 850, 'medium', 0, '45 mins', 42, '1:10', 'Lift', None, None),
        ('Jolly Rancher Remix', 'Steel', 'Boomerang', 'Vekoma', 116, 47, 935, 1991, None, 1, 0, 0, 760, 'high', 6, '30 mins', 48, '1:48', 'Lift', None, None),
        ('Trailblazer', 'Steel', 'Mine Train', 'Arrow Dynamics', 43, 45, 1600, 1974, None, 1, 0, 0, 1000, 'medium', 0, '15 mins', 36, '1:15', 'Lift', None, None),
        ('Wild Mouse', 'Steel', 'Wild Mouse', 'Mack Rides', 45, 28, 1213, 1999, None, 1, 0, 0, 900, 'medium', 0, '20 mins', 48, '1:58', 'Lift', None, None),
        ('Cocoa Cruiser', 'Steel', 'Family Coaster', 'Zamperla', 13, 15, 279, 2014, None, 1, 0, 0, 400, 'kiddie', 0, '10 mins', 36, '1:00', 'Drive Tires', None, None),

        # --- REMOVED / REPLACED COASTERS ---
        ('Wildcat', 'Wood', 'Wooden Coaster', 'Great Coasters International', 106, 50, 3183, 1996, 2022, 0, 0, 1, 1000, 'high', 0, None, 48, '2:15', 'Lift', 5000000, None),
        ('Roller Soaker', 'Steel', 'Suspended Family Coaster', 'Setpoint', 70, 20, 1300, 2002, 2012, 0, 0, 1, 800, 'medium', 0, None, 48, '1:30', 'Lift', None, None)
    ]

    coaster_id_map = {}

    for c in coasters:
        (name, c_type, model, mfg_name, h, s, l, yr_open, yr_closed, active, sbno, rem, 
         rph, thrill, inv, wait, restrict, dur, lift, cost, drop) = c
        
        age = current_year - yr_open
        
        cursor.execute('''
            INSERT INTO rollercoasters (
                name, type, model, manufacturer_id, height, speed, length, 
                year_opened, year_closed, currently_operating, SBNO, removed, park_id, 
                riders_per_hour, thrill_level, inversions, avg_wait_time, 
                height_restriction, ride_duration, lift_or_launch, cost, 
                drop_angle_in_degrees, age
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            name, c_type, model, mfg_map[mfg_name], h, s, l, 
            yr_open, yr_closed, active, sbno, rem, hp_id, 
            rph, thrill, inv, wait, restrict, dur, lift, cost, drop, age
        ))
        
        coaster_id_map[name] = cursor.lastrowid

    # 4. Map Replacements
    replacements = {
        "Wildcat": "Wildcat's Revenge"
    }

    # 5. Update the replaced_by_id foreign key
    for old_coaster, new_coaster in replacements.items():
        if old_coaster in coaster_id_map and new_coaster in coaster_id_map:
            old_id = coaster_id_map[old_coaster]
            new_id = coaster_id_map[new_coaster]
            
            cursor.execute('''
                UPDATE rollercoasters 
                SET replaced_by_id = ? 
                WHERE rollercoaster_id = ?
            ''', (new_id, old_id))

    conn.commit()
    conn.close()
    print("Hersheypark data successfully added.")

def populate_universal_orlando():
    conn = sqlite3.connect('database_new.db')
    cursor = conn.cursor()
    current_year = datetime.now().year

    # 1. Insert Manufacturers
    mfg_data = [
        ('Bolliger & Mabillard', 1988),
        ('Intamin', 1967),
        ('Mack Rides', 1780),
        ('Premier Rides', 1994),
        ('Vekoma', 1926),
        ('Maurer Rides', 1993),
        ('Setpoint', 1992),
        ('Universal Creative', 1997)
    ]
    
    mfg_map = {}
    for name, year in mfg_data:
        cursor.execute("SELECT manufacturer_id FROM manufacturers WHERE name = ?", (name,))
        result = cursor.fetchone()
        if result:
            mfg_map[name] = result[0]
        else:
            cursor.execute("INSERT INTO manufacturers (name, year_founded) VALUES (?, ?)", (name, year))
            mfg_map[name] = cursor.lastrowid

    # 2. Insert The Three Parks
    cursor.execute('''
        INSERT INTO parks (name, owned_by, year_opened, visitors_per_year, visitors_per_day, location)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', ("Universal Studios Florida", "NBCUniversal", 1990, 9700000, 26500, "Orlando, Florida"))
    usf_id = cursor.lastrowid

    cursor.execute('''
        INSERT INTO parks (name, owned_by, year_opened, visitors_per_year, visitors_per_day, location)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', ("Universal's Islands of Adventure", "NBCUniversal", 1999, 11000000, 30100, "Orlando, Florida"))
    ioa_id = cursor.lastrowid

    cursor.execute('''
        INSERT INTO parks (name, owned_by, year_opened, visitors_per_year, visitors_per_day, location)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', ("Universal Epic Universe", "NBCUniversal", 2025, 8000000, 21900, "Orlando, Florida"))
    epic_id = cursor.lastrowid

    # 3. Universal Coaster Data (Split by park to maintain the 21-item format)
    
    usf_coasters = [
        # --- OPERATING ---
        ('Revenge of the Mummy', 'Steel', 'Enclosed LIM Launch', 'Premier Rides', 44, 45, 2200, 2004, None, 1, 0, 0, 2000, 'high', 0, '45 mins', 48, '2:57', 'LIM Launch', 40000000, None),
        ('Harry Potter and the Escape from Gringotts', 'Steel', 'Enclosed Launch', 'Intamin', 100, 24, 2000, 2014, None, 1, 0, 0, 2500, 'medium', 0, '60 mins', 42, '4:30', 'Tilt/Launch', 400000000, None),
        ('Trolls Trollercoaster', 'Steel', 'Junior Coaster', 'Vekoma', 28, 21, 679, 2024, None, 1, 0, 0, 750, 'kiddie', 0, '20 mins', 36, '1:00', 'Lift', None, None),
        
        # --- REMOVED ---
        ('Hollywood Rip Ride Rockit', 'Steel', 'X-Car', 'Maurer Rides', 167, 65, 3800, 2009, 2025, 0, 0, 1, 1850, 'high', 0, None, 51, '1:37', 'Vertical Lift', 33000000, None),
        ("Woody Woodpecker's Nighthawk Coaster", 'Steel', 'Junior Coaster', 'Vekoma', 28, 21, 679, 1999, 2023, 0, 0, 1, 750, 'kiddie', 0, None, 36, '1:00', 'Lift', None, None)
    ]

    ioa_coasters = [
        # --- OPERATING ---
        ('Jurassic World VelociCoaster', 'Steel', 'LSM Launch Coaster', 'Intamin', 155, 70, 4700, 2021, None, 1, 0, 0, 1800, 'high', 4, '60 mins', 51, '2:00', 'LSM Launch', None, 80),
        ("Hagrid's Magical Creatures Motorbike Adventure", 'Steel', 'Motorbike Coaster', 'Intamin', 65, 50, 5053, 2019, None, 1, 0, 0, 2000, 'high', 0, '90 mins', 48, '3:00', 'LSM Launch', 300000000, None),
        ('The Incredible Hulk Coaster', 'Steel', 'Sitting Coaster', 'Bolliger & Mabillard', 110, 67, 3670, 1999, None, 1, 0, 0, 1926, 'high', 7, '45 mins', 54, '2:15', 'Tire Propelled Launch', None, None),
        ('Flight of the Hippogriff', 'Steel', 'Junior Coaster', 'Vekoma', 42, 28, 1099, 2000, None, 1, 0, 0, 800, 'medium', 0, '30 mins', 36, '1:05', 'Lift', None, None),
        ('Pteranodon Flyers', 'Steel', 'Suspended Family Coaster', 'Setpoint', 15, 20, 800, 1999, None, 1, 0, 0, 300, 'kiddie', 0, '60 mins', 36, '1:15', 'Lift', None, None),
        
        # --- REMOVED ---
        ('Dragon Challenge', 'Steel', 'Inverted Coaster', 'Bolliger & Mabillard', 125, 60, 3200, 1999, 2017, 0, 0, 1, 2000, 'high', 5, None, 54, '2:25', 'Lift', None, None)
    ]

    epic_coasters = [
        # --- OPERATING ---
        ('Stardust Racers', 'Steel', 'Dual Launch Coaster', 'Mack Rides', 133, 62, 5000, 2025, None, 1, 0, 0, 2000, 'high', 1, '90 mins', 48, '2:00', 'LSM Launch', None, None),
        ('Curse of the Werewolf', 'Steel', 'Spinning Coaster', 'Mack Rides', 65, 37, 2000, 2025, None, 1, 0, 0, 1000, 'medium', 0, '60 mins', 40, '1:45', 'LSM Launch', None, None),
        ('Mine-Cart Madness', 'Steel', 'Boom Coaster', 'Universal Creative', 50, 40, 2500, 2025, None, 1, 0, 0, 1500, 'medium', 0, '90 mins', 36, '2:00', 'Lift', None, None),
        ("How to Train Your Dragon - Hiccup's Wing Gliders", 'Steel', 'Family Launch Coaster', 'Intamin', 65, 45, 2800, 2025, None, 1, 0, 0, 1200, 'medium', 0, '60 mins', 40, '1:30', 'LSM Launch', None, None)
    ]

    coaster_id_map = {}

    # Helper function to insert coasters for a specific park
    def insert_park_coasters(coaster_list, park_db_id):
        for c in coaster_list:
            (name, c_type, model, mfg_name, h, s, l, yr_open, yr_closed, active, sbno, rem, 
             rph, thrill, inv, wait, restrict, dur, lift, cost, drop) = c
            
            age = current_year - yr_open
            
            cursor.execute('''
                INSERT INTO rollercoasters (
                    name, type, model, manufacturer_id, height, speed, length, 
                    year_opened, year_closed, currently_operating, SBNO, removed, park_id, 
                    riders_per_hour, thrill_level, inversions, avg_wait_time, 
                    height_restriction, ride_duration, lift_or_launch, cost, 
                    drop_angle_in_degrees, age
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                name, c_type, model, mfg_map[mfg_name], h, s, l, 
                yr_open, yr_closed, active, sbno, rem, park_db_id, 
                rph, thrill, inv, wait, restrict, dur, lift, cost, drop, age
            ))
            
            coaster_id_map[name] = cursor.lastrowid

    # Execute insertions for all three parks
    insert_park_coasters(usf_coasters, usf_id)
    insert_park_coasters(ioa_coasters, ioa_id)
    insert_park_coasters(epic_coasters, epic_id)

    # 4. Map Replacements
    replacements = {
        "Dragon Challenge": "Hagrid's Magical Creatures Motorbike Adventure",
        "Woody Woodpecker's Nighthawk Coaster": "Trolls Trollercoaster"
    }

    # 5. Update the replaced_by_id foreign key
    for old_coaster, new_coaster in replacements.items():
        if old_coaster in coaster_id_map and new_coaster in coaster_id_map:
            old_id = coaster_id_map[old_coaster]
            new_id = coaster_id_map[new_coaster]
            
            cursor.execute('''
                UPDATE rollercoasters 
                SET replaced_by_id = ? 
                WHERE rollercoaster_id = ?
            ''', (new_id, old_id))

    conn.commit()
    conn.close()
    print("Universal Orlando Resort data successfully added.")

def populate_kings_island():
    conn = sqlite3.connect('database_new.db')
    cursor = conn.cursor()
    current_year = datetime.now().year

    # 1. Insert Manufacturers (Safe check logic)
    mfg_data = [
        ('Bolliger & Mabillard', 1988),
        ('Philadelphia Toboggan Coasters', 1904),
        ('Great Coasters International', 1994),
        ('Premier Rides', 1994),
        ('Arrow Dynamics', 1946),
        ('Vekoma', 1926),
        ('Roller Coaster Corporation of America', 1993),
        ('Togo', 1935)
    ]
    
    mfg_map = {}
    for name, year in mfg_data:
        cursor.execute("SELECT manufacturer_id FROM manufacturers WHERE name = ?", (name,))
        result = cursor.fetchone()
        if result:
            mfg_map[name] = result[0]
        else:
            cursor.execute("INSERT INTO manufacturers (name, year_founded) VALUES (?, ?)", (name, year))
            mfg_map[name] = cursor.lastrowid

    # 2. Insert Kings Island
    # Note: Owned by Six Flags Entertainment Corporation post-2024 Cedar Fair merger
    cursor.execute('''
        INSERT INTO parks (name, owned_by, year_opened, visitors_per_year, visitors_per_day, location)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', ("Kings Island", "Six Flags Entertainment Corporation", 1972, 3500000, 24000, "Mason, Ohio"))
    ki_id = cursor.lastrowid

    # 3. Kings Island Coaster Data
    # Format: name, type, model, mfg, h, s, l, yr_open, yr_closed, active, sbno, rem, rph, thrill, inv, wait, restrict, dur, lift_launch, cost, drop_angle
    coasters = [
        # --- OPERATING COASTERS ---
        ('Orion', 'Steel', 'Giga Coaster', 'Bolliger & Mabillard', 287, 91, 5321, 2020, None, 1, 0, 0, 1650, 'high', 0, '60 mins', 54, '3:00', 'Lift', 30000000, 85),
        ('Diamondback', 'Steel', 'Hyper Coaster', 'Bolliger & Mabillard', 230, 80, 5282, 2009, None, 1, 0, 0, 1620, 'high', 0, '45 mins', 54, '3:00', 'Lift', 22000000, 74),
        ('Banshee', 'Steel', 'Inverted Coaster', 'Bolliger & Mabillard', 167, 68, 4124, 2014, None, 1, 0, 0, 1650, 'high', 7, '45 mins', 52, '2:40', 'Lift', 24000000, None),
        ('The Beast', 'Wood', 'Wooden Coaster', 'Philadelphia Toboggan Coasters', 110, 65, 7361, 1979, None, 1, 0, 0, 1200, 'high', 0, '45 mins', 48, '4:10', 'Lift', 3200000, 45),
        ('Mystic Timbers', 'Wood', 'Wooden Coaster', 'Great Coasters International', 109, 53, 3265, 2017, None, 1, 0, 0, 1200, 'high', 0, '45 mins', 48, '2:00', 'Lift', 15000000, 54),
        ('Flight of Fear', 'Steel', 'Enclosed LIM Launch', 'Premier Rides', 74, 54, 2705, 1996, None, 1, 0, 0, 2000, 'high', 4, '60 mins', 54, '1:00', 'LIM Launch', None, None),
        ('The Racer', 'Wood', 'Racing Coaster', 'Philadelphia Toboggan Coasters', 88, 53, 3415, 1972, None, 1, 0, 0, 2640, 'medium', 0, '15 mins', 48, '2:00', 'Lift', 1200000, None),
        ('The Bat', 'Steel', 'Suspended Coaster', 'Arrow Dynamics', 78, 51, 2352, 1993, None, 1, 0, 0, 1000, 'medium', 0, '30 mins', 48, '1:52', 'Lift', None, None),
        ('Backlot Stunt Coaster', 'Steel', 'LIM Launch', 'Premier Rides', 39, 40, 1960, 2005, None, 1, 0, 0, 800, 'medium', 0, '30 mins', 48, '1:04', 'LIM Launch', None, None),
        ('Invertigo', 'Steel', 'Inverted Boomerang', 'Vekoma', 131, 50, 1013, 1999, None, 1, 0, 0, 850, 'high', 6, '30 mins', 54, '1:30', 'Lift', None, None),
        ('Adventure Express', 'Steel', 'Mine Train', 'Arrow Dynamics', 63, 35, 2963, 1991, None, 1, 0, 0, 1000, 'medium', 0, '15 mins', 48, '2:53', 'Lift', 1000000, None),
        ("Snoopy's Soap Box Racers", 'Steel', 'Family Boomerang', 'Vekoma', 74, 36, 826, 2024, None, 1, 0, 0, 600, 'medium', 0, '30 mins', 38, '1:15', 'Lift', None, None),

        # --- REMOVED / REPLACED COASTERS ---
        ('Son of Beast', 'Wood', 'Wooden Coaster', 'Roller Coaster Corporation of America', 218, 78, 7032, 2000, 2009, 0, 0, 1, 1600, 'high', 1, None, 48, '2:20', 'Lift', 20500000, 55),
        ('Firehawk', 'Steel', 'Flying Coaster', 'Vekoma', 115, 50, 3340, 2007, 2018, 0, 0, 1, 1430, 'high', 5, None, 54, '2:30', 'Lift', None, None),
        ('Vortex', 'Steel', 'Custom Looping Coaster', 'Arrow Dynamics', 148, 55, 3800, 1987, 2019, 0, 0, 1, 1600, 'high', 6, None, 48, '2:30', 'Lift', 4000000, 55),
        ('King Cobra', 'Steel', 'Stand-Up Coaster', 'Togo', 95, 50, 2210, 1984, 2001, 0, 0, 1, 1000, 'high', 1, None, 54, '2:00', 'Lift', 3000000, None)
    ]

    coaster_id_map = {}

    for c in coasters:
        (name, c_type, model, mfg_name, h, s, l, yr_open, yr_closed, active, sbno, rem, 
         rph, thrill, inv, wait, restrict, dur, lift, cost, drop) = c
        
        age = current_year - yr_open
        
        cursor.execute('''
            INSERT INTO rollercoasters (
                name, type, model, manufacturer_id, height, speed, length, 
                year_opened, year_closed, currently_operating, SBNO, removed, park_id, 
                riders_per_hour, thrill_level, inversions, avg_wait_time, 
                height_restriction, ride_duration, lift_or_launch, cost, 
                drop_angle_in_degrees, age
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            name, c_type, model, mfg_map[mfg_name], h, s, l, 
            yr_open, yr_closed, active, sbno, rem, ki_id, 
            rph, thrill, inv, wait, restrict, dur, lift, cost, drop, age
        ))
        
        coaster_id_map[name] = cursor.lastrowid

    # 4. Map Replacements
    replacements = {
        "Son of Beast": "Banshee",
        "Firehawk": "Orion"
    }

    # 5. Update the replaced_by_id foreign key
    for old_coaster, new_coaster in replacements.items():
        if old_coaster in coaster_id_map and new_coaster in coaster_id_map:
            old_id = coaster_id_map[old_coaster]
            new_id = coaster_id_map[new_coaster]
            
            cursor.execute('''
                UPDATE rollercoasters 
                SET replaced_by_id = ? 
                WHERE rollercoaster_id = ?
            ''', (new_id, old_id))

    conn.commit()
    conn.close()
    print("Kings Island data successfully added.")

def populate_dollywood():
    conn = sqlite3.connect('database_new.db')
    cursor = conn.cursor()
    current_year = datetime.now().year

    # 1. Insert Manufacturers (Safe check logic)
    mfg_data = [
        ('Rocky Mountain Construction', 2001),
        ('Bolliger & Mabillard', 1988),
        ('Great Coasters International', 1994),
        ('Gerstlauer', 1982),
        ('Arrow Dynamics', 1946),
        ('Mack Rides', 1780),
        ('Vekoma', 1926),
        ('Zamperla', 1966),
        ('In-House', 1986) # For Blazing Fury
    ]
    
    mfg_map = {}
    for name, year in mfg_data:
        cursor.execute("SELECT manufacturer_id FROM manufacturers WHERE name = ?", (name,))
        result = cursor.fetchone()
        if result:
            mfg_map[name] = result[0]
        else:
            cursor.execute("INSERT INTO manufacturers (name, year_founded) VALUES (?, ?)", (name, year))
            mfg_map[name] = cursor.lastrowid

    # 2. Insert Dollywood
    cursor.execute('''
        INSERT INTO parks (name, owned_by, year_opened, visitors_per_year, visitors_per_day, location)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', ("Dollywood", "Herschend Family Entertainment", 1986, 3000000, 12000, "Pigeon Forge, Tennessee"))
    dw_id = cursor.lastrowid

    # 3. Dollywood Coaster Data
    # Format: name, type, model, mfg, h, s, l, yr_open, yr_closed, active, sbno, rem, rph, thrill, inv, wait, restriction, duration, lift_launch, cost, drop_angle
    coasters = [
        # --- OPERATING COASTERS ---
        ('Lightning Rod', 'Steel', 'IBox Track', 'Rocky Mountain Construction', 165, 73, 3800, 2016, None, 1, 0, 0, 1000, 'high', 0, '60 mins', 48, '3:12', 'High-Speed Chain Lift', 22000000, 73),
        ('Wild Eagle', 'Steel', 'Wing Coaster', 'Bolliger & Mabillard', 210, 61, 3127, 2012, None, 1, 0, 0, 1400, 'high', 4, '30 mins', 50, '2:22', 'Lift', 20000000, None),
        ('Thunderhead', 'Wood', 'Wooden Coaster', 'Great Coasters International', 100, 53, 3230, 2004, None, 1, 0, 0, 1000, 'high', 0, '30 mins', 48, '2:30', 'Lift', 7000000, None),
        ('Big Bear Mountain', 'Steel', 'Multi-Launch Family Coaster', 'Mack Rides', 66, 48, 3990, 2023, None, 1, 0, 0, 1200, 'medium', 0, '60 mins', 39, '2:00', 'LSM Launch', 25000000, None),
        ('Mystery Mine', 'Steel', 'Euro-Fighter', 'Gerstlauer', 85, 46, 1811, 2007, None, 1, 0, 0, 1000, 'high', 2, '45 mins', 48, '2:30', 'Vertical Lift', 17500000, 95),
        ('Tennessee Tornado', 'Steel', 'Custom Looping Coaster', 'Arrow Dynamics', 163, 63, 2682, 1999, None, 1, 0, 0, 1300, 'high', 3, '20 mins', 48, '1:48', 'Lift', None, None),
        ('FireChaser Express', 'Steel', 'Family Launch Coaster', 'Gerstlauer', 79, 34, 2427, 2014, None, 1, 0, 0, 1000, 'medium', 0, '45 mins', 39, '2:19', 'Tire Propelled Launch', 15000000, None),
        ('Dragonflier', 'Steel', 'Suspended Family Coaster', 'Vekoma', 63, 46, 1486, 2019, None, 1, 0, 0, 800, 'medium', 0, '30 mins', 39, '1:00', 'Lift', None, None),
        ('Blazing Fury', 'Steel', 'Enclosed Coaster / Dark Ride', 'In-House', 0, 18, 0, 1986, None, 1, 0, 0, 1000, 'medium', 0, '30 mins', 42, '3:00', 'Lift', None, None),
        ('Whistle Punk Chaser', 'Steel', 'Junior Coaster', 'Zamperla', 13, 15, 426, 2017, None, 1, 0, 0, 400, 'kiddie', 0, '15 mins', 36, '1:00', 'Lift', None, None),

        # --- REMOVED / REPLACED COASTERS ---
        ('Thunder Express', 'Steel', 'Mine Train', 'Arrow Dynamics', 0, 0, 0, 1989, 1998, 0, 0, 1, 1000, 'medium', 0, None, 42, '2:00', 'Lift', None, None)
    ]

    coaster_id_map = {}

    for c in coasters:
        (name, c_type, model, mfg_name, h, s, l, yr_open, yr_closed, active, sbno, rem, 
         rph, thrill, inv, wait, restrict, dur, lift, cost, drop) = c
        
        age = current_year - yr_open
        
        cursor.execute('''
            INSERT INTO rollercoasters (
                name, type, model, manufacturer_id, height, speed, length, 
                year_opened, year_closed, currently_operating, SBNO, removed, park_id, 
                riders_per_hour, thrill_level, inversions, avg_wait_time, 
                height_restriction, ride_duration, lift_or_launch, cost, 
                drop_angle_in_degrees, age
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            name, c_type, model, mfg_map[mfg_name], h, s, l, 
            yr_open, yr_closed, active, sbno, rem, dw_id, 
            rph, thrill, inv, wait, restrict, dur, lift, cost, drop, age
        ))
        
        coaster_id_map[name] = cursor.lastrowid

    # 4. Map Replacements
    replacements = {
        "Thunder Express": "Tennessee Tornado"
    }

    # 5. Update the replaced_by_id foreign key
    for old_coaster, new_coaster in replacements.items():
        if old_coaster in coaster_id_map and new_coaster in coaster_id_map:
            old_id = coaster_id_map[old_coaster]
            new_id = coaster_id_map[new_coaster]
            
            cursor.execute('''
                UPDATE rollercoasters 
                SET replaced_by_id = ? 
                WHERE rollercoaster_id = ?
            ''', (new_id, old_id))

    conn.commit()
    conn.close()
    print("Dollywood data successfully added.")

def populate_silver_dollar_city():
    conn = sqlite3.connect('database_new.db')
    cursor = conn.cursor()
    current_year = datetime.now().year

    # 1. Insert Manufacturers
    mfg_data = [
        ('Mack Rides', 1780),
        ('Rocky Mountain Construction', 2001),
        ('Bolliger & Mabillard', 1988),
        ('S&S Worldwide', 1994),
        ('Arrow Dynamics', 1946),
        ('Zamperla', 1966),
        ('Premier Rides', 1994),
        ('In-House', 1960)
    ]
    
    mfg_map = {}
    for name, year in mfg_data:
        cursor.execute("SELECT manufacturer_id FROM manufacturers WHERE name = ?", (name,))
        result = cursor.fetchone()
        if result:
            mfg_map[name] = result[0]
        else:
            cursor.execute("INSERT INTO manufacturers (name, year_founded) VALUES (?, ?)", (name, year))
            mfg_map[name] = cursor.lastrowid

    # 2. Insert Silver Dollar City
    cursor.execute('''
        INSERT INTO parks (name, owned_by, year_opened, visitors_per_year, visitors_per_day, location)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', ("Silver Dollar City", "Herschend Family Entertainment", 1960, 2200000, 11000, "Branson, Missouri"))
    sdc_id = cursor.lastrowid

    # 3. Silver Dollar City Coaster Data
    # Format: name, type, model, mfg, h, s, l, yr_open, yr_closed, active, sbno, rem, rph, thrill, inv, wait, restrict, dur, lift_launch, cost, drop_angle
    coasters = [
        # --- OPERATING COASTERS ---
        ('Time Traveler', 'Steel', 'Xtreme Spinning Coaster', 'Mack Rides', 100, 50.3, 3020, 2018, None, 1, 0, 0, 1000, 'high', 3, '45 mins', 51, '1:57', 'LSM Launch', 26000000, 90),
        ('Outlaw Run', 'Wood', 'Topper Track Coaster', 'Rocky Mountain Construction', 107, 68, 2937, 2013, None, 1, 0, 0, 900, 'high', 3, '45 mins', 48, '1:27', 'Lift', 10000000, 81),
        ('Wildfire', 'Steel', 'Sitting Coaster', 'Bolliger & Mabillard', 120, 66, 3073, 2001, None, 1, 0, 0, 1300, 'high', 5, '30 mins', 52, '2:16', 'Lift', 14000000, None),
        ('Powder Keg', 'Steel', 'Air Launched Coaster', 'S&S Worldwide', 98, 64, 3506, 2005, None, 1, 0, 0, 1000, 'high', 0, '60 mins', 42, '2:53', 'Compressed Air Launch', 10000000, None),
        ('Thunderation', 'Steel', 'Mine Train', 'Arrow Dynamics', 121, 48, 3018, 1993, None, 1, 0, 0, 1800, 'medium', 0, '20 mins', 42, '2:10', 'Lift', None, None),
        ('Fire in the Hole', 'Steel', 'Indoor Family Coaster', 'Rocky Mountain Construction', 50, 20, 1512, 2024, None, 1, 0, 0, 1200, 'medium', 0, '45 mins', 36, '2:50', 'Powered Incline', 30000000, None),
        ('Grand Exposition Coaster', 'Steel', 'Family Gravity Coaster', 'Zamperla', 13, 15, 295, 2006, None, 1, 0, 0, 400, 'kiddie', 0, '15 mins', 36, '1:00', 'Lift', None, None),

        # --- REMOVED / REPLACED COASTERS ---
        ('Fire in the Hole (Original)', 'Wood', 'Indoor Powered Coaster', 'In-House', 0, 0, 1520, 1972, 2023, 0, 0, 1, 1000, 'medium', 0, None, 36, '2:45', 'Powered Incline', None, None),
        ('BuzzSaw Falls', 'Steel', 'Liquid Coaster', 'Premier Rides', 120, 50, 3000, 1999, 2003, 0, 0, 1, 800, 'high', 0, None, 42, '2:00', 'Lift', 5000000, None)
    ]

    coaster_id_map = {}

    for c in coasters:
        (name, c_type, model, mfg_name, h, s, l, yr_open, yr_closed, active, sbno, rem, 
         rph, thrill, inv, wait, restrict, dur, lift, cost, drop) = c
        
        age = current_year - yr_open
        
        cursor.execute('''
            INSERT INTO rollercoasters (
                name, type, model, manufacturer_id, height, speed, length, 
                year_opened, year_closed, currently_operating, SBNO, removed, park_id, 
                riders_per_hour, thrill_level, inversions, avg_wait_time, 
                height_restriction, ride_duration, lift_or_launch, cost, 
                drop_angle_in_degrees, age
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            name, c_type, model, mfg_map[mfg_name], h, s, l, 
            yr_open, yr_closed, active, sbno, rem, sdc_id, 
            rph, thrill, inv, wait, restrict, dur, lift, cost, drop, age
        ))
        
        coaster_id_map[name] = cursor.lastrowid

    # 4. Map Replacements
    replacements = {
        "Fire in the Hole (Original)": "Fire in the Hole",
        "BuzzSaw Falls": "Powder Keg"
    }

    # 5. Update the replaced_by_id foreign key
    for old_coaster, new_coaster in replacements.items():
        if old_coaster in coaster_id_map and new_coaster in coaster_id_map:
            old_id = coaster_id_map[old_coaster]
            new_id = coaster_id_map[new_coaster]
            
            cursor.execute('''
                UPDATE rollercoasters 
                SET replaced_by_id = ? 
                WHERE rollercoaster_id = ?
            ''', (new_id, old_id))

    conn.commit()
    conn.close()
    print("Silver Dollar City data successfully added.")

def populate_sfot():
    conn = sqlite3.connect('database_new.db')
    cursor = conn.cursor()
    current_year = datetime.now().year

    # 1. Insert Manufacturers (Updated "Unknown" year to 0 to pass NOT NULL constraint)
    mfg_data = [
        ('Rocky Mountain Construction', 2001),
        ('Dinn Corporation', 1983),
        ('Giovanola', 1998),
        ('Premier Rides', 1994),
        ('Bolliger & Mabillard', 1988),
        ('Schwarzkopf', 1932),
        ('Arrow Dynamics', 1946),
        ('Mack Rides', 1780),
        ('S&S Worldwide', 1994),
        ('Gerstlauer', 1982),
        ('Zamperla', 1966),
        ('Unknown', 0)
    ]
    
    mfg_map = {}
    for name, year in mfg_data:
        cursor.execute("SELECT manufacturer_id FROM manufacturers WHERE name = ?", (name,))
        result = cursor.fetchone()
        if result:
            mfg_map[name] = result[0]
        else:
            cursor.execute("INSERT INTO manufacturers (name, year_founded) VALUES (?, ?)", (name, year))
            mfg_map[name] = cursor.lastrowid

    # 2. Insert Six Flags Over Texas
    cursor.execute('''
        INSERT INTO parks (name, owned_by, year_opened, visitors_per_year, visitors_per_day, location)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', ("Six Flags Over Texas", "Six Flags Entertainment Corporation", 1961, 3000000, 15000, "Arlington, Texas"))
    sfot_id = cursor.lastrowid

    # 3. SFOT Coaster Data
    coasters = [
        # --- OPERATING COASTERS ---
        ('New Texas Giant', 'Steel', 'IBox Track', 'Rocky Mountain Construction', 153, 65, 4200, 2011, None, 1, 0, 0, 1000, 'high', 0, '60 mins', 48, '2:00', 'Lift', 10000000, 79),
        ('Titan', 'Steel', 'Mega Coaster', 'Giovanola', 245, 85, 5312, 2001, None, 1, 0, 0, 1200, 'high', 0, '45 mins', 48, '3:30', 'Lift', 25000000, 65),
        ('Mr. Freeze', 'Steel', 'LIM Shuttle Loop', 'Premier Rides', 218, 70, 1300, 1998, None, 1, 0, 0, 1000, 'high', 1, '45 mins', 54, '1:30', 'LIM Launch', 12000000, 90),
        ('BATMAN The Ride', 'Steel', 'Inverted Coaster', 'Bolliger & Mabillard', 105, 50, 2693, 1999, None, 1, 0, 0, 1200, 'high', 5, '30 mins', 54, '2:00', 'Lift', None, None),
        ('Shock Wave', 'Steel', 'Custom Looping Coaster', 'Schwarzkopf', 116, 60, 3500, 1978, None, 1, 0, 0, 1000, 'high', 2, '30 mins', 42, '2:00', 'Lift', None, None),
        ('AQUAMAN: Power Wave', 'Steel', 'PowerSplash', 'Mack Rides', 148, 62, 708, 2023, None, 1, 0, 0, 700, 'high', 0, '45 mins', 48, '1:10', 'LSM Launch', None, 90),
        ('Runaway Mine Train', 'Steel', 'Mine Train', 'Arrow Dynamics', 35, 36, 2484, 1966, None, 1, 0, 0, 1200, 'medium', 0, '20 mins', 42, '2:30', 'Lift', None, None),
        ('Runaway Mountain', 'Steel', 'Enclosed Coaster', 'Premier Rides', 65, 40, 1400, 1996, None, 1, 0, 0, 900, 'medium', 0, '30 mins', 48, '1:30', 'Lift', None, None),
        ('The Joker', 'Steel', '4D Free Spin', 'S&S Worldwide', 120, 38, 1019, 2017, None, 1, 0, 0, 600, 'high', 6, '45 mins', 48, '1:00', 'Vertical Lift', None, 90),
        ('Pandemonium', 'Steel', 'Spinning Coaster', 'Gerstlauer', 43, 31, 1351, 2008, None, 1, 0, 0, 800, 'medium', 0, '30 mins', 42, '1:51', 'Lift', None, None),

        # --- REMOVED / REPLACED COASTERS ---
        ('Texas Giant (Original)', 'Wood', 'Wooden Coaster', 'Dinn Corporation', 143, 62, 4920, 1990, 2009, 0, 0, 1, 1200, 'high', 0, None, 48, '2:30', 'Lift', 5500000, 53)
    ]

    coaster_id_map = {}

    for c in coasters:
        (name, c_type, model, mfg_name, h, s, l, yr_open, yr_closed, active, sbno, rem, 
         rph, thrill, inv, wait, restrict, dur, lift, cost, drop) = c
        
        age = current_year - yr_open
        
        cursor.execute('''
            INSERT INTO rollercoasters (
                name, type, model, manufacturer_id, height, speed, length, 
                year_opened, year_closed, currently_operating, SBNO, removed, park_id, 
                riders_per_hour, thrill_level, inversions, avg_wait_time, 
                height_restriction, ride_duration, lift_or_launch, cost, 
                drop_angle_in_degrees, age
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            name, c_type, model, mfg_map[mfg_name], h, s, l, 
            yr_open, yr_closed, active, sbno, rem, sfot_id, 
            rph, thrill, inv, wait, restrict, dur, lift, cost, drop, age
        ))
        
        coaster_id_map[name] = cursor.lastrowid

    # 4. Map Replacements
    replacements = {
        "Texas Giant (Original)": "New Texas Giant"
    }

    # 5. Update the replaced_by_id foreign key
    for old_coaster, new_coaster in replacements.items():
        if old_coaster in coaster_id_map and new_coaster in coaster_id_map:
            old_id = coaster_id_map[old_coaster]
            new_id = coaster_id_map[new_coaster]
            
            cursor.execute('''
                UPDATE rollercoasters 
                SET replaced_by_id = ? 
                WHERE rollercoaster_id = ?
            ''', (new_id, old_id))

    conn.commit()
    conn.close()
    print("Six Flags Over Texas data successfully added.")

def populate_kings_dominion():
    conn = sqlite3.connect('database_new.db')
    cursor = conn.cursor()
    current_year = datetime.now().year

    # 1. Insert Manufacturers
    mfg_data = [
        ('Rocky Mountain Construction', 2001),
        ('Intamin', 1967),
        ('Bolliger & Mabillard', 1988),
        ('Premier Rides', 1994),
        ('Arrow Dynamics', 1946),
        ('S&S Worldwide', 1994),
        ('Philadelphia Toboggan Coasters', 1904),
        ('Mack Rides', 1780),
        ('E&F Miler Industries', 1955),
        ('International Coasters Inc', 1993),
        ('In-House', 0)
    ]
    
    mfg_map = {}
    for name, year in mfg_data:
        cursor.execute("SELECT manufacturer_id FROM manufacturers WHERE name = ?", (name,))
        result = cursor.fetchone()
        if result:
            mfg_map[name] = result[0]
        else:
            cursor.execute("INSERT INTO manufacturers (name, year_founded) VALUES (?, ?)", (name, year))
            mfg_map[name] = cursor.lastrowid

    # 2. Insert Kings Dominion
    cursor.execute('''
        INSERT INTO parks (name, owned_by, year_opened, visitors_per_year, visitors_per_day, location)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', ("Kings Dominion", "Six Flags Entertainment Corporation", 1975, 2000000, 10000, "Doswell, Virginia"))
    kd_id = cursor.lastrowid

    # 3. Kings Dominion Coaster Data
    coasters = [
        # --- OPERATING COASTERS ---
        ('Rapterra', 'Steel', 'Wing Coaster', 'Bolliger & Mabillard', 145, 65, 3086, 2025, None, 1, 0, 0, 1200, 'high', 3, '60 mins', 52, '2:00', 'LSM Launch', None, 0),
        ('Pantherian', 'Steel', 'Giga Coaster', 'Intamin', 305, 90, 5100, 2010, None, 1, 0, 0, 1350, 'high', 0, '30 mins', 54, '3:00', 'Cable Lift', 25000000, 85),
        ('Twisted Timbers', 'Steel', 'IBox Track', 'Rocky Mountain Construction', 111, 54, 3361, 2018, None, 1, 0, 0, 1000, 'high', 3, '45 mins', 48, '2:00', 'Lift', None, 109),
        ('Dominator', 'Steel', 'Floorless Coaster', 'Bolliger & Mabillard', 157, 65, 4210, 2008, None, 1, 0, 0, 1350, 'high', 5, '45 mins', 54, '2:06', 'Lift', None, None),
        ('Flight of Fear', 'Steel', 'LIM Catapult', 'Premier Rides', 74, 54, 2705, 1996, None, 1, 0, 0, 1000, 'high', 4, '30 mins', 54, '1:30', 'LIM Launch', None, None),
        ('Racer 75', 'Wood', 'Racing Coaster', 'Philadelphia Toboggan Coasters', 85, 50, 3369, 1975, None, 1, 0, 0, 1600, 'medium', 0, '15 mins', 48, '2:15', 'Lift', None, None),
        ('Grizzly', 'Wood', 'Wooden Coaster', 'In-House', 97, 50, 3150, 1982, None, 1, 0, 0, 1000, 'medium', 0, '20 mins', 48, '2:30', 'Lift', None, None),
        ('Tumbili', 'Steel', '4D Free Spin', 'S&S Worldwide', 112, 34, 770, 2022, None, 1, 0, 0, 600, 'high', 5, '45 mins', 48, '0:55', 'Vertical Lift', None, 90),

        # --- REMOVED / REPLACED COASTERS ---
        ('Volcano, The Blast Coaster', 'Steel', 'Suspended LIM', 'Intamin', 155, 70, 2757, 1998, 2018, 0, 0, 1, 1000, 'high', 4, None, 54, '1:15', 'LIM Launch', 20000000, None),
        ('Hurler', 'Wood', 'Wooden Coaster', 'International Coasters Inc', 83, 50, 3157, 1994, 2015, 0, 0, 1, 1000, 'medium', 0, None, 48, '2:00', 'Lift', None, None),
        ('Anaconda', 'Steel', 'Custom Looping', 'Arrow Dynamics', 153, 50, 2700, 1991, 2024, 0, 0, 1, 1200, 'high', 4, None, 48, '2:10', 'Lift', None, None)
    ]

    coaster_id_map = {}

    for c in coasters:
        (name, c_type, model, mfg_name, h, s, l, yr_open, yr_closed, active, sbno, rem, 
         rph, thrill, inv, wait, restrict, dur, lift, cost, drop) = c
        
        age = current_year - yr_open
        
        cursor.execute('''
            INSERT INTO rollercoasters (
                name, type, model, manufacturer_id, height, speed, length, 
                year_opened, year_closed, currently_operating, SBNO, removed, park_id, 
                riders_per_hour, thrill_level, inversions, avg_wait_time, 
                height_restriction, ride_duration, lift_or_launch, cost, 
                drop_angle_in_degrees, age
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            name, c_type, model, mfg_map[mfg_name], h, s, l, 
            yr_open, yr_closed, active, sbno, rem, kd_id, 
            rph, thrill, inv, wait, restrict, dur, lift, cost, drop, age
        ))
        
        coaster_id_map[name] = cursor.lastrowid

    # 4. Map Replacements
    replacements = {
        "Volcano, The Blast Coaster": "Rapterra",
        "Hurler": "Twisted Timbers"
    }

    # 5. Update the replaced_by_id foreign key
    for old_coaster, new_coaster in replacements.items():
        if old_coaster in coaster_id_map and new_coaster in coaster_id_map:
            old_id = coaster_id_map[old_coaster]
            new_id = coaster_id_map[new_coaster]
            
            cursor.execute('''
                UPDATE rollercoasters 
                SET replaced_by_id = ? 
                WHERE rollercoaster_id = ?
            ''', (new_id, old_id))

    conn.commit()
    conn.close()
    print("Kings Dominion data successfully added.")

def populate_kennywood():
    conn = sqlite3.connect('database_new.db')
    cursor = conn.cursor()
    current_year = datetime.now().year

    # 1. Insert Manufacturers (Safe check logic, using 0 for unknown founding years)
    mfg_data = [
        ('D.H. Morgan Manufacturing', 1983),
        ('Arrow Dynamics', 1946),
        ('Premier Rides', 1994),
        ('S&S Worldwide', 1994),
        ('Philadelphia Toboggan Coasters', 1904),
        ('Reverchon', 1927),
        ('Schwarzkopf', 1932),
        ('John Miller', 0),
        ('Harry C. Baker', 0),
        ('Andy Vettel', 0)
    ]
    
    mfg_map = {}
    for name, year in mfg_data:
        cursor.execute("SELECT manufacturer_id FROM manufacturers WHERE name = ?", (name,))
        result = cursor.fetchone()
        if result:
            mfg_map[name] = result[0]
        else:
            cursor.execute("INSERT INTO manufacturers (name, year_founded) VALUES (?, ?)", (name, year))
            mfg_map[name] = cursor.lastrowid

    # 2. Insert Kennywood
    cursor.execute('''
        INSERT INTO parks (name, owned_by, year_opened, visitors_per_year, visitors_per_day, location)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', ("Kennywood", "Palace Entertainment", 1898, 1200000, 8000, "West Mifflin, Pennsylvania"))
    kw_id = cursor.lastrowid

    # 3. Kennywood Coaster Data
    # Format: name, type, model, mfg, h, s, l, yr_open, yr_closed, active, sbno, rem, rph, thrill, inv, wait, restriction, duration, lift_launch, cost, drop_angle
    coasters = [
        # --- OPERATING COASTERS ---
        ("Phantom's Revenge", 'Steel', 'Hypercoaster', 'D.H. Morgan Manufacturing', 160, 85, 3200, 2001, None, 1, 0, 0, 1400, 'high', 0, '45 mins', 48, '1:57', 'Lift', None, None),
        ('Steel Curtain', 'Steel', 'Custom Looping Coaster', 'S&S Worldwide', 220, 75, 4000, 2019, None, 1, 0, 0, 1000, 'high', 9, '60 mins', 48, '2:00', 'Lift', None, 90),
        ('Sky Rocket', 'Steel', 'LSM Launch Coaster', 'Premier Rides', 95, 50, 2100, 2010, None, 1, 0, 0, 600, 'high', 3, '30 mins', 46, '1:05', 'LSM Launch', 5700000, 90),
        ('Exterminator', 'Steel', 'Spinning Wild Mouse', 'Reverchon', 42, 29, 1377, 1999, None, 1, 0, 0, 900, 'medium', 0, '30 mins', 46, '1:45', 'Lift', None, None),
        ('Thunderbolt', 'Wood', 'Wooden Coaster', 'Andy Vettel', 70, 55, 2887, 1968, None, 1, 0, 0, 900, 'high', 0, '15 mins', 46, '1:48', 'Lift', None, None),
        ('Jack Rabbit', 'Wood', 'Wooden Coaster', 'Harry C. Baker', 40, 45, 2132, 1920, None, 1, 0, 0, 800, 'medium', 0, '15 mins', 36, '1:30', 'Lift', None, None),
        ('Racer', 'Wood', 'Racing Coaster', 'John Miller', 72, 40, 4500, 1927, None, 1, 0, 0, 1200, 'medium', 0, '15 mins', 46, '1:30', 'Lift', None, None),

        # --- REMOVED / REPLACED COASTERS ---
        ('Steel Phantom', 'Steel', 'Custom Looping Hypercoaster', 'Arrow Dynamics', 160, 80, 3000, 1991, 2000, 0, 0, 1, 1400, 'high', 4, None, 48, '2:15', 'Lift', 4000000, None),
        ('Laser Loop', 'Steel', 'Shuttle Loop', 'Schwarzkopf', 138, 53, 863, 1980, 1990, 0, 0, 1, 1000, 'high', 1, None, 48, '0:45', 'Flywheel Launch', None, None),
        ('Pippin', 'Wood', 'Wooden Coaster', 'John Miller', 70, 50, 2800, 1924, 1967, 0, 0, 1, 800, 'medium', 0, None, 46, '1:45', 'Lift', None, None)
    ]

    coaster_id_map = {}

    for c in coasters:
        (name, c_type, model, mfg_name, h, s, l, yr_open, yr_closed, active, sbno, rem, 
         rph, thrill, inv, wait, restrict, dur, lift, cost, drop) = c
        
        age = current_year - yr_open
        
        cursor.execute('''
            INSERT INTO rollercoasters (
                name, type, model, manufacturer_id, height, speed, length, 
                year_opened, year_closed, currently_operating, SBNO, removed, park_id, 
                riders_per_hour, thrill_level, inversions, avg_wait_time, 
                height_restriction, ride_duration, lift_or_launch, cost, 
                drop_angle_in_degrees, age
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            name, c_type, model, mfg_map[mfg_name], h, s, l, 
            yr_open, yr_closed, active, sbno, rem, kw_id, 
            rph, thrill, inv, wait, restrict, dur, lift, cost, drop, age
        ))
        
        coaster_id_map[name] = cursor.lastrowid

    # 4. Map Replacements (Including the 3-ride chain!)
    replacements = {
        "Pippin": "Thunderbolt",
        "Laser Loop": "Steel Phantom",
        "Steel Phantom": "Phantom's Revenge"
    }

    # 5. Update the replaced_by_id foreign key
    for old_coaster, new_coaster in replacements.items():
        if old_coaster in coaster_id_map and new_coaster in coaster_id_map:
            old_id = coaster_id_map[old_coaster]
            new_id = coaster_id_map[new_coaster]
            
            cursor.execute('''
                UPDATE rollercoasters 
                SET replaced_by_id = ? 
                WHERE rollercoaster_id = ?
            ''', (new_id, old_id))

    conn.commit()
    conn.close()
    print("Kennywood data successfully added.")


    print("\nAll 20 parks have been successfully populated!")

if __name__ == "__main__":
    populate_lagoon_refined()
    populate_cedar_point()
    populate_magic_mountain()
    populate_busch_gardens_tampa()
    populate_busch_gardens_williamsburg()
    populate_seaworld_orlando()
    populate_seaworld_san_diego()
    populate_great_adventure()
    populate_fiesta_texas()
    populate_knotts_berry_farm()
    populate_hersheypark()
    populate_universal_orlando()
    populate_kings_island()
    populate_dollywood()
    populate_silver_dollar_city()
    populate_sfot()
    populate_kings_dominion()
    populate_kennywood()
    print("\nAll parks have been successfully populated!")
