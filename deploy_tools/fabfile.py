from fabric.contrib.files import append, exists, sed, contains
from fabric.api import env, local, run, put
import random

# URL to repo on github.com

# change earc2 to name of actual repository
REPO_URL = 'https://github.com/pineapplejuice/earc2.git'

def _create_directory_structure_if_necessary(site_folder):
	for subfolder in ('database', 'public/static', 'virtualenv', 'source'):
		run(f'mkdir -p {site_folder}/{subfolder}')

def _get_latest_source(source_folder):
	if exists(source_folder + '/.git'):
		run(f'cd {source_folder} && git fetch')
	else:
		run(f'git clone {REPO_URL} {source_folder}')
	current_commit = local("git log -n 1 --format=%H", capture=True)
	run(f'cd {source_folder} && git reset --hard {current_commit}')

def _update_settings(source_folder, site_name):
	# Update path to settings.py if re-using for other projects
	settings_path = source_folder + '/earc2/settings.py'
	
	# Sets debug and allowed hosts
	sed(settings_path, "DEBUG = True", "DEBUG = False")
	sed(settings_path, 
		'ALLOWED_HOSTS =.+$',
		f'ALLOWED_HOSTS = ["{site_name}", "www.{site_name}"]'
	)
	
	# Tweaks database path
	run(f'sed -i.bak -r -e \'s/BASE_DIR, \'\\\'\'db\.sqlite3\'\\\'\'/BASE_DIR, \'\\\'\'\.\.\/database\/db\.sqlite3\'\\\'\'/g\' {settings_path}')
	
	# Add static root if not there
	if not contains(settings_path, "STATIC_ROOT"):
		append(settings_path,
			"STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR, '\.\./public/static'))"
		)
	else:
		run(f'sed -i.bak -r -e \'s/BASE_DIR, \'\\\'\'static\'\\\'\'/BASE_DIR, \'\\\'\'\.\.\/public\/static\'\\\'\'/g\' {settings_path}')
		
	
	# Generates new secret key
	secret_key_file = source_folder + '/earc2/secret_key.py'
	if not exists(secret_key_file):
		chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
		key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
		append(secret_key_file, f'SECRET_KEY = "{key}"')
	append(settings_path, '\nfrom .secret_key import SECRET_KEY')
	
	# Copy email config file
	email_config_file = source_folder + '/earc2/gmail_config.py'
	put(local_path = '../earc2/gmail_config.py',
		remote_path = email_config_file)
	

def _update_virtualenv(source_folder):
	virtualenv_folder = source_folder + '/../virtualenv'
	if not exists(virtualenv_folder + '/bin/pip'):
		run(f'python3.6 -m venv {virtualenv_folder}')
	run(f'{virtualenv_folder}/bin/pip install -r {source_folder}/requirements.txt')

def _update_static_files(source_folder):
	run(
		f'cd {source_folder}'
		' && ../virtualenv/bin/python manage.py collectstatic --noinput'
	)

def _update_database(source_folder):
	run(
		f'cd {source_folder}'
		' && ../virtualenv/bin/python manage.py migrate --noinput'
	)

def touch_restart_txt(site_folder):
	run(
		f'touch {site_folder}/tmp/restart.txt'
	)

def deploy():
	site_folder = f'/home/{env.user}/{env.host}'
	source_folder = site_folder + '/source'
	_create_directory_structure_if_necessary(site_folder)
	_get_latest_source(source_folder)
	_update_settings(source_folder, env.host)
	_update_virtualenv(source_folder)
	_update_static_files(source_folder)
	_update_database(source_folder)

