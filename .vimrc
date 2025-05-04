

" 显示 Copilot 提示的快捷键

" 创建接受当前单词建议的自定义命令
"function! AcceptWord()
    " 模拟按键以接受当前单词建议
"    let l:original_text = getline('.')
"    let l:cursor_position = col('.')
 "   call copilot#Accept("")
  "  let l:new_text = getline('.')
   " let l:new_word = matchstr(l:new_text, '\k\+')
"    call setline('.', l:original_text[:l:cursor_position-2] . l:new_word . l:original_text[l:cursor_position-1:])
 "   call cursor(0, l:cursor_position + len(l:new_word))
"endfunction

"command! CopilotAcceptWord call AcceptWord()

"inoremap <silent> <C-L> <C-O>:call AcceptWord()<CR>

"imap <silent><script><expr> <C-L> AcceptWord()


"command! CopilotAcceptWord call AcceptWord()
"imap <silent><script><expr> <C-L> copilot#Accept("")

"imap <silent><script> <C-L> :call AcceptWord()<CR>


"imap <silent><script><expr> <C-L> copilot#Accept("<C-J>")

" 配置 Copilot 的建议触发键绑定
"let g:copilot_no_tab_map = v:true

" 接受整个句子的快捷键
"imap <silent><script><expr> <Tab> copilot#Accept("\<Tab>")

" 逐词接受建议的快捷键
" Map Ctrl+L to accept the next word of the suggestion
"imap <silent><script><expr> <C-l> copilot#Accept("\<Plug>(copilot-accept-word)")

" Map Ctrl+J to accept the next line of the suggestion
"imap <silent><script><expr> <C-j> copilot#Accept("\<Plug>(copilot-accept-line)")

" Function to accept one word from Copilot suggestion
function! SuggestOneWord()
  let suggestion = copilot#Accept("")
  let bar = copilot#TextQueuedForInsertion()
  return strlen(bar) > 0 ? matchstr(bar, '^\s*\S\+') : ""
endfunction

inoremap <expr> <C-l> SuggestOneWord()


"imap <silent><script><expr> <C-J> copilot#Next()
"imap <silent><script><expr> <C-K> copilot#Previous()
"imap <silent><script><expr> <C-H> copilot#Dismiss()


"syntax on
"set t_Co=256

set maxmempattern=2000


if (has("termguicolors"))
  set termguicolors
endif

"colorscheme molokai
" 切换光标形状
if has("nvim") || has("patch-8.0.0722")
  " 插入模式下光标形状为竖线
  let &t_SI = "\e[5 q"
  " 替换模式下光标形状为竖线
  let &t_SR = "\e[5 q"
  " 离开插入模式下光标形状为块状
  let &t_EI = "\e[1 q"
endif

"Vundle Settings


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
let g:mkdp_markdown_css='/Users/qiruili/Dropbox/Latex/markdown.css'
let g:mkdp_highlight_css='/Users/qiruili/Dropbox/Latex/highlight.css'
let g:mkdp_theme = 'light'

colorscheme torte
set transparency=20
set guifont=Courier_new:h16
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
:let g:highlightArray1 = [] " This is the highlight sss.
:let g:highlightArray2 = [] " This is the highlight sss.
:let g:highlightArray3 = [] " This is the highlight sss.
:map <Backspace> X
":map ≥ :!(cd ~/Dropbox/Latex && latex -shell-escape main && bibtex main && latex -shell-escape main && makeindex -s nomencl.ist -t "main.nlg" -o "main.nls" "main.nlo"&& pdflatex -shell-escape main && open -a '/Applications/Skim.app' main.pdf)<CR><CR>
":map ≥ <Plug>MarkdownPreview
":map ≤ :!(cd ~/Dropbox/Latex && pdflatex -shell-escape main && open -a '/Applications/Skim.app' main.pdf)<CR><CR>
":map ≤ :!(pdflatex -shell-escape main && open -a '/Applications/Skim.app' main.pdf && cp main.pdf ~/Desktop)<CR><CR>
autocmd BufRead,BufNewFile *.md set filetype=markdown
autocmd BufRead,BufNewFile *.tex set filetype=tex

