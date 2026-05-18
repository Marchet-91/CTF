from Crypto.Util.number import getPrime, bytes_to_long, long_to_bytes
import os, enum, hashlib, hmac, time, datetime as dt, dataclasses

DEBUG = True


class DataType(enum.Enum):
    RSA_ENC = 1
    RSA_SIG = 2


VERSION = "Just some version between v0.0.1 and v1.0.0"
ENC_OID = ('Just an OID for encryption, maybe I should have asked GPT for some ideas, '
           'although I prefer Claude for encryption OIDs that involve RSA and SHA1 '
           ':).')
SIG_OID = ('Just an OID for signing, maybe I should have asked Claude for some ideas, '
           'although I prefer GPT for signing OIDs that involve RSA and SHA1 '
           ':).')
ENC_ALGORITHM = ('Just an encryption algorithm, maybe I should have asked GPT for some ideas, '
                 'although I prefer Claude for encryption algorithms that involve RSA and SHA1 '
                 ':).')
SIG_ALGORITHM = ('Just a signing algorithm, maybe I should have asked Claude for some ideas, '
                 'although I prefer GPT for signing algorithms that involve RSA and SHA1 '
                 ':).')


@dataclasses.dataclass(frozen=True)
class RSAEncryptionData:
    version: bytes
    oid: bytes
    algorithm_name: bytes
    hmac_key: bytes
    digest_message: bytes
    timestamp: bytes
    plaintext: bytes
    
    def serialize(self) -> bytes:
        data = b""
        data += len(self.version).to_bytes(2, 'little') + self.version
        data += len(self.oid).to_bytes(2, 'little') + self.oid
        data += len(self.algorithm_name).to_bytes(2, 'little') + self.algorithm_name
        data += len(self.hmac_key).to_bytes(2, 'little') + self.hmac_key
        data += len(self.digest_message).to_bytes(2, 'little') + self.digest_message
        data += len(self.timestamp).to_bytes(2, 'little') + self.timestamp
        data += len(self.plaintext).to_bytes(2, 'little') + self.plaintext
        return data
    
    @classmethod
    def deserialize(cls, data: bytes):
        offset = 0

        def parse_field() -> bytes:
            nonlocal offset, data
            field_len = int.from_bytes(data[offset:offset+2], 'little')
            offset += 2
            field = data[offset:offset+field_len]
            offset += field_len
            return field
        
        version = parse_field()
        oid = parse_field()
        algorithm_name = parse_field()
        hmac_key = parse_field()
        digest_message = parse_field()
        timestamp = parse_field()
        plaintext = parse_field()
        
        return cls(
            version=version,
            oid=oid,
            algorithm_name=algorithm_name,
            hmac_key=hmac_key,
            digest_message=digest_message,
            timestamp=timestamp,
            plaintext=plaintext,
        )


@dataclasses.dataclass(frozen=True)
class RSASignatureData:
    version: bytes
    oid: bytes
    algorithm_name: bytes
    hmac_key: bytes
    digest_message: bytes
    timestamp: bytes

    def serialize(self) -> bytes:
        data = b""
        data += len(self.version).to_bytes(2, 'little') + self.version
        data += len(self.oid).to_bytes(2, 'little') + self.oid
        data += len(self.algorithm_name).to_bytes(2, 'little') + self.algorithm_name
        data += len(self.hmac_key).to_bytes(2, 'little') + self.hmac_key
        data += len(self.digest_message).to_bytes(2, 'little') + self.digest_message
        data += len(self.timestamp).to_bytes(2, 'little') + self.timestamp
        return data
    
    @classmethod
    def deserialize(cls, data: bytes):
        offset = 0

        def parse_field() -> bytes:
            nonlocal offset, data
            field_len = int.from_bytes(data[offset:offset+2], 'little')
            offset += 2
            field = data[offset:offset+field_len]
            offset += field_len
            return field
        
        version = parse_field()
        oid = parse_field()
        algorithm_name = parse_field()
        hmac_key = parse_field()
        digest_message = parse_field()
        timestamp = parse_field()
        
        return cls(
            version=version,
            oid=oid,
            algorithm_name=algorithm_name,
            hmac_key=hmac_key,
            digest_message=digest_message,
            timestamp=timestamp,
        )


def pad(data: bytes, block_size: int) -> bytes:
    # ISO/IEC 7816-4 padding
    assert len(data) < block_size
    padding_len = block_size - len(data) % block_size
    padding = b'\x80' + b'\x00'*(padding_len - 1)
    return data + padding


def unpad(data: bytes, block_size: int) -> bytes:
    # ISO/IEC 7816-4 padding.
    padding_len = len(data) - data.rfind(b'\x80')
    return data[:-padding_len]


def timestamp_diff(t0: str, t1: str) -> dt.timedelta:
    t0 = dt.datetime.strptime(t0, "%c")
    t1 = dt.datetime.strptime(t1, "%c")
    return t1 - t0


