

set nocompatible              " be iMproved, required
filetype off                  " required
syntax on

let s:vimconfig_path = expand('<sfile>:p:h')

if isdirectory(s:vimconfig_path . '/../syncpdf-remote')
"if isdirectory(expand('~/repositories/syncpdf-remote'))
"	source ~/repositories/syncpdf-remote/synccurl.vim
	execute 'source ' . fnameescape(s:vimconfig_path . '/../syncpdf-remote/synccurl.vim')
else
  echo "Can not find the directory: ".s:vimconfig_path . '/../syncpdf-remote'
endif

if filereadable(s:vimconfig_path . '/../vimconfig/config.ini')
"if filereadable(expand('~/repositories/vimconfig/config.ini'))
"  source ~/repositories/vimconfig/channel.vim
	 execute 'source ' . fnameescape(s:vimconfig_path . '/../vimconfig/channel.vim')
"	 execute 'source' . fnameescape(s:vimconfig_path. '/../vimconfig/worker.vim')
else
  echo "Can not fine the config file: ".s:vimconfig_path . '/../vimconfig/config.ini'
endif

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
  let l:dir = resolve(fnamemodify(expand('%:p:h') . '/' . l:didi, ':p'))
"  echom "Directory: " . l:dir

"  let l:dir = fnamemodify(expand('<sfile>:p:h') . '/' . l:didi, ':p')
  if !isdirectory(expand(l:dir))
    call mkdir(l:dir, 'p')
    echo "Created: " . l:dir
  else
"    echom "Directory already exists". l:dir
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

