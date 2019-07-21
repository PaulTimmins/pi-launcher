Summary:
The goal is an NFPA 1123 Chapter 9 compliant electronic firing system that uses a cell phone and costs substantially less than commercial firing systems for hobbyist use.

* 9.2.1.1 - Compliant because of 9.2.1.2 - you'll be manufacturing it yourself.
* 9.2.2 - Compliance achieved through the keyswitch that applies firing current
* 9.2.3 - Exceeds - You must: Turn key to energize circuit, flip up covered switch and select ARM locally, then from the handset you must select ARM and the fire buttons become available and operational. Only two positive steps are *required* to ignite an e-match (ARM and Fire would work) but here we are, being awesome.
* 9.2.4 - The switches must be clearly labeled to indicate what they do. That's on you.
* 9.2.5 - My arm switch has an illuminating shroud, but you could use an LED or buzzer to achieve the same compliance

9.2.6 Handheld firing unit requirements (ie: your phone or laptop/tablet)
* 9.2.6.1 - Must have two actions to fire unit, one to arm and one to fire. (see 9.2.3, we're protecting well beyond this)
* 9.2.6.2 - Switches must be identified - the interface makes it clear enough
* 9.2.6.3 - irrelevant
* 9.2.6.2 - irrelevant
* 9.2.7 - not currently relevant as auto-firing doesn't exist so there's not a deadman switch implementation
* 9.2.8 - Final design will implement the 0.05ampere test current into a short limitation. A small resistor inline works great while still reaching the trigger requirement for the Raspberry Pi's GPIO pin.
* 9.2.9 - if you're going to use a multimeter, use a high internal resistance one. That's on you though.
* 9.2.10 - Shunts aren't required. But too bad, you're getting them anyway because returning with 10 fingers and 10 toes is my top priority and ESD is no joke.
* 9.2.11 - The power supply for firing should be independent. Good news, that's why we have the LiPo. You'll want that for the current rating anyway and LiPo balance chargers are cheap. Thanks, RC enthusiasts!
* 9.2.11.1 - Batteries should be enclosed. Well, we're using LiPo and hell yeah, put those in a box. There's basically fire inside those things just BEGGING to be released. Don't let fireworks sparks touch them. That should be a given but hey, since we're here I'll say it.
* 9.2.11.2 - Running the blasting unit from commercial power. It needs to be isolated. But really, who has commercial power close enough to be using this most of the time. Well, if you do, you'll need a stepdown transformer anyway so you'll probably be compliant.

The rest are operational requirements. Read them. They're really, really good ideas.


System prep after installing Raspian lite:

add iwconfig wlan0 power off to /etc/rc.local

apt-get install lightttpd python3-gpiozero python3-aiohttp python3-daemonize

cp index.html /var/www/html/index.html (or change permissions and ln to it)

add /root/pi-launcher/fireproxy.py to /etc/rc.local

References:

Make the system expose its own AP:
https://blog.thewalr.us/2017/09/26/raspberry-pi-zero-w-simultaneous-ap-and-managed-mode-wifi/

NFPA 1123 - Free read available with account:
https://www.nfpa.org/codes-and-standards/all-codes-and-standards/list-of-codes-and-standards/detail?code=1123
