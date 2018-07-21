#!/bin/bash

show_answer=true
while [ $# -gt 0 ]; do
  	case "$1" in
    	-y)
    	  	show_answer=false
      	;;
  	esac
	shift
done

if $show_answer ; then
	echo "WARNING!! This script REMOVE your Tweets2Cash's database and you LOSE all the data."
	read -p "Are you sure you want to delete all data? (Press Y to continue): " -n 1 -r
	echo    # (optional) move to a new line
	if [[ ! $REPLY =~ ^[Yy]$ ]] ; then
		exit 1
	fi
fi


echo "-> Remove tweets2cash DB"
dropdb tweets2cash
echo "-> Create tweets2cash DB"
createdb tweets2cash

echo "->Installing Requirements"
sudo pip3 install requirements.txt
echo "->Setting up TWITTER_CONSUMER_KEY"
export TWITTER_CONSUMER_KEY="hkHJOSR0AJu9Y6Aklup2NFyE2"
echo "->Setting up TWITTER_CONSUMER_SECRET"
export TWITTER_CONSUMER_SECRET="mRtao55eHZRJFGY1eKVkqvGBAGXLwpIIJ7MHfVNaYMJbOYALhB"
echo "->Setting up TWITTER_ACCESS_TOKEN"
export TWITTER_ACCESS_TOKEN="854666544772775937-zG37GMvK4qGuxeBt4LKo1KU9g7BKCwd"
echo "->Set TWITTER_ACCESS_TOKEN_SECRET"
export TWITTER_ACCESS_TOKEN_SECRET=" LF6eYY7UlzYurSewwsBnheGpJRsLMWnBA2yvv9OGm76QM"
echo "->Set GOOGLE_APPLICATION_CREDENTIALS"
export GOOGLE_APPLICATION_CREDENTIALS="~/tweets2cash/settings/Tweets2Cash-cf8479ee7ccf.json"
echo "-> Load migrations"
python3 manage.py makemigrations
echo "-> Migrating"
python3 manage.py migrate
echo "-> Load initial user (admin/123123)"
python3 manage.py loaddata initial_user --traceback
echo "-> Generate sample data"
python3 manage.py sample_data --traceback


sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
sudo su - postgres
createuser --interactive -P
createdb --owner tweets2cash tweets2cash
logout
sudo groupadd --system webapps
sudo useradd --system --gid webapps --shell /bin/bash --home /webapps/tweets2cash tweets2cash
sudo apt-get install python-virtualenv
sudo mkdir -p /webapps/tweets2cash/
sudo chown tweets2cash /webapps/tweets2cash/
sudo su - tweets2cash
virtualenv -p /usr/bin/python3 .
source bin/activate
git clone https://gitlab.com/martneInc/tweets2cash.git
logout
mv /webapps/tweets2cash/tweets2cash-master/gunicorn_start /webapps/tweets2cash/bin/gunicorn_start
sudo chmod u+x /webapps/tweets2cash/bin/gunicorn_start
sudo chown -R tweets2cash:users /webapps/tweets2cash
sudo chmod -R g+w /webapps/tweets2cash
sudo apt-get install libpq-dev python-dev
sudo apt-get install supervisor
sudo mv /webapps/tweets2cash/tweets2cash-master/tweets2cash.conf /etc/supervisor/conf.d/tweets2cash.conf
mkdir -p /webapps/tweets2cash/logs/
touch /webapps/tweets2cash/logs/gunicorn_supervisor.log 
touch /webapps/tweets2cash/logs/nginx-access.log 
touch /webapps/tweets2cash/logs/nginx-error.log 
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl status tweets2cash
sudo apt-get install nginx
sudo service nginx start
sudo mv /webapps/tweets2cash/tweets2cash-master/ssl/tweets2cash.key /etc/ssl/tweets2cash.key
sudo mv /webapps/tweets2cash/tweets2cash-master/ssl/tweets2cash_cert_chain.crt /etc/ssl/tweets2cash_cert_chain.crt
sudo mv /webapps/tweets2cash/tweets2cash-master/tweets2cash.txt /etc/nginx/sites-available/tweets2cash
sudo ln -s /etc/nginx/sites-available/tweets2cash /etc/nginx/sites-enabled/tweets2cash
sudo service nginx restart


