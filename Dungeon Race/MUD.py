import socket
import urllib
from urllib import parse
import json
from random import randint

in_store = False

LOGIN_MESSAGE = "What is your name?"

DIRECTIONS = ['north', 'south', 'east', 'west']

def match_command(txt):
    return lambda cmd: cmd['match'](txt)


def match_exactly(m):
    return lambda s: s == m


def match_one_of(list):
    return lambda s: s in list


def match_in(d, val):
    return lambda x: d[x] == val


def match_starting_with(str):
    return lambda s: s.startswith(str)


def match_by(key, val):
    return lambda x: x[key] == val


def find_where(is_true, list):
    for item in list:
        if is_true(item):
            return item
    return None


def get_directions(room):
    dirs = []
    for d in DIRECTIONS:
        if room[d] is not None:
            dirs.append(d)
    return dirs
        

world = {
      'users': [],
      'store': [],
      'rooms': [{'id': 1, 'desc': "", 'north': None, 'south': None, 'east': None, 'west': None}],
      'monsters': [],
      'items': []
  }

def decode(start, end, str):
    start_index = str.find(start)
    if start_index > -1 and end == '':
        return str[start_index + len(start):].strip()
    if start_index > -1 and end != '':
        end_index = str.find(end, start_index)
        return str[start_index + len(start):end_index].strip()
    else:
        return ''
    
def http_response(headers, msg):
    return "HTTP/1.1 200 OK\r\n%s\r\n\r\n%s" % ('\r\n'.join(headers), html_page(msg))

def html_page(msg):
    return """
<!DOCTYPE html>
  <html>
    <head>
        <title>My game</title>
        <style>
           li {
            list-style:none;
            font-size:20px;
           }
           .box {
                border:3px solid white;
                border-radius:10px;
                display:inline-block;
                padding:5px;
                text-align:left;
                background-color: #000000;
           }
           body{
               color:#61c8ed;
               background-image:url(https://tinyurl.com/2p9cwnps);
               background-repeat:no-repeat;
               background-size:cover;
               font-family:papyrus;
               font-weight:bold;
           }
           input{
               background-color:rgb(0,0,0, 0.1);
               color:#61c8ed;
               font-family:papyrus;
               width: 300px;
               height:40px;
               border-radius:20px;
               font-size:20px;
               margin:20px;
           }
        </style>
        
    </head>
    
    <body style=text-align:center>
    <div>
      <h1>%s</h1>
      <form method="POST">
        <input id="input" name="txt" placeholder="Type a command and press enter" autofocus autocomplete="off">
      </form>
      
    </div>
    <div class=box>
        <ul>
            <li><b>store:</b> Brings you to the store</li>
            <li><b>inv:</b> Shows your inventory</li>
            <li><b>look:</b> Show room description and avaiable rooms</li>
            <li><b>north:</b> Moves you north...if room available</li>
            <li><b>south:</b> Moves you south...if room available</li>
            <li><b>east:</b> Moves you east...if room available</li>
            <li><b>west:</b> Moves you west...if room available</li>
            <li><b>attack:</b> Type attack, then the name of the monster</li>
            <li><b>grab:</b> Type grab, then the name of the item</li>
            <li><b>logout:</b> End game</li>
        </ul>
    </div>
        
    </body>
    
    <script>

            let myInput;
         
            input.addEventListener("keypress", function(e)
            {
                if(e.key === 'Enter')
                {
                    myInput = document.getElementById("input").value;
                    document.getElementById("input").value = myInput.toLowerCase()
                }
            });
    </script>
    
  </html> """ %msg


def new_user(username):   
    user = {
        'name':username,
        'money': 10,
        'inventory':[],
        'room_id':1,
        'health':20,
        'message':''
    }
    
    world['users'].append(user)
    txt = yield f'''Welcome {username.title()}!
    <br> Read the command list below<br>
    {next(look(username, user))}'''
    
    while txt != 'logout':
        match = find_where(match_command(txt), commands)
        if match is None:
            txt = yield f"Hmm, I don't understand {txt}"
        else:
            gen = match['action'](txt, user)
            result = next(gen)
            while True:
                if 'logout' in user:
                    return
                txt = yield result
                try:
                    result = gen.send(txt)
                except StopIteration:
                    break

