import sys
from bot import BoatBot
from boards import shot_calculators as shots

class CosmoBot(BoatBot):
    def __init__(self, host, port):
        super().__init__(host, port, shots.RandomShotCalculator(), 'cosmo')

# Cosmo boat bot main
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: ' + sys.argv[0] + ' server_host server_port')
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])

    cosmo = CosmoBot(host, port)
    cosmo.run()
