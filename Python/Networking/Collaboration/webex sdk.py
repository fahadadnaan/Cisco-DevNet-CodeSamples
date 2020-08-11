from webexteamssdk import WebexTeamsAPI
api = WebexTeamsAPI(
    access_token='MTYzNjU0NzgtZmUyMi00YThhLWFhNjQtMjhjMDZhZjIzZTcxZTBkNWNmMDAtN2Nl_PF84_75e84279-5cba-4094-949a-7133a3be6509')

#### GET TEAM INFO ###

teams = api.teams.list()

for team in teams:
    print(team)
    if getattr(team, 'name') != 'Fahad Team':
        create_team = api.teams.create('Fahad Team')
        teamId = getattr(create_team, 'id')
    else:
        teamId = team.id


###### PEOPLE #####
print(api.people.me())
print(api.people.list())
api.people.create(emails=['fahad.adnan@my.com'], displayName='Fahad Adnan 2', firstName='Fahad',
                  lastName='Adnan 2', roles=['Y2lzY29zcGFyazovL3VzL1JPTEUvaWRfZnVsbF9hZG1pbg'])

#### ROLES #####
roles = api.roles.list()
# print(roles)
for role in roles:
    print(role)


#### ROOMS #####
rooms = api.rooms.list()
evaluator = False
for room in rooms:
    if room.title == 'Fahad Room':
        evaluator = True
        roomId = room.id

if evaluator == False:
    new_room = api.rooms.create('Fahad Room', teamId=teamId)
    roomId = new_room.id


#### MESSAGES ####
api.messages.create(roomId, text='Posted from the SDK')

# CLEANUP
# for room in rooms:
#     if getattr(room, 'title') == 'Fahad Room':
#         api.rooms.delete(getattr(room, 'id'))

# for team in teams:
#     if getattr(team, 'name') == 'Fahad Team':
#         api.teams.delete(getattr(team, 'id'))
