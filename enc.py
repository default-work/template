#import dis
import hashlib
import math
from operator import itemgetter

def frequency(text):
  count = {}
  for key in text:
    count[key] = count[key] + 1 if count.get(key) else 1
  return count

def convert(obj):
  return sorted(list(map(lambda key: [key, obj[key]], obj.keys())), key=itemgetter(0))

def multisort(xs, specs):
  for key, reverse in reversed(specs):
    xs.sort(key=itemgetter(key), reverse=reverse)
  return xs

def sort(array):
  return multisort(list(array), ((1,True), (0, False)))

def chars(text):
  freq = frequency(text)
  items = convert(freq)
  sort_items = sort(items)
  return {
    "char": list(map(itemgetter(0), sort_items)),
    "freq": list(map(itemgetter(1), sort_items))
  }

IV = 1
shift = 1

alphabet = """QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm1234567890 .
"""
plaintext = "A"
sha_alphabet = hashlib.sha1(alphabet.encode("utf-8")).hexdigest()
sha_plaintext = hashlib.sha1(plaintext.encode("utf-8")).hexdigest()

class prng:
  def __init__(self, seed):
    self._seed = seed % 2147483647
    if self._seed <= 0:
      self._seed += 2147483646

  def next(self, *argv):
    self._seed = (self._seed * 48271) % 2147483647
    length = len(argv)
    if length == 0:
      return self._seed / 2147483647
    elif length == 1:
      a = argv[0]
      return (self._seed / 2147483647) * a
    elif length == 2:
      a = argv[0]
      b = argv[1]
      return (self._seed / 2147483647) * (b - a) + a

max = 2147483647
min = 0

def random():
  return math.floor(rnd.next(min, max))

seed = 1238473661
rnd = prng(seed)

def size():
  return len(alphabet)

def next_position(alphabet, char):
  j = random()
  position = alphabet.index(char)
  return (position + 1 + j) % size()

def hex2binb(string):
  result = []
  while len(string) >= 8:
    result.append(int(string[:8], 16))
    string = string[8:]
  return result

def shuffle(array, seed):
  rng = prng(seed)
  for i in reversed(range(len(array))):
    j = math.floor(rng.next(i))
    array[i], array[j] = array[j], array[i]

def shuffle_binb(alphabet, str):
  array = hex2binb(str)
  shuffle(alphabet, array[0])
  shuffle(alphabet, array[1])
  shuffle(alphabet, array[2])
  shuffle(alphabet, array[3])

def cipher_function(cipher):
  def function(random, shift, alpha, array, sha_alphabet, sha_plaintext):
    global rnd
    alphabet = alpha
    shuffle_binb(alphabet, sha_alphabet)
    shuffle_binb(alphabet, sha_plaintext)
    rnd = prng(random)
    for i in range(shift):
      array = map(cipher, array)
    return list(array)
  return function

def shift_encrypt(char):
  position = alphabet.index(char)
  newPosition = next_position(alphabet, char)
  while newPosition == position:
    newPosition = next_position(alphabet, char)
  return alphabet[newPosition]

def encrypt_cipher(IV, shift, alphabet, plaintext, sha_alphabet, sha_plaintext):
  return cipher_function(shift_encrypt)(IV, shift, [*alphabet], [*plaintext], sha_alphabet, sha_plaintext)

encoded = encrypt_cipher(IV, shift, alphabet, plaintext, sha_alphabet, sha_plaintext)

print(encoded)