autocmd BufRead,BufNewFile ~/Dropbox/Latex/fuck/readme.md source ~/Dropbox/Latex/date.vim
autocmd FileType tex nnoremap ≤ :!(pdflatex --shell-escape main && open -a '/Applications/Skim.app' main.pdf && cp main.pdf ~/Desktop)<CR><CR>
autocmd FileType python map ≤ :!python3 %<CR>
autocmd FileType markdown map ≤ <Plug>MarkdownPreview
au BufRead,BufNewFile *.json setlocal foldmethod=indent





:map ≠ :let line=getline('.')<CR>:if line[0]=='%'<CR>:call insert(counter,expand('%:p'),0)<CR>:execute "e ".strpart(line,1).".tex"<CR>:elseif line[0]=='+'<CR>:call insert(counter,expand('%:p'),0)<CR>:execute "e ~/Desktop/_/Website/".strpart(line,1)<CR>:else<CR>:let temp=split(line,'<r>\\|<\/r>',1)<CR>:if len(temp)==3<CR>:let shazi=temp[1]<CR>:let fengzi=split(shazi,'#',1)<CR>:call insert(counter,expand('%:p'),0)<CR>:execute "e ~/Desktop/_/Website/".fengzi[0]<CR>:if(len(fengzi)>1)<CR>:call search(fengzi[1])<CR>:endif<CR>:else<CR>:let temp=split(line,'href=\"',1)<CR>:if len(temp)>1<CR>:let shazi=split(temp[1],'\"')[0]<CR>:call insert(counter,expand('%:p'),0)<CR>:execute "e ~/Desktop/_/Website/".shazi<CR>:else<CR>:let temp=split(line,'src=\"',1)<CR>:if len(temp)>1<CR>:let shazi=split(temp[1],'\"')[0]<CR>:if(len(split(shazi,'js',1))>0)<CR>:call insert(counter,expand('%:p'),0)<CR>:execute "e ~/Desktop/_/Website/".shazi<CR>:endif<CR>:endif<CR>:endif<CR>:endif<CR>:endif<CR><CR>

":map « :if(len(counter)>0)<CR>:let a=expand('%:t')<CR>:execute "e ".counter[0]<CR>:call remove(counter,0)<CR>:execute position[0]<CR>:call remove(position,0)<CR>:call search(a)<CR>:else<CR>:e ~/Dropbox/Latex/readme.md<CR>:endif<CR><CR>

:map « :source ~/Dropbox/Latex/escape.vim<CR>
:map \ :source ~/Dropbox/Latex/main.vim<CR>
:map ‘ :source ~/Dropbox/Latex/highlight.vim<CR>
":map \ :source ~/Dropbox/Latex/enter.vim<CR>




:map <D-Bslash> /src=\\|href=\\|<r><CR>

" The command for duplicate a tab
:map æ :let a=line(".")<CR>:tabe %<CR>:execute a<CR>
:map ç :let @"=expand('%:p')<CR>



