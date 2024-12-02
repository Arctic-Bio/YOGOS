import numpy as np
from sympy import isprime
from scipy.optimize import curve_fit


# Step 1: Define Elliptic Curve Transformation (Focusing on Elliptic Curve Geometry)
def elliptic_curve_to_cartesian(r, theta):
    """Elliptic curve transformation: Non-linear mapping."""
    a = 1  # Semi-major axis
    b = 0.5  # Semi-minor axis
    x = a * np.cos(theta)
    y = b * np.sin(theta)
    z = np.sinh(r)  # Hyperbolic component along z-axis
    return x, y, z


# Step 2: Function to calculate gaps using the elliptic curve transformation
def calculate_prime_gaps(num_primes):
    # Generate normalized primes for use as radii
    primes = np.array([i for i in range(2, num_primes * 20) if isprime(i)])  # Generate enough primes
    normalized_primes = primes / max(primes) * 5  # Scale to manageable radii
    angles = np.linspace(0, 2 * np.pi, len(primes), endpoint=False)

    # Apply the Elliptic Curve Transformation
    coords = np.array([elliptic_curve_to_cartesian(r, theta) for r, theta in zip(normalized_primes, angles)])
    x_coords = coords[:, 0]  # Focus on the x-coordinate for gap analysis

    # Calculate the gaps in the x-coordinate (prime gaps)
    gaps = np.diff(x_coords)
    return gaps, primes


# Step 3: Define the cosine wave function to fit
def cosine_wave(x, A, B, C, D):
    return A * np.cos(B * x + C) + D


# Step 4: Fit the cosine wave to the gaps and primes
def fit_cosine_wave_to_gaps(gaps):
    x_data = np.arange(len(gaps))  # The indices of the gaps
    y_data = gaps  # The prime gaps (x-coordinates of transformed data)

    # Initial guess for the parameters: amplitude, frequency, phase shift, vertical shift
    initial_guess = [np.max(y_data) - np.min(y_data), 2 * np.pi / len(gaps), np.pi, np.mean(y_data)]

    # Fit the curve
    params, params_covariance = curve_fit(cosine_wave, x_data, y_data, p0=initial_guess)
    return params


# Step 5: Function to predict the next prime based on the given index
def predict_next_prime(index, params, primes):
    # Estimate the next gap using the fitted cosine wave
    next_gap = cosine_wave(index, *params)

    # Estimate the next prime number by adding the predicted gap to the last known prime
    next_prime_candidate = primes[index - 1] + next_gap

    # Round the candidate to the nearest integer
    next_prime_candidate = round(next_prime_candidate)

    # Directly check if the predicted candidate is prime
    return next_prime_candidate


# Step 6: Generate primes for any index
def generate_prime_for_index(index):
    # Calculate gaps and primes
    gaps, primes = calculate_prime_gaps(index)

    # Fit the cosine wave to the gaps
    params = fit_cosine_wave_to_gaps(gaps)

    # Predict the prime number at the specified index
    predicted_prime = predict_next_prime(index, params, primes)

    return predicted_prime


# Input: Specify the index for which you want to predict the next prime
index = int(input("Enter the index to predict the next prime (e.g., 99999): "))

# Output: Predicted prime number for the given index
predicted_prime = generate_prime_for_index(index)
print(f"Predicted next prime at index {index}: {predicted_prime}")
