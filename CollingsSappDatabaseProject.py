import easygui as eg
from tabulate import tabulate
import sqlite3

conn = sqlite3.connect('DatabaseProjPrototypeV1.12.db')
c = conn.cursor()

def tableExists():

    test = c.execute('SELECT name FROM sqlite_master WHERE type="table"')
    i = 0
    for row in test:
        i += 1
    if i == 0:
        return False
    else:
        return True

def createDB():
    
    c.execute('''CREATE TABLE Character_Description(CHAR_ID int, CHAR_Name varchar(30), CHAR_Race
            varchar(30), CHAR_Class varchar(30), CHAR_Disposition varchar(30) CHECK (CHAR_Disposition IN ('PC',
            'Friendly NPC', 'Enemy NPC')), WEAPON_ID int, SPELL_Name varchar(30), PARTY_Name varchar(30), LOCATION_ID
            int, CHARLVL_Level int, PRIMARY KEY (CHAR_ID), FOREIGN KEY (WEAPON_ID) REFERENCES Weapon(WEAPON_ID),
            FOREIGN KEY (SPELL_Name) REFERENCES Spell(SPELL_Name), FOREIGN KEY (PARTY_Name) REFERENCES
            Party(PARTY_Name), FOREIGN KEY (LOCATION_ID) REFERENCES Location(LOCATION_ID), FOREIGN KEY (CHARLVL_Level)
            REFERENCES Character_Level(CHARLVL_Level))''')

    c.execute("CREATE TABLE Character_Level(CHAR_Level int, CHAR_TotalExp int, PRIMARY KEY (CHAR_Level))")
            
    c.execute('''CREATE TABLE Character_Stats(STAT_ID int, STAT_Strength int, STAT_Dexterity int, STAT_Wisdom int,
            STAT_Intelligence int, STAT_Constitution int, STAT_Charisma int, STAT_AC int, STAT_HP int, STAT_Speed int,
            CHAR_ID int, PRIMARY KEY (STAT_ID), FOREIGN KEY (CHAR_ID) REFERENCES Character_Description(CHAR_ID))''')

    c.execute('''CREATE TABLE Party(PARTY_Name varchar(30), PARTY_Size int NOT NULL, QUEST_Name varchar(30),
            LOCATION_ID int, PRIMARY KEY (PARTY_Name), FOREIGN KEY (QUEST_Name) REFERENCES Quest(QUEST_Name),
            FOREIGN KEY (LOCATION_ID) REFERENCES Location(LOCATION_ID))''')

    c.execute('''CREATE TABLE Weapon(WEAPON_ID int, WEAPON_Description varchar(30), WEAPON_Size int, WEAPON_Type
            varchar(30), WEAPON_MagicType varchar(30), WEAPON_DamageDice varchar(10) NOT NULL, LOCATION_ID int,
            PRIMARY KEY (WEAPON_ID), FOREIGN KEY (LOCATION_ID) REFERENCES Location(LOCATION_ID))''')

    c.execute('''CREATE TABLE Spell(SPELL_Name varchar(30), SPELL_Level int NOT NULL, SPELL_Type varchar(30),
            SPELL_Description varchar(60), SPELL_PrimaryStat varchar(30) CHECK (SPELL_PrimaryStat IN ('Strength',
            'Dexterity', 'Wisdom', 'Intelligence', 'Constitution', 'Charisma')), SPELL_Range int, SPELL_DamageDice
            varchar(10), SPELL_Class varchar(15), PRIMARY KEY (SPELL_Name))''')

    c.execute('''CREATE TABLE Learns(SPELL_Name varchar(30), CHAR_ID int, PRIMARY KEY (SPELL_Name, CHAR_ID),
            FOREIGN KEY (SPELL_Name) REFERENCES Spell(SPELL_Name), FOREIGN KEY (CHAR_ID) REFERENCES
            Character_Description(CHAR_ID))''')

    c.execute('''CREATE TABLE Location(LOCATION_ID int, LOCATION_Name varchar(30), LOCATION_Description varchar(60),
            PRIMARY KEY (LOCATION_ID))''')

    c.execute('''CREATE TABLE Route(R_LOCATION_ID int, ROUTE_Length int CHECK (ROUTE_Length > 0), ROUTE_TravelTime time,
            PRIMARY KEY (R_LOCATION_ID))''')

    c.execute('''CREATE TABLE Settlement(S_LOCATION_ID int, SETTLEMENT_Type varchar(30) CHECK (SETTLEMENT_Type IN
            ('Encampment', 'Village', 'Town', 'City')), PRIMARY KEY (S_LOCATION_ID))''')

    c.execute('''CREATE TABLE Dungeon(D_LOCATION_ID int, DUNGEON_Size int CHECK (DUNGEON_Size > 0), DUNGEON_HasEnemies
            varchar(5) NOT NULL CHECK (DUNGEON_HasEnemies IN ('Yes', 'No')), PRIMARY KEY (D_LOCATION_ID))''')

    c.execute('''CREATE TABLE Quest(QUEST_Name varchar(30), QUEST_Type varchar(30) NOT NULL, QUEST_ItemReward
            varchar(45), QUEST_ExpReward int NOT NULL CHECK (QUEST_ExpReward > 0), LOCATION_ID int, QUEST_MainObjective
            varchar(60), PRIMARY KEY (QUEST_Name), FOREIGN KEY (LOCATION_ID) REFERENCES Location(LOCATION_ID),
            FOREIGN KEY (QUEST_MainObjective) REFERENCES Quest_Progress(QUEST_MainObjective))''')

    c.execute('''CREATE TABLE Quest_Progress(QUEST_MainObjective varchar(60), QUEST_CompletionStatus varchar(5)
            NOT NULL, PRIMARY KEY (QUEST_MainObjective))''')


