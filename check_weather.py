import requests
from datetime import datetime
import schedule
import time
import smtplib
from email.mime.text import MIMEText

# Replace 'YOUR_API_KEY' with your actual OpenWeatherMap API key
api_key = '89ebc1b90f8374b3c8c75e65e0d21f79'
# city = input('Enter city name: ')

# Construct the API URL
url = f'http://api.openweathermap.org/data/2.5/weather?q=Brussels&appid={api_key}'

# Make the API request
response = requests.get(url)

# Check if the request was successful

def check_temp_week():
    sender_email = "thomas.vdn96@gmail.com"
    receiver_email = "thomas.vdniad@gmail.com"
    password = input("Type your password and press enter: ")
    message = MIMEText("This is a plain text email.")
    message["Subject"] = "Plain Text Email"
    message["From"] = sender_email
    message["To"] = receiver_email
    url = f'http://api.openweathermap.org/data/2.5/weather?q=Brussels&appid={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temp = data['main']['temp'] - 273.15  # Convert from Kelvin to Celsius
        desc = data['weather'][0]['description']
        print(f'Temperature: {temp:.2f}°C')
        print(f'Description: {desc}')
    else:
        print('Error fetching weather data')
    
    url = f'http://api.openweathermap.org/data/2.5/forecast?q=Brussels&appid={api_key}'
    
    response = requests.get(url)
    
    count = 0
    
    templist = []
    
    def has_three_consecutive_below_zero(lst):
        count = 0 
        for num in lst:
            if num < 0:
                count += 1 
                if count == 3:
                    return True
                else:
                    count = 0 
        return False
    
    if response.status_code == 200:
        data = response.json()
        for i, forecast in enumerate(data['list']):
            if i % 7 == 6:
                if count < 5:
                    count = count + 1
                    timestamp = forecast['dt']
                    dt_object = datetime.fromtimestamp(timestamp)
                    day_of_week = dt_object.strftime('%a')
                    readable_time = datetime.fromtimestamp(timestamp).strftime('%d-%m-%Y %H')
                    temperature = forecast['main']['temp'] - 273.15  # Convert from Kelvin to Celsius
                    templist.append(temperature)
                    weather_description = forecast['weather'][0]['description']
                    print(f"{day_of_week} {readable_time} | {temperature:.2f}°C | Weather: {weather_description}")
        result = has_three_consecutive_below_zero(templist)
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Secure the connection
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print(result) 

print('program is running!')
schedule.every(12).seconds.do(check_temp_week)

while True:
   
    schedule.run_pending()  # Run scheduled tasks

    time.sleep(1)
