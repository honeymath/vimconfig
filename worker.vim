function! s:OnOut(channel, msg)
  if !empty(a:msg)
    exec a:msg
    echom '[stdout] ' . a:msg
  endif
endfunction

function! s:OnErr(channel, msg)
  if !empty(a:msg)
    echom '[stderr] ' . a:msg
  endif
endfunction

function! s:OnExit(job, status)
  echom '[exit] Job exited with status ' . a:status
endfunction

let s:opts = {
      \ 'out_cb': function('s:OnOut'),
      \ 'err_cb': function('s:OnErr'),
      \ 'exit_cb': function('s:OnExit')
      \ }

call job_start(['python', expand('~/repositories/syncpdf-remote/listener.py')], s:opts)
