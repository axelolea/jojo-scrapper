from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def create_driver():
    binary_location = '/usr/bin/google-chrome'
    rute = ChromeDriverManager(path='./driver').install()
    service = Service(rute)
    options = Options()
    user_agent = ''
    options.binary_location = binary_location
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument('--start-maximized')
    options.add_argument('--disable-web-security')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-notifications')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--no-sandbox')
    options.add_argument('--log-level=3')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument('--no-default-browser-check')
    options.add_argument('--no-first-run')
    options.add_argument('--no-proxy-server')
    options.add_argument('--disable-blink-features=AutomationControlled')
    exp_opt = [
        'enable-automation',
        'ignore-certificate-errors',
        'enable-logging'
    ]
    options.add_experimental_option('excludeSwitches', exp_opt)
    prefs = {
        'profile.default_content_setting_values.notifications': 2,
        'intl.accept_languages': ['es-ES', 'es'],
        'credentials_enable_service': False
    }
    options.add_experimental_option('prefs', prefs)
    return webdriver.Chrome(service=service, options=options)