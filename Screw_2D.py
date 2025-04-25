import streamlit as st
import math
import matplotlib.pyplot as plt

# Constants
STANDARD_TROUGH_LOAD = 0.45
DRIVE_EFFICIENCY = 0.88
GRAVITY = 32.2

# App Title
st.title("Biomass Screw Conveyor Designer")

# Sidebar Inputs
st.sidebar.header("Input Parameters")

biomass_type = st.sidebar.text_input("Biomass Type", "rice husk")
feed_rate_kgph = st.sidebar.number_input("Feed Rate (kg/hr)", min_value=1, max_value=500, value=100)
bulk_density = st.sidebar.number_input("Bulk Density (kg/m³)", min_value=50, max_value=1000, value=180)
moisture_content = st.sidebar.slider("Moisture Content (%)", 0, 100, 15)
incline_angle_deg = st.sidebar.slider("Inclination Angle (°)", 0, 45, 20)

# Volume flow rate in ft³/hr
feed_rate_cfh = (feed_rate_kgph / bulk_density) * 35.3147

# Design Calculations
def calculate_screw_diameter(cfh):
    if cfh < 1000: return 4
    elif cfh < 2000: return 6
    elif cfh < 4000: return 9
    else: return 12

def calculate_pitch(d): return d
def calculate_shaft_diameter(d): return round(d * 0.3, 2)
def calculate_thickness(d): return 0.25 if d <= 6 else 0.375

def calculate_power(cfh, bd, angle, d):
    MHP = (cfh * bd * GRAVITY * math.sin(math.radians(angle))) / (33000 * 60)
    FHP = 0.5
    fi = 1 + (angle / 90)
    TSHP = ((FHP + MHP) * fi) / DRIVE_EFFICIENCY
    return round(TSHP, 2)

def recommend_material(biomass, mc):
    if "wood" in biomass or "husk" in biomass:
        return "Stainless Steel 304"
    elif mc > 25:
        return "316 SS or Coated Carbon Steel"
    else:
        return "Mild Steel"

# Results
Ds = calculate_screw_diameter(feed_rate_cfh)
pitch = calculate_pitch(Ds)
shaft_dia = calculate_shaft_diameter(Ds)
thickness = calculate_thickness(Ds)
material = recommend_material(biomass_type.lower(), moisture_content)
power_hp = calculate_power(feed_rate_cfh, bulk_density / 62.4, incline_angle_deg, Ds)

# Display Results
st.subheader("Design Output")
st.write(f"**Screw Diameter:** {Ds} inch")
st.write(f"**Pitch:** {pitch} inch")
st.write(f"**Shaft Diameter:** {shaft_dia} inch")
st.write(f"**Flight Thickness:** {thickness} inch")
st.write(f"**Material Suggested:** {material}")
st.write(f"**Inclination Angle:** {incline_angle_deg}°")
st.write(f"**Estimated Power Requirement:** {power_hp} HP")

# Real-Time 2D Sketch
st.subheader("Real-Time 2D Screw Conveyor Sketch")

def draw_2d_screw(Ds, shaft_dia, pitch, angle):
    fig, ax = plt.subplots(figsize=(8, 3))
    screw_radius = Ds / 2
    shaft_radius = shaft_dia / 2
    num_flights = 2

    for i in range(num_flights):
        x = i * pitch + pitch / 2
        ax.add_patch(plt.Circle((x, screw_radius), screw_radius, edgecolor='black', facecolor='lightgrey'))
        ax.add_patch(plt.Circle((x, screw_radius), shaft_radius, color='black'))

    ax.set_xlim(-1, num_flights * pitch + 1)
    ax.set_ylim(0, Ds + 2)
    ax.set_aspect('equal')
    ax.set_xlabel("Length (inches)")
    ax.set_ylabel("Height (inches)")
    ax.set_title(f"Screw Conveyor Side View @ {angle}°")
    ax.grid(True)

    ax.annotate(f"Screw Ø = {Ds}\"", xy=(pitch / 2, Ds + 0.5), fontsize=9)
    ax.annotate(f"Shaft Ø = {shaft_dia}\"", xy=(pitch / 2, shaft_dia + 0.2), fontsize=9)
    ax.annotate(f"Pitch = {pitch}\"", xy=(pitch, -0.5), fontsize=9, ha='center')

    st.pyplot(fig)

draw_2d_screw(Ds, shaft_dia, pitch, incline_angle_deg)

# Download CSV
st.subheader("Download Design")
csv = f"""Parameter,Value
Biomass Type,{biomass_type}
Feed Rate (kg/hr),{feed_rate_kgph}
Bulk Density (kg/m³),{bulk_density}
Moisture Content (%),{moisture_content}
Inclination Angle (°),{incline_angle_deg}
Screw Diameter (inch),{Ds}
Pitch (inch),{pitch}
Shaft Diameter (inch),{shaft_dia}
Flight Thickness (inch),{thickness}
Material,{material}
Power Requirement (HP),{power_hp}
"""

st.download_button("Download Design Summary as CSV", data=csv, file_name="screw_conveyor_design.csv", mime="text/csv")