class RSA:
    def __init__(self, nbits=1 << 12): # nbits = 4096
        self.e = 0x10001
        self.p = getPrime(nbits // 2) # 2048
        self.q = getPrime(nbits // 2) # 2048
        self.dp = pow(self.e, -1, self.p - 1)
        self.dq = pow(self.e, -1, self.q - 1)
        self.qInv = pow(self.q, -1, self.p) # inverso di 1 modulo p
        self.n = self.p * self.q # N
        self.bl = self.n.bit_length() // 8

    def parse(self, msg: bytes, hmac_key: bytes, data_type: DataType):
        timestamp = time.ctime().encode()
        digest_message = self.hmac_digest(hmac_key, msg, timestamp)
        
        if data_type == DataType.RSA_ENC:
            data = RSAEncryptionData(
                version=VERSION.encode(),
                hmac_key=hmac_key,
                oid=ENC_OID.encode(),
                timestamp=timestamp,
                algorithm_name=ENC_ALGORITHM.encode(),
                digest_message=digest_message,
                plaintext=msg
            )
        elif data_type == DataType.RSA_SIG:
            data = RSASignatureData(
                version=VERSION.encode(),
                hmac_key=hmac_key,
                oid=SIG_OID.encode(),
                timestamp=timestamp,
                algorithm_name=SIG_ALGORITHM.encode(),
                digest_message=digest_message
            )
        else:
            raise ValueError('Unknown Data Type.')
        
        m = bytes_to_long(pad(data.serialize(), self.bl))
        if m >= self.n:
            raise ValueError('Message is too long.')
        return m

    def unparse(self, m: int, data_type: DataType):
        data = unpad(long_to_bytes(m), self.bl)
        if data_type == DataType.RSA_ENC:
            return RSAEncryptionData.deserialize(data)
        elif data_type == DataType.RSA_SIG:
            return RSASignatureData.deserialize(data)
        else:
            raise ValueError('Unknown Data Type.')

    @staticmethod
    def hmac_digest(hmac_key: bytes, msg: bytes, timestamp: bytes) -> bytes:
        return hmac.digest(hmac_key, msg + b"|" + timestamp, hashlib.sha1)

    def encrypt(self, msg: bytes, hmac_key: bytes) -> int:
        return pow(self.parse(msg, hmac_key, DataType.RSA_ENC), self.e, self.n)

    def decrypt(self, enc: int) -> bytes:
        mp = pow(enc, self.dp, self.p)
        mq = pow(enc, self.dq, self.q)
        h = (self.qInv * (mp - mq)) % self.p
        m = mq + h * self.q
        data = self.unparse(m, DataType.RSA_ENC)
        digest_message = self.hmac_digest(
            data.hmac_key,
            data.plaintext,
            data.timestamp
        )
        if digest_message != data.digest_message:
            raise ValueError('Invalid HMAC.')
        return data.plaintext

    def sign(self, msg: bytes, hmac_key: bytes) -> int:
        sp = pow(self.parse(msg, hmac_key, DataType.RSA_SIG), self.dp, self.p)
        sq = pow(self.parse(msg, hmac_key, DataType.RSA_SIG), self.dq, self.q)
        h = (self.qInv * (sp - sq)) % self.p
        s = sq + h * self.q
        return s

    def verify(self, msg: bytes, sig: int, max_elapsed=dt.timedelta(minutes=5)) -> bool:
        m = pow(sig, self.e, self.n)
        data = self.unparse(m, DataType.RSA_SIG)
        try:
            if timestamp_diff(data.timestamp.decode(), time.ctime()) > max_elapsed:
                return False
        except (ValueError, UnicodeDecodeError):
            return False
        digest_message = self.hmac_digest(data.hmac_key, msg, data.timestamp)
        return digest_message == data.digest_message


class MenuChoice(enum.Enum):
    GET_PUBLIC_KEY = 1
    GET_ENCRYPTED_FLAG = 2
    DECRYPT_FLAG = 3
    GET_SIGNED_FLAG = 4
    VERIFY_SIGNED_FLAG = 5
    EXIT = 6


if __name__ == "__main__":
    flag = os.getenv("FLAG", "srdnlen{this_is_a_fake_flag}").encode()
    rsa = RSA()
    print("Welcome to the RSA encryption and signing service!")

    while True:
        choice = int(input(">>> "))
        if choice == MenuChoice.GET_PUBLIC_KEY.value:
            print(f"e = {rsa.e:#x}")
            print(f"n = {rsa.n:#x}")
        elif choice == MenuChoice.GET_ENCRYPTED_FLAG.value:
            hmac_key = os.urandom(16)
            enc = rsa.encrypt(flag, hmac_key)
            print(f"enc = {enc:#x}")
            if DEBUG:
                assert rsa.decrypt(enc) == flag
        elif choice == MenuChoice.DECRYPT_FLAG.value:
            enc = int(input("enc (hex)? "), 16)
            try:
                res = rsa.decrypt(enc)
                if res == flag:
                    print("Decryption successful!")
                else:
                    print("Decryption failed. This is not ENC(flag).")
            except ValueError:
                print("Something went wrong during decryption")
        elif choice == MenuChoice.GET_SIGNED_FLAG.value:
            hmac_key = os.urandom(16)
            sig = rsa.sign(flag, hmac_key)
            print(f"sig = {sig:#x}")
            if DEBUG:
                assert rsa.verify(flag, sig)
        elif choice == MenuChoice.VERIFY_SIGNED_FLAG.value:
            sig = int(input("sig (hex)? "), 16)
            try:
                res = rsa.verify(flag, sig)
                if res:
                    print("Signature is valid!")
                else:
                    print("Signature is invalid.")
            except ValueError:
                print("Something went wrong during signature verification")
        elif choice == MenuChoice.EXIT.value:
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
