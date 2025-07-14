" Vundle Settings

set nocompatible              " be iMproved, required
filetype off                  " required
syntax on

if isdirectory(expand('~/repositories/syncpdf-remote'))
	source ~/repositories/syncpdf-remote/synccurl.vim
else
  echo "找不到目录：~/repositories/syncpdf-remote"
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
  let l:didi = fnamemodify(l:path, ':h')
  let l:dir = fnamemodify(expand('<sfile>:p:h') . '/' . l:didi, ':p')
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



:map <Backspace> X

:map « :call SmartCtrlO()<CR>

nnoremap œ :execute g:exec<CR>

:map <D-Bslash> /src=\\|href=\\|<r><CR>

:map æ :let a=line(".")<CR>:tabe %<CR>:execute a<CR>
:map ç :let @"=expand('%:p')<CR>

:map ˙ :tabp<CR>
:map ¬ :tabn<CR>
:map Ω :execute "!(open ".expand('%:p:h').")"<CR><CR>
:map ≈ :execute "!open -a Terminal.app '".expand('%:p:h')."'"<CR><CR>
:map ∑ :.s/^-\(\s*\)/\\item\1<CR>
:map ª :execute "!(/usr/bin/open -a '/Applications/Google Chrome.app' '@@/index.html')"<CR><CR>
:map å :cd %:p:h<CR>
:map ¢ :source test.vim<CR>

:map ¡ :execute 'e ' . local_path . '/../readme.md'<CR>
:map ™ :execute 'e ' . local_path . '/readme.md'<CR>
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




autocmd BufEnter main.tex,ReadMe.md execute('cd '.expand('%:p:h'))

" the following just add up to git
au BufWritePost * silent !(git add %:p)


" Python settings
au BufNewFile,BufRead *.py set expandtab
au BufNewFile,BufRead *.py set shiftwidth=4
au BufNewFile,BufRead *.py set softtabstop=4
au BufNewFile,BufRead *.py set tabstop=4

autocmd FileType tex iabbrev AA ⋀
autocmd FileType tex iabbrev VV ⋁
autocmd FileType tex iabbrev /\/\ ♡
autocmd FileType tex iabbrev [- ∈
autocmd FileType tex iabbrev \[- ∉
autocmd FileType tex iabbrev -] ∋
autocmd FileType tex iabbrev \-] ∌
autocmd FileType tex iabbrev ¬ ⊥
autocmd FileType tex iabbrev l__ ⌊
autocmd FileType tex iabbrev __l ⌋
autocmd FileType tex iabbrev ¯¯l ⌉
autocmd FileType tex iabbrev l¯¯ ⌈
autocmd FileType tex iabbrev <=> ⟺
autocmd FileType tex iabbrev ⟸> ⟺
autocmd FileType tex iabbrev => ⟹
autocmd FileType tex :iab <= ⟸
autocmd FileType python :iab <= ⟸  |iunabbrev <=
":iab <= ⟸
autocmd FileType tex iabbrev << ⊆
autocmd FileType tex iabbrev nn ∩
autocmd FileType tex iabbrev φφ ϕ
autocmd FileType tex iabbrev uu ∪
autocmd FileType tex iabbrev ><< ⊈
autocmd FileType tex iabbrev <>> ⊉
autocmd FileType tex iabbrev >>>> ⊇
autocmd FileType tex iabbrev O+ ⨁
autocmd FileType tex iabbrev OX ⨂
autocmd FileType tex iabbrev ~= ≅
autocmd FileType tex iabbrev ~~ ≈
autocmd FileType tex :iab == ≡
autocmd FileType python :iab == ≡|iunabbrev ==
":iab == ≡
autocmd FileType tex iabbrev ≅-> ⥱
autocmd FileType tex iabbrev ≅−> ⥱
autocmd FileType tex iabbrev ~=⟶  ⥱
autocmd FileType tex iabbrev ~=-> ⥱
autocmd FileType tex iabbrev ~=−> ⥱
autocmd FileType tex iabbrev ~≠ ≇
autocmd FileType tex iabbrev ?= ≟
autocmd FileType tex iabbrev ∑∑ ∃
autocmd FileType tex iabbrev ∏∏ ∀
autocmd FileType tex iabbrev ±± ∓
autocmd FileType tex iabbrev (-> ↪
autocmd FileType tex iabbrev (−> ↪
autocmd FileType tex iabbrev <-) ↩
autocmd FileType tex iabbrev <−) ↩
autocmd FileType tex iabbrev ←) ↩
autocmd FileType tex iabbrev ->> ↠
autocmd FileType tex iabbrev −>> ↠
autocmd FileType tex iabbrev <<- ↞
autocmd FileType tex iabbrev <<− ↞
autocmd FileType tex iabbrev -> ⟶
autocmd FileType tex iabbrev −> ⟶
autocmd FileType tex iabbrev <- ⟵
autocmd FileType tex iabbrev <− ⟵
autocmd FileType tex iabbrev <−> ⟵
autocmd FileType tex iabbrev ⟵> ↔
autocmd FileType tex iabbrev --> ⤍
autocmd FileType tex iabbrev −-> ⤍
autocmd FileType tex iabbrev −−> ⤍
autocmd FileType tex iabbrev ⟵- ⤌
autocmd FileType tex iabbrev l-> ↦
autocmd FileType tex iabbrev <-l ↤
autocmd FileType tex iabbrev l−> ↦
autocmd FileType tex iabbrev llv ↧
autocmd FileType tex iabbrev lla ↥
autocmd FileType tex iabbrev lV ⭣
autocmd FileType tex iabbrev lv ⭣
autocmd FileType tex iabbrev lA ⭡
autocmd FileType tex iabbrev la ⭡
autocmd FileType tex iabbrev <> ⬨
autocmd FileType tex iabbrev \\\ ∖
"autocmd FileType tex iabbrev [] ∎
":lab lx ⋉
"autocmd FileType tex iabbrev xl ⋊
autocmd FileType tex iabbrev xoo ⊠
autocmd FileType tex iabbrev poo ⊞

