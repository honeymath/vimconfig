"let s:socket_path = 'unix:'. expand('<sfile>:p:h') . '/vimsocket'
let s:config_file_path = expand('<sfile>:p:h') . '/config.ini'
let config_lines = readfile(s:config_file_path)
let host = ""
let port = ""
for line in config_lines
    let line = trim(line)
    if line ==# '' || line =~# '^\s*[#;]'
        continue
    endif
    if line =~# '^\s*\w\+\s*='
        let parts = split(line, '=')
        if len(parts)>=2
            let key = trim(parts[0])
            let value = trim(parts[1])
            if key == "port"
                let port = value
            endif
            if key == "host"
                let host = value
            endif
        endif
    endif
endfor
if  host ==# "" || port ==# ""
    echoerr "Missing host or port in config.ini"
    finish
endif


let s:socket_path = host.":".port
    
"let s:socket_path = '192.168.2.51:8765'
let s:tools_path = expand('<sfile>:p:h') . '/tools'

"let s:socket_path = 'vimsocket'

function! s:OnData(chan, msg)
  echomsg 'Vim channel received message: ' . string(a:msg)
  try
    let request = a:msg
    let g:vimsocket_request = request
    let g:vimsocket_result = {}
    let target = request['target']
    let args = request['args']
    if !filereadable(s:tools_path . '/' . target . '.py')
      echomsg 'Script not found: tools/' . target . '.py'
      let g:vimsocket_result = {'success': v:false, 'error': 'Script not found'}
    else
	  echomsg 'Executing script: tools/' . target . '.py with args: ' . string(args)
        execute 'py3 import sys; sys.path.insert(0,"' . s:tools_path . '")'
        execute 'py3 import function_caller'
        execute 'py3 import ' . target
        execute 'py3 import vim; __vimsocket_result = function_caller.call_function(' . target . '.handler, vim.eval("g:vimsocket_request")["args"])'
        execute 'py3 import vim; vim.vars["vimsocket_py_result"] = __vimsocket_result'
        let g:vimsocket_result.result = get(g:, 'vimsocket_py_result', {})
    endif
    let g:vimsocket_result.task_id = request['task_id']
    echomsg 'Result: ' . string(g:vimsocket_result)
    call ch_sendraw(a:chan, json_encode(g:vimsocket_result) . "\n")
  catch
    call ch_sendraw(a:chan, '{"success": false, "error": "unexpected error"}\n')
  endtry
endfunction

"let s:ch = ch_open(s:socket_path, {'mode': 'json','callback': 's:OnData'})
"call ch_setoptions(s:ch, })
"echomsg 'Vim channel callback set'
func Handle(channel, msg)
  echomsg 'Received: ' . string(a:msg)
endfunc
func OpenChannel()
	let channel = ch_open(s:socket_path, {"callback": function('s:OnData')})
	"let channel = ch_open("localhost:8765", {"callback": "Handle", "mode": "json"})
	let g:vimsocket_ch = channel
	echomsg channel
    return channel
endfunc

let s:msg = "fail"
let s:attempts = 0
let s:maxattempts = 20
while s:msg =~# "fail" && s:attempts < s:maxattempts
    let s:attempts = s:attempts +1
    let s:msg = OpenChannel()
    sleep 100m
endwhile
