import tingbot
from tingbot import *
from tingbot.graphics import Image
import json, urllib
import random, time
import requests

screen.fill(color='black')

state = {
    'autoloop': True,
    'colors': ['black'],
    'img': 'empty.png',
    'json': '',
    'lapse': 0,
    'pause': False,
    'pos': 0,
    'scroll_position': 0,
    'showMenu': True,
}
#tingbot.app.settings['showMenu'] = True

def drawMenu():
    if state['showMenu']:
        screen.rectangle(xy=(0,0), size=(320,17), color=(128,128,128), align='topleft')
        screen.rectangle(xy=(0,0), size=(320,16), color=(220,220,220), align='topleft')
        screen.text('<<', xy=(0,0), color='black', align='topleft', font_size=12)
        screen.text('Loop', xy=(40,0), color='black', align='topleft', font_size=12)
        screen.text('Pause', xy=(245,0), color='black', align='topleft', font_size=12)
        screen.text('>>', xy=(304,0), color='black', align='topleft', font_size=12)
        screen.text('(Tap screen to hide menu)', xy=(160,1), color='black', align='top', font_size=10)

def loadingScreen():
    screen.fill(color=random.choice(state['colors']))
    screen.image('loading.gif',max_width=320, max_height=240, scale='fit')
    drawMenu()
    screen.update()

def clearScreen():
    screen.fill(color='black')
    screen.update()

def loadurl():
    loadingScreen()
    url = 'http://api.giphy.com/v1/gifs/search?limit=100&q=seinfeld&api_key=dc6zaTOxFJmzC'
    state['json'] = json.load(urllib.urlopen(url))
    state['pos'] = random.randrange(0,len(state['json']['data']),1)
    query()

def query():
    state['img'] = state['json']['data'][state['pos']]['images']['fixed_height']['url']

def switch(forward):
    state['lapse'] = 0
    if forward:
        state['pos'] += 1
    else:
        state['pos'] -= 1
    if state['pos'] < 1:
        state['pos'] = len(state['json']['data']) - 1
    elif state['pos'] == len(state['json']['data']):
        state['pos'] = 0
    query()

@left_button.press
def left():
    #prev
    switch(False)

@right_button.press
def right():
    #next
    switch(True)

@midright_button.press
def midright():
    #pause
    state['pause'] = not state['pause']

@midleft_button.press
def toggleauto():
    #toggle auto loop
    state['autoloop'] = not state['autoloop']

@touch()
def on_touch(xy, action):
    if action == 'down':
        state['showMenu'] = not state['showMenu']

@every(seconds=1.0/30)
def loop():
    if not state['pause']:
        if state['autoloop']:
            state['lapse'] += 1;
            if state['lapse'] > 1 * 30 * 5:
                    state['lapse'] = 0
                    switch(True)
        screen.fill(color='black')
        screen.image(state['img'] + '.gif',max_width=320, max_height=240, scale='fit')
        drawMenu()

loadurl()
tingbot.run()
