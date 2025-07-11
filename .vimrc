" Vundle Settings

set nocompatible              " be iMproved, required
filetype off                  " required
syntax on

if isdirectory('~/repositories/syncpdf-remote')
	source ~/repositories/syncpdf-remote/synccurl.vim
	source ~/repositories/syncpdf-remote/worker.vim
endif
source ~/repositories/vimconfig/channel.vim

"call plug#begin('~/.vim/plugged')
"Plug 'github/copilot.vim'
"call plug#end()

if has("termguicolors")
  let &t_SI = "\e[6 q"   " I-beam in Insert mode
  let &t_EI = "\e[2 q"   " Block in Normal mode
endif

function! SuggestOneWord()
  let suggestion = copilot#Accept("")
  let bar = copilot#TextQueuedForInsertion()
  return strlen(bar) > 0 ? matchstr(bar, '^\s*\S\+') : ""
endfunction

inoremap <expr> <C-l> SuggestOneWord()

set jumpoptions+=stack


autocmd BufEnter ~/repositories/readme.md clearjumps
:nnoremap \ :call EnterPath()<CR>
function! EnterPath()
  let l:line = getline('.')
  if l:line =~ '\[\zs.*\ze\](\zs[^)]\+\ze)'  " Markdown style
    let l:path = matchstr(l:line, '\[\zs.*\ze\](\zs[^)]\+\ze)')
  elseif l:line =~ '\\input{\zs[^}]\+\ze}'  " LaTeX \input style
    let l:path = matchstr(l:line, '\\input{\zs[^}]\+\ze}')
    let l:path = substitute(l:path, '\.tex$', '', '')  " Remove .tex if it exists
    let l:path = l:path . '.tex'  " Always add .tex explicitly
  else
    echo "No matching path found"
    return
  endif
  let l:dir = fnamemodify(l:path, ':h')
  if !isdirectory(l:dir)
    call mkdir(l:dir, 'p')
    echo "Created: " . l:dir
  else
    echo "Directory already exists"
  endif
  execute 'edit' fnameescape(expand('%:p:h') . '/' .l:path)
endfunction
function! SmartCtrlO()
  " Get the current position in the jumplist
  " first, let try to jump for one step.
  execute "normal! \<C-o>" 
  let [jumplist, idx] = getjumplist()
  let save_cursor = getpos('.')
  while idx > 0
    let prev = jumplist[idx - 1]
    " prev is a list: [bufnr, lnum, col, text]
    let bufnr = prev['bufnr']
    if bufnr != bufnr('%')  " It's a jump to another file
      break
    endif
    " jump to the previous entry
    execute "normal! \<C-o>"
    let [jumplist, idx] = getjumplist()
  endwhile
  call setpos('.', save_cursor)  
endfunction
" set the runtime path to include Vundle and initialize
set rtp+=~/.vim/bundle/Vundle.vim
"call vundle#begin()
"Plugin 'ybian/smartim'
"Plugin 'iamcco/markdown-preview.nvim'
"call vundle#end()            " required
"filetype plugin indent on    " required
"let g:smartim_default = 'com.apple.keylayout.ABC'
"inoremap <C-c> <esc>

"End Vundle Settings
:set relativenumber

"let g:mkdp_auto_start=0
"let g:mkdp_browser='/Applications/Safari.app'
"let g:mkdp_markdown_css = local_path . '/markdown.css'
"let g:mkdp_highlight_css = local_path . '/highlight.css'
"let g:mkdp_theme = 'light'

colorscheme torte
"set transparency=20
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
":let counter=[]
":let position=[]
:map <Backspace> X
":map ≥ :!(cd ~/Dropbox/Latex && latex -shell-escape main && bibtex main && latex -shell-escape main && makeindex -s nomencl.ist -t "main.nlg" -o "main.nls" "main.nlo"&& pdflatex -shell-escape main && open -a '/Applications/Skim.app' main.pdf)<CR><CR>
":map ≥ <Plug>MarkdownPreview
":map ≤ :!(cd ~/Dropbox/Latex && pdflatex -shell-escape main && open -a '/Applications/Skim.app' main.pdf)<CR><CR>
":map ≤ :!(pdflatex --synctex=1 -shell-escape main && open main.pdf && cp main.pdf ~/Desktop)<CR><CR>

:map « :call SmartCtrlO()<CR>
":map « :execute 'source ' . local_path . '/escape.vim'<CR>
":map \ :execute 'source ' . local_path . '/main.vim'<CR>
"I wanna map \ to whenever it is markdown file, then it doing %gf, when it is latex, it doing %%gf
":map \ 
":map \ gf<CR>

":map œ :execute 'source ' . local_path . '/change.vim'<CR>

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
":map • :e @@/API.js<CR>
":map œ :source ~/Dropbox/Latex/readme.md<CR>
:map ¢ :source test.vim<CR>
":map º :cd @/MAT<CR>

