def Error(error):
    print("\033[1;31;40mError: \033[0;31;40m" + error + "\033[0;37;40m")

def Warning(warning):
    print("\033[1;33;40mWARNING: \033[0;33;40m" + warning + "\033[0;37;40m")

def Info(info):
    print("\033[1;34;40mINFO: \033[0;34;40m" + info + "\033[0;37;40m")

def Game(game):
    print("\033[1;32;40m" + game + "\033[0;37;40m")

def Bold(bold):
    print("\033[1;37;40m" + bold + "\033[0;37;40m")