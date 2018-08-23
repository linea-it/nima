from datetime import datetime
import numpy as np
import subprocess
import os
import shutil

#Function to execute scripts, the parameters must be an numpy array 
#with specific and ordered values
#for example the script sc_wget needs [number, name, par1, par2]
#where par1 is the parameter for creation of observations file
#and par2 is the parameter for creation of orbital elements file
#errors for this example: [name, number, par1, par2]
#[number, name, par2, par1], [number, par1, name, par2], etc.
def executeScript(script, parameters):

    strParameters = '\n'.join(map(str, parameters))

    #open the script .sh with the necessary configurations
    p = subprocess.Popen(script, stdin=subprocess.PIPE, shell=True)

    #set the input parameters to the script
    p.communicate(strParameters)


def NIMAmanager(inputParametersFile):
    parameters, comment = np.loadtxt(inputParametersFile, dtype='str', delimiter='|', converters={0: lambda s: s.strip()}, unpack=True)


    pathNIMAuser = parameters[0]
    number = parameters[5]
    name = parameters[6]

    #Check if necessary files exist (if not then it is finalized here)

    in_astrometry = os.path.join(parameters[1], name + ".txt")

    if not os.path.exists(in_astrometry):
        raise Exception("No Astrometry file found. [ %s ]" % in_astrometry)
        exit(1)

    f_bsp_jpl = name + ".bsp"
    in_bsp_jpl = os.path.join(parameters[2], f_bsp_jpl)

    if not os.path.exists(in_bsp_jpl):
        raise Exception("No BSP_JPL file found. [ %s ]" % in_bsp_jpl)
        exit(1)

    # Observations AstDys
    in_observatios = os.path.join(parameters[3], name + ".rwo")

    if not os.path.exists(in_observatios):
        # Nao existe arquivo do AstDys verifica do MPC
        print("No Observations AstDys found. [ %s ]" % in_observatios)

        # Observations MPC
        in_observatios = os.path.join(parameters[3], name + ".rwm")
        if not os.path.exists(in_observatios):
            raise Exception("No Observations file found. [ %s ]" % in_observatios)
            exit(1)

    # Orbital Parameters AstDys
    in_orb_parameters = os.path.join(parameters[4], name + ".eq0")

    if not os.path.exists(in_orb_parameters):
        # Nao existe arquivo do AstDys verifica do MPC
        print("No Orbital Parameters AstDys found. [ %s ]" % in_orb_parameters)

        in_orb_parameters = os.path.join(parameters[4], name + ".eqm")
        if not os.path.exists(in_orb_parameters):
            raise Exception("No Orbital Parameters file found. [ %s ]" % in_orb_parameters)
            exit(1)


    asteroidFolder = pathNIMAuser + "/results/" + number
    # create the folder "number" if it does not exist    
    if os.path.exists(asteroidFolder):
        subprocess.call(["rm", "-r", asteroidFolder])
    os.mkdir(asteroidFolder)

    print("Asteroid Folder: %s" % asteroidFolder)


    myPath = os.getcwd()
    # changing from local path to especific path 
    os.chdir(pathNIMAuser)


    #copy the bsp file (JPL) and astrometry file (PRAIA) to NIMA
    subprocess.call(["cp", in_astrometry, asteroidFolder])

    jplbsp = os.path.join(pathNIMAuser, 'jplbsp', f_bsp_jpl )
    subprocess.call(["cp", in_bsp_jpl, jplbsp])


    #============================= EXECUTE ALL SCRIPTS NIMA =============================
    
    # ========================== sc_AstDySMPC2NIMA ==========================
    executeScript("./sc_AstDySMPC2NIMA.sh", np.concatenate([parameters[5:7], parameters[3:5]]) )

    # ============================== sc_esoopd ==============================
    executeScript("./sc_esoopd.sh", parameters[5:7])
    
    # =============================== sc_cat ================================
    executeScript("./sc_cat.sh", np.insert(parameters[7:8],0,number))

    # ============================== sc_merge ===============================

    executeScript("./sc_merge.sh", np.insert(parameters[8:10],0,number))

    # =============================== sc_fit ================================
    executeScript("./sc_fit.sh", np.insert(parameters[10:17],0,number))

    # ============================= sc_importbsp ============================
    executeScript("./sc_importbsp.sh", np.append(parameters[5:7],jplbsp))

    # ============================ sc_diffjplomc ============================
    executeScript("./sc_diffjplomcPython.sh", np.insert(parameters[17:31],0,number))

    
    # ============================== sc_makebsp =============================
    executeScript("./sc_makebsp.sh", np.insert(parameters[31:38],0,number))

    # =============================== sc_ephem ==============================
    executeScript("./sc_ephem.sh", np.insert(parameters[38:],0,number))

    # TODO: COPIAR ARQUIVO DE DUPLICIDADE

    # ============================ move results ==============================

    result_folder = os.environ.get("DIR_RESULTS")
    print("Result Folder: %s" % result_folder)

    files = os.listdir(asteroidFolder)
    print("Result Files: %s" % len(files))

    result_files = []

    for f in files:
        try:
            # Ignorar o Link Simbolico para o arquivo jplbsp
            if f != os.path.basename(jplbsp):
                dest_file = os.path.join(result_folder, f)
                shutil.move(os.path.join(asteroidFolder, f), dest_file)

                os.chmod(dest_file, 0776)

                result_files.append(dest_file)

                print("File: [ %s ] Size: [ %s ]" %(dest_file, os.path.getsize(dest_file)))
            
        except Exception as e:
            print(e)

    return result_files

if __name__ == "__main__":

    # parametersFile = raw_input("Write the file name with all NIMA parameters: ")

    parametersFile = os.path.join(os.environ.get("DIR_INPUTS"), "input.txt")

    start_time = datetime.now()

    files = NIMAmanager(parametersFile)
    
    # Check Results 
    if len(files) == 18:
        status = "SUCCESS"
    else:
        status = "WARNING"

    end_time = datetime.now()

    print "Duration: ", end_time - start_time
    print "Execution Status: %s" % status

