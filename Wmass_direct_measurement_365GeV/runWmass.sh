var1input="/afs/cern.ch/user/s/slablack/fcc/heppy/ee_qq_365_Bkg_50K_ee_kt_SM.root"
var1output="/afs/cern.ch/user/s/slablack/fcc/output_wmass_y34cut_ejetcut_edijetcut_openingangle_mw2_mw1_365GeV/output_ee_qq_365_y34cut_ejetcut_edijetcut_openinganglecut_mw2_mw1_Bkg_50K_ee_kt_SM"

var2input="/afs/cern.ch/user/s/slablack/fcc/heppy/ee_WW_qqllBkg_365_50K_ee_kt_SM.root"
var2output="/afs/cern.ch/user/s/slablack/fcc/output_wmass_y34cut_ejetcut_edijetcut_openingangle_mw2_mw1_365GeV/output_ee_WW_qqllBkg_365_y34cut_ejetcut_edijetcut_openinganglecut_mw2_mw1_50K_ee_kt_SM"

var3input="/afs/cern.ch/user/s/slablack/fcc/heppy/ee_WW_qqqq_365_50K_ee_kt_SM.root"
var3output="/afs/cern.ch/user/s/slablack/fcc/output_wmass_y34cut_ejetcut_edijetcut_openingangle_mw2_mw1_365GeV/output_ee_WW_qqqq_365_y34cut_ejetcut_edijetcut_openinganglecut_mw2_mw1_50K_ee_kt_SM"

var5input="/afs/cern.ch/user/s/slablack/fcc/heppy/ee_ZZ_qqllBkg_365_50K_ee_kt_SM.root"
var5output="/afs/cern.ch/user/s/slablack/fcc/output_wmass_y34cut_ejetcut_edijetcut_openingangle_mw2_mw1_365GeV/output_ee_ZZ_qqllBkg_365_y34cut_ejetcut_edijetcut_openinganglecut_mw2_mw1_50K_ee_kt_SM"

var6input="/afs/cern.ch/user/s/slablack/fcc/heppy/ee_ZZ_qqqqBkg_365_50K_ee_kt_SM.root"
var6output="/afs/cern.ch/user/s/slablack/fcc/output_wmass_y34cut_ejetcut_edijetcut_openingangle_mw2_mw1_365GeV/output_ee_ZZ_qqqqBkg_365_y34cut_ejetcut_edijetcut_openinganglecut_mw2_mw1_50K_ee_kt_SM"

var7input="/afs/cern.ch/user/s/slablack/fcc/heppy/ee_ZH_qqqqBkg_365_50K_ee_kt_SM.root"
var7output="/afs/cern.ch/user/s/slablack/fcc/output_wmass_y34cut_ejetcut_edijetcut_openingangle_mw2_mw1_365GeV/output_ee_ZH_qqqqBkg_365_y34cut_ejetcut_edijetcut_openinganglecut_mw2_mw1_50K_ee_kt_SM"

var8input="/afs/cern.ch/user/s/slablack/fcc/heppy/ee_ZH_llqqBkg_365_50K_ee_kt_SM.root"
var8output="/afs/cern.ch/user/s/slablack/fcc/output_wmass_y34cut_ejetcut_edijetcut_openingangle_mw2_mw1_365GeV/output_ee_ZH_llqqBkg_365_y34cut_ejetcut_edijetcut_openinganglecut_mw2_mw1_50K_ee_kt_SM"

var9input="/afs/cern.ch/user/s/slablack/fcc/heppy/ee_ZH_qqllBkg_365_50K_ee_kt_SM.root"
var9output="/afs/cern.ch/user/s/slablack/fcc/output_wmass_y34cut_ejetcut_edijetcut_openingangle_mw2_mw1_365GeV/output_ee_ZH_qqllBkg_365_y34cut_ejetcut_edijetcut_openinganglecut_mw2_mw1_50K_ee_kt_SM"

python Wmass1.py "$var1input" "$var1output" &
python Wmass1.py "$var2input" "$var2output" &
python Wmass1.py "$var3input" "$var3output" &
python Wmass1.py "$var5input" "$var5output" &
python Wmass1.py "$var6input" "$var6output" &
python Wmass1.py "$var7input" "$var7output" &
python Wmass1.py "$var8input" "$var8output" &
python Wmass1.py "$var9input" "$var9output"

echo "end"
