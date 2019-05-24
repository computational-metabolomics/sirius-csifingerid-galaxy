from __future__ import absolute_import, print_function
import argparse
import csv
import sys
import six
import re
import os
import tempfile
import multiprocessing
import glob

from collections import defaultdict

parser = argparse.ArgumentParser()
parser.add_argument('--input_pth')
parser.add_argument('--result_pth')
parser.add_argument('--database')
parser.add_argument('--profile')
parser.add_argument('--candidates')
parser.add_argument('--ppm_max')
parser.add_argument('--polarity')
parser.add_argument('--results_name')
parser.add_argument('--out_dir')
parser.add_argument('--tool_directory')
parser.add_argument('--temp_dir')

parser.add_argument('--meta_select_col', default='all')
parser.add_argument('--cores_top_level', default=1)
parser.add_argument('--chunks', default=1)
parser.add_argument('--minMSMSpeaks', default=1)
parser.add_argument('--schema', default='msp')
args = parser.parse_args()
print(args)


if args.temp_dir:
    wd = args.temp_dir
    if not os.path.exists(wd):
        os.mkdir(wd)

else:
    wd = tempfile.mkdtemp()

######################################################################
# Setup parameter dictionary
######################################################################
paramd = defaultdict()
paramd["cli"] = {}
paramd["cli"]["--database"] = args.database
paramd["cli"]["--profile"] = args.profile
paramd["cli"]["--candidates"] = args.candidates
paramd["cli"]["--ppm-max"] = args.ppm_max
if args.polarity == 'positive':
    paramd["default_ion"] = "[M+H]+"
elif args.polarity == 'negative':
    paramd["default_ion"] = "[M-H]-"
else:
    paramd["default_ion"] = ''

print(paramd)


######################################################################
# Setup regular expressions for MSP parsing dictionary
######################################################################
regex_msp = {}
regex_msp['name'] = ['^Name(?:=|:)(.*)$']
regex_msp['polarity'] = ['^ion.*mode(?:=|:)(.*)$', '^ionization.*mode(?:=|:)(.*)$', '^polarity(?:=|:)(.*)$']
regex_msp['precursor_mz'] = ['^precursor.*m/z(?:=|:)\s*(\d*[.,]?\d*)$', '^precursor.*mz(?:=|:)\s*(\d*[.,]?\d*)$']
regex_msp['precursor_type'] = ['^precursor.*type(?:=|:)(.*)$', '^adduct(?:=|:)(.*)$', '^ADDUCTIONNAME(?:=|:)(.*)$']
regex_msp['num_peaks'] = ['^Num.*Peaks(?:=|:)\s*(\d*)$']
regex_msp['msp'] = ['^Name(?:=|:)(.*)$']  # Flag for standard MSP format

regex_massbank = {}
regex_massbank['name'] = ['^RECORD_TITLE:(.*)$']
regex_massbank['polarity'] = ['^AC\$MASS_SPECTROMETRY:\s+ION_MODE\s+(.*)$']
regex_massbank['precursor_mz'] = ['^MS\$FOCUSED_ION:\s+PRECURSOR_M/Z\s+(\d*[.,]?\d*)$']
regex_massbank['precursor_type'] = ['^MS\$FOCUSED_ION:\s+PRECURSOR_TYPE\s+(.*)$']
regex_massbank['num_peaks'] = ['^PK\$NUM_PEAK:\s+(\d*)']
regex_massbank['cols'] = ['^PK\$PEAK:\s+(.*)']
regex_massbank['massbank'] = ['^RECORD_TITLE:(.*)$']  # Flag for massbank format

if args.schema == 'msp':
    meta_regex = regex_msp
elif args.schema == 'massbank':
    meta_regex = regex_massbank
elif args.schema == 'auto':
    # If auto we just check for all the available paramter names and then determine if Massbank or MSP based on
    # the name parameter
    meta_regex = {}
    meta_regex.update(regex_massbank)
    meta_regex['name'].extend(regex_msp['name'])
    meta_regex['polarity'].extend(regex_msp['polarity'])
    meta_regex['precursor_mz'].extend(regex_msp['precursor_mz'])
    meta_regex['precursor_type'].extend(regex_msp['precursor_type'])
    meta_regex['num_peaks'].extend(regex_msp['num_peaks'])
    meta_regex['msp'] = regex_msp['msp']

    print(meta_regex)



# this dictionary will store the meta data results form the MSp file
meta_info = {}


# function to extract the meta data using the regular expressions
def parse_meta(meta_regex, meta_info={}):
    for k, regexes in six.iteritems(meta_regex):
        for reg in regexes:
            m = re.search(reg, line, re.IGNORECASE)
            if m:
                meta_info[k] = '-'.join(m.groups()).strip()
    return meta_info


adduct_types = {
    '[M+H]+': 1.007276,
    '[M+NH4]+': 18.034374,
    '[M+Na]+': 22.989218,
    '[M+K]+': 38.963158,
    '[M+CH3OH+H]+': 33.033489,
    '[M+ACN+H]+': 42.033823,
    '[M+ACN+Na]+': 64.015765,
    '[M+2ACN+H]+': 83.06037,
    '[M-H]-': -1.007276,
    '[M+Cl]-': 34.969402,
}

# keep list of commands if performing in CLI in parallel
cmds = []
# keep a dictionary of all params
paramds = {}
# keep count of spectra (for uid)
spectrac = 0

