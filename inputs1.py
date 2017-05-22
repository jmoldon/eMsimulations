global_path = '/mirror2/scratch/jmoldon/emerlin/support/img_simulations/test/'

do_simulation = True
do_imaging = True

###  Info on arrays
array_path = '/mirror2/scratch/jmoldon/emerlin/support/img_simulations/antennalist/'
antennalist = {}
antennalist = {'e-MERLIN' : array_path+'e-MERLIN.cfg',
               'e-MERLIN_goon' : array_path+'e-MERLIN_goon.cfg',
               'vla.a'  : 'vla.a.cfg',
               'vla.b'  : 'vla.b.cfg',
               'vla.bna': 'vla.bna.cfg',
               'vla.c'  : 'vla.c.cfg',
               'vla.cnb': 'vla.cnb.cfg',
               'vla.d'  : 'vla.d.cfg',
               'vla.dnc': 'vla.dnc.cfg',
               'vlba'   : 'vlba.cfg'}

###  Initialize simulation and paths
simulation = {}

simulation['global_path'] = global_path
simulation['modelspath'] = global_path+'models/'
simulation['msfilespath'] = global_path+'msdata/'
simulation['imagespath'] = global_path+'imgsim/'

###  Model using components
simulation['model'] = {}
simulation['model']['name'] = 'disk_core'
simulation['model']['comps'] = {}
simulation['model']['comps']['core1'] = {'direction':"J2000 10h00m00.060s 40d00m00.700s",
                           'flux': 0.001,
                           'freq': '2.3GHz',
                           'bmaj': '0.08arcsec',
                           'bmin': '0.08arcsec',
                           'bpa': '0deg',
                           'spectrum': 0}
simulation['model']['comps']['disk2'] = {'direction':"J2000 10h00m00.060s 40d00m00.750s",
                           'flux': 0.001,
                           'freq': '2.0GHz',
                           'bmaj': '0.4arcsec',
                           'bmin': '0.1arcsec',
                           'bpa': '60deg',
                           'spectrum': +2.0}


simulation['ms'] = {}

###################### e-EMERLIN / L band / 0.5 GHz BW /  512  ######################
simulation['ms']['L'] = {'name': 'Lband',
                          'freqcenter': '1.5GHz',
                          'bandwidth_ghz':0.5,
                          'nchan': 512,
                          'integration_s': 30,
                          'totaltime': '16h',
                          'hourangle': '-1:00:00',
                          'ra': "10h00m00.05s",
                          'dec': "40d00m00.600s",
                          'tsys_K': 50,
                          'diameter_mean_m': 25,
                          'antennalist': antennalist['e-MERLIN'],
                          'imsize': 512, # Only used to generate the model
                          'cellsize': '0.004arcsec'} # Only used to generate the model

simulation['ms']['L']['images'] = {}
simulation['ms']['L']['images']['img1'] = {'num': 1,
                                             'nterms': 1,
                                             'multiscale': [0, 10],
                                             'imsize': [512,512],
                                             'cell': '0.016arcsec',
                                             'weighting': 'briggs',
                                             'robust': 0.5,
                                             'gain': 0.05,
                                             'niter': 1000,
                                             'threshold': '0.01mJy',
                                             'mask' : ''}

###################### e-EMERLIN / S band / 2 GHz BW /  512  ######################
simulation['ms']['S'] = {'name': 'Sband',
                          'freqcenter': '3.0GHz',
                          'bandwidth_ghz':2,
                          'nchan': 512,
                          'integration_s': 30,
                          'totaltime': '16h',
                          'hourangle': '-1:00:00',
                          'ra': "10h00m00.05s",
                          'dec': "40d00m00.600s",
                          'tsys_K': 50,
                          'diameter_mean_m': 25,
                          'antennalist': antennalist['e-MERLIN'],
                          'imsize': 512, # Only used to generate the model
                          'cellsize': '0.004arcsec'} # Only used to generate the model

simulation['ms']['S']['images'] = {}
simulation['ms']['S']['images']['img1'] = {'num': 1,
                                             'nterms': 1,
                                             'multiscale': [0, 10],
                                             'imsize': [1024,1024],
                                             'cell': '0.008arcsec',
                                             'weighting': 'briggs',
                                             'robust': 0.0,
                                             'gain': 0.05,
                                             'niter': 5000,
                                             'threshold': '0.01mJy',
                                             'mask' : ''}

###################### e-EMERLIN / C band / 2 GHz BW /  512  ######################
simulation['ms']['C'] = {'name': 'Cband',
                          'freqcenter': '6GHz',
                          'bandwidth_ghz':2,
                          'nchan': 512,
                          'integration_s': 30,
                          'totaltime': '16h',
                          'hourangle': '-1:00:00',
                          'ra': "10h00m00.05s",
                          'dec': "40d00m00.600s",
                          'tsys_K': 50,
                          'diameter_mean_m': 25,
                          'antennalist': antennalist['e-MERLIN'],
                          'imsize': 512, # Only used to generate the model
                          'cellsize': '0.004arcsec'} # Only used to generate the model

