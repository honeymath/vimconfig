import requests
import configparser
import subprocess
import os
import sys
import json
import shutil
import gzip



def parse_synctex(synctex_path):
    #print(f"Parsing synctex file: {synctex_path}", flush=True)
    data = []
    files = {}
    with open(synctex_path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

#    print(f"Total lines in synctex: {len(lines)}", flush=True)

    content_mode = False
    current_pdf_page_index = None

    for line in lines:
        line = line.strip()
#following code added by human
        if line.startswith("Input:"):
            _, file_index, file_path = line.split(":")
            files[file_index] = os.path.normpath(file_path) ## normalize the path
#above codes added by human
        if not content_mode:
            if line.startswith("Content:"):
                content_mode = True
        else:
            if line.startswith("{") and line[1:].isdigit():
                current_pdf_page_index = int(line[1:]) - 1
            elif line.startswith("}") and line[1:].isdigit():
                current_pdf_page_index = None
            elif line.startswith("!"):
                continue
            elif current_pdf_page_index is not None and line and (line[0].isalpha() or line[0] in "($)"):
                record_type = ''
                i = 0
                while i < len(line) and not line[i].isdigit() and line[i] not in "([":
                    record_type += line[i]
                    i += 1
                try:
                    left, coords_part = line[len(record_type):].split(":", 1)
                    # 从这里直接解析 file_num 和 line_num
                    file_num_str, line_num_str = left.split(",", 1)
                    file_num = int(file_num_str)
                    line_num = int(line_num_str)
                    pdf_coords = coords_part.split(":")[0]
                    pdf_x, pdf_y = map(float, pdf_coords.split(","))
                    data.append({
                        "type": record_type,
                        "tag": file_num,   # tag 就是 file_num
                        "line": line_num,
                        "file_num": file_num,
                        "pdf_page_index": current_pdf_page_index,
                        "pdf_x": pdf_x / 65536.0,
                        "pdf_y": pdf_y / 65536.0
                    })
                except:
                    pass
#    print(f"Prepare for return ", flush=True)
    return data, files

def type_color(t):
    if t.startswith('k'):
        return (1, 0, 0)  # red
    elif t.startswith('g'):
        return (0, 0, 1)  # blue
    elif t.startswith('x'):
        return (0, 0.5, 0)  # green
    elif t.startswith('$'):
        return (0.5, 0, 0.5)  # purple
    else:
        return (0, 0, 0)  # black

def build_forward_map(records):
#    print("Building forward map...", flush=True)
    forward_map = {}
    seen = set()
    for rec in records:
        key = (rec['file_num'], rec['line'])
        if key not in seen:
            seen.add(key)
            forward_map.setdefault(str(rec['file_num']), {})[str(rec['line'])] = {
                "x": rec['pdf_x'],
                "y": rec['pdf_y'],
                "page": rec['pdf_page_index']+1
            }
    # 排序 key
    forward_map_sorted = {k: dict(sorted(v.items(), key=lambda kv: int(kv[0]))) for k, v in sorted(forward_map.items(), key=lambda kv: int(kv[0]))}
    #print(f"Forward map built with {len(forward_map_sorted)} entries. Prepare return", flush=True)
    return forward_map_sorted

def build_reverse_map(records):
    #print("Building reverse map...", flush=True)
    reverse_map = {}
    for rec in records:
        page = str(rec['pdf_page_index']+1)  # 1-based page
        y = f"{rec['pdf_y']:.2f}"
        x = f"{rec['pdf_x']:.2f}"
        reverse_map.setdefault(page, {}).setdefault(y, {})
        reverse_map[page][y][x] = [rec['file_num'], rec['line']]
    # 合并相邻x，并排序
    for page, ydict in reverse_map.items():
        new_ydict = {}
        for y, xdict in sorted(ydict.items(), key=lambda kv: float(kv[0])):
            xs_sorted = sorted(xdict.keys(), key=lambda v: float(v))
            merged = {}
            prev_x = None
            prev_val = None
            for x in xs_sorted:
                val = xdict[x]
                if prev_x is not None and val == prev_val:
                    continue
                merged[x] = val
                prev_x = x
                prev_val = val
            new_ydict[y] = merged
        reverse_map[page] = new_ydict
    reverse_map_sorted = dict(sorted(reverse_map.items(), key=lambda kv: int(kv[0])))
    #print(f"Reverse map built with {len(reverse_map_sorted)} pages. Prepare return", flush=True)
    return reverse_map_sorted

def draw_boxes( synctex_path, json_dir):
    #print("BOXES! FUCKING BOXES!", flush=True)
    #print(f"synctex_path: {synctex_path}", flush=True)
    #print(f"json_dir: {json_dir}", flush=True)
    records , filetable = parse_synctex(synctex_path)
    #print(f"Total records parsed: {len(records)}", flush=True)
    #print(f"Total files parsed: {len(filetable)}", flush=True)

    forward_map = build_forward_map(records)
    reverse_map = build_reverse_map(records)
    
    full_dir = os.path.join(os.path.dirname(__file__), json_dir)

    forward_file = os.path.join(full_dir, "forward_map.json")

    with open(forward_file, "w", encoding="utf-8") as f:
        json.dump(forward_map, f, indent=2)
    reverse_file = os.path.join(full_dir, "reverse_map.json")
    with open(reverse_file, "w", encoding="utf-8") as f:
        json.dump(reverse_map, f, indent=2)
    filetable_file = os.path.join(full_dir, "file_map.json")
    with open(filetable_file, "w", encoding="utf-8") as f: ## added by human
        json.dump(filetable, f, indent = 2)
    #print("FUCKING BOXES DRAWN AND SAVED!", flush=True)
    return reverse_map,forward_map, filetable ## the filetable have to be used again






def handler(**data):
    print(f"THE SYNC PDF LATEX FUNCTION HAS BEEN CALLED!!!!! CONGRADS{data}", flush=True)
    latexfile = data.get("file", None) ## the latex file with main.tex at the end
    ## get syntex gz
    dirname = os.path.dirname(latexfile) ## the directory of the latex file
    syncgz = os.path.join(dirname,"main.synctex.gz")
    synctex_path = os.path.join(dirname, "main.synctex")
    #print(f"PREPARING THOSE FUCKING PATH FUCKINGS: syncgz::{syncgz}, synctex_path::{synctex_path}", flush=True)
    try:
        with gzip.open(syncgz, "rb") as f_in, open(synctex_path, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)
    except Exception as e:
        print(f"Error during gunzip: {e}", flush=True)
        return
    
        



        
    line = data.get("line", None) ## the line number
    if line is None or latexfile is None:
        print("Error: 'file' or 'line' parameter is missing.", flush=True)
        return

    #print(f"NOW YOU HAVE GUNZIPED FUCK FUCK", flush=True)
    #print(f"file: {latexfile}, line: {line}", flush=True) 
    json_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '../static'))
    os.makedirs(json_path, exist_ok=True)

    shutil.copy(os.path.join(dirname,"main.pdf"),os.path.join(json_path,"main.pdf"))## copy the fucking pdf file into fucks.


    #print(f"PDF file copied. FUCKING synctex_path: {synctex_path}", flush=True)
   
    reverse_map, forward_map, filetable = draw_boxes(synctex_path = synctex_path, json_dir = json_path)


    #print(f"NOW DOING FUCK FUCK AGIN", flush=True)
    searchfile = data.get("searchfile", None)
    if searchfile is None:
        print("Error: 'searchfile' is missing", flush = True)
        return
    

   ### The following are search file logic 
    #print(f"Now searching file begins with {searchfile}", flush = True)
    path = os.path.normpath(os.path.expanduser(searchfile)).strip()
    filekey = None

    #print(f"READY?GO206", flush = True)
    
    #print(f"FILETABLE {filetable}", flush=True)
    file_map = filetable

    for key, value in file_map.items():
        if value.strip() == path:
            filekey = key
            break

    #print(f"GOT KEY VALUE{filekey}",flush = True)

    if filekey is None:
        print(f"Error: not able to find file {path}", flush = True)
        raise Exception(f"Not able to find the suggested file {path}")

    if filekey not in forward_map:
        print(f"Not able to identify the file in the forward map {path} with filekey {filekey}", flush = True)
        raise Exception(f"Not able to identify the file in the forward map {path} with filekey {filekey}")

    line_dict = forward_map[filekey]
    parsed_lines = sorted(map(int, line_dict.keys()))

    #print(f"Parsed lines: {parsed_lines}", flush=True)

    until = None
    for l in parsed_lines:
        if l <= line:
            until = l
        else:
            break

    if until is None:
        raise Exception(f"No valid line found in forward map for {path} with given line {line}")

