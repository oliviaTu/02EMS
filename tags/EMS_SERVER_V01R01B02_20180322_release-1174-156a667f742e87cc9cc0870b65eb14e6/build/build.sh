#!/bin/sh

PROPERTIES="build.properties"
PRODUCT_NAME="EMS_SERVER"
DEPENDENCY="dependencies"

RED_COLOE='\E[31m'
GREEN_COLOR='\E[32m'
YELLOW_COLOR='\E[33m'
BLUE_COLOR='\E[34m'

REDB_COLOE='\E[1;31m'
GREENB_COLOR='\E[1;32m'
YELLOWB_COLOR='\E[1;33m'
BLUEB_COLOR='\E[1;34m'

RES='\E[0m'

log_info() {
    echo -e "${GREEN_COLOR}$1${RES}"
}

log_info_wait() {
    echo -en "${GREEN_COLOR}$1${RES}"
}

log_error() {
    echo -e "${REDB_COLOE}$1${RES}"
}

log_success() {
    echo -e "${GREENB_COLOR}$1${RES}"
}

clean_up() {
    rm -rf ${BUILD}
    exit 1
}

die() {
    log_error "$1"
    clean_up
}

trap clean_up SIGINT SIGTERM

#if [ "$1" != "-t" ] && [ "$1" == "" ]; then
#    who=$(whoami)
#    if [[ ${who} != "root" ]]; then
#        die "Need root privilege"
#    fi
#fi

if [ ! -f ${PROPERTIES} ]; then
    die "${PROPERTIES} is not exists."
fi

NEName="EMS"
Version=$(grep 'ProductVersion=' ${PROPERTIES} | cut -d'=' -f2)
Module=$(grep 'Module=' ${PROPERTIES} | cut -d'=' -f2)
Provider="Svi 视维"
BuildTime=$(date +"%Y-%m-%d %H:%M:%S")
BuildVersion=$(date +"%Y%m%d")

OUTPUT="output"


OUTPUTPATH="${PWD}/output"
rm -rf ${OUTPUTPATH}
mkdir -p ${OUTPUTPATH}

cd ..
PYINSTALLERBUILD=pyinstaller_build
PYINSTALLERDIST=pyinstaller_dist
SOURCEFILE=ems.py
PYINSTALLSOFTWARE=${PYINSTALLERDIST}/software
PYINSTALLERNAME=${SOURCEFILE%.*}
mkdir -p ${PYINSTALLSOFTWARE}
log_info_wait "Start to Pyinstaller ..."
PATH=/opt/rh/python27/root/usr/bin:/sbin:/usr/sbin:/bin:/usr/bin
export PATH
pyinstaller --distpath ${PYINSTALLERDIST} --workpath ${PYINSTALLERBUILD}  ${SOURCEFILE}

echo ${./pyinstaller --distpath ${PYINSTALLERDIST} --workpath ${PYINSTALLERBUILD}  ${SOURCEFILE}}

rm -rf ${PYINSTALLSOFTWARE}/${PYINSTALLERNAME}
pwd
ls
mv ${PYINSTALLERDIST}/${PYINSTALLERNAME} ${PYINSTALLSOFTWARE} 
if [ $? -ne 0 ]; then
    die " [FAIL]"
fi

cp -r utils ${PYINSTALLSOFTWARE}/ems
if [ $? -ne 0 ]; then
    die " [FAIL]"
fi

cd ${PYINSTALLSOFTWARE}/ems/utils
rm -rf *.py *.pyc
if [ $? -ne 0 ]; then
    die " [FAIL]"
fi

cd logsuite 
rm -rf *.py *.pyc
if [ $? -ne 0 ]; then
    die " [FAIL]"
fi

pwd
cd ../../../../
ls

cp -r ../scripts ./
ls ../
if [ $? -ne 0 ]; then
    die " [FAIL]"
fi
pwd


cp -r ../docker ./
if [ $? -ne 0 ]; then
    die " [FAIL]"
fi
cp -r ../Dockerfile ./
if [ $? -ne 0 ]; then
    die " [FAIL]"
fi

