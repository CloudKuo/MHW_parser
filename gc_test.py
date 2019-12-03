import sys
import gc
import random
from random import randrange
a = 'my-jhg-string'
# print(sys.getrefcount(a))
b = [a]
g = {"d": a}
print(sys.getrefcount(a))
# print(c)


class Myclass(object):
    pass


c = Myclass()
print(sys.getrefcount(c))
c.obj = c
del c
# 雖然刪除掉了這變數但是並沒有刪除掉這東西從記憶體 只是沒有東西reference他 這問題叫reference cycle
print(gc.get_count())
# print(gc.get_threshold())
# gc.set_threshold(1000, 15, 15)
gc.collect()
# print(gc.get_threshold())
print(gc.get_count())
d = {"Kelly": 50,
  "Red": 68,
  "Jhon": 70,
  "Emma" :40}
l = [1, 2, 3, 4, 5]
print(random.choices(l, k=2))
r_key = random.choice(list(d))
print(r_key, d[r_key])
random_index = randrange(len(l))
item = l[random_index]
print("Randomly selected item and its index is - ", item, "Index - ", random_index)
print(random.randint(0, 1000))