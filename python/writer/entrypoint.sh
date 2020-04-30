export $(id)
echo "default:x:$uid:0:user for openshift:/tmp:/bin/bash" >> /etc/passwd
python python/writer/listener.py
