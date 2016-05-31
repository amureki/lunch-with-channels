import random

from .exceptions import ClientError


def catch_client_error(func):
    """
    Decorator to catch the ClientError exception and translate it into a reply.
    """

    def inner(message):
        try:
            return func(message)
        except ClientError as e:
            # If we catch a client error, tell it to send an error string
            # back to the client on their reply channel
            e.send_to(message.reply_channel)

    return inner


def generate_name():
    adjective_list = [
        'Admiring',
        'Adoring',
        'Agitated',
        'Amazing',
        'Angry',
        'Awesome',
        'Backstabbing',
        'Berserk',
        'Big',
        'Boring',
        'Clever',
        'Compassionate',
        'Condescending',
        'Cranky',
        'Desperate',
        'Determined',
        'Distracted',
        'Dreamy',
        'Drunk',
        'Ecstatic',
        'Elated',
        'Elegant',
        'Evil',
        'Fervent',
        'Focused',
        'Furious',
        'Gigantic',
        'Gloomy',
        'Goofy',
        'Grave',
        'Happy',
        'High',
        'Hopeful',
        'Hungry',
        'Infallible',
        'Jolly',
        'Jovial',
        'Kickass',
        'Lonely',
        'Loving',
        'Mad',
        'Modest',
        'Naughty',
        'Nauseous',
        'Nostalgic',
        'Pedantic',
        'Pensive',
        'Prickly',
        'Reverent',
        'Romantic',
        'Sad',
        'Serene',
        'Sharp',
        'Sick',
        'Silly',
        'Sleepy',
        'Small',
        'Stoic',
        'Stupefied',
        'Suspicious',
        'Tender',
        'Thirsty',
        'Tiny',
        'Trusting',
    ]
    subject_list = [
        'Kraven the Hunter',
        'Juggernaut',
        'Marvel Girl',
        'Swarm',
        'Black Bolt',
        'Loki Lauyefson',
        'Ghost Rider',
        'Professor X',
        'Quicksilver',
        'Kingpin',
        'Doctor Octopus',
        'Green Goblin',
        'Red Skull',
        'Colossus',
        'Shadowcat',
        'Cyclops',
        'Havok',
        'Luke Cage',
        'Black Widow',
        'Beast',
        'The Multiple Man',
        'Silver Surfer',
        'Ultron',
        'Captain Britain',
        'Iron Man',
        'The Punisher',
        'Ego the Living Planet',
        'Nightcrawler',
        'Annihilus',
        'Deadpool',
        'Captain America',
        'Fin Fang Foom',
        'Daredevil',
        'J Jonah Jameson',
        'Kang the Conqueror',
        'Beta Ray Bill',
        'Doctor Stephen Strange',
        'Wolverine',
        'MODOK',
        'Nick Fury',
        'Emma Frost',
        'Black Panther',
        'The Hulk',
        'Thing',
        'Galactus',
        'Magneto',
        'Spider-Man',
        'Doctor Victor Von Doom',
    ]

    left = random.choice(adjective_list)
    right = random.choice(subject_list)
    name = '{} {}'.format(left, right)
    return name
