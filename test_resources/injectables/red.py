from jacked import injectable
from test_resources.color import Color


@injectable()
class Red(Color):
    def name(self):
        return 'RED'
