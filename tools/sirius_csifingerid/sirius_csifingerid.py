import argparse
import os
import glob
import shutil
from subprocess import Popen, PIPE


parser = argparse.ArgumentParser()
parser.add_argument('--input')
parser.add_argument('--db_online')
parser.add_argument('--profile')
parser.add_argument('--candidates')
parser.add_argument('--ppm_max')
parser.add_argument('--polarity')
parser.add_argument('--results_name')
parser.add_argument('--out_dir')
parser.add_argument('--tool_directory')
args = parser.parse_args()
print args

result_pth = os.path.join(args.out_dir, args.results_name)
with open(args.input,"r") as infile:
 
    numlines = 0
    for line in infile:
        line = line.strip()
        if numlines == 0: #read the headers
            if "NAME" in line:
                featid = line.split("NAME: ")[1]
            if "PRECURSORMZ" in line:
                mz = float(line.split("PRECURSORMZ: ")[1])
                if args.polarity=="pos":
                    mz2 = mz-1.007276
                else:
                    mz2 = mz+1.007276
            if "Num Peaks" in line:
                numlines = int(line.split("Num Peaks: ")[1]) # number of spectra peaks
                linesread = 0
                peaklist = []
        else:
            if linesread != numlines: # read spectra
                line = tuple(line.split("\t"))
                linesread += 1
                peaklist.append(line)
            else:
                numlines = 0 #reset for next header
                #write spec file
                specpth = os.path.join(args.out_dir,'tmpspec.txt')
                tmpdir = os.path.join(args.out_dir,'tempout')
                with open(specpth, 'w') as outfile1:
                    for p in peaklist:
                        outfile1.write(p[0]+" "+p[1]+"\n")
                    #create commandline input
                    if args.polarity == "pos":
                        ion = "[M+H]+"
                    else:
                        ion = "[M-H]-"
                #cmd_command = os.path.join(args.tool_directory, 'bin', 'sirius ')
                cmd_command = 'sirius '
                cmd_command += "-c {} -o {} -i {} -z {} -2 {} ".format(args.candidates, tmpdir , ion, mz, specpth)
                cmd_command += "-d {} --ppm-max {} --fingerid".format(args.db_online, args.ppm_max)

                # run
                print cmd_command
                os.system(cmd_command)
     
                # if fingerid found hits
                mtching_files = glob.glob(os.path.join(tmpdir, "*_tmpspec_", "summary_csi_fingerid.csv"))
                if mtching_files:
                    first_read=True
                    if len(mtching_files)>1:
                        print 'multiple folder names being used', mtching_files
                    latest_file = max(mtching_files, key=os.path.getmtime)
 
                    with open(result_pth, 'a') as outfile2:

                        with open(latest_file) as infile_csi:
                            for iline in infile_csi:
                                if "inchi" in iline:
                                    if first_read:
                                        iline = iline.replace("inchi","InChI")
                                        iline = iline.replace("rank", "Rank")
                                        iline = iline.replace("name", "Name")
                                        iline = iline.replace("score", "Score")
                                        outfile2.write("UID\t"+iline)
                                        first_read=False
                                else:
                                    outfile2.write(featid+"\t"+ iline)
                shutil.rmtree(tmpdir)