with open(args.input_pth, "r") as infile:
    numlines = 0
    for line in infile:
        line = line.strip()

        if numlines == 0:
            # =============== Extract metadata from MSP ========================
            meta_info = parse_meta(meta_regex, meta_info)

            if ('massbank' in meta_info and 'cols' in meta_info) or ('msp' in meta_info and 'num_peaks' in meta_info):

                numlines = int(meta_info['num_peaks'])
                linesread = 0
                peaklist = []

        elif linesread < numlines:
            # =============== Extract peaks from MSP ==========================
            line = tuple(line.split())  # .split() will split on any empty space (i.e. tab and space)
            # Keep only m/z and intensity, not relative intensity
            save_line = tuple(line[0].split() + line[1].split())
            linesread += 1
            peaklist.append(save_line)

        elif linesread == numlines:
            # =============== Get sample name and additional details for output =======
            # use a unique uuid4 to keep track of processing (important for multicore)
            #rd = str(uuid.uuid4())
            spectrac += 1


            # Get sample details (if possible to extract) e.g. if created as part of the msPurity pipeline)
            # choose between getting additional details to add as columns as either all meta data from msp, just
            # details from the record name (i.e. when using msPurity and we have the columns coded into the name) or
            # just the spectra index (spectrac)
            if args.meta_select_col == 'name':
                # have additional column of just the name
                paramd['additional_details'] = {'name': meta_info['name']}
            elif args.meta_select_col == 'name_split':
                # have additional columns split by "|" and then on ":" e.g. MZ:100.2 | RT:20 | xcms_grp_id:1
                paramd['additional_details'] = {sm.split(":")[0].strip(): sm.split(":")[1].strip() for sm in
                               meta_info['name'].split("|")}
            elif args.meta_select_col == 'all':
                # have additional columns based on all the meta information extracted from the MSP
                paramd['additional_details'] = meta_info
            else:
                # Just have and index of the spectra in the MSP file
                paramd['additional_details'] = {'spectra_idx': spectrac}

            paramd["SampleName"] = "{}_sirius_result".format(spectrac)

            paramd["cli"]["--output"] = os.path.join(wd, "{}_sirius_result".format(spectrac))

            # =============== Output peaks to txt file  ==============================
            numlines = 0
            paramd["cli"]["--ms2"] = os.path.join(wd, "{}_tmpspec.txt".format(spectrac))
            print(paramd["cli"]["--ms2"])
            # write spec file
            with open(paramd["cli"]["--ms2"], 'w') as outfile:
                for p in peaklist:
                    outfile.write(p[0] + "\t" + p[1] + "\n")

            # =============== Update param based on MSP metadata ======================
            # Replace param details with details from MSP if required
            if 'precursor_type' in meta_info and meta_info['precursor_type']:
                paramd["cli"]["--ion"] = meta_info['precursor_type']
            else:
                if paramd["default_ion"]:
                    paramd["cli"]["--ion"] = paramd["default_ion"]
                else:
                    paramd["cli"]["--auto-charge"] = ''

            if 'precursor_mz' in meta_info and meta_info['precursor_mz']:
                paramd["cli"]["--precursor"] = meta_info['precursor_mz']

            # =============== Create CLI cmd for metfrag ===============================
            cmd = "sirius --fingerid"
            for k, v in six.iteritems(paramd["cli"]):
                    cmd += " {} {}".format(str(k), str(v))
            paramds[paramd["SampleName"]] = paramd

            # =============== Run metfrag ==============================================
            # Filter before process with a minimum number of MS/MS peaks
            if linesread >= float(args.minMSMSpeaks):

                if int(args.cores_top_level) > 1:
                    cmds.append(cmd)
                else:
                    print(cmd)
                    os.system(cmd)

            meta_info = {}

def work(cmds):
    return [os.system(cmd) for cmd in cmds]


# Perform multiprocessing on command line call level
if int(args.cores_top_level) > 1:
    cmds_chunks = [cmds[x:x + int(args.chunks)] for x in list(range(0, len(cmds), int(args.chunks)))]
    pool = multiprocessing.Pool(processes=int(args.cores_top_level))
    pool.map(work, cmds_chunks)
    pool.close()
    pool.join()

######################################################################
# Concatenate and filter the output
######################################################################
# outputs might have different headers. Need to get a list of all the headers before we start merging the files
# outfiles = [os.path.join(wd, f) for f in glob.glob(os.path.join(wd, "*_metfrag_result.csv"))]
outfiles = glob.glob(os.path.join(wd, '*', 'summary_csi_fingerid.csv'))

print(outfiles)

headers = []
c = 0
for fn in outfiles:
    with open(fn, 'r') as infile:
        reader = csv.reader(infile, delimiter='\t')
        if sys.version_info >= (3, 0):
            headers.extend(next(reader))
        else:
            headers.extend(reader.next())
        break

headers = list(paramd['additional_details'].keys()) + headers


with open(args.result_pth, 'a') as merged_outfile:
    dwriter = csv.DictWriter(merged_outfile, fieldnames=headers, delimiter='\t', quotechar='"',
        quoting=csv.QUOTE_NONNUMERIC,)
    dwriter.writeheader()

    for fn in outfiles:
        print(fn)

        with open(fn) as infile:
            reader = csv.DictReader(infile, delimiter='\t')

            ad = paramds[fn.split(os.sep)[-2]]['additional_details']

            for line in reader:

                line.update(ad)

                dwriter.writerow(line)
