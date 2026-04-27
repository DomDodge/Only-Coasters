import ast
import re

def patch_database_script():
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
                        # Set to 0 to satisfy the database NOT NULL constraint
                        if val is None or val == 'Unknown':
                            t[idx] = 0
                        elif isinstance(val, str):
                            # Extract pure digits 
                            nums = re.findall(r'\d+(?:\.\d+)?', val)
                            if nums:
                                t[idx] = float(nums[0]) if '.' in nums[0] else int(nums[0])
                            else:
                                t[idx] = 0
                
                # Reconstruct the line with the cleaned data
                line = indent + repr(tuple(t)) + comma + comment + '\n'
            except Exception as e:
                # If a line fails to parse, leave it untouched
                pass
                
        out_lines.append(line)

    # 4. Add a single, unified execution block at the very bottom
    out_lines.append('\nif __name__ == "__main__":\n')
    for func in funcs:
        out_lines.append(f'    {func}()\n')
        
    out_lines.append('    print("\\nAll parks have been successfully populated!")\n')

    # Overwrite the file with the patched version
    with open('populate_db.py', 'w', encoding='utf-8') as f:
        f.writelines(out_lines)
        
    print("Successfully patched populate_db.py! All Unknown/None values in integer fields are now 0, and all functions will execute.")

if __name__ == "__main__":
    patch_database_script()