def store(txt, user):
    #in_store = True
    
    choice = None
    while choice == None:
        result=''
        result = "You are in the store. Money: %d <br>" % user['money']
        for item in world['store']:
            result += item['name'].title()
            for a in item:
                if a != 'name':
                    result += " %s: %s: " % (a, item[a])
            result += "<br>"
        
        name = yield result + '<br>What would you like to buy? (q to quit)'
        if name == "q":
            yield "Thanks for visiting the store!<br>" + next(look(txt,user))
            return

        choice = find_where(match_by('name', name), world['store'])
        if choice != None and choice['price'] > user['money']:
            result = "You don't have enough money to buy the %s" % choice['name']
            choice = None

    user['money'] -= choice['price']
    user['inventory'].append(choice)
    world['store'].remove(choice)
    yield 'You bought %s. You now have %d dollars left' % (choice['name'].title(), user['money'])

def inv(txt, user):
    result = "Here is your inventory <br>"
    
    for item in user['inventory']:
        result += item['name'].title() + "<br>"
        
    yield result

def escape(txt, user):
    if in_store:
        yield "Bye for Now!"
    yield "Invalid Command"

def look(txt, user):
    room = find_where(match_by('id', user['room_id']), world['rooms'])
    result = 'You look around and see %s<br>' % room['desc']
    result += "You can go %s " % ', '.join(get_directions(room))
    
    for monster in filter(match_by('room_id', room['id']), world['monsters']):
        result += '<br>You see a %s<br>' % monster['name']

    for item in filter(match_by('room_id', room['id']), world['items']):
        result += f"<br>You see a {item['name']}<br>"
        
    yield result

def move(txt, user):
    if txt in DIRECTIONS:
        room = find_where(match_by('id', user['room_id']), world['rooms'])
        if txt in room and room[txt] != None:

            next_room = find_where(match_by('id', room[txt]), world['rooms'])
    
            if('requires_key' in next_room and find_where(match_by('name', next_room['requires_key']),
user['inventory'])) is None:
               yield f"The door is locked. It requires a {next_room['requires_key']}"
               return
                                                          
            user['room_id'] = room[txt]
            if 'winner' in next_room:
                for u in world['users']:
                    if u['name'] != user['name']:
                        u['message'] = f"{u['name']}, you were too slow!<br> {user['name']} is the winner!"
                        u['logout'] = True
                yield f"Congratulations {user['name']}!<br> You are the winner!!!"
            else:
                yield next(look(txt,user))

        else:
            yield "You can't go %s!<br><br>" % txt
        
def attack(txt, user):
    name = txt[7:]
    result = ''
    monster = find_where(match_by('name', name), world['monsters'])
    if monster is None or monster['room_id'] != user['room_id']:
        yield f"{name} isn't here"
        return
    
    while monster['health'] > 0 and user['health'] > 0:
        result += f"Attacking the {monster['name']} Health {monster['health']}. Your health: {user['health']}<br><br>"
        result += "What weapon do you want to use?<br>"
        result += 'fists<br>'
        for item in user['inventory']:
            result += item['name']

        weapon = None
        while weapon == None:
            name = yield result
            weapon = find_where(match_by('name',name),user['inventory'])
            if name == 'fists':
                weapon = {'name': 'fists', 'power':1}

        dmg = randint(0,4) + weapon['power']
        result = f"<br>Your {weapon['name']} dealt {dmg} damage to the {monster['name']}"
        monster['health'] -= dmg

        if monster['health'] > 0:
            result += f"The {monster['name']} is now at {monster['health']} health.<br>"
            dmg = randint(0,4) + monster['attack']
            result += f"The {monster['name']} hits you for {dmg} damage."
            user['health'] -= dmg
    if monster['health'] <= 0:
        result += f"The {monster['name']} has fallen <br><br>"
        reward = randint(1, monster['attack'] * 2)
        user['money'] += reward
        user['health'] += 5 + reward
        monster['health'] = monster['starting_health']
        result += f"You have {user['money']} dollars, and your health is now {user['health']}"
            
    if user['health'] <=0:
        result += "You have fallen"
            

    yield result
            
