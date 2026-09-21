import numpy as np

MU_EARTH = 398600.4418   # Earth's gravitational parameter, km^3/s^2
EARTH_RADIUS = 6371.0    # km

def hohmann_transfer(alt1, alt2):
    """
    Calculate the Hohmann transfer between two circular orbits.
    alt1, alt2 = altitudes above Earth's surface, in km (either order works)
    Returns a dict with each burn's delta-v (km/s) and the transfer time (hours)
    """
    r1 = EARTH_RADIUS + alt1
    r2 = EARTH_RADIUS + alt2

    # Speed needed for a circular orbit at each radius
    v1_circular = np.sqrt(MU_EARTH / r1)
    v2_circular = np.sqrt(MU_EARTH / r2)

    # The transfer ellipse touches both orbits: periapsis at the smaller
    # radius, apoapsis at the larger one. Its semi-major axis is the average.
    a_transfer = (r1 + r2) / 2

    # Speed ON the transfer ellipse at each radius (vis-viva equation --
    # same formula you used for the elliptical orbit script)
    v_transfer_at_r1 = np.sqrt(MU_EARTH * (2 / r1 - 1 / a_transfer))
    v_transfer_at_r2 = np.sqrt(MU_EARTH * (2 / r2 - 1 / a_transfer))

    # Burn 1: speed up from circular speed at r1 to transfer-ellipse speed
    # Burn 2: speed up from transfer-ellipse speed at r2 to circular speed
    delta_v1 = abs(v_transfer_at_r1 - v1_circular)
    delta_v2 = abs(v2_circular - v_transfer_at_r2)
    total_delta_v = delta_v1 + delta_v2

    # Transfer time = half the transfer ellipse's orbital period
    transfer_time = np.pi * np.sqrt(a_transfer**3 / MU_EARTH)

    return {
        "delta_v1_km_s": delta_v1,
        "delta_v2_km_s": delta_v2,
        "total_delta_v_km_s": total_delta_v,
        "transfer_time_hours": transfer_time / 3600
    }


if __name__ == "__main__":
    # Example: LEO (ISS-like, 400 km) to GEO (35,786 km)
    alt_start = 400.0
    alt_target = 35786.0

    result = hohmann_transfer(alt_start, alt_target)

    print(f"Hohmann transfer: {alt_start:.0f} km -> {alt_target:.0f} km altitude")
    print(f"Burn 1 (departure): {result['delta_v1_km_s']:.3f} km/s")
    print(f"Burn 2 (arrival):   {result['delta_v2_km_s']:.3f} km/s")
    print(f"Total delta-v:      {result['total_delta_v_km_s']:.3f} km/s")
    print(f"Transfer time:      {result['transfer_time_hours']:.2f} hours")
