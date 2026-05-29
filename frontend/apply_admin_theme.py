import glob

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Avoid injecting multiple times
    if 'admin-theme.css' in content:
        print(f"Skipping {filepath} - already has admin theme.")
        return

    # Find the theme.css line and append admin-theme.css
    target_str = '<link rel="stylesheet" href="../../assets/css/theme.css">'
    new_str = target_str + '\n  <link rel="stylesheet" href="../../assets/css/admin-theme.css">'
    
    # Try alternative matching if the spacing is different
    if target_str not in content:
        target_str = '<link rel="stylesheet" href="../../assets/css/theme.css" />'
        new_str = target_str + '\n  <link rel="stylesheet" href="../../assets/css/admin-theme.css">'

    if target_str in content:
        content = content.replace(target_str, new_str)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Processed {filepath}")
    else:
        print(f"Could not find theme.css link in {filepath}")

files = glob.glob('e:/GitHub Repo/school-management-system/frontend/pages/admin/*.html')
for f in files:
    process_file(f)
