# This specifies the appropriate version of Redeem

REDEEM_ENVIRONMENT="/usr/local/Redeem-Custom"



if [ ! -d ${REDEEM_ENVIRONMENT} ]; then

 python2 -m virtualenv ${REDEEM_ENVIRONMENT}

 # python2 -m virtualenv --system-site-packages $REDEEM_ENVIRONMENT

fi



cat >${REDEEM_ENVIRONMENT}/lib/python2.7/site-packages/dist-packages.pth <<EOF

import sys; sys.__plen = len(sys.path)

/usr/lib/python2.7/dist-packages

/usr/local/lib/python2.7/dist-packages

EOF



# Do the actual installation

source ${REDEEM_ENVIRONMENT}/bin/activate

cd ${REDEEM_ENVIRONMENT}/src/redeem

python setup.py develop


chown -R octo:octo ${REDEEM_ENVIRONMENT}
