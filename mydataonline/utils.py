from itsdangerous import URLSafeSerializer


def get_encrypted_decrypted_name(name, flag):
    """
    function return encrypted or decrypted name depend on flag
    :param name:
    :param flag 0: encrypt or 1: decrypt:
    :return:
    """
    secret_key = "*5vmoo6mpq)ep0o*q893go2m3+o30ipc2h9)$%vnbmcge63tp("
    auth_s = URLSafeSerializer(secret_key, "auth")
    if flag == 0:
        return auth_s.dumps(name)
    else:
        return auth_s.loads(name)