import bottle
import os


@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.get('/')
def index():
    head_url = '%s://%s/static/0009.gif' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    return {
        'color': '#000000',
        'head': head_url
    }


@bottle.post('/start')
def start():
    data = bottle.request.json

    # TODO: Do things with data

    return {
        'taunt': 'WAKAWAKAWAKAWAKAWAKA'
    }


@bottle.post('/move')
def move():
    payload = bottle.request.json

    taunt = ''
    bad_tiles = []

    for snake in payload['snakes']:
        if snake['snake_id'] == '07a8c99f-1077-4a4e-86bf-a6ba390f8546':
            bad_tiles += snake['coords'][1:]
            head = snake['coords'][0]
            health = snake['health']
        else:
            bad_tiles += snake['coords']
            bad_tiles.append([snake['coords'][0][0]+1, snake['coords'][0][1]])
            bad_tiles.append([snake['coords'][0][0]-1, snake['coords'][0][1]])
            bad_tiles.append([snake['coords'][0][0], snake['coords'][0][1]+1])
            bad_tiles.append([snake['coords'][0][0], snake['coords'][0][1]-1])

    for wall in payload.get('walls', []):
        bad_tiles.append(wall)

    smallest = 999
    target = [0, 0]
    for food in payload['food']:
        x_dis = abs(food[0] - head[0])
        y_dis = abs(food[1] - head[1])
        distance = x_dis + y_dis
        if distance < smallest:
            smallest = distance
            target = food

    if len(payload.get('gold', [])) > 0 and health > 35:
        target = payload['gold'][0]

    move = None
    if target[1] < head[1]:
        if [head[0], head[1]-1] not in bad_tiles:
            move = 'north'
    if target[1] > head[1]:
        if [head[0], head[1]+1] not in bad_tiles:
            move = 'south'
    if target[0] < head[0]:
        if [head[0]-1, head[1]] not in bad_tiles:
            move = 'west'
    if target[0] > head[0]:
        if [head[0]+1, head[1]] not in bad_tiles:
            move = 'east'

    if not move:
        if [head[0], head[1]-1] not in bad_tiles and head[1] > 0:
            move = 'north'
        if [head[0], head[1]+1] not in bad_tiles and head[1] < payload['height']:
            move = 'south'
        if [head[0]-1, head[1]] not in bad_tiles and head[0] > 0:
            move = 'west'
        if [head[0]+1, head[1]] not in bad_tiles and head[0] < payload['width']:
            move = 'east'

    if payload['turn'] % 10 == 0:
        taunt = 'WAKAWAKAWAKAWAKAWAKA'

    if not move:
        taunt = "Fuck it we'll do it live!"

    return {
        'move': move,
        'taunt': taunt
    }


@bottle.post('/end')
def end():
    data = bottle.request.json

    return {
        'taunt': 'WEOWEOWEOWeoweoweow'
    }


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
