" Vundle Settings

set nocompatible              " be iMproved, required
filetype off                  " required

" set the runtime path to include Vundle and initialize
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()
Plugin 'ybian/smartim'
Plugin 'iamcco/markdown-preview.nvim'
call vundle#end()            " required
"filetype plugin indent on    " required
let g:smartim_default = 'com.apple.keylayout.ABC'
inoremap <C-c> <esc>

"End Vundle Settings
:set relativenumber

let g:mkdp_auto_start=0
let g:mkdp_browser='/Applications/Safari.app'
let g:mkdp_markdown_css = local_path . '/markdown.css'
let g:mkdp_highlight_css = local_path . '/highlight.css'
let g:mkdp_theme = 'light'

colorscheme torte
set transparency=20
set guifont=Courier_new:h24
set backspace=2
set guioptions-=r
set nu

"The following is used may hax files
"syntax on
"autocmd FileType hx colorscheme haxe
"colorscheme haxe

"The following commands are used previously to open fufufuffu
":cd ~/Dropbox/Latex
":e ini.tex
" ahahahahaha

":cd ~/Desktop/big/github/Linkus-Server
:let counter=[]
:let position=[]
:map <Backspace> X
":map ≥ :!(cd ~/Dropbox/Latex && latex -shell-escape main && bibtex main && latex -shell-escape main && makeindex -s nomencl.ist -t "main.nlg" -o "main.nls" "main.nlo"&& pdflatex -shell-escape main && open -a '/Applications/Skim.app' main.pdf)<CR><CR>
:map ≥ <Plug>MarkdownPreview
":map ≤ :!(cd ~/Dropbox/Latex && pdflatex -shell-escape main && open -a '/Applications/Skim.app' main.pdf)<CR><CR>
:map ≤ :!(pdflatex --synctex=1 -shell-escape main && open main.pdf && cp main.pdf ~/Desktop)<CR><CR>

:map « :execute 'source ' . local_path . '/escape.vim'<CR>
:map \ :execute 'source ' . local_path . '/main.vim'<CR>
:map œ :execute 'source ' . local_path . '/change.vim'<CR>

:map <D-Bslash> /src=\\|href=\\|<r><CR>

:map æ :let a=line(".")<CR>:tabe %<CR>:execute a<CR>
:map ç :let @"=expand('%:p')<CR>

:map ˙ :tabp<CR>
:map ¬ :tabn<CR>
:map Ω :execute "!(open ".expand('%:p:h').")"<CR><CR>
":map ≈ :execute "!(/usr/bin/open -a '/Applications/Google Chrome.app' '".expand('%:p')."')"<CR><CR>
:map ≈ :execute "!open -a Terminal.app '".expand('%:p:h')."'"<CR><CR>
:map ∑ :.s/^-\(\s*\)/\\item\1<CR>
":map ≈ :execute "!(/usr/bin/open -a '/Applications/Google Chrome.app' 'http://127.0.0.1:8000')"<CR><CR>
:map ª :execute "!(/usr/bin/open -a '/Applications/Google Chrome.app' '@@/index.html')"<CR><CR>
:map å :cd %:p:h<CR>
:map • :e @@/API.js<CR>
":map œ :source ~/Dropbox/Latex/readme.md<CR>
:map ¢ :source test.vim<CR>
:map º :cd @/MAT<CR>

:map ¡ :execute 'e ' . local_path . '/readme.md'<CR>
:map £ :execute 'e ' . local_path . '/Jobs/prof.md'<CR>
:map ¢ :execute 'e ' . local_path . '/Jobs/postdoc.md'<CR>
:map ∞ :execute 'e ' . local_path . '/../website/honeymath.github.io/README.md'<CR>
:map § :execute 'e ' . local_path . '/Berkeley/README.md'<CR>
:map • :execute 'e ' . 'list.md'<CR>
:map ™ :execute 'e ' . 'markdown/Diary.md'<CR>Gzz
:map ÷ :execute '!rm ' . local_path . '/main.aux'<CR>:execute '!rm ' . local_path . '/main.toc'<CR>:execute '!rm ' . local_path . '/main.bbl'<CR>

:map … /\\a\(\\\\|{\)<CR>
:map ¥ yf$
:map Á F$yf$
:map ƒ f$
:map ∫ F$
:map † lyt$h
:map ˇ F$lyt$h
:map ∂ :.s/<!--//g<CR> :.s/-->//g<CR>
:map ß 0i<!--<esc>A--><esc>
":map ƒ /<!--<CR>∂

inoremap <C-Z> <C-]>

:command W w

(set of `iab` and `lab` commands omitted for brevity here — ask if you'd like them included again)

:nnoremap gf :execute 'source ' . local_path . '/main.vim'<CR>
:nnoremap gl :execute 'source ' . local_path . '/escape.vim'<CR>
:nnoremap ga :execute 'e ' . local_path . '/readme.md'<CR>

set iskeyword=@,192-255

"autocmd BufEnter * if expand('%:p') == 'Users/qiruili/.vimrc'|echo 'it is vimrc file'|endif
autocmd BufEnter main.tex,ReadMe.md execute('cd '.expand('%:p:h'))
"autocmd BufEnter */fuck/readme.md execute 'source '.fnamemodify(local_path.'/date.vim', ':p')

"After write up a buffer, run git command
" the following just add up to git
au BufWritePost * silent !(git add %:p)

:map ` :highlight Normal ctermfg=white guifg=white <CR>:highlight folded ctermfg=yellow ctermbg=black guifg=yellow guibg=black<CR>:source ~/Dropbox/Latex/fold.md<CR>zr

" Python settings
au BufNewFile,BufRead *.py set expandtab
au BufNewFile,BufRead *.py set shiftwidth=4
au BufNewFile,BufRead *.py set softtabstop=4
au BufNewFile,BufRead *.py set tabstop=4