def grab(txt, user):
    name = txt[5:]
    item = find_where(match_by('name', name), world['items'])
    name = name.title()
    if item is None or item['room_id'] != user['room_id']:
        yield f"{name} isn't here"
        return
    user['inventory'].append(item)
    yield f"You picked up the {name}<br> Check your inventory!<br>" + next(look(txt, user))

def use_item(txt, user):
    name = txt[4:]
    item = find_where(match_by('name', name), user['inventory'])
    if item is None:
        yield f"You do not have a {name}"
        return
    if 'health' in item:
        user['health'] += item['health']
        result = f"You used the {name} and gained {item['health']} health."
        result += f"<br>You now have {user['health']} health."
    elif 'power' in item:
        user['health'] -= item['power']
        result = f"Oops!You hit yourself for {item['power']} damage!<br>YOu should be more careful!"
        result += f"<br>You now have {user['health']} health."
    else:
        result = f"You cannot use the {name}"
        
    yield result

def opposite_direction(dir):
    if dir == 'north': return 'south'
    if dir == 'south': return 'north'
    if dir == 'east': return 'west'
    if dir == 'west': return 'east'

def create_room(txt, user):
    room = find_where(match_by('id', user['room_id']), world['rooms'])
    desc = ''
    while desc == '':
        desc = yield 'Type a description'
    direction = ''
    while direction not in DIRECTIONS:
        direction = yield 'Type a direction (%s)' % ', '.join(filter(match_in(room, None), DIRECTIONS))
        if direction not in DIRECTIONS or room[direction] != None:
            direction = ''
    new_room = {
        'id': len(world['rooms']) + 1, 'desc':desc, 'north': None,'south':None, 'east':None, 'west':None
    }
    world['rooms'].append(new_room)
    room[direction] = new_room['id']
    new_room[opposite_direction(direction)] = room['id']
    user['room_id'] = new_room['id']
    yield next(look(txt, user))

def save_world(txt, user):
    worldName = 'world.json'
    with open(worldName, 'w') as file:
        json.dump(world, file, indent=4)
    yield f"Your world has been saved!<br>You should now have a file named {worldName}"

def load_world(txt, user):
    worldName = 'world.json'
    global world
    with open(worldName, 'r') as file:
        world = json.load(file)
    user['room_id'] = 1
    user['inventory'] = []
    user['health'] = 20
    user['money'] = 10
    world['users'] = user
    yield f"{worldName} loaded!<br><br>" + next(look(txt, user))
    

commands = [
      {'match': match_exactly('store'), 'action':store},
      {'match': match_exactly('inv'), 'action':inv},
      {'match': match_exactly('q'), 'action':escape},
      {'match': match_exactly('look'), 'action':look},
      {'match': match_one_of(DIRECTIONS), 'action':move},
      {'match': match_starting_with('attack '), 'action':attack},
      {'match': match_starting_with('grab '), 'action':grab},
      {'match': match_starting_with('use '), 'action':use_item},
      {'match': match_exactly('create room'), 'action':create_room},
      {'match': match_exactly('save world'), 'action':save_world},
      {'match': match_exactly('load world'), 'action':load_world}
  ]

def start_server():
  
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    port = 12345
    print('Listening at http://localhost:%d' % port)
    s.bind(('',port))
    s.listen(5)

    clients = {}

    while True:
        c,addr = s.accept()
        print("Got connection from %s\n" % str(addr))
        request = c.recv(4096).decode()
        print(request)
        headers = []

        txt = parse.unquote_plus(decode('txt=', '', request))
        print(txt)

        username = decode('username=', '\r\n', request)

        if username == '' and txt == '':
            result = LOGIN_MESSAGE
            
        if username == '' and txt !='':
            username = txt

        if username != '':
            if username not in clients:
                clients[username] = new_user(username)
                headers = ['Set-Cookie: username=%s;' % username]
                result = next(clients[username])
            else:
                try:
                    result = clients[username].send(txt)
                except StopIteration:
                    del clients[username]
                    
                    user = find_where(match_by('name', username), world['users'])
                    print(user)
                    result = user['message'] + LOGIN_MESSAGE
                    headers = ['Set-Cookie: username=; expires=Thu, 01 Jan 1970 00:00:00 GMT;']


        output = http_response(headers, result)
        c.sendall(output.encode())
        c.close()

start_server()
  
