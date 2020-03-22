''' Compute the invariant mass from the four-vector of given objects

    Example :
        lepto_mass = compute_mass(lepton, misen)
'''

def compute_mass(obj1, obj2):
    '''This function compute the invariant mass of two objects'''
    lvec_sum = obj1.get_p4() + obj2.get_p4()
    return abs(lvec_sum.M())
