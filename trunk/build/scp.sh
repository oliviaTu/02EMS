#!/usr/bin/expect -f
set timeout 30
spawn scp -r ./output  root@192.168.100.132:/home/test/SysManage
expect "*password:"
send "123456\r"
# expect "*Are you sure you want to continue connecting (yes/no)?"
# send "yes\r"
sleep 3
expect eof
