var1input="/afs/cern.ch/user/s/slablack/fcc/heppy/ee_qq_240_Bkg_50K_ee_kt_SM.root"
var1output="1"
var1treename="events1"
var1outdirname="/afs/cern.ch/user/s/slablack/fcc/heppy_cuts/output_ee_qq_240_allcuts_50K_ee_kt_SM"

var2input="/afs/cern.ch/user/s/slablack/fcc/heppy/ee_WW_qqllBkg_240_50K_ee_kt_SM.root"
var2output="2"
var2treename="events2"
var2outdirname="/afs/cern.ch/user/s/slablack/fcc/heppy_cuts/output_ee_WWqqll_240_allcuts_50K_ee_kt_SM"

var3input="/afs/cern.ch/user/s/slablack/fcc/heppy/ee_WW_qqqq_240_50K_ee_kt_SM.root"
var3output="0"
var3treename="events0"
var3outdirname="/afs/cern.ch/user/s/slablack/fcc/heppy_cuts/output_ee_WWqqqq_240_allcuts_50K_ee_kt_SM"

var5input="/afs/cern.ch/user/s/slablack/fcc/heppy/ee_ZZ_allBkg_240_50K_ee_kt_SM.root"
var5output="3"
var5treename="events3"
var5outdirname="/afs/cern.ch/user/s/slablack/fcc/heppy_cuts/output_ee_ZZ_all_240_allcuts_50K_ee_kt_SM"

#var6input="/afs/cern.ch/user/s/slablack/fcc/heppy/ee_ZZ_qqqqBkg_240_50K_ee_kt_SM.root"
#var6output="3"
#var6treename="events3"

#var7input="/afs/cern.ch/user/s/slablack/fcc/heppy/ee_ZH_qqqqBkg_240_50K_ee_kt_SM.root"
#var7output="/afs/cern.ch/user/s/slablack/fcc/heppy_cuts/output_ee_ZH_qqqqBkg_240_allcuts_50K_ee_kt_SM"

#var8input="/afs/cern.ch/user/s/slablack/fcc/heppy/ee_ZH_llqqBkg_240_50K_ee_kt_SM.root"
#var8output="/afs/cern.ch/user/s/slablack/fcc/heppy_cuts/output_ee_ZH_llqqBkg_240_allcuts_50K_ee_kt_SM"

#var9input="/afs/cern.ch/user/s/slablack/fcc/heppy/ee_ZH_qqllBkg_240_50K_ee_kt_SM.root"
#var9output="/afs/cern.ch/user/s/slablack/fcc/heppy_cuts/output_ee_ZH_qqllBkg_240_allcuts_50K_ee_kt_SM"

python Wmass1.py "$var1input" "$var1output" "$var1treename" "$var1outdirname"
python Wmass1.py "$var2input" "$var2output" "$var2treename" "$var2outdirname"
python Wmass1.py "$var3input" "$var3output" "$var3treename" "$var3outdirname"
python Wmass1.py "$var5input" "$var5output" "$var5treename" "$var5outdirname"
#python Wmass1.py "$var6input" "$var6output" "$var6treename"
#python Wmass1.py "$var7input" "$var7output" &
#python Wmass1.py "$var8input" "$var8output" &
#python Wmass1.py "$var9input" "$var9output"

echo "end"
