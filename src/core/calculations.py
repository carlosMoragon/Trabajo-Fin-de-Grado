def fscore_peor_caso(lista):
    return min(lista) if lista else 0

def fscore_caso_medio(lista):
    return sum(lista)/len(lista) if lista else 0

def fscore_mejor_caso(lista):
    return max(lista) if lista else 0

def alpha(rta, rtb, t0a, t0b):
    return (rta - t0a) / (rtb - t0b) if rtb != t0b else float('inf')

def diff(rta, rtb, total):
    return (rtb - rta) / total

def best_config(lista_tuplas):
    mejor = max(lista_tuplas, key=lambda tupla: float(tupla[1]))
    return mejor[0]