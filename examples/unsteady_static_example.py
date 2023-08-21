"""This is script is an example of how to run Ptera Software's unsteady ring vortex
lattice method solver on a custom airplane with static geometry. """

import pterasoftware as ps
import numpy as np
import matplotlib.pyplot as plt

cs_y_les = np.linspace(0, 3.30/10, 9)
wing_cross_sections = []
for y in cs_y_les :
    wing_cross_sections.append(
        ps.geometry.WingCrossSection(
            x_le=0.0,
            y_le=y,
            z_le=0.0,
            twist=0.0,
            control_surface_type="symmetric",
            control_surface_hinge_point=0.75,
            control_surface_deflection=0.0,
            num_spanwise_panels=1,
            spanwise_spacing="cosine",
            chord=1 / 10,
            # Every wing cross section has an airfoil object.
            airfoil=ps.geometry.Airfoil(
                name="naca0012",
                coordinates=None,
                repanel=True,
                n_points_per_side=400,
            ),
        ),
    )

example_airplane = ps.geometry.Airplane(
    name="Example Airplane",
    x_ref=0.0,
    y_ref=0.0,
    z_ref=0.0,
    s_ref=None,
    b_ref=None,
    c_ref=None,
    # All airplane objects have a list of wings.
    wings=[
        # Create the first wing object in this airplane.
        ps.geometry.Wing(
            # Give the wing a name, this defaults to "Untitled Wing".
            name="Main Wing",
            x_le=0.0,
            y_le=0.0,
            z_le=0.0,
            symmetric=True,
            num_chordwise_panels=6,
            chordwise_spacing="uniform",
            wing_cross_sections=wing_cross_sections,
        ),
    ],
)

main_wing_root_wing_cross_section_movement = ps.movement.WingCrossSectionMovement(
    # Provide the base cross-section.
    base_wing_cross_section=example_airplane.wings[0].wing_cross_sections[0],
    sweeping_amplitude=0.0,
    sweeping_period=0.0,
    sweeping_spacing="sine",
    pitching_amplitude=0.0,
    pitching_period=0.0,
    pitching_spacing="sine",
    heaving_amplitude=0.0,
    heaving_period=0.0,
    heaving_spacing="sine",
)

wing_cs_movements = []
wing_cs_movements.append(main_wing_root_wing_cross_section_movement)
for wing_cs in example_airplane.wings[0].wing_cross_sections[1:]:
    wing_cs_movements.append(
        ps.movement.WingCrossSectionMovement(
            # Provide the base cross-section.
            base_wing_cross_section=wing_cs,
            sweeping_amplitude=54/2,
            sweeping_period=1 / 5,
            sweeping_spacing="sine",
        )
    )

# Now define the main wing's movement. In addition to their wing cross sections'
# relative movements, wings' leading edge positions can move as well.
main_wing_movement = ps.movement.WingMovement(  # Define the base wing object.
    base_wing=example_airplane.wings[0],
    # Add the list of wing cross section movement objects.
    wing_cross_sections_movements=wing_cs_movements,
    # Define the amplitude of the leading edge's change in x position. This value is
    # in meters. This is set to 0.0 meters, which is the default value.
    x_le_amplitude=0.0,
    # Define the period of the leading edge's change in x position. This is set to
    # 0.0 seconds, which is the default value.
    x_le_period=0.0,
    # Define the time step spacing of the leading edge's change in x position. This
    # is "sine" by default. The options are "sine" and "uniform".
    x_le_spacing="sine",
    # Define the amplitude of the leading edge's change in y position. This value is
    # in meters. This is set to 0.0 meters, which is the default value.
    y_le_amplitude=0.0,
    # Define the period of the leading edge's change in y position. This is set to
    # 0.0 seconds, which is the default value.
    y_le_period=0.0,
    # Define the time step spacing of the leading edge's change in y position. This
    # is "sine" by default. The options are "sine" and "uniform".
    y_le_spacing="sine",
    # Define the amplitude of the leading edge's change in z position. This value is
    # in meters. This is set to 0.0 meters, which is the default value.
    z_le_amplitude=0.0,
    # Define the period of the leading edge's change in z position. This is set to
    # 0.0 seconds, which is the default value.
    z_le_period=0.0,
    # Define the time step spacing of the leading edge's change in z position. This
    # is "sine" by default. The options are "sine" and "uniform".
    z_le_spacing="sine",
)

