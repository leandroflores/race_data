import matplotlib.pyplot

from typing import List

a: list[str] = ["2"]
meses: List[str] = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho"]
valores: List[int] = [105235, 107697, 110256, 109236, 108859, 109986]

matplotlib.pyplot.plot(meses, valores)
matplotlib.pyplot.show()