:map ˙ :tabp<CR>
:map ¬ :tabn<CR>
:map Ω :execute "!(cd %:p:h && open ".expand('%:p:h').")"<CR><CR>
":map ≈ :execute "!(/usr/bin/open -a '/Applications/Google Chrome.app' '".expand('%:p')."')"<CR><CR>
":map ≈ :execute "!(/usr/bin/open -a Terminal)"<CR><CR>
":map ≈ :execute "!osascript -e 'tell app \"Terminal\" to do script \"cd " . expand('%:p:h') . " && clear\"'"<CR>
:map ≈ :execute "!osascript -e 'tell app \"Terminal\" to activate' -e 'tell app \"Terminal\" to do script \"cd " . expand('%:p:h') . " && clear\"'"<CR><CR>
:map ∑ :.s/^-\(\s*\)/\\item\1<CR>
":map ≈ :execute "!(/usr/bin/open -a '/Applications/Google Chrome.app' 'http://127.0.0.1:8000')"<CR><CR>
:map ª :execute "!(/usr/bin/open -a '/Applications/Google Chrome.app' '@@/index.html')"<CR><CR>
:map å :cd %:p:h<CR>
:map • :e @@/API.js<CR>
:map œ :source ~/Dropbox/Latex/change.vim<CR>
":map œ :source ~/Dropbox/Latex/readme.md<CR>
:map ¢ :source test.vim<CR>
":map ¡ :e change.vim<CR>
:map ¡ :e ~/Dropbox/Latex/readme.md<CR>
":map £ :e test.vim<CR>
":map £ :e ~/Dropbox/Latex/Jobs/prof.md<CR>
":map £ :e ~/Dropbox/Latex/Jobs/gen/main.tex<CR>
":map £ :e ~/Dropbox/Latex/gl4/main.tex<CR>
:map £ :e ~/Dropbox/Latex/mathAI.md<CR>
":map ¢ :e ~/Dropbox/Latex/Jobs/postdoc.md<CR>
:map ¢ :e ~/Dropbox/Latex/Korean/learn.md<CR>
":map ∑ :!mkdir -p %:h<CR>:w<CR>
:map ∞ :e ~/Dropbox/website/honeymath.github.io/README.md<CR>
:map § :e ~/Dropbox/Latex/Berkeley/README.md<CR>
:map ¶ :execute "e ~/Dropbox/Latex/schedule/".strftime('%Y%m%d').".md"<CR>:let backfilename="main.md"<CR>:let filetitle = "Schedule of ".strftime('%B %e')<CR><CR>
:map • :e ~/Dropbox/Latex/list.md<CR>


":map ÷ :execute "!(rm ~/Dropbox/Latex/main.aux)"<CR>:execute "!(rm ~/Dropbox/Latex/main.toc)"<CR>:execute "!(rm ~/Dropbox/Latex/main.bbl)"<CR>
:map ÷ :execute "!(rm main.aux)"<CR>:execute "!(rm main.toc)"<CR>:execute "!(rm main.bbl)"<CR>
:map … /\\a\(\\\\|{\)<CR>
":map º :cd @/MAT<CR>

"Open Snippers
":map ™ : e ~/.vim/UltiSnips/tex.snippets<CR>
:map ™ : e ~/Dropbox/Latex/markdown/Diary.md<CR>Gzz
" Following is to sycronise github to my server
":map µ :!(ssh -i ~/.ssh/Essential liqirui@qirui.li "cd public_html/3m.run/3M && git pull")
:map µ :!(scp -i ~/.ssh/authorized_keys/id_rsa ~/Dropbox/Latex/game/index.html liqirui@qirui.li:~/public_html/qirui.li/games.html)<CR>
:map ¥ yf$
:map Á F$yf$
:map ƒ f$
:map ∫ F$
:map † lyt$h
:map ˇ F$lyt$h
:map ∂ :.s/<!--//g<CR> :.s/-->//g<CR>
:map ß 0i<!--<esc>A--><esc>
":map ƒ /<!--<CR>∂


"" The CD key maps
nnoremap <D-r> <C-r>
inoremap <D-r> <C-r>
vnoremap <D-r> <C-r>


inoremap <C-Z> <C-]>


:command W w
":iab --> \longrightarrow
":iab \|-> \longmapsto
":iab ;; \mathbb
":iab '' \mathscr
":iab $'' $\mathscr
":iab $;; $\mathbb
":iab :: \mathcal
":iab $:: $\mathcal
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

:iab [=] 🏷