cp -r ../sql ./
if [ $? -ne 0 ]; then
    die " [FAIL]"
fi

cp -r ../lib ./
if [ $? -ne 0 ]; then
    die " [FAIL]"
fi

chmod 755 scripts/*.sh
if [ $? -ne 0 ]; then
    die " [FAIL]"
fi

mv scripts/setup.sh ./
if [ $? -ne 0 ]; then
    die " [FAIL]"
fi


cat << EOF > param.properties
[DB]
;postgresql数据库用户名
db_username = root
;数据库密码
db_password = 123456
;数据库名
postgres_database = ems
;数据库链接类型(一般默认不变)
database_type = mysql
;数据库连接池(可根据实际情况做调整)
pool_size = 5
;数据库所在服务器IP
db_host = 192.168.100.132
;数据库端口
db_port = 3306

[LOGCONFPATH]
;SysManage日志的配置文件路径
log_conf_path = /home/tm/workspace/ems/utils/logsuite/LogSuite.conf
log_db_path = /home/tm/workspace/ems/utils/logsuite/logdb.conf

[CAS]
;cas后台服务地址
cas_operator_search  = 192.168.100.101:8000

;cas日志的配置文件路径
cas_log_path = /home/tm/workspace/ems/utils/casclient/LogSuite.conf
;cas配置文件路径
cas_conf_path = /home/tm/workspace/ems/utils/casclient/casclient.ini

;libcas.so动态库文件路径
cas_lib_path = /usr/lib/libcas.so

[HOST]
local_host = 192.168.100.134


EOF

cat << EOF > licenseclient.conf
[NAME]                         
name=EMS

[VERSION]                      
version=1.0.1                  

[SERVER]                       
ip=auth-master.cywc.com            
port=8888                      
url=/api/auth/heartbeat         

[RSA]                          
public_key=/opt/powercloud/ems/ems_server/software/ems/utils/authclient/rsa_public_key.pem
private_key=/opt/powercloud/ems/ems_server/software/ems/utils/authclient/rsa_private_key.pem

[AUTH]
path=/opt/powercloud/ems/ems_server/software/ems/utils/authclient/authfile

[LICENSE]
path=/opt/powercloud/ems/ems_server/software/ems/utils/authclient

[LOGCONF]
path=/opt/powercloud/ems/ems_server/software/ems/utils/authclient/LogSuite.conf
EOF

cat << EOF > logdb.conf
[logdbinfo]
#记录操作日志的远程数据库IP
dbip=192.168.100.132

#数据库用户名
usrid=root

#数据库登录密码
passwd=123456

#数据库端口
dbport=3306

#数据库名
logdbname=ems
EOF

touch version
echo "NEName=${NEName}" > version
echo "Version=${Version}" >> version
echo "Provider=${Provider}" >> version
echo "BuildTime=${BuildTime}" >> version


cd ../
PACKAGENAME=${PRODUCT_NAME}_${Version}_${BuildVersion}_${Module}
mv ${PYINSTALLERDIST} ${PACKAGENAME}
log_info_wait "Start to pack ${NEName}..."
SVNVERSION=$(svnversion -c |sed 's/^.*://' |sed 's/[A-Z]*$//')
# SVNVERSION=${SVN_REVISION}
echo ${SVNVNERSION}
tar -zcvf ${OUTPUTPATH}/${PRODUCT_NAME}_${Version}_${BuildVersion}_${Module}.tar.gz ${PACKAGENAME} --exclude=.svn &> /dev/null
#MD5=`md5sum ${OUTPUTPATH}/*.tar.gz |cut -d ' ' -f 1`

#mv ${OUTPUTPATH}/*.tar.gz ${OUTPUTPATH}/${PRODUCT_NAME}_${Version}_${BuildVersion}_${Module}-${SVNVERSION}-${MD5}.tar.gz
#echo "===============new tag"

if [ $? -eq 0 ]; then
    log_success " [OK]"
else
    die " [FAIL]"
fi

rm -rf ${PACKAGENAME} ${PYINSTALLERBUILD} *.spec
pwd
exit 0


