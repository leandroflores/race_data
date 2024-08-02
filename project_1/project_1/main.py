from typing import List, Union

print("Hello World")
a: List[int] = [2, 3]
print(a)

def max_value(list: List[int]) -> Union[int, None]:
    if len(list) == 0:
        return None
    return max(list)

print()