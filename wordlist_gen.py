import tkinter as tk
from tkinter import messagebox
import itertools
import os

LEET_MAP = {
    'a': ['a', '@', '4'],
    'e': ['e', '3'],
    'i': ['i', '1', '!'],
    'o': ['o', '0'],
    's': ['s', '$', '5'],
    't': ['t', '7'],
    'b': ['b', '8']
}

COMMON_SUFFIXES = ["123", "1234", "@123", "007", "!", "2024"]
SPECIAL_SYMBOLS = ["!", "@", "#", "$", "%", "&"]

def leetspeak_variants(word):
    def helper(prefix, chars):
        if not chars:
            return [prefix]
        char = chars[0]
        rest = chars[1:]
        replacements = LEET_MAP.get(char.lower(), [char])
        return [variant for rep in replacements for variant in helper(prefix + rep, rest)]
    return set(helper('', word))

def capitalize_variants(word):
    return {word.lower(), word.upper(), word.capitalize()}

def generate_variants(word):
    base = set()
    if word:
        base.update(capitalize_variants(word))
        base.update(leetspeak_variants(word))
    return base

def extract_dob_parts(dob):
    year = ''
    day = ''
    month = ''
    if len(dob) == 8:
        day = dob[:2]
        month = dob[2:4]
        year = dob[4:]
    elif len(dob) == 4:
        year = dob
    return day, month, year

def create_wordlist(info):
    first_name, last_name, dob, nickname, mobile, extras, min_len, max_len, filename = info
    parts = set()

    # Extract DOB parts
    day, month, year = extract_dob_parts(dob)

    # Add name/dob/nickname/mobile/special
    for item in [first_name, last_name, nickname, year, dob, mobile] + extras:
        parts.update(generate_variants(item))

    wordlist = set()
    wordlist.update(parts)

    # Normal combinations (no reverse)
    for a, b in itertools.permutations(parts, 2):
        wordlist.add(a + b)

    # Mobile-specific combos
    base_names = [first_name, last_name, nickname]
    for name in base_names:
        if not name:
            continue
        for variant in generate_variants(name):
            if dob:
                wordlist.add(f"{variant}@{dob}")
                wordlist.add(f"{variant}{dob}")
            if year:
                wordlist.add(f"{variant}{year}")
                wordlist.add(f"{variant}@{year}")
                wordlist.add(f"{variant}_{year}")
                wordlist.add(f"{variant}{year}!")
                wordlist.add(f"{variant}@{year}!")
            if day and month:
                wordlist.add(f"{variant}{day}{month}")
                wordlist.add(f"{variant}@{day}{month}")
            if mobile:
                wordlist.add(f"{variant}{mobile}")
                wordlist.add(f"{variant}@{mobile}")
                wordlist.add(f"{mobile}{variant}")
                wordlist.add(f"{mobile}@{variant}")

    if mobile:
        wordlist.add(mobile)
        for word in parts:
            wordlist.add(f"{word}{mobile}")
            wordlist.add(f"{mobile}{word}")

    # Add suffixes
    extended = set()
    for word in wordlist:
        extended.add(word)
        for suffix in COMMON_SUFFIXES + SPECIAL_SYMBOLS:
            extended.add(word + suffix)
            extended.add(suffix + word)

    final_list = [w for w in extended if min_len <= len(w) <= max_len]
    return sorted(set(final_list)), filename

def save_to_file(wordlist, filename):
    with open(filename, "w") as f:
        for word in wordlist:
            f.write(word + "\n")
    messagebox.showinfo("Success", f"✅ Wordlist saved to:\n{os.path.abspath(filename)}\nTotal: {len(wordlist)} passwords")

def generate():
    fname = entry_fname.get().strip()
    lname = entry_lname.get().strip()
    dob = entry_dob.get().strip()
    nickname = entry_nick.get().strip()
    mobile = entry_mobile.get().strip()
    special = entry_special.get().strip().split(',')
    min_len = int(entry_min.get() or "6")
    max_len = int(entry_max.get() or "16")
    filename = entry_file.get().strip() or "wordlist.txt"

    wordlist, file = create_wordlist((fname, lname, dob, nickname, mobile, [s.strip() for s in special], min_len, max_len, filename))
    save_to_file(wordlist, file)

# GUI SETUP
root = tk.Tk()
root.title("Wordlist Generator")
root.geometry("400x580")
root.resizable(False, False)

tk.Label(root, text="First Name").pack()
entry_fname = tk.Entry(root, width=40)
entry_fname.pack()

tk.Label(root, text="Last Name").pack()
entry_lname = tk.Entry(root, width=40)
entry_lname.pack()

tk.Label(root, text="Date of Birth (DDMMYYYY or YYYY)").pack()
entry_dob = tk.Entry(root, width=40)
entry_dob.pack()

tk.Label(root, text="Nickname").pack()
entry_nick = tk.Entry(root, width=40)
entry_nick.pack()

tk.Label(root, text="Mobile Number").pack()
entry_mobile = tk.Entry(root, width=40)
entry_mobile.pack()

tk.Label(root, text="Special Words (comma separated)").pack()
entry_special = tk.Entry(root, width=40)
entry_special.pack()

tk.Label(root, text="Min Password Length").pack()
entry_min = tk.Entry(root, width=40)
entry_min.insert(0, "6")
entry_min.pack()

tk.Label(root, text="Max Password Length").pack()
entry_max = tk.Entry(root, width=40)
entry_max.insert(0, "12")
entry_max.pack()

tk.Label(root, text="Output Filename").pack()
entry_file = tk.Entry(root, width=40)
entry_file.insert(0, "wordlist.txt")
entry_file.pack()

tk.Button(root, text="🚀 Generate Wordlist", command=generate, bg="green", fg="white").pack(pady=20)

root.mainloop()