:map ¡ :execute 'e ' . local_path . '/readme.md'<CR>
":map £ :execute 'e ' . local_path . '/Jobs/prof.md'<CR>
":map ¢ :execute 'e ' . local_path . '/Jobs/postdoc.md'<CR>
":map ∞ :execute 'e ' . local_path . '/../website/honeymath.github.io/README.md'<CR>
":map § :execute 'e ' . local_path . '/Berkeley/README.md'<CR>
":map • :execute 'e ' . 'list.md'<CR>
":map ™ :execute 'e ' . 'markdown/Diary.md'<CR>Gzz
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

"(set of `iab` and `lab` commands omitted for brevity here — ask if you'd like them included again)

":nnoremap gf :execute 'source ' . local_path . '/main.vim'<CR>
":nnoremap gl :execute 'source ' . local_path . '/escape.vim'<CR>
":nnoremap ga :execute 'e ' . local_path . '/readme.md'<CR>

"set iskeyword=@,192-255

"autocmd BufEnter * if expand('%:p') == 'Users/qiruili/.vimrc'|echo 'it is vimrc file'|endif
autocmd BufEnter main.tex,ReadMe.md execute('cd '.expand('%:p:h'))
"autocmd BufEnter */fuck/readme.md execute 'source '.fnamemodify(local_path.'/date.vim', ':p')

"After write up a buffer, run git command
" the following just add up to git
au BufWritePost * silent !(git add %:p)

":map ` :highlight Normal ctermfg=white guifg=white <CR>:highlight folded ctermfg=yellow ctermbg=black guifg=yellow guibg=black<CR>:source ~/Dropbox/Latex/fold.md<CR>zr

" Python settings
au BufNewFile,BufRead *.py set expandtab
au BufNewFile,BufRead *.py set shiftwidth=4
au BufNewFile,BufRead *.py set softtabstop=4
au BufNewFile,BufRead *.py set tabstop=4

:iab AA ⋀
:iab VV ⋁
:iab /\/\ ♡
:iab [- ∈
:iab \[- ∉
:iab -] ∋
:iab \-] ∌
:iab ¬ ⊥
:iab l__ ⌊
:iab __l ⌋
:iab ¯¯l ⌉
:iab l¯¯ ⌈
:iab <=> ⟺
:iab ⟸> ⟺
:iab => ⟹
autocmd FileType tex :iab <= ⟸
autocmd FileType python :iab <= ⟸  |iunabbrev <=
":iab <= ⟸
:iab << ⊆
:iab nn ∩
:iab φφ ϕ
:iab uu ∪
:iab ><< ⊈
:iab <>> ⊉
:iab >>>> ⊇
:iab O+ ⨁
:iab OX ⨂
:iab ~= ≅
:iab ~~ ≈
autocmd FileType tex :iab == ≡
autocmd FileType python :iab == ≡|iunabbrev ==
":iab == ≡
:iab ≅-> ⥱
:iab ≅−> ⥱
:iab ~=⟶  ⥱
:iab ~=-> ⥱
:iab ~=−> ⥱
:iab ~≠ ≇
:iab ?= ≟
:iab ∑∑ ∃
:iab ∏∏ ∀
:iab ±± ∓
:iab (-> ↪
:iab (−> ↪
:iab <-) ↩
:iab <−) ↩
:iab ←) ↩
:iab ->> ↠
:iab −>> ↠
:iab <<- ↞
:iab <<− ↞
:iab -> ⟶
:iab −> ⟶
":iab -> ➔
:iab <- ⟵
:iab <− ⟵
:iab <−> ⟵
:iab ⟵> ↔
":iab <- ⬅ 
:iab --> ⤍
:iab −-> ⤍
:iab −−> ⤍
:iab ⟵- ⤌
":iab ⬅- ⤌
:iab l-> ↦
:iab <-l ↤
:iab l−> ↦
:iab llv ↧
:iab lla ↥
:iab lV ⭣
:iab lv ⭣
:iab lA ⭡
:iab la ⭡
:iab <> ⬨
":iab ** ⁎
:iab \\\ ∖
":iab [] ∎
":lab lx ⋉
":iab xl ⋊
:iab xoo ⊠
:iab poo ⊞

":iab^0 <BS>⁰
":iab^2 <BS>²
":iab^3 <BS>³
":iab^4 <BS>⁴
":iab^5 <BS>⁵
":iab^6 <BS>⁶
":iab^7 <BS>⁷
":iab^8 <BS>⁸
":iab^9 <BS>⁹

":iab_0 <BS>₀
":iab_1 <BS>₁
":iab_2 <BS>₂
":iab_3 <BS>₃
":iab_4 <BS>₄
":iab_5 <BS>₅
":iab_6 <BS>₆
":iab_7 <BS>₇
":iab_8 <BS>₈
":iab_9 <BS>₉