#    print(f"GOT THE UNTIL: {line_dict[str(until)]}", flush=True)

    ## now load the config and click the fucker


    sabi = {k:v for k,v in line_dict[str(until)].items()}
    print(f"FUCKING FUCKING result: {sabi}",flush=True)
    sabi["filestamp"]="fuck"
    sabi["refresh"]=True
    config_path = os.path.normpath(os.path.join(os.path.dirname(__file__), "../config.ini"))
    config = configparser.ConfigParser()
    config.read(config_path)
    host = config.get("local_server", "host", fallback="localhost")
    port = config.get("local_server", "port", fallback=5001)
    try:
        results = requests.get(f"{host}:{port}/send_pdf_reload",params = sabi)
    except Exception as e:
        print(e)









    return sabi#line_dict[str(until)]
    ### the following logic is to find out the main.tex in the above langauge.

    #the following: run pdflatex on the taregt
    ## maybe should let vim to run it? and afterwards come back again?
#    synctex_in = os.path.join(dirname, "main.synctex")
 #   draw_boxes(synctex_path = synctex_in)
# ../../test/drawboxes_v11.py

    ### the data type.

    ### after pdflatex, gunzip the main.synctex.gz and get synctex.

    ### then copy the color code here to decode the synctex, put the file into the static as synctex, and json.
    ### then from the file data and the line data try to forward search.. sure apply the logic here. 

if __name__ == "__main__":
    para = {'file': '/Users/qiruili/repositories/688ab3080dfb1b2f53fde40a/main.tex', 'line': 2, 'searchfile': '/Users/qiruili/repositories/688ab3080dfb1b2f53fde40a/contents/total-space/cm-cycles.tex'}
    para = {'file': '/Users/qiruili/repositories/688ab3080dfb1b2f53fde40a/main.tex', 'line': 5, 'searchfile': '/Users/qiruili/repositories/688ab3080dfb1b2f53fde40a/contents/analytic-side/orbits-classification.tex'}
    result = handler(**para)
    print(f"Result: {result}", flush=True)
#    if len(sys.argv) < 2:
#        print("Usage: python syncpdf.py <synctex_path>")
#        sys.exit(1)
#    synctex_path = sys.argv[1]
#    json_dir = "static"
#    draw_boxes(synctex_path, json_dir)
