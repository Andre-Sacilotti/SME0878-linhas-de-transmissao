import pandas as pd
import numpy as np
import re
from unidecode import unidecode
from Levenshtein import distance, ratio

class Decomposer:
    def __init__(self):
        pass
    
    def filter_text(text):
        # print(text)
        text = text.upper()
        text = unidecode(text)
        
        # Filtro tokens inúteis
        # (?<=\s)NO( |$)|
        # (?<=\s)DO( |$)|
        # (?<=\s)E( |$)|
        # \.|(D:)
        # ()|"|.|:
        # espaços seguidos ou inúteis
        text = re.sub(r'(?<=\s)N(A|O)( |$)|(?<=\s)EM( |$)|(?<=\s)D(A|E|O)( |$)|(?<=\s)E( |$)|(D:)|\/( |$)',' ', text)
        text = re.sub(r'\(|\)|\.|:|"',' ', text)
        text = re.sub(r'(^\s+)|(\s{1,})(?=\s\S)|(\s+$)', '', text)
        
        # Fitro T**
        # ((?<=T)(\D|)(?=\d+))
        text = re.sub(fr'((?<=T)(\D|)(?=\d{1,}))', '', text)
        
        # Completar palavras cortadas padrão
        # Fases
        if match := re.search(r'((?<= )FASE\s)([A-Z]{1,}(?=\s|$))', text):
            fase = match.group(2)
            text = text[:match.span()[0]] + text[match.span()[1]:]
            # Match com as possiblidades
            if fase[0] == 'S':
                fase = 'SUPERIOR'
            elif fase[0] == 'M' or fase[0] == 'C':
                fase = 'MEIO'
            elif fase[0] == 'V':
                fase = 'VERMELHA'
            elif fase[0] == 'B':
                fase = 'BRANCA'
            elif len(fase) > 1:
                if fase[:2] == 'EX':
                    fase = 'EXTERNA'
                elif fase[:2] == 'ES':
                    fase = 'ESQUERDA'
                elif fase[:2] == 'DI':
                    fase = 'DIREITA'
                elif len(fase) > 2:
                    if fase[:2] == 'IN':
                        if fase[2] == 'F':
                            fase = 'INFERIOR'
                        elif len(fase) > 5:
                            if fase[5] == 'N':
                                fase = 'INTERNA'
                            elif fase[5] == 'M':
                                fase = 'INTERMEDIARIA'
            # inconclusiva => excluir
            else: fase = ''
            text = text + ' ' + fase
            
        # Lado
        if match := re.search(r'((?<= )LADO\s)([A-Z]{1,}(?=\s|$))', text):
            lado = match.group(2)
            text = text[:match.span()[0]] + text[match.span()[1]:]
            # Match com as possiblidades
            if lado[0] == 'V':
                lado = 'VIVO'
            elif lado[0] == 'M':
                lado = 'MORTO'
            elif len(lado) > 1:
                if lado[:2] == 'ES':
                    lado = 'ESQUERDO'
                elif lado[:2] == 'DI':
                    lado = 'DIREITO'
                elif lado[:2] == 'IN':
                    lado = 'INFERIOR'
                elif lado[:2] == 'EN':
                    lado = 'ENERGIZADO'
                elif lado[:2] == 'DE':
                    lado = 'DESENERGIZADO'
            elif lado == 'CAV' or lado == 'CPV':
                lado = lado
            # inconclusiva => excluir
            else: lado = ''
            text = text + ' ' + lado
        
        # termos comuns:
        text = re.sub(r'DI GUEDES', 'DIGUEDES', text)
        
        # print(denom)
        # print(item)
        # print(text)
        return text

    def parser(self, text):
        tags = re.split(r'\. |\/| | - ', text)
        
        for i in range(len(tags)):
            if tags[i] == None: continue
            # Remoção de ' ' duplicados e inúteis
            # só ta dando match no primeiro :(
            tags[i] = re.sub(r'(^\s+)|(\s{1,})(?=\s\S)|(\s+$)', '', tags[i])
        tags = list(filter(None, tags))
        print(tags)
        return tags
    
    '''
    Retorna dataframe com palavras únicas e sua presença por linha
        dataset: pd.series de texto
    '''
    def create(self, dataset):
        texts = dataset.fillna('').apply(lambda x: self.filter_text(x))
        tags = texts.apply(lambda x: self.parser(x))
        temp = [x for y in tags for x in y]
    
        unique_tags = list(set(temp))
        count = dict((x, temp.count(x)) for x in unique_tags)
        frequency = {k:v for k,v in sorted(count.items(), key=lambda item: item[1], reverse=False)}

        keys = list(frequency.keys())
        for i in range(len(keys)):
            h0 = keys[i]
            if not h0.isalpha(): continue
            for j in range(i+1,len(keys)):
                h1 = keys[j]
                # primeiro caracter é igual
                if h0[0] == h1[0]:
                    if h0 in h1:
                        if (distance(h0, h1) <= len(h0)/2):
                            h0 = h1
                    elif (distance(h0, h1) == 1):
                        left = 0
                        right = 0
                        if h0[-1] in ['S', 'A', 'O']:
                            left += 1
                            if h0[-2:] in ['AS','OS']:
                                left += 1
                        if h1[-1] in ['S', 'A', 'O']: 
                            right += 1
                            if h1[-2:] in ['AS','OS']:
                                right += 1
                        if left > 0 and right > 0:
                            if (distance(h0[:-(left)], h1[:-(right)]) == 0): 
                                # print(h0, left, h1, right, distance(h0[:-(left)], h1[:-(right)]))
                                h0=h1
                    elif (ratio(h0, h1) > 0.8):
                        h0 = h1
            
            temp = [h0 if x == keys[i] else x for x in temp]
        
        
        unique_tags = list(set(temp)) 
        matrix = np.zeros((len(tags), len(unique_tags)))
        j = 0
        for i in range(len(tags)):
            words = temp[j:j+len(tags[i])]
            matrix[i] = [1 if x in words else 0 for x in unique_tags]
            j += len(tags[i])
        wordbox = pd.DataFrame(matrix, columns=unique_tags)
        
        return wordbox