from StructuralAnalysis import Node, Structure, Section, Material, Solver
from StructuralAnalysis.FrameElements import *
# General considerations:
#    - y-axis is upward
#    - use consistent units
#    - each node has 3 degrees of freedom

# Parameters for Stress Calculation (This will be needed at the end for the stress calculation)
area = 0.00391
center_of_gravity = 1
inertia_z = 3.892 * (10 ** -5)

# create node objects <Node(x, y)>
n1 = Node(0, 0)
n2 = Node(0, 4)
n3 = Node(0, 7)
n4 = Node(0, 10)
n5 = Node(0, 13)
n6 = Node(0, 16)
n7 = Node(6, 16)
n8 = Node(6, 13)
n9 = Node(6, 10)
n10 = Node(6, 7)
n11 = Node(6, 4)
n12 = Node(6, 0)


# create section object
I_section = Section.ArbitrarySection(area=0.00391, inertia_y=2.840 * (10 ** -6), inertia_z=3.892 * (10 ** -5),
                                     polar_inertia=0.00003892, warping_rigidity=0.0374)

# create material object
steel = Material.Steel(yield_strength=700, ultimate_strength=1000, elasticity_modulus=210000000, poissons_ratio=0.3)

# create frame element objects <FrameElement(start_node: Node, end_node: Node, section: Section, material: Material)>
e1 = TwoDimensionalFrameElement(n1, n2, I_section, steel, length=4)
e2 = TwoDimensionalFrameElement(n2, n11, I_section, steel, length=6)
e3 = TwoDimensionalFrameElement(n11, n12, I_section, steel, length=4)
e4 = TwoDimensionalFrameElement(n2, n3, I_section, steel, length=3)
e5 = TwoDimensionalFrameElement(n3, n10, I_section, steel, length=6)
e6 = TwoDimensionalFrameElement(n10, n11, I_section, steel, length=3)
e7 = TwoDimensionalFrameElement(n3, n4, I_section, steel, length=3)
e8 = TwoDimensionalFrameElement(n4, n9, I_section, steel, length=6)
e9 = TwoDimensionalFrameElement(n9, n10, I_section, steel, length=3)
e10 = TwoDimensionalFrameElement(n4, n5, I_section, steel, length=3)
e11 = TwoDimensionalFrameElement(n5, n8, I_section, steel, length=6)
e12 = TwoDimensionalFrameElement(n8, n9, I_section, steel, length=3)
e13 = TwoDimensionalFrameElement(n5, n6, I_section, steel, length=3)
e14 = TwoDimensionalFrameElement(n6, n7, I_section, steel, length=6)
e15 = TwoDimensionalFrameElement(n7, n8, I_section, steel, length=3)

# assign boundary conditions; node_1 and node_12 are fixed


n1.dof_1.restrained = True
n1.dof_2.restrained = True
n1.dof_3.restrained = True


n12.dof_1.restrained = True
n12.dof_2.restrained = True
n12.dof_3.restrained = True

# assign loads (in kN)

# Force
n2.dof_2.force = -165.6
n2.dof_3.force = -165.6
n3.dof_2.force = -165.6
n3.dof_3.force = -165.6
n4.dof_2.force = -165.6
n4.dof_3.force = -165.6
n5.dof_2.force = -165.6
n5.dof_3.force = -165.6
n6.dof_2.force = -122.4
n6.dof_3.force = -122.4
n7.dof_2.force = -122.4
n7.dof_3.force = 122.4
n8.dof_2.force = -165.6
n8.dof_3.force = 165.6
n9.dof_2.force = -165.6
n9.dof_3.force = 165.6
n10.dof_2.force = -165.6
n10.dof_3.force = 165.6
n11.dof_2.force = -165.6
n11.dof_3.force = 165.6



# create structure object
structure = Structure([e1, e2, e3, e4, e5, e6, e7, e8, e9, e10, e11, e12, e13, e14, e15])

forces_array = []
for node in structure.nodes:
    forces_array.extend((node.dof_1.force, node.dof_2.force,
                         node.dof_3.force))

# run first_order_elastic analysis
Solver.analyze_first_order_elastic(structure, forces_array, area, center_of_gravity, inertia_z, "resultsAHSS.txt")



