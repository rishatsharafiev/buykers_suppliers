# Buykers suppliers

### Pre-install configuration
```
# docker
sudo apt-get update
sudo apt-get install htop python-pip -y

sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common -y

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo apt-key fingerprint 0EBFCD88
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   edge"
sudo apt-get update
sudo apt-get install docker-ce -y



# docker compose
sudo pip install docker-compose

# enable swap 4G
sudo swapoff /swapfile

sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile

sudo mkswap /swapfile
sudo swapon /swapfile
sudo swapon --show

sudo cp /etc/fstab /etc/fstab.bak
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab

sudo nano /etc/sysctl.conf
vm.swappiness=10 # add to /etc/sysctl.conf
vm.vfs_cache_pressure = 50 # add to /etc/sysctl.conf


sudo sysctl vm.swappiness=10
sudo sysctl vm.vfs_cache_pressure=50

# create user 
mkdir /home/buykers_suppliers
useradd -d /home/buykers_suppliers buykers_suppliers
passwd buykers_suppliers # add password to user
chown buykers_suppliers:buykers_suppliers /home/buykers_suppliers -R
nano /etc/sudoers
buykers_suppliers  ALL=(ALL) ALL
 # add to sudo 

# docker without sudo
su buykers_suppliers
sudo groupadd docker
sudo usermod -aG docker $USER

# ufw
sudo apt install ufw
sudo nano /etc/default/ufw 
IPV6=yes # in  /etc/default/ufw

sudo ufw default deny incoming
sudo ufw default allow outgoing

sudo ufw allow ssh
sudo ufw allow 22
sudo ufw allow 2222

sudo ufw enable

sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 54321/tcp
sudo ufw allow 9001:9005/tcp
sudo ufw allow 9008:9009/tcp
sudo ufw allow 9010/tcp
```

### Docker Compose build
```
rm celeryev.pid
cd devops && docker-compose -p buykers_suppliers build
```

### Docker Compose up
```
docker-compose -p buykers_suppliers up --force-recreate -d
```

### Static and media
```
sudo chmod 777 static -R
sudo chmod 777 media -R
```

### Install Supervisor
```
apt-get install supervisor -y
systemctl restart supervisor.service
```
