import sqlite3
import sys
import xml.etree.ElementTree as ET

# Incoming Pokemon MUST be in this format
#
# <pokemon pokedex="" classification="" generation="">
#     <name>...</name>
#     <hp>...</name>
#     <type>...</type>
#     <type>...</type>
#     <attack>...</attack>
#     <defense>...</defense>
#     <speed>...</speed>
#     <sp_attack>...</sp_attack>
#     <sp_defense>...</sp_defense>
#     <height><m>...</m></height>
#     <weight><kg>...</kg></weight>
#     <abilities>
#         <ability />
#     </abilities>
# </pokemon>



# Read pokemon XML file name from command-line
# (Currently this code does nothing; your job is to fix that!)
if len(sys.argv) < 2:
    print("You must pass at least one XML file name containing Pokemon to insert")

connect = sqlite3.connect('pokemon.sqlite')
cursor = connect.cursor()


# Parse the XML file
tree = ET.parse(sys.argv[1])
root = tree.getroot()

# Extract data from XML and insert into database
pokedex = root.get('pokedexNumber')
name = root.find('name').text
classification = root.get('classification')
generation = root.get('generation')
hp = root.find('hp').text
attack = root.find('attack').text
defense = root.find('defense').text
speed = root.find('speed').text
sp_attack = root.find('sp_attack').text
sp_defense = root.find('sp_defense').text
height = root.find('height/m').text
weight = root.find('weight/kg').text
abilities = root.findall('abilities/ability')
ability_list = []
for ability in abilities:
    ability_list.append(ability.text)
ability = ', '.join(ability_list)

# Check if the Pokemon already exists in the database
cursor.execute("SELECT * FROM pokemon WHERE name=?", (name,))
result = cursor.fetchone()
if result is not None:
    print(name, "already exists in the database!")
else:
    # Insert the new Pokemon into the database
    cursor.execute("INSERT INTO pokemon VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
              (pokedex, name, classification, generation, hp, attack, defense, speed, sp_attack, sp_defense, height, weight))
    print(name, "has been added to the database!")

# Commit changes and close connection
connect.commit()
connect.close()
