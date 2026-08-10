
import hashlib
def generate_short_code(url: str) -> str:
    hash_object = hashlib.sha256(url.encode())
    short_code = hash_object.hexdigest()[:6]
    return short_code
if __name__ == "__main__":
    print(generate_short_code("https://google.com"))
    print(generate_short_code("https://youtube.com"))
    print(generate_short_code("https://github.com"))