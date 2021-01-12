import json
import requests
from tqdm import tqdm
import numpy as np
import os
from natsort import natsorted

def get_youtube_vids(folder_name):
    url_prefix = 'https://storage.googleapis.com/data.yt8m.org/2/j/v/{category_id}.js'
    with open('yt8m_categories.csv', 'r') as f:
        lines = f.readlines()

    filename = os.path.join(folder_name, 'category_mapping.npy')

    if os.path.exists(filename):
        mapping = np.load(filename, allow_pickle=True).item()

    else:
        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))
        lines = [[s.strip() for s in maps.split(',')] for maps in lines]
        mapping = {l[0]: {'name':l[1], 
                          'url':url_prefix.format(category_id=l[0]),
                          'file_dict':{}} 
                   for l in lines}
        np.save(filename, mapping)

    youtube_videos_per_category = {}

    for category in tqdm(mapping.keys()):
        if mapping[category]['file_dict'] == {}:
            try:
                file_url = mapping[category]['url']
                name = mapping[category]['url']
                response = requests.get(file_url)
                p = lambda k,v: v
                string = response.text
                string = string.split('[')[1]
                string = string.split(']')[0]
                list_of_names_string = '[' + string + ']'
                list_of_names = eval(list_of_names_string)
                mapping[category]['file_dict'] = {k:None for k in list_of_names}
            except:
                print("Couldn't get category mapping for ID:{} NAME:{} URL:{}".format(
                    category, mapping['category']['name'], mapping['category']['url']))
        else:
            list_of_names = natsorted(list(mapping[category]['file_dict'].keys()))
        for k in tqdm(natsorted(list_of_names)):
            # print(mapping)
            # print(k)
            if mapping[category]['file_dict'][k] is not None:
                pass
            else:
                url = 'https://storage.googleapis.com/data.yt8m.org/2/j/i/{}/{}.js'.format(k[:2], k)
                print(url)
                try:
                    resp = requests.get(url)
                    txt = resp.text
                    print(txt)
                    txt = txt.split('(')[1]
                    txt = txt.split(')')[0]
                    name = txt.split(',')[1]
                    mapping[category]['file_dict'][k] = eval(name)
                except:
                    print("Couldn't get video id mapping for ID:{} URL:{}".format(
                    category, k, url))
                    mapping[category]['file_dict'][k] = 'not-found'
            np.save(filename, mapping)


if __name__ == '__main__':

    get_youtube_vids('./yt8m_videos')