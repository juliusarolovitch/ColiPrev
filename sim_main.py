from time import *
from math import *
from vpython import *

time = 0
time_step = 1

print("Welcome to the space collision risk calculator.")
sleep(1.5)
print("The calculator will ask you to input data about your target satellite\nand space object to determine the risk "
      "of collision. Please ensure accurate units for correct calculations.")
sleep(2.5)
# satellite data
print("Let's start with the satellite:")
sleep(1.2)
satellite_period = float(input("What is the orbital period of the satellite? (in seconds)"))
satellite_lon = float(input("What is the initial longitude position of the satellite?"))
satellite_lat = float(input("What is the initial latitude position of the satellite?"))
# checking that inputs are within the acceptable range
while True:
    if satellite_lon < -180 or satellite_lon > 180:
        print("Your input wasn't within the acceptable range of [-180, 180]. Let's try that again.")
        satellite_lon = float(input("What is the initial longitude of the satellite?"))
    else:
        break
while True:
    if satellite_lat < -180 or satellite_lat > 180:
        print("Your input wasn't within the acceptable range of [-180, 180]. Let's try that again.")
        satellite_lat = float(input("What is the initial longitude of the satellite?"))
    else:
        break
satellite_lon_original = satellite_lon
satellite_lat_original = satellite_lat
satellite_orbit_angle = atan(satellite_lat_original / satellite_lon_original)
print(f"Satellite orbit angle is {satellite_orbit_angle}")

# space junk data
sleep(.5)
print("Great. Let's continue with the space object:")
sleep(1)
junk_period = float(input("What is the orbital period of the space object? (in seconds)"))
junk_lon = float(input("What is the initial longitude position of the space object?"))
junk_lat = float(input("What is the initial latitude position of the space object?"))
# checking that inputs are within the accpetable range
while True:
    if junk_lon < -180 or junk_lon > 180:
        print("Your input wasn't within the acceptable range of [-180, 180]. Let's try that again.")
        junk_lon = float(input("What is the initial longitude of the satellite?"))
    else:
        break
while True:
    if junk_lat < -180 or junk_lat > 180:
        print("Your input wasn't within the acceptable range of [-180, 180]. Let's try that again.")
        junk_lat = float(input("What is the initial longitude of the satellite?"))
    else:
        break
junk_lon_original = junk_lon
junk_lat_original = junk_lat
junk_orbit_angle = atan(junk_lat_original / junk_lon_original)
print(f"Junk orbit angle is {junk_orbit_angle}")

# finding the orbital radii of the objects
satellite_radius = (((satellite_period ** 2) * 6.673e-11 * 5.98e24) / (4 * (pi ** 2))) ** (1 / 3)
junk_radius = (((junk_period ** 2) * 6.673e-11 * 5.98e24) / (4 * (pi ** 2))) ** (1 / 3)

# calculating the orbital velocities of both objects
satellite_vel = (2 * pi * satellite_radius) / satellite_period
junk_vel = (2 * pi * junk_radius) / junk_period
# calculating the orbit times of both objects
junk_orbit_time = (2 * pi * junk_radius) / junk_vel
satellite_orbit_time = (2 * pi * satellite_radius) / satellite_vel

print(
    f"The satellite velocity is {round(satellite_vel, 3)} m/s. Its orbital radius is {round(satellite_radius, 3)} m.\n The object "
    f"velocity is {round(junk_vel, 3)} m/s. Its orbital radius is {round(junk_radius, 3)} m .")

# calculating the initial positions of both objects in xyz
satellite_x = satellite_radius * cos(satellite_lat) * cos(satellite_lon)
satellite_x_original = satellite_x

satellite_y = satellite_radius * cos(satellite_lat) * sin(satellite_lon)
satellite_y_original = satellite_y

satellite_z = satellite_radius * sin(satellite_lat)
satellite_z_original = satellite_z

satellite_x_range = satellite_radius * sin(satellite_orbit_angle)
satellite_y_range = satellite_radius * cos(satellite_orbit_angle)
satellite_z_range = satellite_radius

junk_x = junk_radius * cos(junk_lat) * cos(junk_lon)
junk_x_original = junk_x

junk_y = junk_radius * cos(junk_lat) * sin(junk_lon)
junk_y_original = junk_y

junk_z = junk_radius * sin(junk_lat)
junk_z_original = junk_z

junk_x_range = junk_radius * sin(junk_orbit_angle)
junk_y_range = junk_radius * cos(junk_orbit_angle)
junk_z_range = junk_radius

earth = sphere(
    texture=textures.earth,
    radius=6371000,
    pos=vec(0, 0, 0),

)

junk = sphere(
    color=color.gray(2),
    radius=2000000,
    pos=vec(junk_x, junk_y, junk_z)
)

satellite = sphere(
    color=color.red,
    radius=3000000,
    pos=vec(satellite_x, satellite_y, satellite_z)
)

# if the two objects are more than 50.000 meters apart then the risk of collision is negligible
if abs(satellite_radius - junk_radius) < 5000000:
    while time < 31556926:
        time += time_step

        satellite_x = satellite_x_original + sin(((2 * pi) / satellite_orbit_time) * time) * satellite_x_range
        satellite_z = satellite_z_original + sin(((2 * pi) / satellite_orbit_time) * time) * satellite_z_range
        satellite_y = satellite_y_original + sin(((2 * pi) / satellite_orbit_time) * time) * satellite_y_range

        junk_x = junk_x_original + sin(((2 * pi) / junk_orbit_time) * time) * junk_x_range
        junk_z = junk_z_original + sin(((2 * pi) / junk_orbit_time) * time) * junk_z_range
        junk_y = junk_y_original + sin(((2 * pi) / junk_orbit_time) * time) * junk_y_range

        satellite.pos = vec(satellite_x, satellite_y, satellite_z)
        junk.pos = vec(junk_x, junk_y, junk_z)

        print(f"Evaluated at time {time} s: The x, y, z position of the satellite was ({satellite_x}, {satellite_y}, {satellite_z}).\n The x, y, z position of the space object was ({junk_x}, {junk_y}, {junk_z}")

        if abs(satellite_x - junk_x) < 50000:
            if abs(satellite_y - junk_y) < 50000:
                if abs(satellite_z - junk_z) < 50000:
                    print(f"At time {time} s, there is a significant risk of collision between the satellite and "
                          f"objects at an approximate location of ({(satellite_x + junk_x) / 2}, {(satellite_y + junk_y) / 2}, {(satellite_z + junk_z) / 2}) relative to the center of the Earth. ")
                    junk.color = color.orange
                    satellite.color = color.orange
                    break
        if time > 31556920:
            print("No significant risk of collision detected within the coming year.")
else:
    print(f"There is virtually no risk of collision in the coming year due to the difference in orbital radius of the "
          f"two objects. The difference in orbital radius is {abs(round(satellite_radius-junk_radius))}")

