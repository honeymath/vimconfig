let s:socket_path = 'unix:'. expand('<sfile>:p:h') . '/vimsocket'
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
      try
	execute 'py3 import sys; sys.path.insert(0,"' . s:tools_path . '")'
        "execute 'py3 from tools import ' . target
        execute 'py3 import ' . target
        "execute 'py3 __vimsocket_result = ' . target . '.handler(**' . string(args) . ')'
        execute 'py3 import json; __vimsocket_result = ' . target . '.handler(**json.loads("""' . json_encode(args) . '"""))'
        execute 'py3 import vim; vim.vars["vimsocket_py_result"] = __vimsocket_result'
        let g:vimsocket_result.success = v:true
        let g:vimsocket_result.result = get(g:, 'vimsocket_py_result', {})
      catch
        let g:vimsocket_result.success = v:false
        let g:vimsocket_result.error = v:exception
      endtry
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
endfunc

call OpenChannel()
