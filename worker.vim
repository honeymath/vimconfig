function! s:OnOut(channel, msg)
  echom "OUT"
	if !empty(a:msg)
		"    exec a:msg
		echom '[stdout] ' . a:msg
	endif
	let lnum = line('.')
	call setline(lnum, getline(lnum).a:msg)
	if(a:msg == 'X')
		"X for running the script
		call append(line('.'),'miaomiao')
		call SendToWorker("我操你妈！！！！\n 草泥马草泥马的，傻逼！".join(getline(1,'$'),"\n"))
		call s:ActivateCaller(s:shortts)
	endif
    if a:msg[0] ==# 'E'
        let new_msg = 'e' . a:msg[1:]
        execute new_msg
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
      else
          echom "FUCK YOU NO SUCH DIR"
          return
      endif
    endif
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
endfunction

function! s:OnExit(job, status)
"  echom '[exit] Job exited with status ' . a:status
endfunction

let s:opts = {
      \ 'in_io' : "pipe",
      \ 'out_cb': function('s:OnOut'),
      \ 'err_cb': function('s:OnErr'),
      \ 'exit_cb': function('s:OnExit')
      \ }

function! s:ActivateCaller(uuid)
	echom 'Activating the fucker caller with UUID: ' . a:uuid
	let s:tools_path = expand('<sfile>:p:h') 
endfunction

function! SendToWorker(msg)
    "call chansend(s:fuck_id, a:msg . "\n")
    "call ch_sendexpr(s:fuck_id, a:msg . "\n")
    call ch_sendraw(s:fuck_id, a:msg . "\n")
endfunction

echom "I am fucking here"
let s:path = expand(fnamemodify(expand('<sfile>'), ':p:h') . '/channel.py')
echom s:path


let chars = '0123456789abcdefghijklmnopqrstuvwxyz'
let s:t = localtime()
let s:shortts = ''
while s:t > 0
    let s:shortts = chars[s:t % 36] . s:shortts
    let s:t = s:t / 36
endwhile
echom 'Fucking shortts: ' . s:shortts

let s:job_id = job_start(['python', s:path, s:shortts], s:opts)
let s:fuck_id = job_getchannel(s:job_id)
