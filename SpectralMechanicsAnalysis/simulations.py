import numpy as np
from numpy.fft import fft, ifft, fftfreq, rfftfreq, irfft

from models import G_Maxwell, G_Kelvin_Voigt, G_fractional_Kelvin_Voigt, PSD
def create_noise_with_desired_psd(power_spectrum_function, max_time, N_samples):
    # Define the time step and frequency step
    dt = max_time / N_samples
    freqs = fftfreq(N_samples, dt)

    # Calculate the desired power spectrum values
    psd_values = power_spectrum_function(freqs)


    # Ensure the PSD is real and positive
    psd_values = np.abs(psd_values)/dt

    # Generate white noise
    white_noise = np.random.normal(0, 1, N_samples)

    # Take the Fourier transform of the white noise
    white_noise_fft = fft(white_noise)

    # Shape the white noise to have the desired PSD
    # Use only the positive frequencies (rfft)
    colored_noise_fft = white_noise_fft[:len(freqs)] * np.sqrt(psd_values)

    # Take the inverse FFT to get back to the time domain
    # Use irfft for real output
    colored_noise = np.real(ifft(colored_noise_fft, n=N_samples))
    time = np.linspace(0, max_time, N_samples)

    return time, colored_noise

def simulate_trajectory(max_time,N_samples,G, args):	
    PSD_function = lambda f: PSD(f, G, args)
    time, trajectory = create_noise_with_desired_psd(PSD_function, max_time, N_samples)
    return time, trajectory

###simulation of diffusing Harmonic potential
def forcefield(x,x_0,k):
    return (x_0-x)*k
def timestep(x,force,Diffusion_particle,dt):
    return x+force*dt+np.random.normal()*np.sqrt(2*Diffusion_particle*dt)
def simulate_diffusing_harmonic(time,dt,k,Diffusion_particle,Diffusion_oscillator):
    x=np.random.normal()
    x_0=0
    treyectory_particle=[x]
    treyectory_oscillator=[0]
    for i in range(int(time/dt)):
        force=forcefield(x,x_0,k)
        x_0+=np.random.normal()*np.sqrt(2*Diffusion_oscillator*dt)
        x=timestep(x,force,Diffusion_particle,dt)
        treyectory_particle.append(x)
        treyectory_oscillator.append(x_0)
    return treyectory_particle,treyectory_oscillator

    
