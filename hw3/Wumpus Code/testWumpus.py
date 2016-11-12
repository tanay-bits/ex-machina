import updatewumpus

name = updatewumpus.intialize_world()

print updatewumpus.take_action(name, "Up")
print updatewumpus.take_action(name, "Step")
updatewumpus.take_action(name, "Exit")
print updatewumpus.look_ahead(name)