autocmd FileType tex,plaintex iabbrev AA ⋀
autocmd FileType tex,plaintex iabbrev VV ⋁
autocmd FileType tex,plaintex iabbrev /\/\ ♡
autocmd FileType tex,plaintex iabbrev [- ∈
autocmd FileType tex,plaintex iabbrev \[- ∉
autocmd FileType tex,plaintex iabbrev -] ∋
autocmd FileType tex,plaintex iabbrev \-] ∌
autocmd FileType tex,plaintex iabbrev ¬ ⊥
autocmd FileType tex,plaintex iabbrev l__ ⌊
autocmd FileType tex,plaintex iabbrev __l ⌋
autocmd FileType tex,plaintex iabbrev ¯¯l ⌉
autocmd FileType tex,plaintex iabbrev l¯¯ ⌈
autocmd FileType tex,plaintex iabbrev <=> ⟺
autocmd FileType tex,plaintex iabbrev ⟸> ⟺
autocmd FileType tex,plaintex iabbrev => ⟹
autocmd FileType tex,plaintex :iab <= ⟸
autocmd FileType python :iab <= ⟸  |iunabbrev <=
":iab <= ⟸
autocmd FileType tex,plaintex iabbrev << ⊆
autocmd FileType tex,plaintex iabbrev nn ∩
autocmd FileType tex,plaintex iabbrev φφ ϕ
autocmd FileType tex,plaintex iabbrev uu ∪
autocmd FileType tex,plaintex iabbrev ><< ⊈
autocmd FileType tex,plaintex iabbrev <>> ⊉
autocmd FileType tex,plaintex iabbrev >>>> ⊇
autocmd FileType tex,plaintex iabbrev O+ ⨁
autocmd FileType tex,plaintex iabbrev OX ⨂
autocmd FileType tex,plaintex iabbrev ~= ≅
autocmd FileType tex,plaintex iabbrev ~~ ≈
autocmd FileType tex,plaintex :iab == ≡
autocmd FileType python :iab == ≡|iunabbrev ==
":iab == ≡
autocmd FileType tex,plaintex iabbrev ≅-> ⥱
autocmd FileType tex,plaintex iabbrev ≅−> ⥱
autocmd FileType tex,plaintex iabbrev ~=⟶  ⥱
autocmd FileType tex,plaintex iabbrev ~=-> ⥱
autocmd FileType tex,plaintex iabbrev ~=−> ⥱
autocmd FileType tex,plaintex iabbrev ~≠ ≇
autocmd FileType tex,plaintex iabbrev ?= ≟
autocmd FileType tex,plaintex iabbrev ∑∑ ∃
autocmd FileType tex,plaintex iabbrev ∏∏ ∀
autocmd FileType tex,plaintex iabbrev ±± ∓
autocmd FileType tex,plaintex iabbrev (-> ↪
autocmd FileType tex,plaintex iabbrev (−> ↪
autocmd FileType tex,plaintex iabbrev <-) ↩
autocmd FileType tex,plaintex iabbrev <−) ↩
autocmd FileType tex,plaintex iabbrev ←) ↩
autocmd FileType tex,plaintex iabbrev ->> ↠
autocmd FileType tex,plaintex iabbrev −>> ↠
autocmd FileType tex,plaintex iabbrev <<- ↞
autocmd FileType tex,plaintex iabbrev <<− ↞
autocmd FileType tex,plaintex iabbrev -> ⟶
autocmd FileType tex,plaintex iabbrev −> ⟶
autocmd FileType tex,plaintex iabbrev <- ⟵
autocmd FileType tex,plaintex iabbrev <− ⟵
autocmd FileType tex,plaintex iabbrev <−> ⟵
autocmd FileType tex,plaintex iabbrev ⟵> ↔
autocmd FileType tex,plaintex iabbrev --> ⤍
autocmd FileType tex,plaintex iabbrev −-> ⤍
autocmd FileType tex,plaintex iabbrev −−> ⤍
autocmd FileType tex,plaintex iabbrev ⟵- ⤌
autocmd FileType tex,plaintex iabbrev l-> ↦
autocmd FileType tex,plaintex iabbrev <-l ↤
autocmd FileType tex,plaintex iabbrev l−> ↦
autocmd FileType tex,plaintex iabbrev llv ↧
autocmd FileType tex,plaintex iabbrev lla ↥
autocmd FileType tex,plaintex iabbrev lV ⭣
autocmd FileType tex,plaintex iabbrev lv ⭣
autocmd FileType tex,plaintex iabbrev lA ⭡
autocmd FileType tex,plaintex iabbrev la ⭡
autocmd FileType tex,plaintex iabbrev <> ⬨
autocmd FileType tex,plaintex iabbrev \\\ ∖
"autocmd FileType tex,plaintex iabbrev [] ∎
":lab lx ⋉
"autocmd FileType tex,plaintex iabbrev xl ⋊
autocmd FileType tex,plaintex iabbrev xoo ⊠
autocmd FileType tex,plaintex iabbrev poo ⊞

"autocmd FileType tex,plaintex iabbrev^0 <BS>⁰
"autocmd FileType tex,plaintex iabbrev^2 <BS>²
"autocmd FileType tex,plaintex iabbrev^3 <BS>³
"autocmd FileType tex,plaintex iabbrev^4 <BS>⁴
"autocmd FileType tex,plaintex iabbrev^5 <BS>⁵
"autocmd FileType tex,plaintex iabbrev^6 <BS>⁶
"autocmd FileType tex,plaintex iabbrev^7 <BS>⁷
"autocmd FileType tex,plaintex iabbrev^8 <BS>⁸
"autocmd FileType tex,plaintex iabbrev^9 <BS>⁹

"autocmd FileType tex,plaintex iabbrev_0 <BS>₀
"autocmd FileType tex,plaintex iabbrev_1 <BS>₁
"autocmd FileType tex,plaintex iabbrev_2 <BS>₂
"autocmd FileType tex,plaintex iabbrev_3 <BS>₃
"autocmd FileType tex,plaintex iabbrev_4 <BS>₄
"autocmd FileType tex,plaintex iabbrev_5 <BS>₅
"autocmd FileType tex,plaintex iabbrev_6 <BS>₆
"autocmd FileType tex,plaintex iabbrev_7 <BS>₇
"autocmd FileType tex,plaintex iabbrev_8 <BS>₈
"autocmd FileType tex,plaintex iabbrev_9 <BS>₉

