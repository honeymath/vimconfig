function! s:OnOut(channel, msg)
  echom "OUT"
  if !empty(a:msg)
"    exec a:msg
    echom '[stdout] ' . a:msg
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
"see: look at the following
"call job_start(['python', expand('~/repositories/syncpdf-remote/listener.py')], s:opts)
"end
"ai: I wanna modify the above so that it is starting channel.py, with the same directory of this script file. Write it at following
echom "I am fucking here"
let s:path = expand(fnamemodify(expand('<sfile>'), ':p:h') . '/channel.py')
echom s:path
function! Starto()
	call job_start(['python', s:path], s:opts)
endfunction
call Starto()
"end
