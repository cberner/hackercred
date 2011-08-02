#!/bin/bash

if [ "$1" == "deploy" ]; then
	echo "aye aye captain!"
	echo
	cd /www/hackercred/django/src/hackercred
	git pull
	echo
	/etc/init.d/postgresql restart
	echo
	python manage.py migrate app
	echo
	/etc/init.d/apache2 restart
	echo
	echo "mission accomplished!"
else
	ssh root@hackercred.com "/www/hackercred/make_it_so.sh deploy"
fi
