#!/bin/sh

# Generate all
echo "Generating ALL revoke-set"
CA_CERTS=`ls ../Windows/Certs/Online/*.crt`
python ./revoke_china_certs/main.py generate $CA_CERTS >revoke-china-certs.ALL.conf

# Generate basic
echo "Generating BASE revoke-set"
CA_CERTS=`ls ../Windows/Certs/Online/CNNIC_*.crt ../Windows/Certs/Online/China_Internet_Network_Information_Center_EV_Certificates_Root.crt ../Windows/Certs/Online/[Suspicious]WaccBaiduCom.crt ../Windows/Certs/Online/GiantRootCA.crt`
python ./revoke_china_certs/main.py generate $CA_CERTS >revoke-china-certs.BASE.conf

# Generate extended
echo "Generating EXTENDED revoke-set"
CA_CERTS=`ls ../Windows/Certs/Online/CNNIC_*.crt ../Windows/Certs/Online/China_Internet_Network_Information_Center_EV_Certificates_Root.crt ../Windows/Certs/Online/[Suspicious]WaccBaiduCom.crt ../Windows/Certs/Online/GiantRootCA.crt ../Windows/Certs/Online/CFCA_*.crt  ../Windows/Certs/Online/UCA_*.crt  ../Windows/Certs/Online/[Suspicious]GoAgent_CA.crt`
python ./revoke_china_certs/main.py generate $CA_CERTS >revoke-china-certs.EXTENDED.conf

echo "DONE"