# Delete the extraneous wing cross section movement objects, as these are now
# contained within the wing movement object. This is unnecessary, but it can make
# debugging easier.
del wing_cs_movements
del main_wing_root_wing_cross_section_movement

# Now define the airplane's movement object. In addition to their wing's and wing
# cross sections' relative movements, airplane's reference positions can move as well.
airplane_movement = ps.movement.AirplaneMovement(
    # Define the base airplane object.
    base_airplane=example_airplane,
    # Add the list of wing movement objects.
    wing_movements=[main_wing_movement],
    # Define the amplitude of the reference position's change in x position. This
    # value is in meters. This is set to 0.0 meters, which is the default value.
    x_ref_amplitude=0.0,
    # Define the period of the reference position's change in x position. This value
    # is in seconds. This is set to 0.0 seconds, which is the default value.
    x_ref_period=0.0,
    # Define the time step spacing of the reference position's change in x position.
    # This is "sine" by default. The options are "sine" and "uniform".
    x_ref_spacing="sine",
    # Define the amplitude of the reference position's change in y position. This
    # value is in meters. This is set to 0.0 meters, which is the default value.
    y_ref_amplitude=0.0,
    # Define the period of the reference position's change in y position. This value
    # is in seconds. This is set to 0.0 seconds, which is the default value.
    y_ref_period=0.0,
    # Define the time step spacing of the reference position's change in y position.
    # This is "sine" by default. The options are "sine" and "uniform".
    y_ref_spacing="sine",
    # Define the amplitude of the reference position's change in z position. This
    # value is in meters. This is set to 0.0 meters, which is the default value.
    z_ref_amplitude=0.0,
    # Define the period of the reference position's change in z position. This value
    # is in seconds. This is set to 0.0 seconds, which is the default value.
    z_ref_period=0.0,
    # Define the time step spacing of the reference position's change in z position.
    # This is "sine" by default. The options are "sine" and "uniform".
    z_ref_spacing="sine",
)

# Delete the extraneous wing movement objects, as these are now contained within the
# airplane movement object.
del main_wing_movement
# st_air = flapping_frequency*flapping_sweep*np.pi/180*wing_span/velocity_air
# Define a new operating point object. This defines the state at which the airplane
# object is operating.
example_operating_point = ps.operating_point.OperatingPoint(
    # Define the density of the fluid the airplane is flying in. This defaults to
    # 1.225 kilograms per meters cubed.
    density=1.29,
    # Define the angle of sideslip the airplane is experiencing. This defaults to 0.0
    # degrees.
    beta=0.0,
    # Define the freestream velocity at which the airplane is flying. This defaults
    # to 10.0 meters per second.
    velocity=5.0,
    # Define the angle of attack the airplane is experiencing. This defaults to 5.0
    # degrees.
    alpha=0.0,
    # Define the kinematic viscosity of the air in meters squared per second. This
    # defaults to 15.06e-6 meters squared per second, which corresponds to an air
    # temperature of 20 degrees Celsius.
    nu=15.06e-6,
)

# Define the operating point's movement. The operating point's velocity can change
# with respect to time.
operating_point_movement = ps.movement.OperatingPointMovement(
    # Define the base operating point object.
    base_operating_point=example_operating_point,
    # Define the amplitude of the velocity's change in time. This value is set to 0.0
    # meters per second, which is the default value.
    velocity_amplitude=0.0,
    # Define the period of the velocity's change in time. This value is set to 0.0
    # seconds, which is the default value.
    velocity_period=0.0,
    # Define the time step spacing of the velocity's change in time. This is "sine"
    # by default. The options are "sine" and "uniform".
    velocity_spacing="sine",
)

