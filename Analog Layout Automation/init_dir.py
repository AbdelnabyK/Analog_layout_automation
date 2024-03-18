def cdsenv():
    """
    Creates or overwrites a '.cdsenv' file to suppress exit confirmation in Cadence Virtuoso.

    This function does not take any parameters. When called, it writes a specific line of text
    ("ddserv.ciw   promptOnExit   boolean   nil\n") to a file named '.cdsenv'. This text is a
    configuration setting that turns off the prompt asking for exit confirmation in Cadence Virtuoso.

    If the '.cdsenv' file does not exist in the working directory, the function will create it. If
    it does exist, the function will overwrite the existing content.

    Note: This function will affect data in your current working directory. Be aware of any existing
    '.cdsenv' files in your directory before using.

    Raises:
        IOError: If the file cannot be written.
    """

    text = "ddserv.ciw   promptOnExit   boolean   nil\n"
    with open(".cdsenv", 'w') as file:
        file.write(text)


def cdslib():
    """
    Creates or overwrites a 'cds.lib' file to define libraries that would be used in Cadence Virtuoso.
    It mainly defines TSMC 65 nm library.

    Note: This function will affect data in your current working directory. Be aware of any existing
    'cds.lib' files in your directory before using.

    """
    tsmcN65_definition = "\nDEFINE tsmcN65 /home/islam/Desktop/tsmc65nm/tsmcN65"  # path of TSMC 65 nm Library.

    text = '''SOFTINCLUDE /usr/local/cadence/IC617/share/cdssetup/dfII/cds.lib
SOFTINCLUDE /usr/local/cadence/IC617/share/cdssetup/hdl/cds.lib
SOFTINCLUDE /usr/local/cadence/IC617/share/cdssetup/pic/cds.lib
SOFTINCLUDE /usr/local/cadence/IC617/share/cdssetup/sg/cds.lib
DEFINE MentorObserverLib $MGC_HOME/shared/pkgs/icv/tools/realtime/virtuoso/MentorObserverLib
DEFINE avTech /EDA/Cadence/ASSURA/tools.lnx86/assura/etc/avtech/avTech
DEFINE basic                    ${CDSHOME}/tools/dfII/etc/cdslib/basic
DEFINE analogLib 		${CDSHOME}/tools/dfII/etc/cdslib/artist/analogLib''' + tsmcN65_definition + "\n"

    with open("cds.lib", 'w') as file:
        file.write(text)


