import argparse

class ArgumentParser:
    def __init__(self, arguments):
        self.a_parser = argparse.ArgumentParser()
        for arg in arguments:
            self.a_parser.add_argument(
                arg["short_name"], 
                arg["long_name"], 
                required = arg['required'],
                help = arg['help']
            )
    
    def get_args(self):
        return vars(self.a_parser.parse_args())