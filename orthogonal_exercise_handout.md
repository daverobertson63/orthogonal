# Class Exercise: Orthogonal System Design (Python 3)
**Based on *The Pragmatic Programmer* by Andrew Hunt and David Thomas**

---

## 🎯 The Goal
In this exercise, your team will build a **Weather Dashboard App**. You will practice the concept of **Orthogonality**—designing components that are independent and decoupled from one another. 

If your code is truly orthogonal, a change inside one student's function **will not break** anyone else's code, and the entire app will run perfectly when combined.

---

## 🤝 The Data Contract
To work independently without breaking each other's code, you must strictly agree on the structure of the data. **Student 1** will generate a Python dictionary, and **Students 2–5** will read from it. 

The dictionary **must** contain these exact four keys:
* `"temp"` (float/int representing Celsius)
* `"humidity"` (int representing percentage)
* `"pressure"` (int representing hPa)
* `"rain"` (float/int representing millimeters of rainfall)

---

## 🛠️ The Student Assignment Templates

Copy your designated block below and implement your features inside it. Do not alter the function names or input parameters!

```python
# =====================================================================
# STUDENT 1: THE DATA CONTRACT GENERATOR
# =====================================================================
def get_weather_data(lat: float, lon: float) -> dict:
    """
    Task: Calculate or simulate weather metrics based on coordinates.
    Constraint: You MUST return a dictionary with the exact 4 keys:
    "temp", "humidity", "pressure", "rain"
    """
    # TODO: Write your logic here to generate dynamic values based on lat/lon
    
    weather_package = {
        "temp": 20.0,        
        "humidity": 50,      
        "pressure": 1013,    
        "rain": 0.0          
    }
    return weather_package


# =====================================================================
# STUDENT 2: TEMPERATURE COMPONENT
# =====================================================================
def process_temperature(weather_dict: dict) -> str:
    """
    Task: Extract "temp" from the dictionary and format it as a string.
    """
    # 1. Get the raw value out of the shared package
    raw_temp = weather_dict["temp"]
    
    # 2. Build your display string (e.g., adding text or descriptive status)
    temp_string = f"{raw_temp}°C" 
    
    # 3. Return the final string to the teacher's app
    return temp_string


# =====================================================================
# STUDENT 3: HUMIDITY COMPONENT
# =====================================================================
def process_humidity(weather_dict: dict) -> str:
    """
    Task: Extract "humidity" from the dictionary and format it as a string.
    """
    raw_humidity = weather_dict["humidity"]
    
    humidity_string = f"{raw_humidity}%"
    
    return humidity_string


# =====================================================================
# STUDENT 4: ATMOSPHERIC PRESSURE COMPONENT
# =====================================================================
def process_pressure(weather_dict: dict) -> str:
    """
    Task: Extract "pressure" from the dictionary and format it as a string.
    """
    raw_pressure = weather_dict["pressure"]
    
    pressure_string = f"{raw_pressure} hPa"
    
    return pressure_string


# =====================================================================
# STUDENT 5: RAINFALL COMPONENT
# =====================================================================
def process_rainfall(weather_dict: dict) -> str:
    """
    Task: Extract "rain" from the dictionary and format it as a string.
    """
    raw_rain = weather_dict["rain"]
    
    rain_string = f"{raw_rain} mm"
    
    return rain_string
```

---

## ⚠️ Student Troubleshooting: Guarding Against `KeyError`

Because you are working in parallel, someone might accidentally mistype a dictionary key (e.g., writing `"temperature"` instead of `"temp"`). If this happens, Python will crash with a **`KeyError`**.

To make your components truly bulletproof and resilient, you should **defensively handle errors** using Python's `.get()` method or a `try-except` block. 

### Approach A: Using `.get()` with a Default Value
Instead of using brackets (`weather_dict["temp"]`), use `.get()`. If the key is misspelled or missing, it will safely fallback to a default value instead of crashing.
```python
def process_temperature(weather_dict: dict) -> str:
    # If "temp" doesn't exist, it uses 0.0 instead of crashing
    raw_temp = weather_dict.get("temp", 0.0)
    
    temp_string = f"{raw_temp}°C"
    return temp_string
```

### Approach B: Using `try-except` for Explicit Error Messaging
This approach lets you display a clear, descriptive warning message right on the UI if a teammate violates the data contract.
```python
def process_temperature(weather_dict: dict) -> str:
    try:
        raw_temp = weather_dict["temp"]
        temp_string = f"{raw_temp}°C"
    except KeyError:
        # Gracefully handle the error and inform the team
        temp_string = "[Error: 'temp' key missing from contract!]"
        
    return temp_string
```

---

## 🧑‍🏫 The Core Lesson Check (For the Classroom)
Once all five functions are combined into the teacher's main script, try these tests:
1. **Change the UI presentation:** Student 2 can modify `process_temperature` to convert the value to Fahrenheit. Does the pressure or rainfall tracker break? (No).
2. **Change the Data Source:** Student 1 can completely rewrite how `get_weather_data` calculates its numbers. Do Students 2-5 need to change a single line of code? (No).

**That is the power of Orthogonality!**