autocmd FileType tex,plaintex iabbrev^+ <BS>⁺
autocmd FileType tex,plaintex iabbrev^- <BS>⁻


"autocmd FileType tex,plaintex iabbrev- −

autocmd FileType tex,plaintex iabbrev_+ <BS>₊
autocmd FileType tex,plaintex iabbrev_- <BS>₋

autocmd FileType tex,plaintex iabbrev xx ×
autocmd FileType tex,plaintex iabbrev oo ⚬
autocmd FileType tex,plaintex iabbrev ,, ␣
autocmd FileType tex,plaintex iabbrev UUU ∐
autocmd FileType tex,plaintex iabbrev ππ ϖ


autocmd FileType tex,plaintex iabbrev bA 𝔸
autocmd FileType tex,plaintex iabbrev bB 𝔹
autocmd FileType tex,plaintex iabbrev bC ℂ
autocmd FileType tex,plaintex iabbrev bD 𝔻
autocmd FileType tex,plaintex iabbrev bE 𝔼
autocmd FileType tex,plaintex iabbrev bF 𝔽
autocmd FileType tex,plaintex iabbrev bG 𝔾
autocmd FileType tex,plaintex iabbrev bH ℍ
autocmd FileType tex,plaintex iabbrev bI 𝕀
autocmd FileType tex,plaintex iabbrev bJ 𝕁
autocmd FileType tex,plaintex iabbrev bK 𝕂
autocmd FileType tex,plaintex iabbrev bL 𝕃
autocmd FileType tex,plaintex iabbrev bM 𝕄
autocmd FileType tex,plaintex iabbrev bN ℕ
autocmd FileType tex,plaintex iabbrev bO 𝕆
autocmd FileType tex,plaintex iabbrev bP ℙ
autocmd FileType tex,plaintex iabbrev bQ ℚ
autocmd FileType tex,plaintex iabbrev bR ℝ
autocmd FileType tex,plaintex iabbrev bS 𝕊
autocmd FileType tex,plaintex iabbrev bT 𝕋
autocmd FileType tex,plaintex iabbrev bU 𝕌
autocmd FileType tex,plaintex iabbrev bV 𝕍
autocmd FileType tex,plaintex iabbrev bW 𝕎
autocmd FileType tex,plaintex iabbrev bX 𝕏
autocmd FileType tex,plaintex iabbrev bY 𝕐
autocmd FileType tex,plaintex iabbrev bZ ℤ


autocmd FileType tex,plaintex iabbrev sA 𝒜
autocmd FileType tex,plaintex iabbrev sB ℬ
autocmd FileType tex,plaintex iabbrev sC 𝒞
autocmd FileType tex,plaintex iabbrev sD 𝒟
autocmd FileType tex,plaintex iabbrev sE ℰ
autocmd FileType tex,plaintex iabbrev sF ℱ
autocmd FileType tex,plaintex iabbrev sG 𝒢
autocmd FileType tex,plaintex iabbrev sH ℋ
autocmd FileType tex,plaintex iabbrev sI ℐ
autocmd FileType tex,plaintex iabbrev sJ 𝒥
autocmd FileType tex,plaintex iabbrev sK 𝒦
autocmd FileType tex,plaintex iabbrev sL ℒ
autocmd FileType tex,plaintex iabbrev sM ℳ
autocmd FileType tex,plaintex iabbrev sN 𝒩
autocmd FileType tex,plaintex iabbrev sO 𝒪
autocmd FileType tex,plaintex iabbrev sP 𝒫
autocmd FileType tex,plaintex iabbrev sQ 𝒬
autocmd FileType tex,plaintex iabbrev sR ℛ
autocmd FileType tex,plaintex iabbrev sS 𝒮
autocmd FileType tex,plaintex iabbrev sT 𝒯
autocmd FileType tex,plaintex iabbrev sU 𝒰
autocmd FileType tex,plaintex iabbrev sV 𝒱
autocmd FileType tex,plaintex iabbrev sW 𝒲
autocmd FileType tex,plaintex iabbrev sX 𝒳
autocmd FileType tex,plaintex iabbrev sY 𝒴
autocmd FileType tex,plaintex iabbrev sZ 𝒵

