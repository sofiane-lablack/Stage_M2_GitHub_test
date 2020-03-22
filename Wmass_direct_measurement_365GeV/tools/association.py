"""This file associates the jet to the corresponding parton. The association is done by comparison
   between the jet axis and the parton axis"""


def object_association(list_obj1, list_obj2):
    """Association of each jet to the corresponding parton"""

    pair_assoc = []

    while list_obj1:

        a_min = 100
        pair_min = ()

        for iobj1, obj1 in enumerate(list_obj1):
            #print "list_obj1 "+str(iobj1)
            for iobj2, obj2 in enumerate(list_obj2):
                #print "list_obj2 "+str(list_obj2[iobj2])
		#print ("list_objt2 ",list_obj2[iobj2])
                a = obj1.get_p4().Angle(obj2.get_p4().Vect())
                #print "angle "+str(a)

                if a <= a_min:
                    a_min = a
                    pair_min = (obj1, obj2)
		    #print "a_min "+str(a_min)
		    #print "pair_min"+str(pair_min)
		    #print "obj1 "+str(obj1)+" obj 2 "+str(obj2)
		    #print list(list_obj2)

        pair_assoc.append(pair_min)
        #print "pair_assoc  "+str(list(pair_assoc))
        #print "lenght pair_assoc list "+str(len(pair_assoc))
        #print "pair_assoc 1"+str(pair_assoc[0])
        #print "pair_assoc 2"+str(pair_assoc[1])
        list_obj1.remove(pair_min[0])
        list_obj2.remove(pair_min[1])

    return pair_assoc

"""This file associates the jet to the corresponding parton. The association is done by comparison
   between the jet axis and the parton axis"""


def object_association_semi(list_obj1, list_obj2):
    """Association of each jet to the corresponding parton"""

    pair_assoc = []

    while list_obj1:

        a_min = 100
        pair_min = ()

        for iobj1, obj1 in enumerate(list_obj1):
            #print "list_obj1 "+str(iobj1)
            for iobj2, obj2 in enumerate(list_obj2):
                #print "list_obj2 "+str(list_obj2[iobj2])
		#print ("list_objt2 ",list_obj2[iobj2])
                a = obj1.get_p4().Angle(obj2.get_p4().Vect())
                #print "angle "+str(a)

                if a <= a_min:
                    a_min = a
                    pair_min = (obj1, obj2)
		    #print "a_min "+str(a_min)
		    #print "pair_min"+str(pair_min)
		    #print "obj1 "+str(obj1)+" obj 2 "+str(obj2)
		    #print list(list_obj2)

        pair_assoc.append(pair_min)
        #print "pair_assoc  "+str(list(pair_assoc))
        #print "lenght pair_assoc list "+str(len(pair_assoc))
        #print "pair_assoc 1"+str(pair_assoc[0])
        #print "pair_assoc 2"+str(pair_assoc[1])
        list_obj1.remove(pair_min[0])
        #list_obj2.remove(pair_min[1])

    return pair_assoc
