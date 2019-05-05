from jacked import injectable
from test_resources.color import Color


@injectable()
class Green(Color):
    def name(self):
        return 'GREEN'
