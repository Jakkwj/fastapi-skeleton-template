from base64 import (
    b64decode,
    b64encode,
)

from Crypto import Random
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_cipher
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5 as PKCS1_signature

from config.config import get_settings

settings = get_settings()
"""测试环境下, 此文件处的所有加密解密功能都是跳过的, 即无效的
"""


def get_RAS_keys(name: str = "") -> None:
    """生成 RSA 密钥对.
        https://www.cnblogs.com/qxh-beijing2016/p/15249911.html

    需要生成 2 对 公钥私钥:
        前端: 公钥A + 私钥B: 公钥A 加密信息, 私钥B 签名
        后端: 私钥A + 公钥B: 私钥A 解密信息, 公钥B验证签名
    """
    rsa = RSA.generate(2048, Random.new().read)

    private_pem = rsa.exportKey()
    with open(f"private_{name}.pem", "wb") as f:
        f.write(private_pem)

    public_pem = rsa.publickey().exportKey()
    with open(f"public_{name}.pem", "wb") as f:
        f.write(public_pem)


def encrypt_data(data: str):
    """使用公钥加密"""
    if settings.ENV == "development":
        return data

    rsakey = RSA.importKey(settings.PUBLIC_KEY_CLIENT)
    cipher = PKCS1_cipher.new(rsakey)
    return b64encode(cipher.encrypt(bytes(data.encode("utf8")))).decode("utf-8")


def decrypt_data(data: str) -> str:
    """使用私钥解密"""
    if settings.ENV == "development":
        return data

    rsakey = RSA.importKey(settings.PRIVATE_KEY_SERVER)
    cipher = PKCS1_cipher.new(rsakey)
    return cipher.decrypt(b64decode(data), "Decrypt error.").decode("utf-8")  # type: ignore


def sign_data(data: str) -> str:
    """使用私钥生成签名.
    Returns:
        signature: 签名
    """
    if settings.ENV == "development":
        return data

    rsakey = RSA.importKey(settings.PRIVATE_KEY_SERVER)
    signer = PKCS1_signature.new(rsakey)
    digest = SHA256.new()
    digest.update(data.encode("utf8"))
    sign = signer.sign(digest)
    signature = b64encode(sign)
    return signature.decode("utf-8")


def verifier_sign(data_decrypted: str, signature: str) -> bool:
    """使用公钥验证签名.

    验证签名通过, 说明是正确的前端发起的请求 ,而不是别人的 api

    Args:
        data_decrypted: str, 解密后的数据
        signature: str, 签名

    Returns:
        True: 验证成功, 本人
        False:验证失败, 不是本人
    """
    if settings.ENV == "development":
        return True

    rsakey = RSA.importKey(settings.PUBLIC_KEY_CLIENT)
    verifier = PKCS1_signature.new(rsakey)
    digest = SHA256.new()
    digest.update(data_decrypted.encode("utf8"))
    return verifier.verify(digest, b64decode(signature))


if __name__ == "__main__":
    get_RAS_keys("server")
    get_RAS_keys("client")
