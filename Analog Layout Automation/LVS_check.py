import os
import subprocess
def init_si_env_file(cadence_directory, library_name, cell_view_name):
    try:
        with open(f"{cadence_directory}/si.env", "w") as file:
            file.write(f'simLibName = "{library_name}"\n')
            file.write(f'simCellName = "{cell_view_name}"\n')
            file.write('simViewName = "schematic"\n')
            file.write('simSimulator = "auCdl"\n')
            file.write('simNotIncremental = nil\n')
            file.write('simReNetlistAll = nil\n')
            file.write('simViewList = \'("auCdl" "schematic")\n')
            file.write('simStopList = \'("auCdl")\n')
            file.write('hnlNetlistFileName = "netlist"\n')
            file.write('resistorModel = ""\n')
            file.write('shortRES = 2000.0\n')
            file.write('preserveRES = \'t\n')
            file.write('checkRESVAL = \'t\n')
            file.write('checkRESSIZE = \'nil\n')
            file.write('preserveCAP = \'t\n')
            file.write('checkCAPVAL = \'t\n')
            file.write('checkCAPAREA = \'nil\n')
            file.write('preserveDIO = \'t\n')
            file.write('checkDIOAREA = \'t\n')
            file.write('checkDIOPERI = \'t\n')
            file.write('checkCAPPERI = \'nil\n')
            file.write('simPrintInhConnAttributes = \'nil\n')
            file.write('checkScale = "meter"\n')
            file.write('checkLDD = \'nil\n')
            file.write('pinMAP = \'nil\n')
            file.write('preserveBangInNetlist = \'nil\n')
            file.write('shrinkFACTOR = 0.0\n')
            file.write('globalPowerSig = ""\n')
            file.write('globalGndSig = ""\n')
            file.write('displayPININFO = \'t\n')
            file.write('preserveALL = \'t\n')
            file.write('setEQUIV = ""\n')
            file.write('incFILE = ""\n')
            file.write('auCdlDefNetlistProc = "ansCdlSubcktCall"\n')
        print(f"si.env file was successfully created in {cadence_directory}.")
    except Exception as e:
        print(f"Error: {e}")


def schematic_to_spice():
    subprocess.call(["si", "-batch","-command", "netlist", "-cdslib", "./cds.lib"])


def edit_calibre_lvs(lvs_rules_path, gds_file_name, top_cell_name):
    edited_lvs_rules_path = "./calibre_edited.lvs"
    with open(lvs_rules_path, "r") as in_file, open(edited_lvs_rules_path, "w") as out_file:
        for line in in_file:
            if line.startswith("LAYOUT PATH"):
                line = f'LAYOUT PATH "{gds_file_name}.gds"\n'
            elif line.startswith("LAYOUT PRIMARY"):
                line = f'LAYOUT PRIMARY "{top_cell_name}"\n'
            elif line.startswith("SOURCE PRIMARY"):
                line = f'SOURCE PRIMARY "{top_cell_name}"\n'
            elif line.startswith("SOURCE PATH"):
                line = f'SOURCE PATH "netlist"\n'
            out_file.write(line)
    return os.path.abspath(edited_lvs_rules_path)


def run_calibre_lvs(lvs_rules_path):
    command = ["calibre", "-lvs", lvs_rules_path]

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    stdout, stderr = process.communicate()

    if process.returncode != 0:
        print(f"An error occurred while running the command: {stderr.decode()}")
    else:
        print(f"Output: {stdout.decode()}")


def run_calibre_lvs_rve():
    command = ["calibre", "-rve", "svdb"]

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    stdout, stderr = process.communicate()

    if process.returncode != 0:
        print(f"An error occurred while running the command: {stderr.decode()}")
    else:
        print(f"Output: {stdout.decode()}")


def lvs_check_tsmc65nm(cadence_directory, lvs_rules_path, library_name, cell_view_name):

    init_si_env_file(cadence_directory, library_name, cell_view_name)
    schematic_to_spice()
    edited_lvs_rules_path = edit_calibre_lvs(lvs_rules_path, cell_view_name, cell_view_name)
    run_calibre_lvs(edited_lvs_rules_path)
    run_calibre_lvs_rve()