# Define the movement object. This contains the airplane movement and the operating
# point movement.
movement = ps.movement.Movement(
    # Add the airplane movement.
    airplane_movements=[airplane_movement],
    # Add the operating point movement.
    operating_point_movement=operating_point_movement,
    # Leave the number of time steps and the length of each time step unspecified.
    # The solver will automatically set the length of the time steps so that the wake
    # ring vortices and the bound ring vortices have approximately the same area. The
    # solver will also determine if the geometry is static or not. If it is static,
    # the number of steps will be set such that the wake extends ten chord lengths
    # back from the main wing. If the geometry isn't static, the number of steps will
    # be set such that three periods of the slowest movement oscillation complete.
    num_steps=10,
    # delta_time=0.001,
    # num_cycles=1,
)

# Delete the extraneous airplane and operating point movement objects, as these are
# now contained within the movement object.
del airplane_movement
del operating_point_movement

# Define the unsteady example problem.
example_problem = ps.problems.UnsteadyProblem(
    movement=movement,
)

# Define a new solver. The available solver objects are the steady horseshoe vortex
# lattice method solver, the steady ring vortex lattice method solver, and the
# unsteady ring vortex lattice method solver.
example_solver = ps.unsteady_ring_vortex_lattice_method.UnsteadyRingVortexLatticeMethodSolver(
    # Solvers just take in one attribute: the problem they are going to solve.
    unsteady_problem=example_problem,
)

# Delete the extraneous pointer to the problem as it is now contained within the
# solver.
del example_problem

# Run the example solver.
example_solver.run(
    # This parameter determines the detail of information that the solver's logger
    # will output while running. The options are, in order of detail and severity,
    # "Debug", "Info", "Warning", "Error", "Critical". The default value is "Warning".
    # logging_level="Warnn",
    # Use a prescribed wake model. This is faster, but may be slightly less accurate.
    prescribed_wake=False,
    calculate_streamlines=False,
)

# Call the software's draw function on the solver. Press "q" to close the plotter
# after it draws the output.
ps.output.draw(
    # Set the solver to the one we just ran.
    solver=example_solver,
    # Tell the draw function to color the aircraft's wing panels with the local lift
    # coefficient. The valid arguments for this parameter are None, "induced drag",
    # "side force", or "lift".
    scalar_type="lift",
    # Tell the draw function to show the calculated streamlines. This value defaults
    # to False.
    show_streamlines=False,
    # Tell the draw function to not show the wake vortices. This value defaults to
    # False.
    show_wake_vortices=False,
    # Tell the draw function to not save the drawing as an image file. This way,
    # the drawing will still be displayed but not saved. This value defaults to False.
    save=False,
)
#
# Call the software's animate function on the solver. This produces a GIF of the wake
# being shed. The GIF is saved in the same directory as this script. Press "q",
# after orienting the view, to begin the animation.
ps.output.animate(
    # Set the unsteady solver to the one we just ran.
    unsteady_solver=example_solver,
    # Tell the animate function to color the aircraft's wing panels with the local
    # lift coefficient. The valid arguments for this parameter are None, "induced drag",
    # "side force", or "lift".
    scalar_type="lift",
    # Tell the animate function to show the wake vortices. This value defaults to
    # False.
    show_wake_vortices=False,
    # Tell the animate function to not save the animation as file. This way,
    # the animation will still be displayed but not saved. This value defaults to
    # False.
    save=True,
)
# #
# # # Call the software's plotting function on the solver. This produces graphs of the
# # # output forces and moments with respect to time.
ps.output.plot_results_versus_time(
    # Set the unsteady solver to the one we just ran.
    unsteady_solver=example_solver,
    # Set the show attribute to True, which is the default value. With this set to
    # show, some IDEs (such as PyCharm in "Scientific Mode") will display the plots
    # in a sidebar. Other IDEs may not display the plots, in which case you should
    # set the save attribute to True, and open the files after they've been saved to
    # the current directory.
    show=True,
    save=True,
)
plt.show()

# Compare the output you see with the expected outputs saved in the "docs/examples
# expected output" directory.
