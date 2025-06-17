import requests
from django.conf import settings
from django.shortcuts import render
import random
import subprocess
import logging

# Home page view
def home_view(request):
    return render(request, 'home.html')

# Projects page view
def projects_view(request):
    return render(request, 'projects.html')

# Weather page view
def weather_view(request):
    city = request.GET.get("city")
    weather = None
    forecast = None
    error = None

    if city:
        api_key = settings.WEATHER_API_KEY
        weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=en"
        forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric&lang=en"

        try:
            weather_response = requests.get(weather_url)
            forecast_response = requests.get(forecast_url)

            # Check both responses are OK
            if weather_response.status_code == 200 and forecast_response.status_code == 200:
                weather_data = weather_response.json()
                forecast_data = forecast_response.json()

                # Confirm API returned successful codes
                if weather_data.get("cod") == 200 and forecast_data.get("cod") == "200":
                    weather = {
                        "city": weather_data["name"],
                        "temp": weather_data["main"]["temp"],
                        "description": weather_data["weather"][0]["description"],
                        "icon": weather_data["weather"][0]["icon"],
                        "humidity": weather_data["main"]["humidity"],
                        "wind": weather_data["wind"]["speed"],
                        "pressure": weather_data["main"]["pressure"],
                    }
                    forecast = forecast_data["list"]
                else:
                    error = "Could not retrieve weather data."
            else:
                error = f"Weather server responded with status {weather_response.status_code}."
        except Exception:
            error = "An error occurred while fetching weather data."

    # Render weather template with weather, forecast, and error data
    return render(request, "weather.html", {
        "weather": weather,
        "forecast": forecast,
        "error": error,
    })

# Network speed and ping test view
def speed_ping_view(request):
    result = {
        'download': None,
        'upload': None,
        'ping': None,
        'ping_full': None,
    }
    errors = []

    # Try using the Python speedtest module first
    try:
        import speedtest
        st = speedtest.Speedtest()
        st.get_best_server()
        download_speed = round(st.download() / 1_000_000, 2)  # Convert to Mbps
        upload_speed = round(st.upload() / 1_000_000, 2)      # Convert to Mbps
        result['download'] = f"{download_speed} Mbps"
        result['upload'] = f"{upload_speed} Mbps"
        ping_result = st.results.ping
        result['ping'] = f"{ping_result} ms"
    except Exception as e:
        errors.append(f"Speed test (Python API) failed: {e}")

    # If Python module fails, fallback to CLI speedtest-cli
    if not result['download'] or not result['upload']:
        try:
            output = subprocess.check_output(['speedtest-cli', '--simple'], text=True)
            # Parse CLI output lines
            for line in output.splitlines():
                if line.startswith('Ping:'):
                    result['ping'] = line.split('Ping:')[1].strip()
                elif line.startswith('Download:'):
                    result['download'] = line.split('Download:')[1].strip()
                elif line.startswith('Upload:'):
                    result['upload'] = line.split('Upload:')[1].strip()
        except Exception as e:
            errors.append(f"Speed test (CLI) also failed: {e}")

    # Run full ping test to 8.8.8.8 (Google DNS)
    try:
        # Note: '-n' is for Windows. For Linux/macOS, use '-c 4'
        ping_output = subprocess.check_output(['ping', '-n', '4', '8.8.8.8'], text=True)
        result['ping_full'] = ping_output
    except Exception as e:
        errors.append(f"Ping test failed: {e}")

    # Combine all error messages, if any
    error_message = " | ".join(errors) if errors else None

    return render(request, 'speed_ping.html', {'result': result, 'error': error_message})

# Loto 6/49 game view
def loto_view(request):
    context = {}  # Context dictionary to pass data to the template

    if request.method == 'POST':
        # Get numbers submitted by the user as a comma-separated string
        numbers_str = request.POST.get('numbers', '')
        try:
            # Convert string to list of integers, stripping whitespace
            numbers_list = [int(x.strip()) for x in numbers_str.split(',')]
            # Validate: Exactly 6 numbers, each between 1 and 49
            if len(numbers_list) != 6 or any(n < 1 or n > 49 for n in numbers_list):
                context['error'] = "Please enter exactly 6 numbers between 1 and 49, separated by commas."
            # Validate: Numbers must be unique
            elif len(set(numbers_list)) != 6:
                context['error'] = "Numbers must be unique."
            else:
                # Generate 6 unique random numbers as today's winning numbers
                today_numbers = random.sample(range(1, 50), 6)
                today_numbers.sort()

                # Find which numbers from user's input match the winning numbers
                win_list = [n for n in numbers_list if n in today_numbers]
                win_count = len(win_list)

                # Prepare message depending on number of matches
                if win_count == 6:
                    message = "********** YOU WON THE GRAND PRIZE! **********"
                elif win_count == 5:
                    message = "Congratulations, you guessed 5 numbers!"
                elif win_count == 4:
                    message = "You guessed 4 numbers. Well done!"
                elif win_count == 3:
                    message = "You guessed 3 numbers."
                else:
                    message = "You didn't guess enough numbers."

                # Add results to the context
                context.update({
                    'numbers_played': numbers_list,
                    'today_numbers': today_numbers,
                    'win_list': win_list,
                    'win_count': win_count,
                    'message': message,
                })

        except ValueError:
            # Handle invalid (non-integer) input
            context['error'] = "Please enter valid numbers separated by commas."

    # Render the loto.html template with the context data
    return render(request, 'loto.html', context)