"autocmd FileType tex iabbrev^0 <BS>⁰
"autocmd FileType tex iabbrev^2 <BS>²
"autocmd FileType tex iabbrev^3 <BS>³
"autocmd FileType tex iabbrev^4 <BS>⁴
"autocmd FileType tex iabbrev^5 <BS>⁵
"autocmd FileType tex iabbrev^6 <BS>⁶
"autocmd FileType tex iabbrev^7 <BS>⁷
"autocmd FileType tex iabbrev^8 <BS>⁸
"autocmd FileType tex iabbrev^9 <BS>⁹

"autocmd FileType tex iabbrev_0 <BS>₀
"autocmd FileType tex iabbrev_1 <BS>₁
"autocmd FileType tex iabbrev_2 <BS>₂
"autocmd FileType tex iabbrev_3 <BS>₃
"autocmd FileType tex iabbrev_4 <BS>₄
"autocmd FileType tex iabbrev_5 <BS>₅
"autocmd FileType tex iabbrev_6 <BS>₆
"autocmd FileType tex iabbrev_7 <BS>₇
"autocmd FileType tex iabbrev_8 <BS>₈
"autocmd FileType tex iabbrev_9 <BS>₉

autocmd FileType tex iabbrev^+ <BS>⁺
autocmd FileType tex iabbrev^- <BS>⁻


"autocmd FileType tex iabbrev- −

autocmd FileType tex iabbrev_+ <BS>₊
autocmd FileType tex iabbrev_- <BS>₋

autocmd FileType tex iabbrev xx ×
autocmd FileType tex iabbrev oo ⚬
autocmd FileType tex iabbrev ,, ␣
autocmd FileType tex iabbrev UUU ∐
autocmd FileType tex iabbrev ππ ϖ