def popTables():
    
    Characters = [(1, 'Alerodrin', 'High Elf', 'Sorcerer', 'PC', 2, 'Magic Missile', 'Party01', 1, 3),
                  (2, 'Thaer', 'Wood Elf', 'Ranger', 'PC', 36, None, 'Party01', 1, 4),
                  (3, 'Ronan', 'Human', 'Fighter', 'PC', 36, None, 'Party01', 1, 4),
                  (4, 'Brontatm', 'Dwarf', 'Fighter', 'PC', 18, None, 'Party01', 1, 3),
                  (5, 'Jack', 'Elf', 'Rogue', 'PC', 28, None, 'Party01', 1, 3),
                  (6, 'Nokk', 'Gnome', 'Rogue', 'PC', 28, None, 'Party01', 1, 4),
                  (7, 'Avagantos', 'Dragonborn', 'Paladin', 'PC', 19, None, 'Party01', 1, 5)
                  ]
    
    
    Stats = [(1, 16, 16, 14, 15, 15, 18, 12, 14, 30, 1),
             (2, 12, 17, 14, 13, 15, 15, 16, 21, 35, 2),
             (3, 20, 18, 15, 15, 18, 15, 15, 17, 30, 3),
             (4, 17, 15, 14, 10, 15, 14, 18, 23, 20, 4),
             (5, 13, 16, 11, 13, 11, 13, 14, 22, 30, 5),
             (6, 15, 20, 12, 18, 13, 16, 16, 24, 25, 6),
             (7, 20, 13, 14, 14, 16, 18, 18, 31, 30, 7)
             ]

    Weapons = [(2, 'Dagger', 1, 'Simple Melee', None, '1d4', 3),
               (18, 'Great Axe', 7, 'Martial Melee', None, '1d12', 2),
               (19, 'Greatsword', 6, 'Martial Melee', None, '2d6', 2),
               (28, 'Shortsword', 2, 'Martial Melee', None, '1d6', 1),
               (36, 'Longbow', 2, 'Martial Ranged', None, '1d8', 3)
               ]

   
    Parties = [('Party01', 7, 'Starter Quest', 1)]

    Locations = [(1, 'Adramyttium', 'Spawn Town'),
                 (2, 'Epidamnos', 'Neighboring town to Spawn Town'),
                 (3, 'Neapolis', 'First Major city')
                 ]

    Quests = [('Starter Quest', 'Main Quest', 'Dagger', 500, 1, 'Locate the town of Neapolis')]

    Progress = [('Locate the town of Neapolis', 'No')]

    c.executemany('INSERT INTO Character_Description VALUES (?,?,?,?,?,?,?,?,?,?)', Characters)

    c.executemany('INSERT INTO Character_Stats VALUES (?,?,?,?,?,?,?,?,?,?,?)', Stats)

    c.executemany('INSERT INTO Weapon VALUES (?,?,?,?,?,?,?)', Weapons)

    c.executemany('INSERT INTO Party VALUES (?,?,?,?)', Parties)

    c.executemany('INSERT INTO Location VALUES (?,?,?)', Locations)

    c.executemany('INSERT INTO Quest VALUES (?,?,?,?,?,?)', Quests)

    c.executemany('INSERT INTO Quest_Progress VALUES (?,?)', Progress)

