# BotRoss

[![Build Status](https://travis-ci.org/BotsForRoss/BotRoss.svg?branch=master)](https://travis-ci.org/BotsForRoss/BotRoss)
[![Coverage Status](https://coveralls.io/repos/github/BotsForRoss/BotRoss/badge.svg)](https://coveralls.io/github/BotsForRoss/BotRoss)

## Inspiration

> We tell people sometimes: we're like drug dealers, come into town and get everybody absolutely addicted to painting. It doesn't take much to get you addicted. The least little bit can do so much. This is unplanned it really just happens. Each highlight must have it's own private shadow. Steve wants reflections, so let's give him reflections.

> This is an example of what you can do with just a few things, a little imagination and a happy dream in your heart. You're the greatest thing that has ever been or ever will be. You're special. You're so very special. The shadows are just like the highlights, but we're going in the opposite direction. Everybody needs a friend.

> This is your world. But we're not there yet, so we don't need to worry about it. You need the dark in order to show the light.

> Do an almighty painting with us. How do you make a round circle with a square knife? That's your challenge for the day. We must be quiet, soft and gentle. We spend so much of our life looking - but never seeing.

> I guess that would be considered a UFO. A big cotton ball in the sky. If there's two big trees invariably sooner or later there's gonna be a little tree. It looks so good, I might as well not stop.

> Water's like me. It's laaazy ... Boy, it always looks for the easiest way to do things You have to make those little noises or it won't work. Let's have a happy little tree in here. Poor old tree.

> Just use the old one inch brush. It's a very cold picture, I may have to go get my coat. It’s about to freeze me to death. If you do too much it's going to lose its effectiveness. Get away from those little Christmas tree things we used to make in school. Just pretend you are a whisper floating across a mountain.

- Bot Ross

## Helpful Things

### Install

`pip install -r requirements.txt`

Run the following for xbox controller support (only on Linux):
`sudo apt-get install xboxdrv`

### Test

`python -m unittest discover bot_ross`

### Run

To control the X and Y stepper motors with the left analog stick of an xbox controller:
`sudo python try_xbox`

Other, more sane entry points are `stepper_motor.py` and `servo_motor.py`.

