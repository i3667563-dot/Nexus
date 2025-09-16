import passy.modules.password.main as passyPass

class Password():
    def __init__(self):
        self.generate = passyPass.generate
        self.check_password = passyPass.proverka