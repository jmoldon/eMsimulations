import numpy as np
import glob
import argparse

# Read inputs file
parser = argparse.ArgumentParser()
parser.add_argument("-i",dest='inputsfile', help="Name of inputs file",
                    type=str)

args, unknown = parser.parse_known_args()
inputsfile = args.inputsfile
execfile(inputsfile)


# Function definitions
debug = False

def add_component(cl, c):
    cl.addcomponent(dir=c['direction'], flux=c['flux'], fluxunit='Jy',
                    freq=c['freq'], shape="Gaussian", majoraxis=c['bmaj'],
                    minoraxis=c['bmin'], positionangle=c['bpa'],
                    spectrumtype='spectral index', index = c['spectrum'])
    return cl

def prepare_model(sim, cl=cl):
    modelspath = sim['modelspath']
    if modelspath[-1] != '/': modelspath += '/'
    try: os.mkdir(sim['modelspath'])
    except: pass
    print 'Generating model...'
    model = simulation['model']
    name     = model['name']
    #os.system('rm -rf {0}.cl'.format(name))
    os.system('rm -rf {0}/{1}.cl'.format(modelspath, name))
    os.system('rm -rf {0}/{1}.im'.format(modelspath, name))
    os.system('rm -rf {0}/{1}.fits'.format(modelspath, name))
    cl.done()
    for comp in model['comps'].keys():
        if debug: print 'Adding component...'
        if debug: print  model['comps'][comp]
        cl = add_component(cl, model['comps'][comp])
    cl.rename(modelspath+'{}.cl'.format(name))
    cl.done()
    return


def modelimage(sim, msin):
    print 'Running modelimage ', sim['model']['name']
    prepare_model(sim)
    chanwidth_mhz = 1000.*float(sim['ms'][msin]['bandwidth_ghz'])/sim['ms'][msin]['nchan']
    modelspath = sim['modelspath']
    cl.done()
    cl.open(modelspath+'{}.cl'.format(sim['model']['name']))
    name     = sim['ms'][msin]['name']
    imsize   = sim['ms'][msin]['imsize']
    nchan    = sim['ms'][msin]['nchan']
    cellsize = sim['ms'][msin]['cellsize']
    reffreq  = sim['ms'][msin]['freqcenter']
    chan     = str(chanwidth_mhz)+'MHz'
    ra       = sim['ms'][msin]['ra']
    dec      = sim['ms'][msin]['dec']
    os.system('rm -rf {0}/{1}.im'.format(modelspath, name))
    os.system('rm -rf {0}/{1}.fits'.format(modelspath, name))
    ia.done()
    ia.fromshape(modelspath+"{}.im".format(name),[imsize,imsize,1,nchan],overwrite=True)
    cs=ia.coordsys()
    cs.setunits(['rad','rad','','Hz'])
    cell_rad=qa.convert(qa.quantity(cellsize),"rad")['value']
    cs.setincrement([-cell_rad,cell_rad],'direction')
    cs.setreferencevalue([qa.convert(ra,'rad')['value'],qa.convert(dec,'rad')['value']],type="direction")
    cs.setreferencevalue(reffreq,'spectral')
    cs.setincrement(chan,'spectral')
    ia.setcoordsys(cs.torecord())
    ia.setbrightnessunit("Jy/pixel")
    ia.modify(cl.torecord(),subtract=False)
    imfile = modelspath+'{}.im'.format(name)
    fitsfile = modelspath+'{}.fits'.format(name)
    print 'Model saved in : {0}, {1}'.format(imfile, fitsfile)
    exportfits(imagename=imfile, fitsimage=fitsfile,overwrite=True)
    cl.done()
    ia.done()

def compute_noise(delta_nu_hz, delta_t_s, diameter, tsys):
    """ This computes the noise per visibility given an integration time """
    aperture_eff = 0.7
    aeff_over_tsys = aperture_eff * ( pi * (diameter / 2.0)**2.0 ) / tsys
    # Thompson, Moran and Swenson, 2nd Edition, Equation 6.50
    k_boltzmann = 1.3806503e-23 # Boltzmann's constant
    # Efficiency terms are ALL subsumed into aeff_over_tsys
    noise = (2**0.5 * k_boltzmann) / (((delta_nu_hz * delta_t_s)**0.5) * aeff_over_tsys * 1.0e-26)
    return noise