autocmd FileType tex,plaintex iabbrev fkA 𝕬
autocmd FileType tex,plaintex iabbrev fkB 𝕭
autocmd FileType tex,plaintex iabbrev fkC 𝕮
autocmd FileType tex,plaintex iabbrev fkD 𝕯
autocmd FileType tex,plaintex iabbrev fkE 𝕰
autocmd FileType tex,plaintex iabbrev fkF 𝕱
autocmd FileType tex,plaintex iabbrev fkG 𝕲
autocmd FileType tex,plaintex iabbrev fkH 𝕳
autocmd FileType tex,plaintex iabbrev fkI 𝕴
autocmd FileType tex,plaintex iabbrev fkJ 𝕵
autocmd FileType tex,plaintex iabbrev fkK 𝕶
autocmd FileType tex,plaintex iabbrev fkL 𝕷
autocmd FileType tex,plaintex iabbrev fkM 𝕸
autocmd FileType tex,plaintex iabbrev fkN 𝕹
autocmd FileType tex,plaintex iabbrev fkO 𝕺
autocmd FileType tex,plaintex iabbrev fkP 𝕻
autocmd FileType tex,plaintex iabbrev fkQ 𝕼
autocmd FileType tex,plaintex iabbrev fkR 𝕽
autocmd FileType tex,plaintex iabbrev fkS 𝕾
autocmd FileType tex,plaintex iabbrev fkT 𝕿
autocmd FileType tex,plaintex iabbrev fkU 𝖀
autocmd FileType tex,plaintex iabbrev fkV 𝖁
autocmd FileType tex,plaintex iabbrev fkW 𝖂
autocmd FileType tex,plaintex iabbrev fkX 𝖃
autocmd FileType tex,plaintex iabbrev fkY 𝖄
autocmd FileType tex,plaintex iabbrev fkZ 𝖅
autocmd FileType tex,plaintex iabbrev fka 𝖆
autocmd FileType tex,plaintex iabbrev fkb 𝖇
autocmd FileType tex,plaintex iabbrev fkc 𝖈
autocmd FileType tex,plaintex iabbrev fkd 𝖉
autocmd FileType tex,plaintex iabbrev fke 𝖊
autocmd FileType tex,plaintex iabbrev fkf 𝖋
autocmd FileType tex,plaintex iabbrev fkg 𝖌
autocmd FileType tex,plaintex iabbrev fkh 𝖍
autocmd FileType tex,plaintex iabbrev fki 𝖎
autocmd FileType tex,plaintex iabbrev fkj 𝖏
autocmd FileType tex,plaintex iabbrev fkk 𝖐
autocmd FileType tex,plaintex iabbrev fkl 𝖑
autocmd FileType tex,plaintex iabbrev fkm 𝖒
autocmd FileType tex,plaintex iabbrev fkn 𝖓
autocmd FileType tex,plaintex iabbrev fko 𝖔
autocmd FileType tex,plaintex iabbrev fkp 𝖕
autocmd FileType tex,plaintex iabbrev fkq 𝖖
autocmd FileType tex,plaintex iabbrev fkr 𝖗
autocmd FileType tex,plaintex iabbrev fks 𝖘
autocmd FileType tex,plaintex iabbrev fkt 𝖙
autocmd FileType tex,plaintex iabbrev fku 𝖚
autocmd FileType tex,plaintex iabbrev fkv 𝖛
autocmd FileType tex,plaintex iabbrev fkw 𝖜
autocmd FileType tex,plaintex iabbrev fkx 𝖝
autocmd FileType tex,plaintex iabbrev fky 𝖞
autocmd FileType tex,plaintex iabbrev fkz 𝖟

