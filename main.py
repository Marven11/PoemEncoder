import re
import gzip
import random

chars_dict = {
    "v": "拂倚揽踱溯凝衔涉敛曳叩逐栖萦翩望",
    "a": "明幽清寂朗朦灿皎暗艳秀雅丽柔淡静",
    "n": "钟苔灯雁蓑笠笛帘砧篷烟烬船驿鹤冢",
    "e": "空",
}

chars = "".join(chars_dict.values())

pattern = re.compile(r"[CHARS]{5}([，][\s\n]*[CHARS]{5})*".replace("CHARS", chars))

patterns = [
    "anvan",
    "annaa",
    "avnna",
    "vnnav",
    "naana",
]


def encode(b: bytes) -> str:
    compressed = gzip.compress(b)
    chunks = []
    nums = [int(c, 16) for c in compressed.hex()]
    for i in range(0, len(nums), 5):
        chunk = nums[i : i + 5]
        pattern = random.choice(patterns)
        if len(chunk) < 5:
            pattern = pattern[: len(chunk)] + "e" + pattern[len(chunk) + 1 :]
            chunk += [0] + [random.randint(0, 15) for _ in range(len(chunk) + 1, 5)]
        chunks.append("".join(chars_dict[p][n] for n, p in zip(chunk, pattern)))

    return "，".join(chunks)


def decode(s: str) -> bytes | None:
    match = pattern.search(s)
    if not match or not match.group(0):
        return None
    content = re.sub(r"[\s，]", "",  match.group(0))
    nums = [chars.index(c) for c in content for chars in chars_dict.values() if c in chars]
    compressed_hex = "".join(hex(n)[-1] for n in nums)
    return gzip.decompress(bytes.fromhex(compressed_hex))


def main():
    encoded = encode(b"1145141919 yuanshen")
    print(encoded)
    print(decode("""
<h1>
幽冢敛雅钟，敛钟钟淡曳，敛笛驿艳衔，帘明清冢静，寂雁雁朗寂，朗雁倚寂笠，踱蓑雁幽逐，朗雁溯雅蓑，
凝蓑烟暗揽，栖蓑驿丽栖，清烬栖淡蓑，暗船驿明寂，明钟栖秀笠，揽烬苔灿逐，苔寂明钟明，明拂钟空明
</h1>
"""))


if __name__ == "__main__":
    main()
