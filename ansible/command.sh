###Steps for installing Giunicorn###

##Step1 Update and upgrade##

sudo apt update  
sudo apt upgrade

##Step 2  Install Required Packages##
sudo apt install -y python3 python3-pip

##Step 3: Install Virtual Environment##
sudo pip3 install --yes virtualenv
sudo apt install -y python3-virtualenv

##Step4 Install Git##
sudo apt install -y git

##Step 5 Clone git repository##
git clone -b app_with_mysql_aws https://github.com/azawslearn/wordgame.git

##6 Create a Virtual Environment##

cd /home/azureuser/wordgame
virtualenv venv
source venv/bin/activate

cd /home/ubuntu/wordgame
virtualenv venv
source venv/bin/activate

##7 Install Dependencies##
pip install -r requirements.txt

##Step 8: Install Gunicorn##
pip install gunicorn

##Step 9: Install and Configure Nginx##
sudo apt install -y nginx

##Step 10 Create a new Nginx configuration file for your project##

sudo nano /etc/nginx/sites-available/wordgame

##Add the following content:

server {
    listen 80;
    server_name 54.172.168.14;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}


##11 Create a symbolic link for the Nginx configuration.##

sudo ln -s /etc/nginx/sites-available/wordgame /etc/nginx/sites-enabled


##12 Start and Enable Nginx##

sudo systemctl start nginx
sudo systemctl enable nginx

##13 Set up Systemd for Gunicorn##

sudo nano /etc/systemd/system/wordgame.service

Add the following content:


[Unit]
Description=Wordgame web application
After=network.target

[Service]
User=azureuser
WorkingDirectory=/home/azureuser/wordgame
ExecStart=/home/azureuser/wordgame/venv/bin/gunicorn -w 3 -b 0.0.0.0:8000 app:app
Restart=always

[Install]
WantedBy=multi-user.target

14 
sudo systemctl daemon-reload
sudo systemctl enable wordgame
sudo systemctl start wordgame
sudo systemctl restart nginx
sudo systemctl restart wordgame
