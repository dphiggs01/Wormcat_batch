import pandas as pd
import json
import os
import pkg_resources


def read_rgs_and_categories(file_nm_in):
    nodes_dict = {}
    try:
        df = pd.read_csv(file_nm_in)
        node1_list= []
        nodes_dict = {"name":"rgs", "children":node1_list}

        cat3 = df.groupby(["Category.3"]).count()

        cat3_dict={}
        for cat3_index, row in cat3.iterrows():
            count = int(row['Wormbase.ID'])
            cat3_dict[cat3_index] = count

        for key in cat3_dict:
            components = key.split(':')
            size = int(cat3_dict[key])
            #print("key {} size {}".format(key, size))
            if len(components) == 1:
                #print("add to node1 {}".format(components[0]))
                node1_list.append({"name": components[0].strip(), "size": size})
            elif len(components) == 2:
                node_list = getChildrenFor(components[0].strip(),nodes_dict)
                node_list.append({"name": components[1].strip(), "size": size})
            else:
                node_list = getChildrenFor2(components[0].strip(),components[1].strip(),nodes_dict)
                node_list.append({"name": components[2].strip(), "size": size})
    except Exception as e:
        print("Error in read_rgs_and_categories:", e)
        pass
    return nodes_dict


def create_sunburst(dir_nm):
    file_nm_sunburst_html = f"{dir_nm}{os.path.sep}sunburst.html"
    file_nm_rgs_and_categories = f"{dir_nm}{os.path.sep}rgs_and_categories.csv"
    data = read_sunburst_template()
    json_data = json.dumps(read_rgs_and_categories(file_nm_rgs_and_categories))
    

    with open(file_nm_sunburst_html, "w") as file:
        for d in data:
            file.write(d)
            if "insert json here" in d:
                json_data = json.dumps(read_rgs_and_categories(file_nm_rgs_and_categories))
                json_var = "var json_data = {}".format(json_data)
                file.write(json_var)



def getChildrenFor(parent, nodes_dict):
    children = nodes_dict['children']
    node_list = None
    for key in children:
        if parent == key['name']:
            if 'children' in key:
                node_list = key['children']
            break

    if node_list is None:
        node_list = []
        children.append({"name":parent, "children":node_list})
    return node_list


def getChildrenFor2(grand_parent, parent, nodes_dict):
    children = getChildrenFor(grand_parent, nodes_dict)
    node_list = None
    for key in children:
        if parent == key['name']:
            if 'children' in key:
                node_list = key['children']
            break

    if node_list is None:
        node_list = []
        children.append({"name":parent, "children":node_list})

    return node_list

def read_sunburst_template():
    try:
        data = []
        #data = pkg_resources.resource_string(__name__, 'sunburst.template').decode('utf-8')
        data_file = pkg_resources.resource_filename(__name__, 'sunburst.template')
        with open(data_file, "r") as file:
            data = file.readlines()
        return data
    except Exception as e:
        print("Error reading sunburst_template:", e)
        return None


if __name__ == "__main__":
    print("starting {}".format(os.getcwd()))
    create_sunburst('RGS_Feb-14-2020-11_45_54')


