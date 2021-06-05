import numpy as np
from StructuralAnalysis.FrameElements.Element import Element


class TwoDimensionalFrameElement(Element):
    """
    This class inherits from Element.
    properties:
        self._degrees_of_freedom: 6 degrees of freedom (3 per node) - 2D element
    """

    def __init__(self, start_node, end_node, section, material, length):
        super().__init__(start_node, end_node, section, material, length)

    def _local_matrix(self):
        l = self.length
        a = self.section.area
        e = self.material.elasticity_modulus
        i = self.section.inertia_z
        aa = a * e / l
        ba = 12 * e * i / (l ** 3)
        ca = 6 * e * i / (l ** 2)
        da = 4 * e * i / l
        ea = 2 * e * i / l
        return np.array([[aa, 0, 0, -aa, 0, 0],
                         [0, ba, ca, 0, -ba, ca],
                         [0, ca, da, 0, -ca, ea],
                         [-aa, 0, 0, aa, 0, 0],
                         [0, -ba, -ca, 0, ba, -ca],
                         [0, ca, ea, 0, -ca, da]])

    def _transformation_matrix(self):
        x_diff = self.end_node.x - self.start_node.x
        y_diff = self.end_node.y - self.start_node.y

        cs = x_diff / self.length
        sn = y_diff / self.length

        return np.array([[cs, sn, 0, 0, 0, 0],
                        [-sn, cs, 0, 0, 0, 0],
                        [0, 0, 1, 0, 0, 0],
                        [0, 0, 0, cs, sn, 0],
                        [0, 0, 0, -sn, cs, 0],
                        [0, 0, 0, 0, 0, 1]])

    def shape_function_matrix(self, x):
        le = self.length
        n1 = 1 - x / le
        n2 = x / le
        n3 = 1 - 3 * (x / le) ** 2 + 2 * (x / le) ** 3
        n4 = 3 * (x / le) ** 2 - 2 * (x / le) ** 3
        n5 = x * (1 - x / le) ** 2
        n6 = x * ((x / le) ** 2 - x / le)

        return np.array([[n1, 0, 0, 0, 0, 0, n2, 0, 0, 0, 0, 0],
                        [0, n3, 0, 0, 0, n5, 0, n4, 0, 0, 0, n6]])

    def local_end_displacements(self):
        global_displacements = np.array([dof.displacement for dof in self.degrees_of_freedom])
        return np.dot(self._transformation_matrix(), global_displacements)

    @property
    def degrees_of_freedom(self):
        return [self.start_node.dof_1,
                self.start_node.dof_2,
                self.start_node.dof_3,
                self.end_node.dof_1,
                self.end_node.dof_2,
                self.end_node.dof_3]

    @property
    def matrix(self):
        return np.dot(np.dot(self._transformation_matrix().T, self._local_matrix()),
                      self._transformation_matrix())

    @property
    def elastic_geometric_matrix(self):
        return None