def cdsinit():
    """
    Generates a '.cdsinit' file to configure Cadence Virtuoso environment.

    This function does not take any parameters. When executed, it creates a
    '.cdsinit' file in the current working directory, which is critical for
    customizing the Cadence Virtuoso environment.

    The '.cdsinit' file serves as a startup file for Cadence Virtuoso, loaded
    every time the environment is initiated. It can set system parameters,
    load necessary design kits and libraries, customize tools within the
    Cadence suite, and execute Skill scripts.

    This functionality ensures a consistent, tailored working environment
    across sessions, promoting efficiency in chip design workflows.

    Note: This function will create a new '.cdsinit' file in your current
    directory, potentially overwriting any existing one. Ensure to back up
    any important data before executing.

    Raises:
        IOError: If the file cannot be created due to permission issues or
        other problems.
    """
    text = '''/* 
       filepath:        <cds_install_dir>/cdsuser/.cdsinit
       dfII version:    4.4

       This file can be copied into a users home or project directory
       and customized.

       The site initialization file in <cds_install_dir>/local/.cdsinit should
       set all the defaults for the site.

       For more information on site initialization look at the files

          <cds_install_dir>/samples/local/
                                        cdsinit
                                        aaConfig.il
                                        dciConfig.il
                                        metConfig.il
                                        sysConfig.il
                                        uiConfig.il



       The sample site initialization file supplied is

          <cds_install_dir>/samples/local/cdsinit

       The site administrator should have moved this to

          <cds_install_dir>/local/.cdsinit

       and customized it.

    ###################################################################
       Please read the entire file and the comments before you start
       customizing the file.

       There are bind key definition files supplied for different 
       applications. The relevant bind key definitions files must
       be loaded if you want bind keys defined for that application.
       See section LOAD APPLICATION BIND KEY DEFINITIONS.
    ###################################################################

       The user may copy portions from the above files into the
       home or project customization file and modify the defaults.


       It is recommended that the user copy only portions as opposed
       to copying the whole files.

       Appropriate items for the user's customization file are

       1. Library search path
       2. Specific bind keys
       3. Custom SKILL procedures
       4. User preference options             - examples in uiConfig.il
       5. Form placements                     - examples in uiConfig.il

       In order for any window placements to work correctly the following 
       X resource must be set in the .Xdefaults or .xresources file
       pertaining to your hardware platform.

        Mwm*clientAutoPlace:             False

       After setting the resource read in the resource file with the command

        xrdb <resource_filename>

       and restart the Motif window manager.

       The function 
                 prependInstallPath("string")
       adds the installation path to the string argument
       For this reason there should NOT be a space at the beginning of the
       string.
       There SHOULD be a space at the end of the string if more paths are to
       follow.
       This function is used to make path specification in this file
       independant of the exact installation path.

       The function let() creates local variables ( example: libPath ). 
       This makes sure that any global variables are not accidentally modified.

    */
    ;
    ;################################################
    ;#
    ;# SETTINGS FOR SKILL PATH and SKILL PROGRAMMING
    ;#
    ;################################################
    ;
    ;  The function sstatus() sets the status of variables
    ;  The variable writeProtect controls if a SKILL function can be
    ;  redefined or not;
    ;
    ;  Any functions defined after writeProtect = t CANNOT be redefined
    ;  Any functions defined after writeProtect = nil CAN be redefined
    ;  If you are going to create SKILL programs and define functions set the
    ;  status of writeProtect to nil at the beginning of your session.
    ;
    ;  Set skill search path. The SKILL search path contains directories
    ;  to be searched to locate SKILL programs when program names are
    ;  specified without full path names.
    ;  The operation could be reading, writing or loading a SKILL program.
    ;
    ;  Source technology files are considered SKILL files and when loading 
    ;  or dumping the technology file SKILL search path will be used.
    ;
    ;



    sstatus(writeProtect nil)

    let((skillPath)
       skillPath= strcat(
        ". ~ "                                          ; Current & home directory
        prependInstallPath("samples/techfile ")         ; sample source technology files
       )
       setSkillPath(skillPath)
    )
    ;
    ;
    ;################################################
    ;#                                           
    ;# LOAD APPLICATION BIND KEY DEFINITIONS
    ;#
    ;################################################
    ;
    ;  The bind keys supplied with the Cadence software should have
    ;  been loaded by the site .cdsinit file.
    ;  This file also loads them in case they were not loaded by the
    ;  site customization file.
    ;
    ;  In case they are loaded by the site .cdsinit prevent reloading by
    ;  adding the comment ; to the beginning of the line containing the
    ;  specific file name in the list bindKeyFileList below.
    ;
    ;  If you load the bind key definition file but the application is not
    ;  registered ( product not licensed or checked out ) then you might get
    ;  a warning that looks like
    ;
    ;   *WARNING* "Schematics is not registered yet"
    ;
    ;  This warning can be ignored if you know that the product is not
    ;  licensed or checked out.
    ;
    ; 
    let( (bindKeyFileList file path saveSkillPath)
        bindKeyFileList = '(
                     "leBindKeys.il" 
                     "schBindKeys.il"
                        )

    ;  this is the path that is searched for the files
        path = strcat(
                  ".   ~   "
                  prependInstallPath("local ")
                  prependInstallPath("samples/local")
                 )
        saveSkillPath=getSkillPath()
        setSkillPath(path)
    ;
    ;

       foreach(file bindKeyFileList
           if(isFile(file) then
              loadi(file)
             )
        )

        setSkillPath(saveSkillPath)
    )

    ;
    ;
    ;  An individual user may wish to add some bindkeys of his/her own or
    ;  over ride some default loaded bindkeys.  For more information about
    ;  bindkeys see the manual "SKILL Reference Manual, Language Fundamentals", 
    ;  Chapter 4.
    ;
    ;  Here is an example of setting one bindkey on "F2" than prints 
    ;  "Hello world" to the CIW when pressed in the CIW.
    ;hiSetBindKey("Command Interpreter" "<Key>F2" "printf(\"Hello World\")") 
    ;
    ;  Here is an example of setting keys for more than one application
    ;
    ;let( (app appList)
    ;  appList = '( 
    ;             "Command Interpreter"
    ;             "Schematics"
    ;             "Symbol"
    ;   
    ;    Add other applications here 
    ;
    ;    )
    ;  foreach(app appList
    ;    hiSetBindKey(app "<Key>F4" "printf(\"Hello \")") 
    ;    hiSetBindKey(app "<Key>F5" "printf(\"World\")") 
    ;
    ;    Add more bind keys here
    ;
    ;
    ;  )
    ;)
    ;
    ;
    ;################################################
    ;#
    ;# MISCELLANEOUS
    ;#
    ;################################################
    ;
    ;
    ; Set your own prompt in the CIW. The first argument is the prompt.
    ; The second argument is not used yet.
    ;
    ; The variable editor defines the text editor to be used when any of
    ; the applications invoke an editor. For example technology dump and edit
    ; operation opens an editor window. 
    ;
    ; The editor may also be set by 
    ;               
    ;         unix environment variable EDITOR
    ;
    ;             setenv EDITOR 'xedit'
    ;
    ;
    ; When Design Framework is invoked the SKILL variable editor is set to the
    ; value of the unix variable EDITOR.
    ;  
    ; If EDITOR is not defined the SKILL variable
    ; editor is set to "vi"
    ;
    ; You may also set the variable to execute a UNIX command
    ; that invokes an xterm window of given size and location
    ; and starts an editor program.
    ; Example:
    ;
    ;    editor = "xterm -geometry 80x40 -e emacs"
    ;
    ; Size of xterm in the above example is 80 characters by 40 lines.
    ; With some editors on certain platforms the variable editor must
    ; be defined as shown above.
    ;
    ; Some application which require a text editor may be using the UNIX
    ; variable EDITOR instead of the SKILL variable editor. It is a good
    ; idea to set the UNIX variable EDITOR to the text editor of your
    ; choice which will automatically set the SKILL variable editor.
    ; 
    ;
    ;setPrompts("Ready >" "")
    ;editor = "xterm -geometry 85x50 -e vi";
    ;
    ;
    ;  ENVIRONMENT VARIABLES
    ;  Schematic, Layout and Graphic environment variable defaults are now found in
    ;  <cds_install_dir>/etc/tools/
    ;                           layout/.cdsenv
    ;                           schematic/.cdsenv
    ;                           graphic/.cdsenv
    ;
    ;  These can be customized in the user's ./cdsenv and ~/.cdsenv files.
    ;  A .cdsenv file can be created by using CIW->options->save defaults.
    ;
    printf("END OF USER CUSTOMIZATION\n")
    ;
    ;END OF USER CUSTOMIZATION

    ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

    ;
    ; check CALIBRE_HOME
    ;
    cal_home=getShellEnvVar("CALIBRE_HOME")
    if( cal_home==nil then
        cal_home=getShellEnvVar("MGC_HOME")
        if( cal_home!=nil then
            printf("// CALIBRE_HOME environment variable not set; setting it to value of MGC_HOME\n");
        )
    )

    if( cal_home!=nil && isDir(cal_home) && isReadable(cal_home) then

        ; Load calibre.skl or calibre.4.3.skl, not both!

        ; Load calibre.skl for Cadence versions 4.4 and greater
        load(strcat(cal_home "/lib/calibre.skl"))

    ;;;;Load calibre.4.3.skl for Cadence version 4.3
    ;;; load(strcat(cal_home "/lib/calibre.4.3.skl"))

    else

        ; CALIBRE_HOME is not set correctly. Report the problem.

        printf("//  Calibre Error: Environment variable ")

        if( cal_home==nil || cal_home=="" then
            printf("CALIBRE_HOME is not set.");
        else
            if( !isDir(cal_home) then
                printf("CALIBRE_HOME does not point to a directory.");
            else
                if( !isReadable(cal_home) then
                    printf("CALIBRE_HOME points to an unreadable directory.");
                )
            )
        )
        printf(" Calibre Skill Interface not loaded.\n")

        ; Display a dialog box message about load failure.

        hiDisplayAppDBox(
            ?name           'MGCHOMEErrorDlg
            ?dboxBanner     "Calibre Error"
            ?dboxText       "Calibre Skill Interface not loaded."
            ?dialogType     hicErrorDialog
            ?dialogStyle    'modal
           ?buttonLayout   'Close
        )
    )

    ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

    ddsOpenLibManager()
    envSetVal("asimenv.startup" "projectDir" 'string "/mnt/hgfs/H/simulation")
    envSetVal("asimenv" "saveDir" 'string "/mnt/hgfs/H/simulation")
    (envSetVal "adexl.distribute" "jobFileDir" 'string "/mnt/hgfs/H/simulation")


    ;//--------------------------------------------------------------------------------------------------------
    ;//
    ;//  **** sonnet cadence virtuoso interface ****
    ;//
    ;// All of the files for installation and initialization have been moved to the sonnet_virtuoso_dk directory
    ;//
    ;//--------------------------------------------------------------------------------------------------------

    printf("*WARNING* Sonnet:  All of the files for installation and initialization have been moved from the data directory to the sonnet_virtuoso_dk directory\n")
    printf("*WARNING* Sonnet:  Please refer to the file \"virtuoso.txt\" in the sonnet_virtuoso_dk directory\n")
    printf("*WARNING* Sonnet:  The sonnet_virtuoso_dk directory is located under the Sonnet installation directory\n")

    aSonnetDir = getShellEnvVar("SONNET_DIR")

    if(aSonnetDir then
      if(isDir(aSonnetDir) then
        ;// Loads the Sonnet Cadence Virtuoso Interface
        printf("*WARNING* Sonnet:  Attempting to load sonnet_virtuoso_install.il from the sonnet_virtuoso_dk/install directory\n")
        loadi(simplifyFilename(strcat(aSonnetDir "/sonnet_virtuoso_dk/install/sonnet_virtuoso_install.il")))

        ;// Loads the Sonnet Symbol Model Utility
        printf("*WARNING* Sonnet:  Attempting to load sonnetsymbolutility.il from the sonnet_virtuoso_dk/skillutil directory\n")
        loadi(simplifyFilename(strcat(aSonnetDir "/sonnet_virtuoso_dk/skillutil/sonnetsymbolutility.il")))

        ;// Loads the Sonnet Merge Vias Utility
        printf("*WARNING* Sonnet:  The utility is commented out to load sonnetmergeviasutility.il from the sonnet_virtuoso_dk/skillutil directory\n")
        ;//printf("*WARNING* Sonnet:  Attempting to load sonnetmergeviasutility.il from the sonnet_virtuoso_dk/skillutil directory\n")
        ;//loadi(simplifyFilename(strcat(aSonnetDir "/sonnet_virtuoso_dk/skillutil/sonnetmergeviasutility.il")))
      else
        printf("***The value for SONNET_DIR is not a directory.***\n")
      );// if
    else
      printf("***The Sonnet directory is not set and the Sonnet Cadence Virtuoso Interface is unable to be installed.***\n")
    );// if
    hiSetFont("label" ?size 13)
    hiSetFont("ciw" ?size 13)
    hiSetFont("text" ?size 13)
    d

    load("~/auCdlSchNetlistExportSetup.il")
    ;load("/opt/synopsys/hspice_2017/interface/HSPICE.ile")
    load("/EDA/Cadence/ASSURA/tools.lnx86/dfII/samples/local/uiConfig.il")
    load("/home/islam/.cdsinit.personal")
    setSkillPath(cons(getShellEnvVar("SKILLDIR") getSkillPath()))
    loadi("menu.il")
    loadi(strcat(getShellEnvVar("HPEESOF_DIR") "/idf/config/.cdsinit"))
    ;load("/EDA/animatepreview/virtuosoplugin/animatepreview.ile")

    envSetVal ("ddserv.ciw" "promptOnExit" 'boolean nil)
    '''

    with open(".cdsinit", 'w') as file:
        file.write(text)


def init_dir():
    """
    This script aims to initialize cadence virtuoso when run on a new directory.
    It creates three files .cdsint, .cdslib, and .cdsenv files.


    """
    cdsinit()
    cdslib()
    cdsenv()



