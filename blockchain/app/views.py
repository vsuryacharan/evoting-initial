from django.shortcuts import render,HttpResponse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.conf import settings
import os
from .models import *


options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

def signup(request):
    
   
    if request.method == 'POST':  
        input1 = request.POST.get('username')
        input2 = request.POST.get('password')
        if User.objects.filter(username=input1).exists():
           return HttpResponse('Username already exists')
        
        driver.get("https://erp.cmrit.ac.in/login.htm;jsessionid=551F382BD1B9527FB960DD0810F05A8A")
    
    # Find the username field and enter your username
        username_field = driver.find_element("id","j_username")
        username_field.send_keys(input1)
    
        # Find the password field and enter your password
        password_field = driver.find_element("id","password-1")
        password_field.send_keys(input2)
    
    # Find the login button and click it
        login_button = driver.find_element("xpath",'//button[normalize-space()="Login"]')
        login_button.click()

    # Replace 'element' with an element that is only present when logged in
        driver.find_element("id", "sideBarStudentDashboard")
        print("Logged in successfully")
    

# Get the session cookie
        cookies = driver.get_cookies()
        session_cookie = next((c for c in cookies if c['name'] == 'JSESSIONID'), None)
        session_cookie_value = session_cookie['value'] if session_cookie else None
    
    # URL of the image
        url = "https://erp.cmrit.ac.in/getStudentProfileImage.json"
    
    # Headers
        headers = {
            "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.6",
            "Connection": "keep-alive",
            "Cookie": f"JSESSIONID={session_cookie_value}",
            "Host": "erp.cmrit.ac.in",
            "Referer": "https://erp.cmrit.ac.in/home.htm",
            "Sec-Ch-Ua": '"Chromium";v="124", "Brave";v="124", "Not-A.Brand";v="99"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": "Windows",
            "Sec-Fetch-Dest": "image",
            "Sec-Fetch-Mode": "no-cors",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Gpc": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        }
    
    # Send a GET request to the URL
        response = requests.get(url, headers=headers, stream=True)
    
        file_path = os.path.join(settings.BASE_DIR,'app', 'static', f"{input1}.jpg")

# Open a file in write-binary mode and write the response content to it
        with open(file_path, "wb") as f:
            f.write(response.content)

        
        current_page = driver.current_url
        if(current_page == "https://erp.cmrit.ac.in/home.htm"):
            user = User.objects.create_user(input1,'' ,input2)
           
            user.save()
            driver.quit()
            driver.quit()
            return render(request,"login.html")
        else:
            driver.quit()
            driver.quit()
            return HttpResponse("Login failed")
    
    return render(request,"index.html")

import requests

'''def login(input1,input2):

# Go to the website you want to log into
    driver.get("https://erp.cmrit.ac.in/login.htm;jsessionid=551F382BD1B9527FB960DD0810F05A8A")
    
    # Find the username field and enter your username
    username_field = driver.find_element("id","j_username")
    username_field.send_keys(input1)
    
    # Find the password field and enter your password
    password_field = driver.find_element("id","password-1")
    password_field.send_keys(input2)
    
    # Find the login button and click it
    login_button = driver.find_element("xpath",'//button[normalize-space()="Login"]')
    login_button.click()

    # Replace 'element' with an element that is only present when logged in
    driver.find_element("id", "sideBarStudentDashboard")
    print("Logged in successfully")
    

# Get the session cookie
    cookies = driver.get_cookies()
    session_cookie = next((c for c in cookies if c['name'] == 'JSESSIONID'), None)
    session_cookie_value = session_cookie['value'] if session_cookie else None
    
    # URL of the image
    url = "https://erp.cmrit.ac.in/getStudentProfileImage.json"
    
    # Headers
    headers = {
        "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.6",
        "Connection": "keep-alive",
        "Cookie": f"JSESSIONID={session_cookie_value}",
        "Host": "erp.cmrit.ac.in",
        "Referer": "https://erp.cmrit.ac.in/home.htm",
        "Sec-Ch-Ua": '"Chromium";v="124", "Brave";v="124", "Not-A.Brand";v="99"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "Windows",
        "Sec-Fetch-Dest": "image",
        "Sec-Fetch-Mode": "no-cors",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Gpc": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }
    
    # Send a GET request to the URL
    response = requests.get(url, headers=headers, stream=True)
    
    # Open a file in write-binary mode and write the response content to it
    with open("{}.jpg", "wb") as f:
        f.write(response.content)
    '''
    

def my_view(request):
    
    return render(request, 'login_page.html')
    


    
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Log the user in
            clubs=Club.objects.all()
            login(request, user)
            image_url = settings.STATIC_URL + f'{username}.jpg'
            return render(request, 'logged_page.html', {'username': username, 'image_url': image_url,'clubs':clubs})
        else:
            return HttpResponse('Invalid username or password')

    # If the request method is not POST, render the login page
    return render(request, 'login.html')