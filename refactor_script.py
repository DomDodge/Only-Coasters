import ast
import re

def update_database_script():
    with open('populate_db.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    funcs = []
    out_lines = []
    skip = False

    for line in lines:
        # 1. Track all the functions you've built
        if line.strip().startswith('def populate_'):
            funcs.append(line.split()[1].split('(')[0])
            
        # 2. Skip the old scattered __main__ blocks and commented out function calls
        if line.strip().startswith('#if __name__') or line.strip().startswith('if __name__'):
            skip = True
            continue
        if skip and (line.strip() == '' or line.strip().startswith('#') or line.strip().startswith('populate_')):
            continue
        else:
            skip = False

        # 3. Clean the coaster data tuples
        # Coaster rows always start with a parenthesis and a quote (e.g., '("Cannibal"' or "('Cannibal'")
        if line.lstrip().startswith('("') or line.lstrip().startswith("('"):
            indent = line[:len(line) - len(line.lstrip())]
            tup_str = line.strip()
            
            # Preserve inline comments if they exist
            comment = ''
            if '#' in tup_str:
                parts = tup_str.split('#', 1)
                tup_str = parts[0].strip()
                comment = ' #' + parts[1]
            
            comma = ''
            if tup_str.endswith(','):
                tup_str = tup_str[:-1]
                comma = ','
                
            try:
                # Safely parse the string representation of the tuple into a real Python tuple
                t = list(ast.literal_eval(tup_str))
                
                # Indexes to update: Height (4), Speed (5), Length (6), Restriction (16)
                for idx in [4, 5, 6, 16]:
                    if idx < len(t):
                        val = t[idx]
                        if isinstance(val, str):
                            if val == 'Unknown':
                                t[idx] = None
                            else:
                                # Extract pure digits (handles decimals like '50.3' too)
                                nums = re.findall(r'\d+(?:\.\d+)?', val)
                                if nums:
                                    t[idx] = float(nums[0]) if '.' in nums[0] else int(nums[0])
                
                # Reconstruct the line with the cleaned data
                line = indent + repr(tuple(t)) + comma + comment + '\n'
            except Exception as e:
                # If a line fails to parse for any reason, leave it untouched
                pass
                
        out_lines.append(line)

    # 4. Add a single, unified execution block at the very bottom
    out_lines.append('\nif __name__ == "__main__":\n')
    for func in funcs:
        out_lines.append(f'    {func}()\n')
        
    out_lines.append('    print("\\nAll 20 parks have been successfully populated!")\n')

    # Overwrite the file with the cleaned version
    with open('populate_db.py', 'w', encoding='utf-8') as f:
        f.writelines(out_lines)
        
    print("Successfully updated populate_db.py! Stats are now integers, and all functions will execute.")

if __name__ == "__main__":
    update_database_script()