" :iab ddd ∎definition∎🏷{}∎<ESC>i<CR><ESC>O<backspace>
" :iab ppp ∎proposition∎🏷{}∎<ESC>i<CR><ESC>O<backspace>
":iab ttt ∎theorem∎🏷{}∎<ESC>i<CR><ESC>O<backspace>
":iab lll ∎lemma∎🏷{}∎<ESC>i<CR><ESC>O<backspace>
":iab rrr ∎remark∎🏷{}∎<ESC>i<CR><ESC>O<backspace>
":iab ccc ∎conjecture∎🏷{}∎<ESC>i<CR><ESC>O<backspace>
":iab ooo ∎corollary∎🏷{}∎<ESC>i<CR><ESC>O<backspace>
":iab fff ∎proof∎∎<ESC>i<CR><ESC>O<backspace>
":iab eee ∎equation∎🏷{}∎<ESC>i<CR><ESC>O<backspace>
":iab eeee ∎equation*∎∎<ESC>i<CR><ESC>O<backspace>
":iab iii ∎itemize∎∎<ESC>i<CR><ESC>O<backspace>
":iab iiii ∎enumerate∎∎<ESC>i<CR><ESC>O<backspace>
":iab aaaa ∎cases∎∎<ESC>i<CR><ESC>O<backspace>

:iab ddd \begin{definition}\label{} <ESC>o\end{definition}<ESC>O<backspace>
:iab ppp \begin{proposition}\label{} <ESC>o\end{proposition}<ESC>O<backspace>
:iab ttt \begin{theorem}\label{} <ESC>o\end{theorem}<ESC>O<backspace>
:iab lll \begin{lemma}\label{} <ESC>o\end{lemma}<ESC>O<backspace>
:iab rrr \begin{remark}\label{} <ESC>o\end{remark}<ESC>O<backspace>
:iab ccc \begin{conjecture}\label{} <ESC>o\end{conjecture}<ESC>O<backspace>
:iab ooo \begin{corollary}\label{} <ESC>o\end{corollary}<ESC>O<backspace>
:iab fff \begin{proof} <ESC>o\end{proof}<ESC>O<backspace>
:iab eee \begin{equation}\label{} <ESC>o\end{equation}<ESC>O<backspace>
:iab eeee \begin{equation*} <ESC>o\end{equation*}<ESC>O<backspace>
:iab iii \begin{itemize} <ESC>o\end{itemize}<ESC>O<backspace>
:iab iiii \begin{enumerate} <ESC>o\end{enumerate}<ESC>O<backspace>
:iab aaaa \begin{cases} <ESC>o\end{cases}<ESC>O<backspace>

" The following command, is used to make sure tapstraps

":inoremap eiei <Esc>

:nnoremap gf :source ~/Dropbox/Latex/main.vim<CR>
:nnoremap gl :source ~/Dropbox/Latex/escape.vim<CR>
:nnoremap ga :e ~/Dropbox/Latex/readme.md<CR>

set iskeyword=@,192-255

"autocmd BufEnter * if expand('%:p') == 'Users/qiruili/.vimrc'|echo 'it is vimrc file'|endif
autocmd BufEnter main.tex,ReadMe.md,*.py,*.txt execute('cd '.expand('%:p:h')) | call LoadHighlights()
"    autocmd BufEnter * call LoadHighlights()


"After write up a buffer, run git command

