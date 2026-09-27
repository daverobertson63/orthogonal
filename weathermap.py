import tkinter as tk
from tkinter import ttk
import random

# ==========================================
# STUDENT 1: Core Data Component
# ==========================================
def get_weather_data(lat: float, lon: float) -> dict:
    """
    Student 1's Function.
    Simulates fetching weather data based on latitude and longitude coordinates.
    """
    # Simple simulation logic based roughly on coordinates
    is_near_equator = abs(lat) < 23.5
    base_temp = 28.0 if is_near_equator else 12.0
    
    return {
        "temp": round(base_temp + random.uniform(-10, 10), 1),       # in Celsius
        "humidity": random.randint(30, 95),                         # in %
        "pressure": random.randint(990, 1025),                      # in hPa
        "rain": round(random.uniform(0.0, 25.0), 1) if random.random() > 0.4 else 0.0  # in mm
    }

# ==========================================
# STUDENTS 2-5: Feature Components
# ==========================================
def process_temperature(weather_dict: dict) -> str:
    """Student 2 Function: Formats temperature and adds a quick metric."""
    t = weather_dict["temp"]
    return f"{t}°C / {round((t * 9/5) + 32, 1)}°F"

def process_humidity(weather_dict: dict) -> str:
    """Student 3 Function: Formats humidity."""
    return f"{weather_dict['humidity']}%"

def process_pressure(weather_dict: dict) -> str:
    """Student 4 Function: Formats atmospheric pressure."""
    return f"{weather_dict['pressure']} hPa"

def process_rainfall(weather_dict: dict) -> str:
    """Student 5 Function: Formats rainfall amount."""
    return f"{weather_dict['rain']} mm"


# ==========================================
# TEACHER APPLICATION (The Harness)
# ==========================================
class WeatherMapApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pragmatic Programmer: Orthogonal Weather Map")
        self.root.geometry("650x500")
        self.root.resizable(False, False)

        # Coordinate state
        self.current_lat = 0.0
        self.current_lon = 0.0

        self.setup_ui()

    def setup_ui(self):
        # Top Instruction Label
        instruction = ttk.Label(self.root, text="Click anywhere on the map to sample coordinates", font=("Arial", 11, "bold"))
        instruction.pack(pady=10)

        # Interactive Map Canvas
        self.canvas = tk.Canvas(self.root, width=600, height=300, bg="#add8e6", highlightthickness=1, highlightbackground="gray")
        self.canvas.pack(pady=5)
        
        # Draw placeholder continents/grid lines for visual guidance
        self.canvas.create_rectangle(50, 60, 200, 200, fill="#90ee90", outline="")   # North America
        self.canvas.create_rectangle(120, 180, 220, 280, fill="#90ee90", outline="") # South America
        self.canvas.create_rectangle(280, 40, 550, 160, fill="#90ee90", outline="")  # Eurasia
        self.canvas.create_rectangle(320, 140, 420, 260, fill="#90ee90", outline="") # Africa
        self.canvas.create_rectangle(480, 200, 560, 270, fill="#90ee90", outline="") # Australia
        
        # Equator and Prime Meridian visual guides
        self.canvas.create_line(0, 150, 600, 150, fill="red", dash=(4, 2))  # Equator
        self.canvas.create_line(300, 0, 300, 300, fill="blue", dash=(4, 2)) # Prime Meridian
        
        # Crosshair tracker element
        self.crosshair = self.canvas.create_oval(-5, -5, -5, -5, outline="red", width=2)

        # Bind map click
        self.canvas.bind("<Button-1>", self.on_map_click)

        # Results Frame
        results_frame = ttk.LabelFrame(self.root, text=" Dashboard Metrics (Processed by Student Functions) ", padding=10)
        results_frame.pack(fill="x", padx=25, pady=15)

        # UI Metric Labels
        self.lbl_coords = ttk.Label(results_frame, text="Selected Location: Lat: 0.0, Lon: 0.0", font=("Arial", 10, "italic"))
        self.lbl_coords.grid(row=0, column=0, columnspan=2, sticky="w", pady=5)

        self.lbl_temp = ttk.Label(results_frame, text="Temperature: --", font=("Arial", 10))
        self.lbl_temp.grid(row=1, column=0, sticky="w", padx=10)

        self.lbl_humidity = ttk.Label(results_frame, text="Humidity: --", font=("Arial", 10))
        self.lbl_humidity.grid(row=1, column=1, sticky="w", padx=10)

        self.lbl_pressure = ttk.Label(results_frame, text="Pressure: --", font=("Arial", 10))
        self.lbl_pressure.grid(row=2, column=0, sticky="w", padx=10)

        self.lbl_rain = ttk.Label(results_frame, text="Rainfall: --", font=("Arial", 10))
        self.lbl_rain.grid(row=2, column=1, sticky="w", padx=10)

    def on_map_click(self, event):
        # 1. Map pixel coordinates (X: 0 to 600, Y: 0 to 300) to actual geographic coordinates
        # Longitude: -180 to 180
        self.current_lon = round(((event.x / 600) * 360) - 180, 2)
        # Latitude: 90 to -90 (inverted because Y goes down in Tkinter)
        self.current_lat = round(90 - ((event.y / 300) * 180), 2)

        # Move visual crosshair selector on map
        self.canvas.coords(self.crosshair, event.x-6, event.y-6, event.x+6, event.y+6)

        # Update coordinate label display
        self.lbl_coords.config(text=f"Selected Location: Lat: {self.current_lat}, Lon: {self.current_lon}")

        # 2. RUN THE PIPELINE (Calling the orthogonal student code)
        try:
            # Step A: Student 1 generates the shared payload package
            weather_payload = get_weather_data(self.current_lat, self.current_lon)
            
            # Step B: Students 2-5 slice out only what they care about independently
            temp_string = process_temperature(weather_payload)
            humidity_string = process_humidity(weather_payload)
            pressure_string = process_pressure(weather_payload)
            rain_string = process_rainfall(weather_payload)

            # Step C: App updates display strings
            self.lbl_temp.config(text=f"Temperature: {temp_string}")
            self.lbl_humidity.config(text=f"Humidity: {humidity_string}")
            self.lbl_pressure.config(text=f"Pressure: {pressure_string}")
            self.lbl_rain.config(text=f"Rainfall: {rain_string}")
            
        except KeyError as e:
            self.lbl_temp.config(text=f"Error: Missing contract key {e}")

# Main entry point
if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherMapApp(root)
    root.mainloop()