def runQuery():
    tables = eg.multchoicebox(msg="Pick up to two tables", title="table", choices=['Character_Description', 'Character_Stats', 'Character_Level', 'Party', 'Weapon', 'Spell', 'Learns', 'Location', 'Quest', 'Quest_Progress'], preselect=None)
    table1 = tables[0]
    if len(tables) == 2:
        table2 = tables[1]
    #print(table1)


    if table1 == 'Character_Description':
        attributes = ['CHAR_ID', 'CHAR_Name', 'CHAR_Race', 'CHAR_Class', 'CHAR_Disposition', 'WEAPON_ID', 'SPELL_Name', 'PARTY_Name', 'LOCATION_ID', 'CHARLVL_Level', '*']
    elif table1 == 'Character_Stats':
        attributes = ['STAT_ID', 'STAT_Strength', 'STAT_Dexterity', 'STAT_Wisdom', 'STAT_Intelligence', 'STAT_Constitution', 'STAT_Charisma', 'STAT_AC', 'STAT_HP', 'STAT_Speed', 'CHAR_ID', '*']
    elif table1 == 'Character_Level':
        attributes = ['CHAR_Level', 'CHAR_TotalExp', '*']
    elif table1 == 'Party':
        attributes = ['PARTY_Name', 'PARTY_Size', 'QUEST_Name', 'LOCATION_ID', '*']
    elif table1 == 'Quest':
        attributes = ['QUEST_Name', 'QUEST_Type', 'QUEST_ItemReward', 'QUEST_ExpRewards', 'LOCATION_ID', 'QUEST_MainObjective', '*']
    elif table1 == 'Quest_Progress':
        attributes = ['Quest_MainObjective', 'Quest_CompletionStatus', '*']
    elif table1 == 'Location':
        attributes = ['LOCATION_ID', 'LOCATION_Name', 'LOCATION_Description', '*']
    elif table1 == 'Spell':
        attributes = ['SPELL_Name', 'SPELL_Level', 'SPELL_Type', 'SPELL_Description', 'SPELL_PrimaryStat', 'SPELL_Range', 'SPELL_DamageDice', 'SPELL_Class', '*']
    elif table1 == 'Weapon':
        attributes = ['WEAPON_ID', 'WEAPON_Description', 'WEAPON_Size', 'WEAPON_Type', 'WEAPON_MagicType', 'WEAPON_DamageDice', 'LOCATION_ID', '*']
    col = eg.multchoicebox(msg="Pick attributes", title="attributes", choices=attributes, preselect=None)
    #print(len(col))
    col2=''
    j = 0
    for i in col:
        if j == len(col)-1:
            col2 = col2 + i
        else:
            col2 = col2 + i + ', '
        j = j + 1
    #print(col2)
    where = eg.textbox(msg='Add any stipulations', title='Where')
    #print(where)
    if where == "":
        Query = 'SELECT {0} FROM {1}'.format(col2, table1)
    else:  
        Query = 'SELECT {0} FROM {1} WHERE {2}'.format(col2, table1, where)
    #print(Query)
    result = []
    for row in c.execute(Query):
        result.append(row)
    output = tabulate(result, headers=attributes)
    print(output)
    eg.textbox(msg='Query Result', title='Results', text=output, codebox=True)


