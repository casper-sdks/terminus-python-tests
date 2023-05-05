

def get_user_asset(path, network, user, file):
    return open(path + "/net-" + network + "/" + "user-" + user + "/" + file).read()


def get_user_asset_path(path, network, user, file):
    return path + "/net-" + network + "/" + "user-" + user + "/" + file
