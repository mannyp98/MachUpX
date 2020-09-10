# This script is for me to test the functionality of whatever I'm working on at the moment.
import machupX as MX
import json
import numpy as np
import subprocess as sp
import matplotlib.pyplot as plt
from stl import mesh
from mpl_toolkits import mplot3d

if __name__=="__main__":
    
    # Specify input
    input_dict = {
        "solver" : {
            "type" : "nonlinear",
            "use_total_velocity" : True
        },
        "units" : "English",
        "scene" : {
            "atmosphere" : {
                "rho": [[0.0, 1.225],
                    [2000.0, 1.0066],
                    [4000.0, 0.81935],
                    ["m", "kg/m^3"]]
            }
        }
    }

    # Specify airplane
    airplane_dict = {
        "weight" : 50.0,
        "units" : "SI",
        "controls" : {
            "aileron" : {
                "is_symmetric" : False
            },
            "elevator" : {
                "is_symmetric" : True
            },
            "rudder" : {
                "is_symmetric" : False
            }
        },
        "airfoils" : {
            "NACA_4410" : "dev/NACA_4410.json",
            "NACA_0010" : "dev/NACA_0010.json"
        },
        "plot_lacs" : False,
        "wings" : {
            "main_wing" : {
                "ID" : 1,
                "side" : "both",
                "is_main" : True,
                "airfoil" : "NACA_0010",
                "semispan" : 4.0,
                "dihedral" : 5.0,
                "sweep" : 0.0,
                "twist" : 5.0,
                "control_surface" : {
                    "chord_fraction" : 0.4,
                    "root_span" : 0.55,
                    "tip_span" : 0.95,
                    "control_mixing" : {
                        "aileron" : 1.0,
                        "elevator" : 1.0
                    }
                },
                "grid" : {
                    "N" : 200,
                    "wing_ID" : 1,
                    "reid_corrections" : True
                    #"joint_length" : 2.0,
                    #"blending_distance" : 2.0
                }
            }
        }
    }

    # Specify state
    state = {
        "velocity" : 100.0,
        "alpha" : 10.0,
        "beta" : 0.0
    }

    control_state = {
        "elevator" : 0.0,
        "aileron" : 0.0,
        "rudder" : 0.0
    }

    # Load scene
    scene = MX.Scene(input_dict)
    scene.add_aircraft("plane", airplane_dict, state=state, control_state=control_state)

    #scene.display_wireframe(show_vortices=True)
    #scene.export_dxf()

    # Solve forces
    FM = scene.solve_forces(non_dimensional=False, verbose=True)
    print(json.dumps(FM["plane"]["total"], indent=4))
    scene.out_gamma()

    #scene.distributions(filename="test.dist")

    ## Get derivatives
    #derivs = scene.derivatives(wind_frame=False)
    #print(json.dumps(derivs["plane"], indent=4))

    ## Get state derivatives
    #derivs = scene.state_derivatives()
    #print(json.dumps(derivs["plane"], indent=4))