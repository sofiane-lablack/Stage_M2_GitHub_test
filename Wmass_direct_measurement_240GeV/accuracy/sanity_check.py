"""This file gather all functions used to control the computed results"""

from logging import getLogger
from numpy import dot

_logger = getLogger(__name__)


def check_energy(e_matrix, beta_matrix):
    """The test passes if the product is equals to (Ecm, 0, 0, 0)"""

    mult = dot(beta_matrix, e_matrix)
    _logger.debug("beta and energy matrices product : {}".format(mult))


def check_sum(p4):
    """The test passes if the sums of E, px, py, pz are respectively Ecm, 0, 0, 0"""

    sum_E = 0
    sum_px = 0
    sum_py = 0
    sum_pz = 0

    for item in p4:
        sum_E += item.E()
        sum_px += item.X()
        sum_py += item.Y()
        sum_pz += item.Z()

    _logger.debug("Rescaling test : sum E = {}, sum px = {}, sum py = {}, sum pz = {}".format(sum_E, sum_px, sum_py, sum_pz))
