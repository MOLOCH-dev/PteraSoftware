## Aeroelasticity Module

The aeroelasticity module acts as a feedback loop, enabling dynamic reconfiguration of "Wing twist" parameter 
for each defined cross-section of the wing. 
Wing twist (degrees) is equivalent to the incidence angle of the cross-section, defined about the leading edge. and is
only stable upto 45 degrees.
This module represents aeroelastic feedback as torsion about the leading edge.

Pictured below is the Aeroelastic Feedback loop 
![Aeroelasticity Feedback Loop](assets/aeroelastic_feedback.png)
Where,
![Aeroelastic Feedback Variables](assets/aeroelastic_feedback_variables.png)

### Functions
#### [calculate_aeroelastic_response](https://github.com/MOLOCH-dev/PteraSoftware/blob/446b18ebc34f91f703c73361e0fc57323cd0b612/pterasoftware/unsteady_ring_vortex_lattice_method.py#L1815)
This function :
- Obtains current aerodynamic forces from PteraSoftware's U.V.L.M. solver
![UVLM Forces](assets/uvlm_forces.JPG)
- Obtains linear acceleration along panel normal of every panel's collocation point
![Panel Acceleration](assets/panel_acceleration.JPG)
- Obtains inertial force on every collocation point
![Inertial Forces](assets/inertial_forces.JPG)
- Runs convergence loop to obtain torsion angle of each cross-section due to aerodynamic and inertial forces
![Torsion Angle](assets/torsion_angle_pseudocode.JPG)
- Redefines wing for current timestep ([function : create_new_wing()](https://github.com/MOLOCH-dev/PteraSoftware/blob/446b18ebc34f91f703c73361e0fc57323cd0b612/pterasoftware/unsteady_ring_vortex_lattice_method.py#L1953))

### Overall code flow
![Algorithm flow](assets/algo_flow.JPG)