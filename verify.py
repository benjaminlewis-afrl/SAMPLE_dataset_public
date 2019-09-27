#! /usr/bin/env python

# A script that double-checks that the public release version of SAMPLE 
# only contains data between 10 and 80 degrees azimuth. It also contains
# logic to assert that we have checked all of the various filepaths 
# within the dataset. (This is done by creating lists of all the targets,
# all the PNG types, and real/synth and building all the combinations
# of these paths. As each type of path is encountered in the list of 
# files, we can remove it from the list of combinations, then assert
# that the lists are empty at the end.)
import os
import re
from time import sleep
import itertools
from scipy.io import loadmat, savemat

# These are the main file pathways in the dataset. 
img_types = ['png_images', 'mat_files']
png_types = ['decibel', 'qpm']
real_syn = ['real', 'synth']
targets = ['2s1', 'bmp2', 'btr70', 'm1',  'm2', 'm35', 'm548', 'm60', 't72', 'zsu23']

png_combos = list(itertools.product(png_types, real_syn, targets))
mat_combos = list(itertools.product(real_syn, targets))

count= 0 
# Walk through the entire directory, and get all the files. 
for root, dirs, files in os.walk("/home/lewisbp/DATA/SAMPLE_Public"):
    for f in files:
        if not f.endswith(('.png', '.mat')):
            continue

        count += 1
        fname = os.path.join(root, f)
        print(fname)
        # Regex that searches a fully-qualified path for its parts.
        # It checks whether it is a mat file or png file, if the 
        # normalization is QPM or decibel (for png), real or synth, 
        # and the azimuth angle. 
        matches = re.match('.*\/(mat_files|png_images)\/(qpm|decibel)?\/?(?:real|synth)\/.*?\/(.*?)_(real|synth).*elevDeg_(.*?)_azCenter_(.*?)_.._serial.*', fname)
        # Get the matches from the regular expression and assign
        # them to relevant variables
        png_or_mat = matches.group(1)
        qpm_or_db = matches.group(2)
        target = matches.group(3)
        real_or_syn = matches.group(4)
        elevation = int(matches.group(5))
        azimuth = int(matches.group(6))

        # Check each mat file, verifying that it only has certain file keys. 
        if fname.endswith(('.mat',)):
            data = loadmat(fname)

            target_keys = ['__header__', '__version__', '__globals__', 'aligned', 'azimuth', 'bandwidth', 'center_freq', 'complex_img', 'complex_img_unshifted', 'elevation', 'explanation', 'range_pixel_spacing', 'range_resolution', 'source_mstar_file', 'target_name', 'taylor_weights', 'xrange_pixel_spacing', 'xrange_resolution']

            if not set(data.keys()) == set(target_keys):
                datakeys = data.keys()

                for key in list(data):
                    if key not in target_keys:
                        data.pop(key)

                savemat(fname, data)

                data = loadmat(fname)
                assert set(data.keys()) == set(target_keys), data.keys()

        # Assertions: we only have the targets listed above, 
        # the PNG normalizations, real or synthetic, mat or PNG.
        # More of an assertion that we got the regex right than
        # actual checks. Also check that azimuth is between 10 
        # and 80 degrees. 
        assert target in targets
        if png_or_mat == 'png_images':
            assert qpm_or_db in png_types
        else:
            assert qpm_or_db is None 
        assert real_or_syn in real_syn
        assert png_or_mat in img_types
        assert 9.9 < azimuth < 80.1
        assert 13.9 < elevation < 17.1

        # Build the datapath tuple and remove it from the list, if
        # it is in the list.
        try:
            if png_or_mat == 'png_images':
                png_combos.remove((qpm_or_db, real_or_syn, target))
            else:
                mat_combos.remove((real_or_syn, target))
        except ValueError:
            pass
            # We already removed it. 

# Assert that the path combinations are empty.
assert len(mat_combos) == 0
assert len(png_combos) == 0

print("Count: ", count)