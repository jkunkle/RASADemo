import os
import re
import subprocess
from xml.dom.minidom import parse
import json
from typing import List, Dict

from youtube_search import YoutubeSearch

def search_for_videos(search_string : str) -> List[str]:
    """Search youtube and get list of videos
    
       Arguments:
           search_string [str] : Youtube search string
    """

    result = YoutubeSearch(search_string, max_results=10)

    return json.loads(result.to_json())

def extract_videos(page_html : str) -> List[str]:
    """Find unique list of video IDs from
       youtube search result 

       Arguments:
           page_html [str] : html from requests call
    """

    res = re.findall('"videoId":"(.*?)"', page_html, flags=re.DOTALL)

    sel_videos = set()

    for video in res:
        sel_videos.add(video)

    return list(sel_videos)

def retrieve_captions(video_list  : List[str]):

    if not isinstance(video_list, list):
        video_list = [video_list]

    video_results = {}

    for vid in video_list:

        url = 'https://www.youtube.com/watch?v=%s' %(vid)

        output_dir = '/tmp/video_dl/%s' %vid
        if not os.path.isdir(output_dir):
            os.makedirs(output_dir)
        os.system('cd %s; youtube-dl --write-sub --sub-lang en --sub-format srv1 --skip-download %s' %(output_dir, url))

        dir_contents = list(os.listdir(output_dir))

        if not dir_contents:
            continue

        fname = dir_contents[0]

        captions = extract_captions(os.path.join(output_dir, fname))
        
        video_results[vid] = captions

    return video_results


def extract_captions(file_name : str) -> List[Dict]:
    """Extract captions from xml file
    
        Arguments:
            file_name[str] : path to xml file
    """

    res = parse(file_name)

    elements = res.getElementsByTagName('text')

    results = []

    for ele in elements:
        start = ele.getAttribute('start')
        duration = ele.getAttribute('dur')
        text = getText(ele.childNodes)
        text = text.replace('\n', ' ')

        results.append( {'start' : start, 
                         'duration' : duration,
                         'text' : text} )
    return results

def getText(nodelist):
    """Get text from node
    From https://docs.python.org/3/library/xml.dom.minidom.html
    """

    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)
