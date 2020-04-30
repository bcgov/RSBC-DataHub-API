export $(id)
echo "default:x:$uid:0:Openshift User:/opt/app-root/src:/sbin/nologin" >> /etc/passwd
python python/writer/listener.py
