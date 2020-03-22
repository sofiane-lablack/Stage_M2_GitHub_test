from logging import getLogger
_logger = getLogger(__name__)


def rescaling_factor(new_E, old_E):
    return new_E/old_E


def factor(new_en, p4):

    factors = []

    for idx, en in enumerate(new_en):
        # float() to remove the matrix type
        factors.append(float(rescaling_factor(en, p4[idx].E())))

    return factors


def rescale(p4, alpha):

    lvec_resc_array = []

    for idx, item in enumerate(p4):
        lvec_resc_array.append(item*alpha[idx])

    return lvec_resc_array