from os import environ

import django


def main():
    environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()
    from consumer.pubsub import reader, pubsub
    reader(pubsub)


if __name__ == '__main__':
    main()