def include_noise(msfile, delta_nu_hz, delta_t_s, diameter, tsys):
    noise = compute_noise(delta_nu_hz, delta_t_s, diameter, tsys)
    sm.openfromms(msfile)
    sm.setnoise(mode = 'simplenoise', simplenoise = str(noise)+'Jy')
    sm.corrupt()
    sm.done()
    return noise

def flag_LoMk2(msfile):
    try:
        flagdata(vis=msfile, antenna='*Lo&*Mk2')
    except:
        pass
    return

def run_simobserve(simulation, msin):
    try:
        os.mkdir(simulation['msfilespath'])
    except: pass
    modelimage(simulation, msin)
    name     = simulation['ms'][msin]['name']
    msfilespath = simulation['msfilespath']
    msfile = simulation['ms'][msin]
    indirection = 'J2000 {0} {1}'.format(msfile['ra'], msfile['dec'])
    chanwidth_mhz = 1000.*float(msfile['bandwidth_ghz'])/msfile['nchan']
    cwd0 = os.getcwd()
    os.chdir(msfilespath)
    try: shutil.rmtree(name)
    except: pass
    print 'Generating UVdata with:'
    print 'Model: {}'.format(simulation['modelspath']+'{}.fits'.format(name))
    print 'Center frequency: {0}'.format(msfile['freqcenter'])
    print 'Num. channels:    {0}'.format(msfile['nchan'])
    print 'Chanwidth:        {0:6.3f} MHz'.format(chanwidth_mhz,)
    print 'Total BW:         {0} GHz'.format(msfile['bandwidth_ghz'])
    print 'Generating MS data...'
    simobserve(project = msfile['name'],
    skymodel     = simulation['modelspath']+'{}.fits'.format(name),
    indirection  = indirection,
    incenter     = msfile['freqcenter'],
    inwidth      = str(chanwidth_mhz) + 'MHz',
    hourangle    = msfile['hourangle'],
    totaltime    = msfile['totaltime'],
    integration  = str(msfile['integration_s'])+'s',
    antennalist  = msfile['antennalist'],
    thermalnoise = '',
    graphics     = 'none')
    os.chdir(cwd0)
    msfilename = glob.glob(msfilespath + name + '/*ms')[0]

    # Include noise in the data
    print 'Including random noise in the visibilities...'
    delta_nu_hz = chanwidth_mhz * 1e6
    delta_t_s = msfile['integration_s']
    diameter = float(msfile['diameter_mean_m'])
    tsys = float(msfile['tsys_K'])
    noise = include_noise(msfilename, delta_nu_hz, delta_t_s, diameter, tsys)
    print 'Noise added per visibility {0:10.6f} Jy'.format(noise)
    print 'Produced MS file in: {0}/'.format(msfilename)

    # Flag Lo-Mk2 baseline
    flag_LoMk2(msfilename)
    return


def run_clean(simulation, msin, img):
    print 'Running clean '+simulation['ms'][msin]['name']
    msfilespath = simulation['msfilespath']
    msfile = glob.glob(msfilespath+simulation['ms'][msin]['name']+'/*ms')[0]
    filename = os.path.split(msfile)[-1][:-3]
    image = simulation['ms'][msin]['images'][img]
    try: os.mkdir(simulation['imagespath']+filename)
    except: pass
    i = simulation['ms'][msin]['images'][img]['num']
    imagename = simulation['imagespath']+filename+'/'+ filename+'_{0:02.0f}'.format(i)
    try: shutil.rmtree(imagename+'*')
    except: pass
    clean(vis = msfile,
    imagename = imagename,
    nterms = image['nterms'],
    mode = 'mfs',
    niter = image['niter'],
    gain = image['gain'],
    weighting = image['weighting'],
    robust = image['robust'],
    threshold = image['threshold'],
    multiscale = image['multiscale'],
    imsize = image['imsize'],
    cell = image['cell'],
    #interactive =True,
    mask = '/mirror2/scratch/jmoldon/emerlin/support/img_simulations/sim1.mask')
    #mask = image['mask'])
    return

def run_cleans(simulation, msin):
    try: os.mkdir(simulation['imagespath'])
    except: pass
    for img in simulation['ms'][msin]['images'].keys():
        run_clean(simulation, msin, img)


try: os.mkdir(simulation['global_path'])
except: pass
shutil.copy(inputsfile, simulation['global_path'])


print 'Using inputs file: ' + inputsfile
for msin in sorted(simulation['ms'].keys()):
    if do_simulation:
        run_simobserve(simulation, msin)
    if do_imaging:
        run_cleans(simulation, msin)

