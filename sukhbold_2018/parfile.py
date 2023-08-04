
p = '/mnt/research/SNAPhU/STIR/sukhbold_2018/progenitors/sukhbold_2018_{zams}.FLASH'
flash4 = '/mnt/research/SNAPhU/zac/BANG/obj/obj_sn1987a/flash4'
SFHo.h5 = '/mnt/research/SNAPhU/Tables/SFHo.h5'
NuLib_SFHo.h5 = '/mnt/research/SNAPhU/Tables/NuLib_SFHo_noweakrates_rho82_temp65_ye60_ng12_ns3_Itemp65_Ieta61_version1.0_20170719.h5'

def write_parfile(filepath,
                  zams,
                  dat_steps=100,
                  chk_time=0.1,
                  tmax=1.0):
    """Write .par file
    """
    par_str = get_parfile_str(zams=zams,
                              dat_steps=dat_steps,
                              chk_time=chk_time,
                              tmax=tmax)

    with open(filepath, 'w') as f:
        f.write(par_str)


def get_parfile_str(zams,
                    dat_steps=100,
                    chk_time=0.1,
                    tmax=1.0):
    """Return str of parfile contents

    parameters
    ----------
    zams : str
    dat_steps :str
    chk_time : str
    tmax : str
    """
    par_str = f"""# Parameters file for 1D M1 Core Collapse with MLT
basenm                  = "run_s18_stir2020_{zams}_"
restart                 = False
checkpointFileNumber    = 0
plotFileNumber          = 0
output_directory        = "output"

# IO
wr_integrals_freq              = {dat_steps}
checkpointFileIntervalStep     = 0
checkpointFileIntervalTime     = {chk_time}
plotFileIntervalStep           = 0
plotFileIntervalTime           = 0.00
wall_clock_time_limit          = 172800

# Time
tinitial               = 0.0
tmax                   = {tmax}
nend                   = 1000000000
tstep_change_factor    = 1.05
dtinit                 = 1e-8
dtmax                  = 1e5
dtmin                  = 1e-20

# Domain
geometry            = "spherical"
xmin                = 0.0
xmax                = 3.0e9
xl_boundary_type    = "reflect"
xr_boundary_type    = "user"

# Grid/Refinement
nblockx                     = 15
nblocky                     = 1
nblockz                     = 1
gr_lrefineMaxRedDoByLogR    = True
gr_angularResolution        = 0.5
fullangrefrad               = 300e5
lrefine_max                 = 10
lrefine_min                 = 1
refine_var_1                = "dens"
refine_var_2                = "pres"
refine_var_3                = "entr"
refine_var_4                = "none"
refine_cutoff_1             = 0.8
refine_cutoff_2             = 0.8
refine_cutoff_3             = 0.8
refine_cutoff_4             = 0.8

# Simulation
model_file           = "sukhbold_2018_{zams}.FLASH"
nsub                 = 4
vel_mult             = 1.0
ener_exp             = 0.0
r_exp_max            = 0.0
r_exp_min            = 0.0
mass_loss            = 1.0e-4
vel_wind             = 1.0e4
use_PnotT            = False
rot_a                = 8.0e7
rot_omega            = 0.
mag_e                = 1.0e18
mri_refine           = False
mri_time             = 0.0
alwaysRefineShock    = False

# Hydro
useHydro             = True
cfl                  = 0.5
interpol_order       = 2
updateHydroFluxes    = True
eintSwitch           = 0.0

# Solver
cvisc                = 0.2
use_flattening       = True
use_steepening       = False
flux_correct         = True
use_hybridRiemann    = True

# Gravity
useGravity                    = True
updateGravity                 = True
grav_boundary_type            = "isolated"
mpole_3daxisymmetry           = False
mpole_dumpMoments             = False
mpole_PrintRadialInfo         = False
mpole_IgnoreInnerZone         = False
mpole_lmax                    = 0
mpole_ZoneRadiusFraction_1    = 1.0
mpole_ZoneExponent_1          = 0.005
mpole_ZoneScalar_1            = 0.5
mpole_ZoneType_1              = "logarithmic"
point_mass                    = 0.0
point_mass_rsoft              = 0.e0
mpole_useEffectivePot         = True
mpole_EffPotNum               = 1000

#MLT
useMLT        = True
mlt_alphaL    = 1.25
mlt_Dneut     = 0.166666666667
mlt_Dye       = 0.166666666667
mlt_Deint     = 0.166666666667
mlt_Detrb     = 0.166666666667
mlt_dtFac     = 0.5

# EOS
eos_file       = "./SFHo.h5"
eosMode        = "dens_ie"
eosModeInit    = "dens_temp"
gamma          = 1.2

# RadTrans/M1
rt_useRadTrans    = True
rt_opacTable      = "./NuLib_SFHo.h5"
rt_NumGroups      = 12
rt_dtFactor       = 0.6
rt_rkTime         = True
rt_doVel          = True
rt_doIES          = True

# Small numbers
smallt    = 1.2e8
smlrho    = 1.1e3
smallp    = 1e-20
smalle    = 1e1
smallu    = 1e-10
smallx    = 1e-100
small     = 1e-100
"""
    return par_str
