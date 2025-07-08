from pathlib import Path
import xml.etree.ElementTree as ET
import re
import shutil
import os

##############################################
# Useful functions
##############################################
def clean_illegal_xml_chars(text):
    # delete illegal character, for example: &#x01;
    return re.sub(r"&#x.*;", "", text)

def generate_md_from_dict(data: dict, source_file="More Stacks (2025).py", output_md = "More Stacks (2025).md"):
    """
    :param data: dict：
                 {
                    "Alcohol": (1024, 102400, "4 -> 400"),
                    ...
                 }
    """

    lines = []
    lines.append(f"> ⚠️ This file is **automatically generated** from `{source_file}`.\n")
    lines.append("\n")
    lines.append("| Items   | Original Value（xml） | Modified Value（xml） | Changes           |")
    lines.append("|---------|-------------------|---------------------|--------------------|")

    for item, (original, modified, note) in data.items():
        lines.append(f"| {item} | {original}             | {modified}               | {note} |")

    # write to markdown file
    Path(output_md).write_text("\n".join(lines), encoding="utf-8")
    print(f"✅ Markdown saved to: {output_md}")


##############################################
# Preparation
##############################################
"""
First, 

Read 'Modding Instructions.pdf' in the game root directory.
"""


# Create a new mod:

mod_name = "More Stacks (2025)"
mod_description = """
Many mods on steam workshop don't work now.
I decide to write one.

** In short: Most items can now stack 100 times as much as before. **

For more details, see https://github.com/wqs-s-mods/This-War-of-Mine/blob/main/More%20Stacks%20(2025).md"""
mod_picture = "More Stacks.jpg"


##############################################
# Before running this script, make sure you have the following:
##############################################
# Then, set your mod root directory here.
dir_your_mods_root = Path(r"D:\SteamLibrary\steamapps\common\This War of Mine\Mods\75254c6cc3e3499cab3c81a88c0f6912")

# Set a backup directory for original files.
# Make sure to backup by yourself before running this script.
dir_backup = dir_your_mods_root / "items_backup"
dir_items = dir_your_mods_root / "items"


##############################################
# Function to edit items in the mod
# This function will read each item XML file, check it, and modify the stack size.
##############################################
modified_items = [
    "Alcohol",
    "Ammo",
    "Bandages",
    "Book",
    "BrokenToy",
    "CannedFood",
    "Cigarette",
    "Coffee",
    "Crayons",
    "DeadChildToy",
    "GunPowder",
    "HeaterFuel",
    "HerbalMeds",
    "HomeGrownTobacco",
    "JaredFood",
    "Joint", # ?
    "LockPick",
    "Materials",
    "MedIngredients",
    "Meds",
    "Parts",
    "PistolShells",
    "Plants",
    "PlushDog",
    "RawFood",
    "RifleAmmo",
    "SawBlade",
    "ShotgunAmmo",
    "Snow",
    "StaleFood",
    "Sugar",
    "Tobacco",
    "Vegetables",
    "Water",
    "WeaponParts",
    "Wood",
    "ElectricParts"


]
modified_info = {}

def edit_items():
    # get the original files back.
    shutil.rmtree(dir_items)
    shutil.copytree(dir_backup, dir_items)

    for item_file in dir_items.glob("*.xml"):
        # clean the file content
        xml_raw = item_file.read_text(encoding="utf-8")
        xml_clean = clean_illegal_xml_chars(xml_raw)

       # parse
        root = ET.fromstring(xml_clean)

        # check if the item is in the modified list
        to_modify = False

        for prop in root.findall(".//Prop"):
            if prop.attrib.get("Name") == "Name":
                name = prop.attrib.get("Value")
                if name in modified_items:
                    to_modify = True
                    break
        
        if to_modify:
            # modify the stack size
            for prop in root.findall(".//Prop"):
                if prop.attrib.get("Name") == "StackSize":
                    old_stack_size = int(prop.attrib.get("Value"))
                    new_stack_size = old_stack_size * 100
                    prop.set("Value", str(new_stack_size))
                    modified_info[name] = (old_stack_size, new_stack_size, f"{old_stack_size//256} -> {new_stack_size//256}")
                    print(modified_info[name])

            # write back to the file
            item_file.write_text(ET.tostring(root, encoding="unicode"), encoding="utf-8")

    generate_md_from_dict(modified_info)

    if len(modified_info) != len(modified_items):
        print("❗ Warning: Not all items were modified. Please check the modified_items list.")

if __name__ == "__main__":
    edit_items()