autocmd FileType tex iabbrev bA 𝔸
autocmd FileType tex iabbrev bB 𝔹
autocmd FileType tex iabbrev bC ℂ
autocmd FileType tex iabbrev bD 𝔻
autocmd FileType tex iabbrev bE 𝔼
autocmd FileType tex iabbrev bF 𝔽
autocmd FileType tex iabbrev bG 𝔾
autocmd FileType tex iabbrev bH ℍ
autocmd FileType tex iabbrev bI 𝕀
autocmd FileType tex iabbrev bJ 𝕁
autocmd FileType tex iabbrev bK 𝕂
autocmd FileType tex iabbrev bL 𝕃
autocmd FileType tex iabbrev bM 𝕄
autocmd FileType tex iabbrev bN ℕ
autocmd FileType tex iabbrev bO 𝕆
autocmd FileType tex iabbrev bP ℙ
autocmd FileType tex iabbrev bQ ℚ
autocmd FileType tex iabbrev bR ℝ
autocmd FileType tex iabbrev bS 𝕊
autocmd FileType tex iabbrev bT 𝕋
autocmd FileType tex iabbrev bU 𝕌
autocmd FileType tex iabbrev bV 𝕍
autocmd FileType tex iabbrev bW 𝕎
autocmd FileType tex iabbrev bX 𝕏
autocmd FileType tex iabbrev bY 𝕐
autocmd FileType tex iabbrev bZ ℤ


autocmd FileType tex iabbrev sA 𝒜
autocmd FileType tex iabbrev sB ℬ
autocmd FileType tex iabbrev sC 𝒞
autocmd FileType tex iabbrev sD 𝒟
autocmd FileType tex iabbrev sE ℰ
autocmd FileType tex iabbrev sF ℱ
autocmd FileType tex iabbrev sG 𝒢
autocmd FileType tex iabbrev sH ℋ
autocmd FileType tex iabbrev sI ℐ
autocmd FileType tex iabbrev sJ 𝒥
autocmd FileType tex iabbrev sK 𝒦
autocmd FileType tex iabbrev sL ℒ
autocmd FileType tex iabbrev sM ℳ
autocmd FileType tex iabbrev sN 𝒩
autocmd FileType tex iabbrev sO 𝒪
autocmd FileType tex iabbrev sP 𝒫
autocmd FileType tex iabbrev sQ 𝒬
autocmd FileType tex iabbrev sR ℛ
autocmd FileType tex iabbrev sS 𝒮
autocmd FileType tex iabbrev sT 𝒯
autocmd FileType tex iabbrev sU 𝒰
autocmd FileType tex iabbrev sV 𝒱
autocmd FileType tex iabbrev sW 𝒲
autocmd FileType tex iabbrev sX 𝒳
autocmd FileType tex iabbrev sY 𝒴
autocmd FileType tex iabbrev sZ 𝒵

autocmd FileType tex iabbrev fkA 𝕬
autocmd FileType tex iabbrev fkB 𝕭
autocmd FileType tex iabbrev fkC 𝕮
autocmd FileType tex iabbrev fkD 𝕯
autocmd FileType tex iabbrev fkE 𝕰
autocmd FileType tex iabbrev fkF 𝕱
autocmd FileType tex iabbrev fkG 𝕲
autocmd FileType tex iabbrev fkH 𝕳
autocmd FileType tex iabbrev fkI 𝕴
autocmd FileType tex iabbrev fkJ 𝕵
autocmd FileType tex iabbrev fkK 𝕶
autocmd FileType tex iabbrev fkL 𝕷
autocmd FileType tex iabbrev fkM 𝕸
autocmd FileType tex iabbrev fkN 𝕹
autocmd FileType tex iabbrev fkO 𝕺
autocmd FileType tex iabbrev fkP 𝕻
autocmd FileType tex iabbrev fkQ 𝕼
autocmd FileType tex iabbrev fkR 𝕽
autocmd FileType tex iabbrev fkS 𝕾
autocmd FileType tex iabbrev fkT 𝕿
autocmd FileType tex iabbrev fkU 𝖀
autocmd FileType tex iabbrev fkV 𝖁
autocmd FileType tex iabbrev fkW 𝖂
autocmd FileType tex iabbrev fkX 𝖃
autocmd FileType tex iabbrev fkY 𝖄
autocmd FileType tex iabbrev fkZ 𝖅
autocmd FileType tex iabbrev fka 𝖆
autocmd FileType tex iabbrev fkb 𝖇
autocmd FileType tex iabbrev fkc 𝖈
autocmd FileType tex iabbrev fkd 𝖉
autocmd FileType tex iabbrev fke 𝖊
autocmd FileType tex iabbrev fkf 𝖋
autocmd FileType tex iabbrev fkg 𝖌
autocmd FileType tex iabbrev fkh 𝖍
autocmd FileType tex iabbrev fki 𝖎
autocmd FileType tex iabbrev fkj 𝖏
autocmd FileType tex iabbrev fkk 𝖐
autocmd FileType tex iabbrev fkl 𝖑
autocmd FileType tex iabbrev fkm 𝖒
autocmd FileType tex iabbrev fkn 𝖓
autocmd FileType tex iabbrev fko 𝖔
autocmd FileType tex iabbrev fkp 𝖕
autocmd FileType tex iabbrev fkq 𝖖
autocmd FileType tex iabbrev fkr 𝖗
autocmd FileType tex iabbrev fks 𝖘
autocmd FileType tex iabbrev fkt 𝖙
autocmd FileType tex iabbrev fku 𝖚
autocmd FileType tex iabbrev fkv 𝖛
autocmd FileType tex iabbrev fkw 𝖜
autocmd FileType tex iabbrev fkx 𝖝
autocmd FileType tex iabbrev fky 𝖞
autocmd FileType tex iabbrev fkz 𝖟

