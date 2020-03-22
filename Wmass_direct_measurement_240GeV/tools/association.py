"""This file associates the jet to the corresponding parton. The association is done by comparison
   between the jet axis and the parton axis"""


def object_association(list_obj1, list_obj2):
    """Association of each jet to the corresponding parton"""

    pair_assoc = []

    while list_obj1:

        a_min = 100
        pair_min = ()

        for iobj1, obj1 in enumerate(list_obj1):
            for iobj2, obj2 in enumerate(list_obj2):
                a = obj1.get_p4().Angle(obj2.get_p4().Vect())

                if a <= a_min:
                    a_min = a
                    pair_min = (obj1, obj2)

        pair_assoc.append(pair_min)
        list_obj1.remove(pair_min[0])
        list_obj2.remove(pair_min[1])

    return pair_assoc
