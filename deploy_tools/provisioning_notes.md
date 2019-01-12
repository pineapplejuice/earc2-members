Provisioning a new site (Dreamhost)
===================================

## Required packages

* Python 3.6
* virtualenv + pip
* Git
* Passenger

## Provisioning on dreamhost.com

Passenger WSGI docs:
https://help.dreamhost.com/hc/en-us/articles/215769578-Passenger-overview
https://help.dreamhost.com/hc/en-us/articles/216385637-How-do-I-enable-Passenger-on-my-domain-
https://help.dreamhost.com/hc/en-us/articles/215769548-Passenger-and-Python-WSGI
https://help.dreamhost.com/hc/en-us/articles/215319598-Django-overview


* Create subdomain on dreamhost.com control panel
	* Enable Passenger checkbox
	* Remove index.html from public subdirectory of site
	* May need to 'touch tmp/restart.txt' to force changes
	

Checklist
* In app settings.py file
	* change DEBUG and TEMPLATE_DEBUG to False
	* Add domain names to ALLOWED_HOSTS (with and without www)


##  Folder structure
Assume we have account at /home/username

/home/username/
|-- SITENAME
	|-- database
	|-- source
	|-- static
	|-- public
	|-- virtualenv

