# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import os
from surfer import project_volume_data


import surfer
import neuropythy as ny

import pickle
for sub in range(1,28):
    try:
        print(sub)
        fspath = os.path.abspath('p:/3018028.04/SubjectData/S{:02d}/'.format(sub))
        
        ny_file = r'm:/projects/fmri_compareAtlas/code/sub-{:02d}_desc-neuropythyRetinotopy_surface.pickle'.format(sub)
        
        # if already exists, just load it (much faster)
        if os.path.isfile(ny_file):
             with open(ny_file, "rb") as input_file:
                 (lh_retino,rh_retino)= pickle.load(input_file)
        else:
            # run the neuropythy retinotpy    
            sub_freesurfer = ny.freesurfer_subject(fspath+'Retinotopy/Freesurfer')
            (lh_retino, rh_retino) = ny.vision.predict_retinotopy(sub_freesurfer)
            
            # save it
            with open(ny_file, "wb") as output_file:
                pickle.dump((lh_retino,rh_retino), output_file)
        
        # open pysurfer
        brain = surfer.Brain('Freesurfer','lh','inflated',subjects_dir=fspath+'\Retinotopy')
        
        # neuropythy retinotopy
        brain.add_data((lh_retino.eccen<10) & (lh_retino.varea ==1),thresh=0.5,max=1.5)
        
        # freesurfer retinotopy
        brain.add_label('V1',borders=True)
        
        # load sams manual retinotopy    
        samRetinotopy = ny.load(os.path.abspath('m:/projects/fmri_compareAtlas/code/sub-{:02d}_desc-samRetinotopyV1_surface.mgh'.format(sub)))    
        brain.add_data(samRetinotopy,thresh = 0.3,max=0.02,colormap='RdPu',alpha=0.6)
        
        # view and save
        brain.show_view({'azimuth': -50, 'elevation': 100}, roll=-90,  distance=500,)
        brain.save_image(os.path.abspath('c:/users/benehi/Desktop/sub-{:02d}_desc-retinotpyComparisonV1.png'.format(sub)))
    except:
        print('failed sub {}'.format(sub))
        continue
    
#
# Unfortunately the NILEARN mapping did not work out at all
# t = surface.vol_to_surf(os.path.normpath(fspath+'Retinotopy/Anatomy/V1.nii.gz'),os.path.normpath(fspath+'Retinotopy/Freesurfer/surf/lh.pial'),radius=3,interpolation='nearest',n_samples=160)
# brain.remove_data()
# brain.add_data(t,thresh=0,colormap='YlGn')
