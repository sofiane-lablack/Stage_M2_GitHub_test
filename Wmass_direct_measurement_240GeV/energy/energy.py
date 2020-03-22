from logging import getLogger
from numpy import matrix, dot
from numpy.linalg import solve, pinv

_logger = getLogger(__name__)


def beta(direction, energy):

    if energy == 0:
        _logger.critical("The energy is null")
        return 0

    return direction/energy


def get_beta_matrix(p4):
    """Determine the beta matrix for the E computation"""

    b_E = []
    b_x = []
    b_y = []
    b_z = []

    for item in p4:
        b_E.append(beta(item.E(), item.E()))
        b_x.append(beta(item.X(), item.E()))
        b_y.append(beta(item.Y(), item.E()))
        b_z.append(beta(item.Z(), item.E()))

    _logger.debug('beta matrix : {}'.format(matrix([b_E, b_x, b_y, b_z])))

    return matrix([b_E, b_x, b_y, b_z])


def cm_matrix(Ecm, jet_dim):

    m = [0] * 4

    if jet_dim == 2:
      Ecm = Ecm/2

    m[0] = Ecm

    _logger.debug('center of mass matrix : {}'.format(m))

    return matrix(m)


def energy_from_direction(Ecm, beta_matrix, jet_dim):

    cm = cm_matrix(Ecm, jet_dim)

    if beta_matrix.shape == (jet_dim, jet_dim):
        E = solve(beta_matrix, cm.getT())
    else:
      beta_inv = pinv(matrix(beta_matrix))
      E = dot(beta_inv, cm.getT())

    _logger.debug('Energy computed from direction: {}'.format(E))

    return E


if __name__ == '__main__':
    pass
