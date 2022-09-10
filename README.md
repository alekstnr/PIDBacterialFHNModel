# PID Bacterial FHN Model
Bacterial FHN model including PID control in Python and MATLAB.

This project is developed from the work by the [Asally lab at the University of Warwick](https://gitlab.com/asally-lab/bacteral-fhn-model)

The publication for this work will be published on BioRxiv shortly.

## Known issues 

The equations for the model both in the Python and Matlab implementations do not represent the actual model equations correctly: the external stimulus should be provided as dI/dt not just I. 

The PID in the Python implementation does not behave correctly. 
