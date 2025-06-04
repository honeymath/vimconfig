function! OpenLinkedFile()
    let line = getline('.')
    let filetype = &filetype
    let filename = ''
    let matched = 0

    " Match [label](path) in markdown
    if filetype ==# 'markdown'
        let match = matchlist(line, '\[\zs.*\ze\](\zs[^)]\+\ze)')
        if !empty(match)
            let filename = match[0]
            let matched = 1
        endif
    endif

    " Match \input{filename} in tex
    if filetype ==# 'tex'
        let match = matchlist(line, '\\input{\zs[^}]\+\ze}')
        if !empty(match)
            let filename = match[0] . '.tex'
            let matched = 1
        endif
    endif

    " If a filename was extracted
    if matched
        let fullpath = fnamemodify(expand('%:p:h') . '/' . filename, ':p')
        let dir = fnamemodify(fullpath, ':h')

        " Create directory if missing
        if !isdirectory(dir)
            call mkdir(dir, 'p')
        endif

        " Create empty file if missing
        if !filereadable(fullpath)
            call writefile([], fullpath)
        endif

        " Push current file and position to stack
        if exists('g:counter') == 0 | let g:counter = [] | endif
        if exists('g:position') == 0 | let g:position = [] | endif
        call insert(g:counter, expand('%:p'), 0)
        call insert(g:position, 'call cursor('.line('.').')', 0)

        " Open the new file
        execute 'edit ' . fnameescape(fullpath)
    else
        echo "No valid pattern found in current line"
    endif
endfunction

" Example key binding
nnoremap <silent> <leader>e :call OpenLinkedFile()<CR>

