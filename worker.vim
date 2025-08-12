function! s:OnOut(channel, msg)
  echom "OUT"
	if !empty(a:msg)
		"    exec a:msg
		echom '[stdout] ' . a:msg
	endif
	if(a:msg == 'X')
		"X for running the script
		call s:ActivateCaller(shortts)
	endif
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
      \ 'out_cb': function('s:OnOut'),
      \ 'err_cb': function('s:OnErr'),
      \ 'exit_cb': function('s:OnExit')
      \ }

function! s:ActivateCaller(uuid)
	echom 'Activating caller with UUID: ' . a:uuid
	let s:tools_path = expand('<sfile>:p:h') 
        execute 'py3 import sys; sys.path.insert(0,"' . s:tools_path . '")'
        execute 'py3 import caller'
	execute 'py3 caller.process_commands("' . a:uuid . '")'
endfunction

echom "I am fucking here"
let s:path = expand(fnamemodify(expand('<sfile>'), ':p:h') . '/channel.py')
echom s:path

function! Starto()
	call job_start(['python', s:path, s:shortts], s:opts)
endfunction

let chars = '0123456789abcdefghijklmnopqrstuvwxyz'
let s:t = localtime()
let s:shortts = ''
while s:t > 0
    let s:shortts = chars[s:t % 36] . s:shortts
    let s:t = s:t / 36
endwhile
echom 'Fucking shortts: ' . s:shortts
call Starto()
