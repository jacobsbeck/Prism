from phue import Bridge

b = Bridge('10.0.0.149')

# If the app is not registered and the button is not pressed, press the button and call connect() (this only needs to be run a single time)
#b.connect()

# Get the bridge state (This returns the full dictionary that you can explore)
b.get_api()

# Prints if light 1 is on or not
print(b.get_light(2, 'on'))

b.set_light(2, 'bri', 127)