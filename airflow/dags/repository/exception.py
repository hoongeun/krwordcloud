#!/usr/bin/env python3

class NotImplemented(Exception):
    def __init__(self, args):
        self.message = f'{args} is not implemented'

    def __str__(self):
        return self.message
