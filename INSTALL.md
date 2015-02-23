# Install development environment from scratch
1. Download and install [vagrant](https://www.vagrantup.com/downloads.html)

2. Clone *django-gateway* repository

    `$ mkdir -p ~/workspace/`  
    `$ cd ~/workspace/`  
    `$ git clone git@bitbucket.org:bolivarcoders/django-gateway.git`

3. Create vagrant instance

    `$ cd ~/workspace/django-gateway`  
    `$ vagrant init ubuntu/trusty64`

4. Prepare vagrant instance
    4-1. Add the following line where it belongs:  
    `config.vm.network "forwarded_port", guest: 8000, host: 8000`
    4-2. Replace the `config.vm.provider` section by:  
    `config.vm.provider "virtualbox" do |vb|`  
    `vb.customize ["modifyvm", :id, "--cpus", "2"]`  
    `end`

5. Start and login into vagrant instance

    `$ vagrant up && vagrant ssh`

6.   Update operative system (inside vagrant instance)

    `(vagrant)$ sudo aptitude update && sudo aptitude -y safe-upgrade`

7.  Install dependencies (inside vagrant instance)

    `(vagrant)$ sudo aptitude install -y build-essential python3 python3-dev postgresql postgresql-server-dev-9.3 python3-pip python-virtualenv redis-server`

8. Reload vagrant instance (outside vagrant instance)

    `$ vagrant reload`

9. Log into vagrant instance and create a Python virtual environment

    `(vagrant)$ cd /vagrant`  
    `(vagrant)/vagrant$ virtualenv --python=python3.4 venv`

10. Set new environment

    `(vagrant)/vagrant$ source venv/bin/activate`

11. Install Python requirements

    `(vagrant)(venv)/vagrant$ pip3 install -r requirements.txt`

12. Migrate database

    `(vagrant)(venv)/vagrant$ cd django_gateway`  
    `(vagrant)(venv)/vagrant/django_gateway$ python manage.py migrate`

13. Install NodeJS
    `$ curl -sL https://deb.nodesource.com/setup | sudo bash -`
    `$ sudo apt-get install -y nodejs`

14. Install bower and git
    `$ sudo npm install -g bower`
    `$ sudo apt-get install git`

15. Install Ruby Gems and Compass
    `$ sudo apt-get install ruby1.9.3`
    `$ sudo gem install compass`

16. Create static files
    `(vagrant)(venv)/vagrant/django_gateway$ cd static/`
    `(vagrant)(venv)/vagrant/django_gateway/static$ bower install`
    `(vagrant)(venv)/vagrant/django_gateway/static$ compass compile`

##Notes


* Vagrant creates a shared folder between the host and the guest machine, inside the host the folder is `~/workspace/django-gateway`, inside the guest the folder is `/vagrant`. Files on this folder will be stored in the host but accessible from guest, this is means that you can access to this shared folder even if vagrant instance is not running
