import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# Earth's gravitational parameter (mu = G*M), in km^3/s^2
MU_EARTH = 398600.4418

def two_body_eom(t, state):
    """
    The equations of motion for the two-body problem.
    state = [x, y, z, vx, vy, vz]  (km, km/s)
    Returns d(state)/dt = [vx, vy, vz, ax, ay, az]
    """
    r = state[:3]          # position vector
    v = state[3:]          # velocity vector
    r_norm = np.linalg.norm(r)
    a = -MU_EARTH * r / r_norm**3   # gravitational acceleration
    return np.concatenate((v, a))

# --- Initial conditions: a circular orbit at ~400 km altitude (like the ISS) ---
earth_radius = 6371.0            # km
altitude = 400.0                 # km
r0 = np.array([earth_radius + altitude, 0.0, 0.0])   # start on the x-axis

# For a circular orbit, speed = sqrt(mu / r), directed perpendicular to r
v_circular = np.sqrt(MU_EARTH / np.linalg.norm(r0))
v0 = np.array([0.0, 1.2 * v_circular, 0.0])

state0 = np.concatenate((r0, v0))

# --- Simulate for exactly one orbital period ---
v0_mag = np.linalg.norm(v0)
r0_mag = np.linalg.norm(r0)
a = 1 / (2 / r0_mag - v0_mag**2 / MU_EARTH)   # semi-major axis
T = 2 * np.pi * np.sqrt(a**3 / MU_EARTH)      # orbital period, seconds
t_eval = np.linspace(0, T, 500)

sol = solve_ivp(two_body_eom, (0, T), state0, t_eval=t_eval, rtol=1e-9, atol=1e-9)

print(f"Orbital period: {T/60:.1f} minutes")
print(f"Orbital speed:  {v_circular:.3f} km/s")

# --- Plot the orbit in 3D ---
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(sol.y[0], sol.y[1], sol.y[2], label='Satellite orbit')
earth_radius = 6371.0
u, v = np.mgrid[0:2*np.pi:40j, 0:np.pi:20j]
xs = earth_radius * np.cos(u) * np.sin(v)
ys = earth_radius * np.sin(u) * np.sin(v)
zs = earth_radius * np.cos(v)
ax.plot_surface(xs, ys, zs, color='blue', alpha=0.6)
ax.set_xlabel('x (km)')
ax.set_ylabel('y (km)')
ax.set_zlabel('z (km)')
ax.set_title('Two-Body Orbit Simulation')
ax.legend()
max_range = np.array([sol.y[0].max()-sol.y[0].min(),
                       sol.y[1].max()-sol.y[1].min(),
                       sol.y[2].max()-sol.y[2].min()]).max() / 2.0
mid_x = (sol.y[0].max()+sol.y[0].min()) * 0.5
mid_y = (sol.y[1].max()+sol.y[1].min()) * 0.5
mid_z = (sol.y[2].max()+sol.y[2].min()) * 0.5
ax.set_xlim(mid_x - max_range, mid_x + max_range)
ax.set_ylim(mid_y - max_range, mid_y + max_range)
ax.set_zlim(mid_z - max_range, mid_z + max_range)
plt.show()
