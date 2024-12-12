import numpy as np
import matplotlib.pyplot as plt

# Stałe fizyczne
h = 6.626e-34  # stała Plancka (J·s)
c = 3e8  # prędkość światła (m/s)
electron_mass = 9.109e-31  # masa elektronu (kg)
proton_mass = 1.673e-27  # masa protonu (kg)
neutron_mass = 1.675e-27  # masa neutronu (kg)

particle_names = ["Elektron", "Proton", "Neutron"]
particle_mases = [electron_mass, proton_mass, neutron_mass]


def get_particle_index():
    print("obsługiwane rodzaje cząsteczek:")
    for i in range(len(particle_names)):
        print(f" [ {i} ]: {particle_names[i]}")
    index = -1

    while index == -1:
        input_particle = input("wybierz rodzaj cząsteczki (podaj nr): ")
        try:
            index = int(input_particle)
            particle_mases[index]
        except:
            print("wprowadzona wartość jest nieprawidłowa")
            index = -1
    return index


def get_wave_lenght():
    wave_lenght = 0
    while wave_lenght == 0:
        input_wave_lenght = input("podaj długość fali promieniowania X [między 0,01 a do 10 (nm)]: ")
        input_wave_lenght = input_wave_lenght.replace(",", ".")
        try:
            wave_lenght = float(input_wave_lenght)
            if 0.01 <= wave_lenght <= 10:
                return wave_lenght
            else:
                print("wprowadzona wartość spoza wskazanego przedziału")
                wave_lenght = 0
        except:
            print("wprowadzona wartość jest nieprawidłowa")


def get_angle():
    angle = -1
    while angle == -1:
        input_angle = input("podaj kąt [0 - 180 (stopni)]: ")
        try:
            angle = int(input_angle)
            if 0 <= angle <= 180:
                return angle
            else:
                print("wprowadzona wartość spoza wskazanego przedziału")
                angle = -1
        except:
            print("wprowadzona wartość spoza wskazanego przedziału")

# Funkcja do obliczenia Δλ
def compton_wavelength_shift(theta_rad, mass):
    return (h / (mass * c)) * (1 - np.cos(theta_rad))


# Funkcja do rysowania wykresu Δλ(θ)
def plot_compton_shift(mass, particle_name):
    theta_degrees = np.linspace(0, 180, 1000)  # kąty od 0 do 180 stopni
    theta_radians = np.radians(theta_degrees)
    delta_lambda = compton_wavelength_shift(theta_radians, mass)

    plt.plot(theta_degrees, delta_lambda * 1e12)  # zmiana długości fali w pikometrach (pm)
    plt.xlabel('Kąt θ (stopnie)')
    plt.ylabel('Zmiana długości fali Δλ (pm)')
    plt.title(f'Rozproszenie Comptona dla {particle_name}')
    plt.grid(True)
    plt.show()


# Funkcja do obliczenia zmiany prędkości elektronu
def calculate_electron_speed_change(theta_rad, lambda_initial):
    delta_lambda = compton_wavelength_shift(theta_rad, electron_mass)
    delta_energy = h * c / lambda_initial - h * c / (lambda_initial + delta_lambda)
    return np.sqrt(delta_energy / electron_mass)


def main():
    repeat = True

    print("Program do analizy rozproszenia Comptona.")
    print("=========================================")
    while repeat:
        index = get_particle_index()
        print(
            f"Rysuję wykres zmiany długości fali promieniowania X po zderzeniu z: {particle_names[index]} (aby kontynuować zamknij wykres)")
        plot_compton_shift(particle_mases[index], particle_names[index])

        wave_lenght = get_wave_lenght()
        angle = get_angle()

        print(
            f"Długość fali o długości: {wave_lenght} nm po zderzeniu z {particle_names[index]} pod kątem {angle} stopni wyniesie {wave_lenght + compton_wavelength_shift(np.deg2rad(angle), particle_mases[index]) * 1e9} nm")
        print(
            f"Dla podanego kąta {angle} stopni zmiana prędkości swobodnego elektronu wyniesie {calculate_electron_speed_change(np.deg2rad(angle), wave_lenght) * 1e9} m/s 1e-18")
        repeat = input("Naciśnij 'q' aby zakończyć lub dowolny inny klawisz aby ponowić: ") != "q"


if __name__ == "__main__":
    main()