simulation['ms']['C']['images'] = {}
simulation['ms']['C']['images']['img1'] = {'num': 2,
                                             'nterms': 1,
                                             'multiscale': [0, 25],
                                             'imsize': [2048,2048],
                                             'cell': '0.004arcsec',
                                             'weighting': 'briggs',
                                             'robust': 0.0,
                                             'gain': 0.05,
                                             'niter': 5000,
                                             'threshold': '0.01mJy',
                                             'mask' : ''}

###################### e-EMERLIN / X band / 2 GHz BW /  512  ######################
simulation['ms']['X'] = {'name': 'Xband',
                          'freqcenter': '12GHz',
                          'bandwidth_ghz':2,
                          'nchan': 512,
                          'integration_s': 30,
                          'totaltime': '16h',
                          'hourangle': '-1:00:00',
                          'ra': "10h00m00.05s",
                          'dec': "40d00m00.600s",
                          'tsys_K': 50,
                          'diameter_mean_m': 25,
                          'antennalist': antennalist['e-MERLIN'],
                          'imsize': 512, # Only used to generate the model
                          'cellsize': '0.004arcsec'} # Only used to generate the model

simulation['ms']['X']['images'] = {}
simulation['ms']['X']['images']['img1'] = {'num': 1,
                                             'nterms': 1,
                                             'multiscale': [0, 25, 50],
                                             'imsize': [4096,4096],
                                             'cell': '0.002arcsec',
                                             'weighting': 'briggs',
                                             'robust': 0.0,
                                             'gain': 0.05,
                                             'niter': 5000,
                                             'threshold': '0.01mJy',
                                             'mask' : ''}

###################### e-EMERLIN / K band / 2 GHz BW /  512  ######################
simulation['ms']['K'] = {'name': 'Kband',
                          'freqcenter': '22GHz',
                          'bandwidth_ghz':2,
                          'nchan': 512,
                          'integration_s': 30,
                          'totaltime': '16h',
                          'hourangle': '-1:00:00',
                          'ra': "10h00m00.05s",
                          'dec': "40d00m00.600s",
                          'tsys_K': 50,
                          'diameter_mean_m': 25,
                          'antennalist': antennalist['e-MERLIN'],
                          'imsize': 512, # Only used to generate the model
                          'cellsize': '0.004arcsec'} # Only used to generate the model

simulation['ms']['K']['images'] = {}
simulation['ms']['K']['images']['img1'] = {'num': 1,
                                             'nterms': 1,
                                             'multiscale': [0, 25, 50],
                                             'imsize': [4096,4096],
                                             'cell': '0.002arcsec',
                                             'weighting': 'briggs',
                                             'robust': 0.0,
                                             'gain': 0.05,
                                             'niter': 5000,
                                             'threshold': '0.01mJy',
                                             'mask' : ''}


####################### VLA / Ku band / 2 GHz BW /  512  ######################
#simulation['ms']['VLAKu'] = {'name': 'VLA_Ku',
#                          'freqcenter': '16GHz',
#                          'bandwidth_ghz':2,
#                          'nchan': 512,
#                          'integration_s': 30,
#                          'totaltime': '0.5h',
#                          'hourangle': '-1:00:00',
#                          'ra': "10h00m00.05s",
#                          'dec': "40d00m00.600s",
#                          'tsys_K': 50,
#                          'diameter_mean_m': 25,
#                          'antennalist': antennalist['vla.a'],
#                          'imsize': 512, # Only used to generate the model
#                          'cellsize': '0.004arcsec'} # Only used to generate the model
#
#simulation['ms']['VLAKu']['images'] = {}
#simulation['ms']['VLAKu']['images']['img1'] = {'num': 1,
#                                             'nterms': 1,
#                                             'multiscale': [0, 10],
#                                             'imsize': [512,512],
#                                             'cell': '0.016arcsec',
#                                             'weighting': 'briggs',
#                                             'robust': 0.5,
#                                             'gain': 0.05,
#                                             'niter': 1000,
#                                             'threshold': '0.01mJy',
#                                             'mask' : ''}
#
#
####################### e-EMERLIN / K band / 2 GHz BW /  512  ######################
#simulation['ms']['VLAK'] = {'name': 'VLA_K',
#                          'freqcenter': '24GHz',
#                          'bandwidth_ghz':2,
#                          'nchan': 512,
#                          'integration_s': 30,
#                          'totaltime': '0.5h',
#                          'hourangle': '-1:00:00',
#                          'ra': "10h00m00.05s",
#                          'dec': "40d00m00.600s",
#                          'tsys_K': 50,
#                          'diameter_mean_m': 25,
#                          'antennalist': antennalist['vla.b'],
#                          'imsize': 512, # Only used to generate the model
#                          'cellsize': '0.004arcsec'} # Only used to generate the model
#
#simulation['ms']['VLAK']['images'] = {}
#simulation['ms']['VLAK']['images']['img1'] = {'num': 1,
#                                             'nterms': 1,
#                                             'multiscale': [0, 10],
#                                             'imsize': [512,512],
#                                             'cell': '0.016arcsec',
#                                             'weighting': 'briggs',
#                                             'robust': 0.5,
#                                             'gain': 0.05,
#                                             'niter': 1000,
#                                             'threshold': '0.01mJy',
#                                             'mask' : ''}
#
#
#
