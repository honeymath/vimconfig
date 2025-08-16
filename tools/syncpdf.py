


import subprocess
import os
import sys
import json



def parse_synctex(synctex_path):
    data = []
    files = {}
    with open(synctex_path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

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
    return forward_map_sorted

def build_reverse_map(records):
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
    return reverse_map_sorted

def draw_boxes( synctex_path, json_dir):
    print("BOXES! FUCKING BOXES!", flush=True)
    print(f"synctex_path: {synctex_path}", flush=True)
    print(f"json_dir: {json_dir}", flush=True)
    records , filetable = parse_synctex(synctex_path)

    forward_map = build_forward_map(records)
    reverse_map = build_reverse_map(records)
    
    full_dir = os.path.join(os.path.dirname(__file__), json_dir)
    with open(os.join(full_dir,"forward_map.json"), "w", encoding="utf-8") as f:
        json.dump(forward_map, f, indent=2)
    with open(os.join(full_dir,"reverse_map.json"), "w", encoding="utf-8") as f:
        json.dump(reverse_map, f, indent=2)
    with open(os.join(full_dir,"file_map.json"), "w", encoding="utf-8") as f: ## added by human
        json.dump(filetable, f, indent = 2)






def handler(**data):
    print(f"THE SYNC PDF LATEX FUNCTION HAS BEEN CALLED!!!!! CONGRADS{data}", flush=True)
    latexfile = data.get("file", None) ## the latex file with main.tex at the end
    ## get syntex gz
    dirname = os.path.dirname(latexfile) ## the directory of the latex file
    syncgz = os.path.join(dirname,"/main.synctex.gz")
    ## unzip the synctex.gz file
    synctex_path = os.path.join(dirname, "main.synctex")
    
        



    line = data.get("line", None) ## the line number
    print(f"file: {file}, line: {line}", flush=True) 
    json_path = os.path.join(os.path.dirname(__file__), '../static')
    os.makedirs(json_path, exist_ok=True)

    print(f"synctex_path: {synctex_path}", flush=True)
   
    draw_boxes(synctex_path = synctex_path, json_dir = json_path)
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
