import os
import time


def create_il_file(library_name, cellview_name):
    """
    Creates a Skill script file to create a specified library and a cellview for cadence Virtuoso.

    Args:
        library_name (str): Name of the library.
        cellview_name (str): Name of the cellview.

    Returns:
        None
    """
    text = f'''lib = dbCreateLib("{library_name}", "./{library_name}")
cv = deNewCellView("{library_name}", "{cellview_name}", "schematic", "schematic", nil)
dbSave(cv~>cellView)'''

    with open(f"{cellview_name}.il", 'w') as file:
        file.write(text)


def run_virtuoso(cellview_name):
    command = "virtuoso -restore " + cellview_name + ".il" # This command opens cadence virtuoso and runs the skill script.
    time.sleep(2)  # Pauses execution for 2 seconds
    os.system(command)