cont = True
dbCreated = tableExists()

if dbCreated == False:
    createDB()

popTables()

while cont == True:
    runQuery()
    cont = eg.ynbox(msg="Would you like to perform another query?", title="Continue (Y/N)", choices=['[<F1>]Yes', '[<F2>]No'])

####table1 = input('What table would you like to pull data from: ')
####
####table2 = input('If you would like to use a second table in query, please input the name here (leave blank if only one table will be used: ')
####
####if table2 == "":
####
####    col = input('What attributes would you like to pull data from (use * for all attributes or separate attributes with comma): ')
####
####    where = input('Input any stipulations in results (such as CHAR_Name = "Ronan" or blank for no stipulations): ')
####
####    if where == "":
####        Query = 'SELECT {0} FROM {1}'.format(col, table1)
####    else:  
####        Query = 'SELECT {0} FROM {1} WHERE {2}'.format(col, table1, where)
####else:
####
####    if table1 == "Character_Description":
####        primaryKey = "CHAR_ID"
####    elif table1 == "Character_Stats":
####        primaryKey = "STAT_ID"
####    elif table1 == "Character_Level":
####        primaryKey = "CHAR_Level"
####    elif table1 == "Party":
####        primaryKey = "PARTY_Name"
####    elif table1 == "Weapon":
####        primaryKey = "WEAPON_ID"
####    elif table1 == "Spell":
####        primaryKey = "SPELL_Name"
####    elif table1 == "Location":
####        primaryKey = "LOCATION_ID"
####    elif table1 == "Quest":
####        primaryKey = "QUEST_Name"
####    
####    attributes = input('What attributes would you like to pull data from (use format of TableName.AttributeName, or * for all): ')
####    
####    where = input('Input any stipulations in results (such as Weapon.WEAPON_Description = "Dagger" or blank for no stipulations): ')
####
####    if where == "":
####        Query = 'SELECT {0} FROM {1} LEFT JOIN {2} ON {1}.{3} = {2}.{3}'.format(attributes, table1, table2, primaryKey)
####    else:
####        Query = 'SELECT {0} FROM {1} LEFT JOIN {2} ON {1}.{4} = {2}.{4} WHERE {3}'.format(attributes, table1, table2, where, primaryKey)
####
####for row in c.execute(Query):
####    print(row)
####root_width = int(5, 5)
##
##
##
##
##
##
##
####layout = [[sg.Text('Dungeons and Dragons Database', size=(30, 1), font=("Helvetica", 25), text_color='blue')],      
####    [sg.Text('Please select a table'), sg.DropDown(['Character_Description', 'Character_Stats', 'Character_Level', 'Party', 'Weapon', 'Spell', 'Learns', 'Location', 'Quest', 'Quest_Progress'])],
####    if table1 == 'Party':
####          [sg.Text('Please select attributes'), attributes = sg.DropDown(['PARTY_Name', 'PARTY_Size', 'QUEST_Name', 'LOCATION_ID', '*'])
#### sg.FolderBrowse()],      
####[sg.Submit(), sg.Cancel(), sg.Button('Customized', button_color=('white', 'green'))]]      
####
####event, values  = sg.Window('Everything bagel', auto_size_text=True, default_element_size=(40, 1)).Layout(layout).Read()
####sg.DropDown(['Character_Description', 'Character_Stats', 'Character_Level', 'Party', 'Weapon', 'Spell', 'Learns', 'Location', 'Quest', 'Quest_Progress'])
