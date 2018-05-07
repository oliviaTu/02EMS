#!/bin/sh

PROJECTNAME="SysManage"
WORKSPACE="/home/jenkins/workspace/SysManage" #jenkins项目路径
FTPIP="192.168.100.199"  #FTP服务器IP
FTPUSER="jenkins"
FTPPASSWD="Svi2017"
Filename=$(date +%Y-%m-%d_%H-%M-%S)

mkdir -p ${WORKSPACE}/${PROJECTNAME}/${Filename}
if [ $? -ne 0 ]; then
    exit 1
fi

cp -r ${WORKSPACE}/trunk/build/output/*.tar.gz ${WORKSPACE}/${PROJECTNAME}/${Filename}/
if [ $? -ne 0 ]; then
    exit 1
fi

cd ${WORKSPACE}/trunk/build/output/
if [ $? -ne 0 ]; then
    exit 1
fi
PACKAGENAME=$(ls -t "$@" | head -1)
cd -

ftp -n<<!
open  ${FTPIP}
user  ${FTPUSER} ${FTPPASSWD}
mkdir ${PROJECTNAME}
cd ${PROJECTNAME}
mkdir ${Filename}
cd ${Filename}
put  ${WORKSPACE}/${PROJECTNAME}/${Filename}/${PACKAGENAME} ${PACKAGENAME}
close
bye
!

rm -rf ${WORKSPACE}/${PROJECTNAME}
