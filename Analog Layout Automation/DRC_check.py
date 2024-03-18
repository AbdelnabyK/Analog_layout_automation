import subprocess
import os


def export_layout_to_gds(cadence_directory, library_name, Output_Stream_File, top_Cell, view, Technology_Library):

    # change the current directory to cadence directory in which the library is defined in the cds.lib file
    os.chdir(cadence_directory)

    # Execute the strmout command
    command = f'strmout -library {library_name} -strmFile {Output_Stream_File}.gds -topCell {top_Cell} -view {view} -techLib {Technology_Library}'
    run = subprocess.run(command, shell=True)


def edit_calibre_drc(drc_rules_path, gds_file_name, top_cell_name, drc_results_database):
    edited_drc_rules_path = "./calibre_edited.drc"
    with open(drc_rules_path, "r") as in_file, open(edited_drc_rules_path, "w") as out_file:
        for line in in_file:
            if line.startswith("LAYOUT PATH"):
                line = f'LAYOUT PATH "{gds_file_name}"\n'
            elif line.startswith("LAYOUT PRIMARY"):
                line = f'LAYOUT PRIMARY "{top_cell_name}"\n'
            elif line.startswith("DRC RESULTS DATABASE"):
                line = f'DRC RESULTS DATABASE "{drc_results_database}"\n'
            out_file.write(line)
    return os.path.abspath(edited_drc_rules_path)


def run_calibre_drc(drc_rules_path):
    command = ["calibre", "-drc", drc_rules_path]

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    stdout, stderr = process.communicate()

    if process.returncode != 0:
        print(f"An error occurred while running the command: {stderr.decode()}")
    else:
        print(f"Output: {stdout.decode()}")


def run_calibre_drc_rve(drc_db_file_path):
    command = ["calibre", "-rve", drc_db_file_path]

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    stdout, stderr = process.communicate()

    if process.returncode != 0:
        print(f"An error occurred while running the command: {stderr.decode()}")
    else:
        print(f"Output: {stdout.decode()}")


def drc_check_tsmc65nm(cadence_directory, drc_rules_path, library_name, top_Cell):

    export_layout_to_gds(cadence_directory, library_name, top_Cell, top_Cell, "layout", "tsmcN65")
    os.makedirs("drc")
    edited_drc_rules_path = edit_calibre_drc(drc_rules_path, f"./{top_Cell}.gds", top_Cell, "./drc/DRC_RES.db")
    run_calibre_drc(edited_drc_rules_path)
    run_calibre_drc_rve("./drc/DRC_RES.db")

