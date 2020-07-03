import requests
import re

class pastebin(object):
    def __init__(self, developer_key):
        self.developer_key = developer_key
        self.Session = requests.Session()
    
    def generate_user_key(self, username, password):
        return self.Session.post('https://pastebin.com/api/api_login.php', {'api_dev_key': self.developer_key, 'api_user_name': username, 'api_user_password': password}).text
    
    def create_paste(self, paste_text, paste_private, paste_name, paste_expire_date = 'N', paste_format = 'python', user_key = ''):
        return requests.post('https://pastebin.com/api/api_post.php', {'api_option': 'paste', 'api_user_key': user_key, 'api_paste_private': paste_private, 'api_paste_name': paste_name, 'api_dev_key': self.developer_key, 'api_paste_code': paste_text}).text
    
    def delete_paste(self, user_key, paste_key):
        return requests.post('https://pastebin.com/api/api_post.php', {'api_dev_key': self.developer_key, 'api_user_key': user_key, 'api_paste_key': paste_key}).text
    
    def edit_paste(self, url, thread_name, cookie, user_agent, paste_code, paste_format, paste_expire_date, paste_private, paste_name):
        headers = {'cookie': cookie, 'user-agent': user_agent}
        source = requests.get(url, headers=headers).text
        s = re.search(r'<input type="hidden" name="csrf_token_[A-Z0-8a-z]*" value="[A-Z0-9a-z]*">', source).group()
        Value = re.search(r'value="[A-Za-z0-9]*"', s).group().replace('value="', '').replace('"', '')
        headers['content-type'] = 'application/x-www-form-urlencoded'
        requests.post(url, {'submit_hidden': 'submit_hidden', 'item_key': thread_name, f'csrf_token_{thread_name}': Value, 'paste_code': paste_code, 'paste_format': paste_format, 'paste_expire_date': paste_expire_date, 'paste_private': paste_private, 'paste_name': paste_name, 'submit': 'Save Changes'}, headers=headers)
    
    def get_user_pastes(self, user_key, results_limit):
        return requests.post('https://pastebin.com/api/api_post.php', {'api_option': 'list', 'api_dev_key': self.developer_key, 'api_user_key': user_key, 'api_results_limit': results_limit}).text
