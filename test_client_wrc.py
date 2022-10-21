import logging
import random
import string

from locust import HttpUser, task, between
from locust.exception import RescheduleTask


test_email_host = 'gmail.com'

def unique_str():
    letters = string.ascii_lowercase
    rand_string = ''.join(random.choice(letters) for i in range(6))
    return rand_string

def unique_email():
    return 'e'  +  unique_str()  +  '@'  +  test_email_host



class WebsiteTestUser(HttpUser):
    network_timeout  = 30.0
    connection_timeout  = 30.0

    def on_start(self):

        base_url = 'http://127.0.0.1:8000/api/user'

        # set up urls
        register_url = base_url  +  '/create_user'
        get_token_url = base_url  +  '/login'
        self.get_user_info_url = base_url + '/get_user'

        # get unique email
        email = unique_email()
        login = unique_str()
        password = 'abcdefghi'
        
        # register
        response = self.client.post(
            register_url,
            json={
                  "email": email,
                  "login": login,
                  "password": password
                },
        )
        if response.status_code != 201:
            error_msg = 'register: response.status_code = {}, expected 201'.format(response.status_code)
            logging.error(error_msg)

        # get_token
        # -  username instead of email
        # - x-www-form-urlencoded (instead of json)
        response = self.client.post(
            get_token_url,
            json={"login": login, "password": password},
        )
        access_token = response.json()['Authorization']
        logging.debug('get_token: for email = {}, access_token = {}'.format(email, access_token))

        # set headers with access token
        self.headers = {'Authorization':  access_token}
        
        response = self.client.get(
                self.get_user_info_url,
                headers=self.headers,
                catch_response=True
                ) 
        if response.status_code != 200:
            raise RescheduleTask()
    def on_stop(self):
        pass
    
