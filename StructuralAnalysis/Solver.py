from StructuralAnalysis.__SolverHelper import *
from StructuralAnalysis import Structure
import warnings
import sys


def analyze_first_order_elastic(structure: Structure, forces_array):
    global_matrix = global_elastic_matrix(structure)
    ff, fs, sf, ss = partition_global_matrix(structure, global_matrix)
    support_settlements = restrained_displacement_vector(structure)
    external_force_vector = force_vector(structure)

    __print_input_to_txt(structure)
    displacements = solve_for_displacements(structure, ff, fs, support_settlements, external_force_vector)
    reactions = solve_for_reactions(structure, displacements, support_settlements, sf, ss)
    __print_results_to_txt(structure, forces_array)
    print("*********DISPLACEMENTS***********")
    print(displacements)
    print("***********REACTIONS*************")
    print(reactions)


def analyze_second_order_elastic(structure: Structure):
    pass


def analyze_first_order_inelastic(structure: Structure):
    pass


def analyze_second_order_inelastic(structure: Structure):
    pass


def __print_input_to_txt(structure: Structure):
    txt = open("Input.txt", "w+")
    txt.truncate(0)
    txt.writelines("########################### INPUT ###########################\n\n")

    txt.writelines("******* NODES *******\n")
    txt.writelines("Node ID\t\t\tX\t\t\t\t\t\tY\t\t\t\t\t\tZ\n")
    for node in structure.nodes:
        txt.writelines("%d\t\t\t%.2e\t\t\t\t\t\t%.2e\n" % (node.id, node.x, node.y))

    txt.writelines("\n")
    txt.writelines("******* ELEMENTS *******\n")
    txt.writelines("Element ID\t\t\tStart Node\t\t\tEnd Node\n")
    for element in structure.elements:
        txt.writelines("%d\t\t\t\t%d\t\t\t\t%d\n" % (element.id, element.start_node.id, element.end_node.id))
    txt.writelines("\n")
    txt.writelines("******* BOUNDARY CONDITIONS *******\n")
    txt.writelines("True: Restrained, False: Free\n")
    txt.writelines("Node ID\t\tX-Disp.\t\tY-Disp.\t\tRot.\n")
    for node in structure.nodes:
        txt.writelines("%d\t\t%.2e\t\t%.2e\t\t%.2e\n" %
                       (node.id, node.dof_1.restrained, node.dof_2.restrained,
                        node.dof_3.restrained))
    txt.writelines("\n")
    txt.writelines("******* INITIAL SETTLEMENT *******\n")
    txt.writelines("Node ID\t\tX-Disp.\t\tY-Disp.\t\tRot.\n")
    for node in structure.nodes:
        txt.writelines("%d\t\t%.2e\t\t%.2e\t\t%.2e\n" %
                       (node.id, node.dof_1.displaced, node.dof_2.displaced,
                        node.dof_3.displaced))
    txt.writelines("\n")
    txt.writelines("******* APPLIED FORCES *******\n")
    txt.writelines("Node ID\t\tFX.\t\tFY.\t\tM\n")
    for node in structure.nodes:
        txt.writelines("%d\t\t%.2e\t\t%.2e\t\t%.2e\n" %
                       (node.id, node.dof_1.force, node.dof_2.force,
                        node.dof_3.force))
    txt.close()


def __print_results_to_txt(structure: Structure, forces_array):
    txt = open("Results.txt", "w+")
    txt.truncate(0)
    txt.writelines("########################### OUTPUT ###########################\n\n")

    txt.writelines("\n")
    txt.writelines("******* DISPLACEMENTS *******\n")
    txt.writelines("Node ID\t\t\tX-Disp.\t\t\t\tY-Disp.\t\t\t\tRotation.\n")
    for node in structure.nodes:
        txt.writelines("%d\t\t\t  %.2e\t\t\t  %.2e\t\t\t  %.2e\t\t\t  \n" %
                       (node.id, node.dof_1.displaced, node.dof_2.displaced,
                        node.dof_3.displaced))
    txt.writelines("\n")
    txt.writelines("******* REACTIONS *******\n")
    txt.writelines("Node ID\t\t\tFX.\t\t\t\tFY.\t\t\t\tM\n")
    for node in structure.nodes:
        txt.writelines("%d\t\t\t  %.2e\t\t\t  %.2e\t\t\t  %.2e\t\t\t\n" %
                       (node.id, node.dof_1.force, node.dof_2.force,
                        node.dof_3.force))

    txt.writelines("\n")
    txt.writelines("******* Final Reactions2 *******\n")
    txt.writelines("")

    final_reactions = []
    for node in structure.nodes:
        final_reactions.extend((node.dof_1.force, node.dof_2.force,
                                node.dof_3.force))
    result = np.array(final_reactions) - np.array(forces_array)

    txt.writelines("{}".format(np.array_str(result, max_line_width=np.inf)))
    txt.close()
