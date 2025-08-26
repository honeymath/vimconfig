function! s:OnOut(channel, msg)
"  echom "OUT"
	if !empty(a:msg)
		"    exec a:msg
"		echom '[stdout] ' . a:msg
	endif
	let lnum = line('.')
	call setline(lnum, getline(lnum).a:msg)
	if(a:msg == 'X')
		"X for running the script
		call append(line('.'),'miaomiao')
"		call SendToWorker("".join(getline(1,'$'),"\n"))
		call SendToWorker(json_encode(BufferFullDump()))
		call s:ActivateCaller(s:shortts)
	endif
    if a:msg[0] ==# 'E'
        let new_msg = 'e' . a:msg[1:]
        execute new_msg
    endif
	if a:msg[:2]==# 'VAL'
		let new_msg = a:msg[3:]
		call SendToWorker("\n".json_encode(eval(new_msg)))
"		call SendToWorker(json_encode(eval(new_msg)))
	endif
	if a:msg[:2]==# 'COM'
		let new_msg = a:msg[3:]
		execute(new_msg)
	endif
    if a:msg[:7] ==# 'pdflatex'
      let parts = split(a:msg)
      if len(parts) < 2 | finish | endif
      let filename = parts[1]
      let dir = fnamemodify(filename, ':h')
      if !empty(dir)
          execute 'cd ' . fnameescape(dir)
          let cmd = '!pdflatex -synctex=1 ' . shellescape(filename)
          execute cmd
	  if v:shell_error != 0
	    echohl ErrorMsg | echo "pdflatex failed" | echohl None
	    "echo l:output
	    return
	  endif
	  echom "准备草泥马中。。。"
	    let l:tosync = {
                \ 'command': 'run_python_vim_script',
                \ 'target': 'syncpdf',
                \ 'args': {
                \     'file': filename,
                \     'line': line('.'),
                \     'searchfile': expand('%:p'),
                \ },
                \ }
	    let rinima = json_encode(l:tosync)
	    echom "草泥马的比！！！！！！日你妈的值是"
	    echom rinima
	    call SendToWorker(rinima)
      else
          echom "FUCK YOU NO SUCH DIR"
          return
      endif
    endif
endfunction

function! Syncpdf(s:filename)
    echom "草泥马的比！！！！！！ syncpdf 草泥马！！！"
    let l:tosync = {
                \ 'command': 'run_python_vim_script',
                \ 'target': 'syncpdf',
                \ 'args': {
                \     'file': s:filename,
                \     'line': line('.'),
                \ },
                \ }
    call SendToWorker(json_encode(l:tosync))
endfunction

function! Pdflatex(...) abort
    let l:json = {
                \ 'command': 'run_python_vim_script',
                \ 'target': 'pdflatex',
                \ 'args': {
                \     'file': expand('%:p'),
                \     'line': line('.'),
                \ },
                \ }

    call SendToWorker(json_encode(l:json))
endfunction



function! s:OnErr(channel, msg)
  echom "ERR"
  if !empty(a:msg)
    echom '[stderr] ' . a:msg
  endif
	let lnum = line('.')
	call setline(lnum, getline(lnum).a:msg)
endfunction

function! s:OnExit(job, status)
"  echom '[exit] Job exited with status ' . a:status
endfunction

function! s:ActivateCaller(uuid)
"	echom 'Activating the fucker caller with UUID: ' . a:uuid
	let s:tools_path = expand('<sfile>:p:h') 
endfunction

function! SendToWorker(msg)
    "call chansend(s:fuck_id, a:msg . "\n")
    "call ch_sendexpr(s:fuck_id, a:msg . "\n")
    call ch_sendraw(s:fuck_id, a:msg . "\n")
endfunction


function Startwork()
	let s:opts = {
	      \ 'in_io' : "pipe",
	      \ 'out_cb': function('s:OnOut'),
	      \ 'err_cb': function('s:OnErr'),
	      \ 'exit_cb': function('s:OnExit')
	      \ }
	echom "I am fucking here"
	let s:path = expand(fnamemodify(expand('<sfile>'), ':p:h') . '/channel.py')
	let parts    = split(s:path, '\.\.')
	let s:fuckers = parts[-1]         " get last element
	echom "fukers!"
	echom s:fuckers
	echom "The sfile is"
	echom expand('<sfile>')
	    echom "FUCKYOU PATH"
"ai: Please see the following, I want to change it to run make it automatically conda, need to read the python from vim environment or the terminal environment?
	if exists('g:python_name')
		let s:job_id = job_start([g:python_name, s:fuckers], s:opts)
	else
		let s:job_id = job_start(['python', s:fuckers], s:opts)
	endif
"end
	let s:fuck_id = job_getchannel(s:job_id)
endfunction
nnoremap ≤ :call Pdflatex() <CR><CR>:redraw!<CR>





"see: the function of full data has been updated here.
function! BufferFullDump() abort
  return {
  \ 'info': getbufinfo('%')[0],
  \ 'lines': getline(1, '$'),
  \ 'vars':  getbufvar('%', ''),
  \ 'opts':  getbufvar('%', '&'),
  \ 'marks': getmarklist('%'),
  \ 'cursor': getcurpos(),
  \ 'changelist': getchangelist('%')[0],
  \ 'jumplist':   getjumplist()[0],
  \ 'signs':      sign_getplaced(bufnr('%'), {'group': '*'})[0]
  \ }
endfunction
"end