autocmd FileType tex iabbrev ba 𝗮
autocmd FileType tex iabbrev bb 𝗯
autocmd FileType tex iabbrev bc 𝗰
autocmd FileType tex iabbrev bd 𝗱
autocmd FileType tex iabbrev bbe 𝗲
autocmd FileType tex iabbrev bf 𝗳
autocmd FileType tex iabbrev bg 𝗴
autocmd FileType tex iabbrev bh 𝗵
autocmd FileType tex iabbrev bi 𝗶
autocmd FileType tex iabbrev bj 𝗷
autocmd FileType tex iabbrev bk 𝗸
autocmd FileType tex iabbrev bl 𝗹
autocmd FileType tex iabbrev bm 𝗺
autocmd FileType tex iabbrev bn 𝗻
autocmd FileType tex iabbrev bo 𝗼
autocmd FileType tex iabbrev bp 𝗽
autocmd FileType tex iabbrev bq 𝗾
autocmd FileType tex iabbrev br 𝗿
autocmd FileType tex iabbrev bs 𝘀
autocmd FileType tex iabbrev bt 𝘁
autocmd FileType tex iabbrev bu 𝘂
autocmd FileType tex iabbrev bv 𝘃
autocmd FileType tex iabbrev bw 𝘄
autocmd FileType tex iabbrev bx 𝘅
autocmd FileType tex iabbrev bby 𝘆
autocmd FileType tex iabbrev bz 𝘇

autocmd FileType tex iabbrev cA 𝘼
autocmd FileType tex iabbrev cB 𝘽
autocmd FileType tex iabbrev cC 𝘾
autocmd FileType tex iabbrev cD 𝘿
autocmd FileType tex iabbrev cE 𝙀
autocmd FileType tex iabbrev cF 𝙁
autocmd FileType tex iabbrev cG 𝙂
autocmd FileType tex iabbrev cH 𝙃
autocmd FileType tex iabbrev cI 𝙄
autocmd FileType tex iabbrev cJ 𝙅
autocmd FileType tex iabbrev cK 𝙆
autocmd FileType tex iabbrev cL 𝙇
autocmd FileType tex iabbrev cM 𝙈
autocmd FileType tex iabbrev cN 𝙉
autocmd FileType tex iabbrev cO 𝙊
autocmd FileType tex iabbrev cP 𝙋
autocmd FileType tex iabbrev cQ 𝙌
autocmd FileType tex iabbrev cR 𝙍
autocmd FileType tex iabbrev cS 𝙎
autocmd FileType tex iabbrev cT 𝙏
autocmd FileType tex iabbrev cU 𝙐
autocmd FileType tex iabbrev cV 𝙑
autocmd FileType tex iabbrev cW 𝙒
autocmd FileType tex iabbrev cX 𝙓
autocmd FileType tex iabbrev cY 𝙔
autocmd FileType tex iabbrev cZ 𝙕


autocmd FileType tex iabbrev 𝗯1 𝟙
autocmd FileType tex iabbrev bb1 𝟙
autocmd FileType tex iabbrev 𝗯0 𝟘
autocmd FileType tex iabbrev bb0 𝟘

:clearjumps
