import pandas as pd
from math import log2
from copy import deepcopy
from dataclasses import dataclass

@dataclass
class Node:
    attribute: str
    children:[] # (node_ref,value)

def xlsx_to_list():
    df = pd.read_excel('./DatosSetas.xlsx',skiprows=[0],engine='openpyxl').dropna()
    columns = df.columns.values.tolist()[:-1]
    #print(columns)
    return list(map(lambda x: ({columns[i]:y for i,y in enumerate(x[:-1]) },x[-1]),df.values.tolist())),set(columns)

def build_model(data,attributes):
    class_frecuencies = {}
    # class_entropy = 0
    for row in data:
        class_name = row[1]
        if class_name not in class_frecuencies:
            class_frecuencies[class_name]=1
        else:
            class_frecuencies[class_name]+=1
    data_len = len(data)
    if len(class_frecuencies) <= 1:
        return Node(next(iter(class_frecuencies)),[])
    # for k,v in class_frecuencies.items():
    #     Pi = v / data_len
    #     class_entropy -= Pi * log2(Pi)
    best_attribute = float('inf'),''
    for attribute in attributes:
        sum_f = 0
        value_frecuencies,value_to_class_count = {},{}
        for row in data:
            value = row[0][attribute]
            if value not in value_frecuencies:
                value_frecuencies[value]=1
            else:
                value_frecuencies[value]+=1
            if value not in value_to_class_count:
                value_to_class_count[value]={}
            value_class = row[1]
            if value_class not in value_to_class_count[value]:
                value_to_class_count[value][value_class]=1
            else:
                value_to_class_count[value][value_class]+=1
        antigain = 0
        for k,f in value_frecuencies.items():
            value_entropy = 0
            for frecuency in value_to_class_count[k].values():
                Pi = frecuency  / f
                value_entropy -= Pi * log2(Pi)
            print('value',k,'frecuency',f,'value_entropy based in class',value_entropy)
            antigain +=  f/data_len * value_entropy  
        best_attribute = min((antigain,attribute),best_attribute)
    best_attribute_name = best_attribute[1]
    attributes_copy = deepcopy(attributes)
    attributes_copy.remove(best_attribute_name)
    data_splitted = {}

    for row in data:
        bs_a_value = row[0][best_attribute_name]
        if bs_a_value not in data_splitted:
            data_splitted[bs_a_value]=[]
        row_copy = deepcopy(row)
        row_copy[0].pop(best_attribute_name)
        data_splitted[bs_a_value].append(row_copy)

    node = Node(best_attribute_name,[])
    for value,data in data_splitted.items():
        node.children.append((build_model(data,deepcopy(attributes_copy)),value))
    return node
    # return class_entropy
#print(xlsx_to_list())
data,attributes = xlsx_to_list()
#print(attributes)
print(data)
root = build_model(data,attributes)
def navigate(node):
    print(f'attribute {node.attribute}')
    if not node.children:
        return
    for child in node.children:
        print(f'going to child with {node.attribute}={child[1]}')
        navigate(child[0])

navigate(root)