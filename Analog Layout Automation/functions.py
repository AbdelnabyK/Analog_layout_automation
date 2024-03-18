import os
import subprocess

def get_cell_views(library_name):
    directories = [name for name in os.listdir(library_name) if os.path.isdir(os.path.join(library_name, name))]
    return directories


def check_file_exists(filename):
    return os.path.isfile(filename)


def search_for_libraries(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    result = []
    found_define = False

    for line in lines:
        words = line.split()

        if found_define and words:
            result.append(words[1])  # Append the second word in line

        if "DEFINE" in words and "tsmcN65" in words:
            found_define = True  # Set flag if "DEFINE tsmcN65" is found

    return result


def library_cell_view_dict():
    dic = dict()
    lib = search_for_libraries("cds.lib")
    for key in lib:
        dic[key] = get_cell_views(key)
    return dic


def edit_extract_il(library_name, cell_view_name):
    # Open the file in read mode
    with open("extract.il", "r") as file:
        lines = file.readlines()

    # Edit the first line
    if len(lines) > 0:
        line = lines[0].strip()
        edited_line1 = f'cv=dbOpenCellViewByType("{library_name}" "{cell_view_name}" "schematic" "schematic" "r")'
        lines[0] = edited_line1 + '\n'
        edited_line2 = f'lay = deNewCellView("{library_name}", "{cell_view_name}", "layout", "maskLayout", nil))'
        lines[1] = edited_line2 + '\n'
        edited_line3 = f'layout_view = dbOpenCellViewByType("{library_name}", "{cell_view_name}", "layout", "maskLayout", "w"))'
        lines[2] = edited_line3 + '\n'
        edited_line281 = f'ddDeleteObj(ddGetObj("{library_name}" "{cell_view_name}" "layout"))'
        lines[280] = edited_line281 + '\n'

    # Write the modified lines back to the file
    with open("extract.il", "w") as file:
        file.writelines(lines)


def extract(library_name, cell_view_name):
    edit_extract_il(library_name, cell_view_name)
    subprocess.call(["virtuoso", "-nograph", "-restore", "extract.il"])


def edit_run_skill_il(library_name, cell_view_name):

    # Open the file in read mode
    with open("run_skill.il", "r") as file:
        lines = file.readlines()

    # Write the modified lines back to the file
    with open("run_skill.il", "w") as file:
        file.write(f'joe = deNewCellView("{library_name}", "{cell_view_name}", "layout", "maskLayout", nil)\n')
        file.writelines(lines)
    with open("run_skill.il", "a") as file:
        file.write('dbSave(cv)\n')
        file.write('ciwHiExit()\n')

def view_layout(library_name, cell_view_name):
    # Create a new file or overwrite the existing one
    with open('view.il', 'w') as file:
        # Write the desired line to the file
        file.write(f'cv = deOpenCellView("{library_name}" "{cell_view_name}" "layout" "maskLayout" nil "r")\n')

    # Run the desired Linux command
    subprocess.run(['virtuoso', '-graph', '-restore', 'view.il'])