autocmd FileType tex,plaintex iabbrev ba 𝗮
autocmd FileType tex,plaintex iabbrev bb 𝗯
autocmd FileType tex,plaintex iabbrev bc 𝗰
autocmd FileType tex,plaintex iabbrev bd 𝗱
autocmd FileType tex,plaintex iabbrev bbe 𝗲
autocmd FileType tex,plaintex iabbrev bf 𝗳
autocmd FileType tex,plaintex iabbrev bg 𝗴
autocmd FileType tex,plaintex iabbrev bh 𝗵
autocmd FileType tex,plaintex iabbrev bi 𝗶
autocmd FileType tex,plaintex iabbrev bj 𝗷
autocmd FileType tex,plaintex iabbrev bk 𝗸
autocmd FileType tex,plaintex iabbrev bl 𝗹
autocmd FileType tex,plaintex iabbrev bm 𝗺
autocmd FileType tex,plaintex iabbrev bn 𝗻
autocmd FileType tex,plaintex iabbrev bo 𝗼
autocmd FileType tex,plaintex iabbrev bp 𝗽
autocmd FileType tex,plaintex iabbrev bq 𝗾
autocmd FileType tex,plaintex iabbrev br 𝗿
autocmd FileType tex,plaintex iabbrev bs 𝘀
autocmd FileType tex,plaintex iabbrev bt 𝘁
autocmd FileType tex,plaintex iabbrev bu 𝘂
autocmd FileType tex,plaintex iabbrev bv 𝘃
autocmd FileType tex,plaintex iabbrev bw 𝘄
autocmd FileType tex,plaintex iabbrev bx 𝘅
autocmd FileType tex,plaintex iabbrev bby 𝘆
autocmd FileType tex,plaintex iabbrev bz 𝘇

autocmd FileType tex,plaintex iabbrev cA 𝘼
autocmd FileType tex,plaintex iabbrev cB 𝘽
autocmd FileType tex,plaintex iabbrev cC 𝘾
autocmd FileType tex,plaintex iabbrev cD 𝘿
autocmd FileType tex,plaintex iabbrev cE 𝙀
autocmd FileType tex,plaintex iabbrev cF 𝙁
autocmd FileType tex,plaintex iabbrev cG 𝙂
autocmd FileType tex,plaintex iabbrev cH 𝙃
autocmd FileType tex,plaintex iabbrev cI 𝙄
autocmd FileType tex,plaintex iabbrev cJ 𝙅
autocmd FileType tex,plaintex iabbrev cK 𝙆
autocmd FileType tex,plaintex iabbrev cL 𝙇
autocmd FileType tex,plaintex iabbrev cM 𝙈
autocmd FileType tex,plaintex iabbrev cN 𝙉
autocmd FileType tex,plaintex iabbrev cO 𝙊
autocmd FileType tex,plaintex iabbrev cP 𝙋
autocmd FileType tex,plaintex iabbrev cQ 𝙌
autocmd FileType tex,plaintex iabbrev cR 𝙍
autocmd FileType tex,plaintex iabbrev cS 𝙎
autocmd FileType tex,plaintex iabbrev cT 𝙏
autocmd FileType tex,plaintex iabbrev cU 𝙐
autocmd FileType tex,plaintex iabbrev cV 𝙑
autocmd FileType tex,plaintex iabbrev cW 𝙒
autocmd FileType tex,plaintex iabbrev cX 𝙓
autocmd FileType tex,plaintex iabbrev cY 𝙔
autocmd FileType tex,plaintex iabbrev cZ 𝙕


autocmd FileType tex,plaintex iabbrev 𝗯1 𝟙
autocmd FileType tex,plaintex iabbrev bb1 𝟙
autocmd FileType tex,plaintex iabbrev 𝗯0 𝟘
autocmd FileType tex,plaintex iabbrev bb0 𝟘

set jumpoptions+=stack
:clearjumps
execute 'source ' . fnameescape(s:vimconfig_path . '/../vimconfig/worker.vim')
"let fuckyou =  fnameescape(s:vimconfig_path . '/../vimconfig/channel.py')
"echom "FUCKEYOU IS"
"echom fuckyou
call Startwork()
