Installation
------------

    # Virtualenv setup
    virtualenv -p /usr/bin/python3 env
    source ./env/bin/activate
    
    # Install python packages
    pip install -r requirements.txt
    
    # Set up datatabase
    python manage.py migrate
    python manage.py loaddata core/fixtures/initial_data.json
    
    # Build static assets
    gulp sass

Features
--------

* Django 1.9 (new admin interface)
* Multilanguage support (Rosetta)
* API
* Class-based views
* `GenericForeignKey` for Votes