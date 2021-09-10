import numpy as np
from treevalue import method_treelize

from ..common import TreeObject, TreeData, ireduce


class TreeNumpy(TreeData):
    """
    Overview:
        Real numpy tree.
    """

    @method_treelize(return_type=TreeObject)
    def tolist(self: np.ndarray):
        return self.tolist()

    @property
    @ireduce(sum)
    @method_treelize(return_type=TreeObject)
    def size(self: np.ndarray) -> int:
        return self.size

    @property
    @ireduce(sum)
    @method_treelize(return_type=TreeObject)
    def nbytes(self: np.ndarray) -> int:
        return self.nbytes

    @ireduce(sum)
    @method_treelize(return_type=TreeObject)
    def sum(self: np.ndarray, *args, **kwargs):
        return self.sum(*args, **kwargs)
