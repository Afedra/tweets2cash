# Tweets2Cash Website #

## Setup development environment ##

Just execute these commands in your virtualenv(wrapper):

```
pip install -r requirements.txt
python3 manage.py migrate --noinput
python3 manage.py loaddata initial_user
python3 manage.py sample_data
```

**IMPORTANT: Tweets2Cash only runs with python 3.4+**

Initial auth data: admin/123123