:iab^+ <BS>⁺
:iab^- <BS>⁻


":iab- −

:iab_+ <BS>₊
:iab_- <BS>₋

:iab xx ×
:iab oo ⚬
:iab ,, ␣
:iab UUU ∐
:iab ππ ϖ


:iab bA 𝔸
:iab bB 𝔹
:iab bC ℂ
:iab bD 𝔻
:iab bE 𝔼
:iab bF 𝔽
:iab bG 𝔾
:iab bH ℍ
:iab bI 𝕀
:iab bJ 𝕁
:iab bK 𝕂
:iab bL 𝕃
:iab bM 𝕄
:iab bN ℕ
:iab bO 𝕆
:iab bP ℙ
:iab bQ ℚ
:iab bR ℝ
:iab bS 𝕊
:iab bT 𝕋
:iab bU 𝕌
:iab bV 𝕍
:iab bW 𝕎
:iab bX 𝕏
:iab bY 𝕐
:iab bZ ℤ


:iab sA 𝒜
:iab sB ℬ
:iab sC 𝒞
:iab sD 𝒟
:iab sE ℰ
:iab sF ℱ
:iab sG 𝒢
:iab sH ℋ
:iab sI ℐ
:iab sJ 𝒥
:iab sK 𝒦
:iab sL ℒ
:iab sM ℳ
:iab sN 𝒩
:iab sO 𝒪
:iab sP 𝒫
:iab sQ 𝒬
:iab sR ℛ
:iab sS 𝒮
:iab sT 𝒯
:iab sU 𝒰
:iab sV 𝒱
:iab sW 𝒲
:iab sX 𝒳
:iab sY 𝒴
:iab sZ 𝒵

:iab fkA 𝕬
:iab fkB 𝕭
:iab fkC 𝕮
:iab fkD 𝕯
:iab fkE 𝕰
:iab fkF 𝕱
:iab fkG 𝕲
:iab fkH 𝕳
:iab fkI 𝕴
:iab fkJ 𝕵
:iab fkK 𝕶
:iab fkL 𝕷
:iab fkM 𝕸
:iab fkN 𝕹
:iab fkO 𝕺
:iab fkP 𝕻
:iab fkQ 𝕼
:iab fkR 𝕽
:iab fkS 𝕾
:iab fkT 𝕿
:iab fkU 𝖀
:iab fkV 𝖁
:iab fkW 𝖂
:iab fkX 𝖃
:iab fkY 𝖄
:iab fkZ 𝖅
:iab fka 𝖆
:iab fkb 𝖇
:iab fkc 𝖈
:iab fkd 𝖉
:iab fke 𝖊
:iab fkf 𝖋
:iab fkg 𝖌
:iab fkh 𝖍
:iab fki 𝖎
:iab fkj 𝖏
:iab fkk 𝖐
:iab fkl 𝖑
:iab fkm 𝖒
:iab fkn 𝖓
:iab fko 𝖔
:iab fkp 𝖕
:iab fkq 𝖖
:iab fkr 𝖗
:iab fks 𝖘
:iab fkt 𝖙
:iab fku 𝖚
:iab fkv 𝖛
:iab fkw 𝖜
:iab fkx 𝖝
:iab fky 𝖞
:iab fkz 𝖟

:iab ba 𝗮
:iab bb 𝗯
:iab bc 𝗰
:iab bd 𝗱
:iab bbe 𝗲
:iab bf 𝗳
:iab bg 𝗴
:iab bh 𝗵
:iab bi 𝗶
:iab bj 𝗷
:iab bk 𝗸
:iab bl 𝗹
:iab bm 𝗺
:iab bn 𝗻
:iab bo 𝗼
:iab bp 𝗽
:iab bq 𝗾
:iab br 𝗿
:iab bs 𝘀
:iab bt 𝘁
:iab bu 𝘂
:iab bv 𝘃
:iab bw 𝘄
:iab bx 𝘅
:iab bby 𝘆
:iab bz 𝘇

:iab cA 𝘼
:iab cB 𝘽
:iab cC 𝘾
:iab cD 𝘿
:iab cE 𝙀
:iab cF 𝙁
:iab cG 𝙂
:iab cH 𝙃
:iab cI 𝙄
:iab cJ 𝙅
:iab cK 𝙆
:iab cL 𝙇
:iab cM 𝙈
:iab cN 𝙉
:iab cO 𝙊
:iab cP 𝙋
:iab cQ 𝙌
:iab cR 𝙍
:iab cS 𝙎
:iab cT 𝙏
:iab cU 𝙐
:iab cV 𝙑
:iab cW 𝙒
:iab cX 𝙓
:iab cY 𝙔
:iab cZ 𝙕


:iab 𝗯1 𝟙
:iab bb1 𝟙
:iab 𝗯0 𝟘
:iab bb0 𝟘

:clearjumps