au BufWritePost ~/Dropbox/Latex/* silent !(git add %:p)
au BufWritePost ~/Dropbox/Latex/* call SaveHighlights()
au BufWritePost ~/Dropbox/website/* silent !(git add %:p)
au BufWritePost ~/project/* silent !(git add %:p)

" Python settings
au BufNewFile,BufRead *.py set expandtab
au BufNewFile,BufRead *.py set shiftwidth=4
au BufNewFile,BufRead *.py set softtabstop=4
au BufNewFile,BufRead *.py set tabstop=4



function! LoadHighlights()
    let fname1 = expand('%:p:h') . '/.highlight'
    let fname2 = expand('%:p:h') . '/.highlight2'
    let fname3 = expand('%:p:h') . '/.highlight3'
    
    if filereadable(fname1)
        let lines = readfile(fname1)
        let g:highlightArray1 = map(lines, 'str2nr(v:val)')
    else
        let g:highlightArray1 = []
    endif

    if filereadable(fname2)
        let lines = readfile(fname2)
        let g:highlightArray2 = map(lines, 'str2nr(v:val)')
    else
        let g:highlightArray2 = []
    endif

    if filereadable(fname3)
        let lines = readfile(fname3)
        let g:highlightArray3 = map(lines, 'str2nr(v:val)')
    else
        let g:highlightArray3 = []
    endif

    call ApplyHighlights()
endfunction




function! ApplyHighlights()
    call clearmatches()
    for num in g:highlightArray1
       let pattern = '\(^\|\D\)\zs' . num . '#\ze'
        call matchadd('Search', pattern)
    endfor
    for num in g:highlightArray2
       let pattern = '\(^\|\D\)\zs' . num . '#\ze'
        call matchadd('CursorLineNr', pattern)
    endfor
    for num in g:highlightArray3
        call matchadd('StatusLine', '\V'.escape(num.'#', '\'))
    endfor
endfunction

function! SaveHighlights()
"    let fname1 = expand('%:p:h') . '/.highlight'
"    let fname2 = expand('%:p:h') . '/.highlight2'
"    let fname3 = expand('%:p:h') . '/.highlight3'
    
"    call writefile(map(copy(g:highlightArray1), 'string(v:val)'), fname1)
"    call writefile(map(copy(g:highlightArray2), 'string(v:val)'), fname2)
"    call writefile(map(copy(g:highlightArray3), 'string(v:val)'), fname3)
endfunction

" Auto commands to load and save highlights when entering and leaving a buffer
"augroup Highlight
"    autocmd!
"    autocmd WinEnter * call LoadHighlights()
"    autocmd BufLeave,WinLeave * call SaveHighlights()
"augroup END




:map ` :highlight Normal ctermfg=white guifg=white <CR>:highlight folded ctermfg=yellow ctermbg=black guifg=yellow guibg=black<CR>:source ~/Dropbox/Latex/fold.md<CR>zr


":highlight Normal guifg=white<CR>

autocmd VimEnter * highlight Normal guifg=white

" The following are just for my test
" Function to call GPT and get a suggestion
" Function to call GPT and get a suggestion
" Function to simulate showing suggestions in MacVim
" Function to simulate showing suggestions in MacVim

let g:last_call_time = 0  " Global variable to store last function call time
let g:time_limit = 10    " Time limit in milliseconds (e.g., 1000 ms = 1 second)

function! GetGPTSuggestion()
  " Get the current time in milliseconds
  let current_time = reltimefloat(reltime())

  " Check if enough time has passed since the last call
  if current_time - g:last_call_time < g:time_limit
    echom "Function called too soon. Try again later."
    return
  endif
  " Update the last call time
  let g:last_call_time = current_time
  echo "RINIMA!!!"
  " Get the selected text (visual mode)
  "let selected_text = escape(@", '\')
  let start_line = line("'<")  " Start of Visual selection
  let end_line = line("'>")    " End of Visual selection

  " Extract the selected text directly from the buffer
  let selected_text = join(getline(start_line, end_line), "\n")
  " Call GPT (simulated response for now)
  let gpt_response = 'Suggested replacement: virtual text for '.selected_text
  botright new
  " Open a temporary new window at the bottom of the screen
  setlocal buftype=nofile
  setlocal bufhidden=wipe
  put =gpt_response
  "call timer_start(3000, 'ClosePopupWindow')
  "echo selected_text
endfunction

" Function to close the pop-up window after delay
function! ClosePopupWindow(arg)
  " Print the argument passed to the function
  echom "Argument received: " . string(a:arg)
  " Print the specific value of the passed argumentendfunctio
" Map this function to a key (e.g., ®r) in Visual Mode
  quit
endfunction

" Map this function to a key (e.g., <Leader>r) in Visual Mode
map ® :call GetGPTSuggestion()<CR>

