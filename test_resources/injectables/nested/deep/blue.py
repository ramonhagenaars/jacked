from jacked import injectable
from test_resources.color import Color


@injectable()
class Blue(Color):
    def name(self):
        return 'BLUE'
