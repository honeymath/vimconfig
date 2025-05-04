let line=getline('.')
let linead = '0'.line

let flag = 0 " A flag to indicate if enter successfully

"Append an 0 so that there is no missing position
if flag == 0
	try
		let searchinput=split(split(linead,"\\input\{")[1],"\}")[0]
		let flag = 1
		let enter = searchinput
	catch
	endtry
endif

" The following code are designed for matching anything of the form [a](b), suggestion rewrite it using the regular expression. Prioritized matching

if flag == 0
    let matches = matchlist(linead, '\[\(.*\)\](\(.*\))')
    if len(matches) > 0
        let filetitle = matches[1]
        let enter = matches[2]
        let backfilename = repeat('../', len(split(enter, '/')) - 1) . expand('%p')
        let flag = 1
    endif
endif


" The following are secondarised match. Only when the first group can not match, match this group

if flag == 0
	try
		let filename = expand("<cfile>")
		let leftright = split(linead,filename)
                let leftpart = leftright[0]
		let rightpart = leftright[1]
		if(leftpart[len(leftpart)-1]=='"' && rightpart[0]=='"')
			if len(split(filename,"[.]"))>1
				let flag = 1
				let enter = filename
			endif
		endif
	catch
	endtry
endif
" The following method is trying to see what is the type
if flag == 1
	let soap=split(enter,"[.]")
	if(len(soap)>1)
		if(soap[len(soap)-1]=="md")
			let temp="e ".expand('%:p:h')."/".enter
			call insert(counter,expand('%:p'),0)
			call insert(position,line('.'),0)
			execute temp
			execute "silent !mkdir -p %:h"
		endif
		if(soap[len(soap)-1]=="html")
			let temp="e ".expand('%:p:h')."/".enter
			call insert(counter,expand('%:p'),0)
			call insert(position,line('.'),0)
			execute temp
			execute "silent !mkdir -p %:h"
		endif
		if(soap[len(soap)-1]=="py")
			let temp="e ".expand('%:p:h')."/".enter
			call insert(counter,expand('%:p'),0)
			call insert(position,line('.'),0)
			execute temp
			execute "silent !mkdir -p %:h"
		endif
		if(soap[len(soap)-1]=="pyc")
			let temp=expand('%:p:h')."/".strpart(enter,0,len(enter)-1)
			let next_line_content = getline(line('.') + 1) "This for commnad
			let current_line = line('.')
			let code_lines = []
			while current_line > 0
				let current_line -= 1
				let line_content = getline(current_line)
				if line_content->trim() == ''
				    break
				endif
				let line_content = substitute(line_content, "'", '''\\''''', 'g')
				call add(code_lines, line_content)
		        endwhile
"			echo temp
			let params = join(code_lines, "' '")
			let code = "python3 -W ignore ".temp." '".params."'"
"			echo code
"			execute code
			try
				let result = system(code)
				if v:shell_error == 0
					let @" = result
					echo "Script executed successfully"
					if next_line_content =~ '^/'
						let search_string = matchstr(next_line_content, '^/\zs.*')
			"			let saved_pos = getpos('.') "save mouse
						"let lnum = line('.')
						"let col = col('.')
						execute 'normal! j$'
			"			let second_pos = getpos('.') "save mouse
						execute 'silent! normal! /' . search_string . "\n"
			"			if getpos('.') ==# second_pos
			"				call setpos('.', saved_pos)
			"			endif
					"	if v:searchhit == 0
							"call setpos('.', saved_pos)
						"	call cursor(lnum, col)
					"	endif
				    endif
				else
					echo result
					echo "Script execution failed with error code: " . v:shell_error
				endif
			catch
				echo "An error occurred: " . v:errmsg
			endtry
		endif
		if(soap[len(soap)-1]=="json")
			let temp="e ".expand('%:p:h')."/".enter
			call insert(counter,expand('%:p'),0)
			call insert(position,line('.'),0)
			execute temp
			execute "silent !mkdir -p %:h"
		endif
		if(soap[len(soap)-1]=="yml")
			let temp="e ".expand('%:p:h')."/".enter
			call insert(counter,expand('%:p'),0)
			call insert(position,line('.'),0)
			execute temp
			execute "silent !mkdir -p %:h"
		endif
		if(soap[len(soap)-1]=="scpt")
			let temp="e ".expand('%:p:h')."/".enter
			call insert(counter,expand('%:p'),0)
			call insert(position,line('.'),0)
			execute temp
			execute "silent !mkdir -p %:h"
		endif
		if(soap[len(soap)-1]=="ovpn")
			let temp="e ".expand('%:p:h')."/".enter
			call insert(counter,expand('%:p'),0)
			call insert(position,line('.'),0)
			execute temp
			execute "silent !mkdir -p %:h"
		endif
		if(soap[len(soap)-1]=="pages")
			let temp = expand('%:p:h')."/".enter
			let modifyspace = substitute(temp," ","\ ","g")
			execute "silent !(open ".modifyspace.")"
		endif
		if(soap[len(soap)-1]=="sh")
			let temp="e ".expand('%:p:h')."/".enter
			call insert(counter,expand('%:p'),0)
			call insert(position,line('.'),0)
			execute temp
			execute "silent !mkdir -p %:h"
		endif
		if(soap[len(soap)-1]=="php")
			let temp="e ".expand('%:p:h')."/".enter
			call insert(counter,expand('%:p'),0)
			call insert(position,line('.'),0)
			execute temp
			execute "silent !mkdir -p %:h"
		endif
		if(soap[len(soap)-1]=="css")
			let temp="e ".expand('%:p:h')."/".enter
			call insert(counter,expand('%:p'),0)
			call insert(position,line('.'),0)
			execute temp
			execute "silent !mkdir -p %:h"
		endif
		if(soap[len(soap)-1]=="gitignore")
			let temp="e ".expand('%:p:h')."/".enter
			call insert(counter,expand('%:p'),0)
			call insert(position,line('.'),0)
			execute temp
			execute "silent !mkdir -p %:h"
		endif
		if(soap[len(soap)-1]=="yaml")
			let temp="e ".expand('%:p:h')."/".enter
			call insert(counter,expand('%:p'),0)
			call insert(position,line('.'),0)
			execute temp
			execute "silent !mkdir -p %:h"
		endif
		if(soap[len(soap)-1]=="ts")
			let temp="e ".expand('%:p:h')."/".enter
			call insert(counter,expand('%:p'),0)
			call insert(position,line('.'),0)
			execute temp
			execute "silent !mkdir -p %:h"
		endif
		if(soap[len(soap)-1]=="bash_profile")
			let temp="e ".expand('%:p:h')."/".enter
			call insert(counter,expand('%:p'),0)
			call insert(position,line('.'),0)
			execute temp
			execute "silent !mkdir -p %:h"
		endif
		if(soap[len(soap)-1]=="sty")
			let temp="e ".expand('%:p:h')."/".enter
			call insert(counter,expand('%:p'),0)
			call insert(position,line('.'),0)
			execute temp
			execute "silent !mkdir -p %:h"
		endif
		if(soap[len(soap)-1]=="txt")
			let temp="e ".expand('%:p:h')."/".enter
			call insert(counter,expand('%:p'),0)
			call insert(position,line('.'),0)
			execute temp
			execute "silent !mkdir -p %:h"
		endif
		if(soap[len(soap)-1]=="csv")
			let temp="e ".expand('%:p:h')."/".enter
			call insert(counter,expand('%:p'),0)
			call insert(position,line('.'),0)
			execute temp
			execute "silent !mkdir -p %:h"
		endif
		if(soap[len(soap)-1]=="c")
			let temp="e ".expand('%:p:h')."/".enter
			call insert(counter,expand('%:p'),0)
			call insert(position,line('.'),0)
			execute temp
			execute "silent !mkdir -p %:h"
		endif
		if(soap[len(soap)-1]=="js")
			let temp="e ".expand('%:p:h')."/".enter
			call insert(counter,expand('%:p'),0)
			call insert(position,line('.'),0)
			execute temp
			execute "silent !mkdir -p %:h"
		endif
		if(soap[len(soap)-1]=="q-2")
			let temp="e ".expand('%:p:h')."/".enter
			call insert(counter,expand('%:p'),0)
			call insert(position,line('.'),0)
			execute temp
			execute "silent !mkdir -p %:h"
		endif
		if(soap[len(soap)-1]=="webp")
			let temp = expand('%:p:h')."/".enter
			let modifyspace = substitute(temp," ","\ ","g")
			execute "silent !(open ".modifyspace.")"
		endif
		if(soap[len(soap)-1]=="pdf")
			let temp = expand('%:p:h')."/".enter
			let modifyspace = substitute(temp," ","\ ","g")
			"echo modifyspace
			execute "silent !(open ".modifyspace.")"
		endif
		if(soap[len(soap)-1]=="png")
			let temp = expand('%:p:h')."/".enter
			let modifyspace = substitute(temp," ","\ ","g")
			execute "silent !(open ".modifyspace.")"
		endif
		if(soap[len(soap)-1]=="jpeg")
			let temp = expand('%:p:h')."/".enter
			let modifyspace = substitute(temp," ","\ ","g")
			execute "silent !(open ".modifyspace.")"
		endif
		if(soap[len(soap)-1]=="jpg")
			let temp = expand('%:p:h')."/".enter
			let modifyspace = substitute(temp," ","\ ","g")
			execute "silent !(open ".modifyspace.")"
		endif
		if(soap[len(soap)-1]=="tex")
			let temp="e ".expand('%:p:h')."/".enter
			call insert(counter,expand('%:p'),0)
			call insert(position,line('.'),0)
			execute temp
			execute "silent !mkdir -p %:h"
			execute "setf tex"
		endif
	else "the following is fuck out no meaning, can delete
        if expand('%:e') == 'tex'
    		let temp="e ".expand('%:p:h')."/".enter.".tex"
        else
    		let temp="e ".expand('%:p:h')."/".enter 
        endif
".".tex"
		call insert(counter,expand('%:p'),0)
		call insert(position,line('.'),0)
		execute temp
		execute "silent !mkdir -p %:h"
"		execute "setf tex"
	endif
"elseif getline('.') =~ '.*[^>]>>[^>].*'
elseif getline('.') =~ '.*[^>]>>\(>\)\{0,1\}[^>].*'
	let code = "python3 -W ignore ~/Dropbox/Latex/Data/fetch.py ". shellescape(getline('.'))
	let regname = system("python3 -W ignore ~/Dropbox/Latex/Data/fetch_output_filename.py ". shellescape(getline('.')))
	let outsymbol = system("python3 -W ignore ~/Dropbox/Latex/Data/fetch_output_symbol.py ". shellescape(getline('.')))
	"echo outsymbol
	let regoodname = substitute(regname[1:], '\n', '', 'g')
	let outgood = substitute(outsymbol, '\n', '', 'g')
	try
		let result = system(code)
		if v:shell_error == 0
			if regname[0]==":"
"					echo outgood==">>"
				if outgood == ">>"
"					echo "let @".regoodname."= result"
					execute "let @".regoodname."= result"
				elseif outgood == ">>>"
					execute "let @".regoodname."= @".regoodname.".result"
				endif
"			elseif outsymbol == ">>>"
"				let @" = @".result
			else
				let @" = result
			endif
			echo "Script executed successfully"
		else
			echo result
			echo "Script execution failed with error code: " . v:shell_error
		endif
	catch
		echo "An error occurred: " . v:errmsg
	endtry
"	execute '!python3 ~/Dropbox/Latex/Data/fetch.py ' . shellescape(getline('.'))
elseif getline('.') =~# 'https\?:\/\/'
	execute 'silent !(open -a "Google Chrome" '.getline('.').')'
elseif getline('.') =~# '\<\S\+@\S\+\>'
        let email = matchstr(getline('.'), '<\zs\S\+@\S\+\ze>')
        let formattedEmail = '\%3C'.email.'\%3E'
	echo email
        execute 'silent !open "message:'.formattedEmail.'"'
elseif line[0]=='\'
	let temp=split(line,"oa")
	if(len(temp)>1)
		let temp=temp[1]
		let temp=split(temp,"{")
		if(temp[0]=="d")
			let temp=temp[1]
			let temp=split(temp,"}")
			let temp=temp[0]
			let soap=split(temp,"[.]")
			if(len(soap)>1)
				let temp="e ".expand('%:p:h')."/".temp
				call insert(counter,expand('%:p'),0)
				call insert(position,line('.'),0)
				execute temp
			else
				let temp="e ".expand('%:p:h')."/".temp.".tex"
				call insert(counter,expand('%:p'),0)
				call insert(position,line('.'),0)
				execute temp
				execute "setf tex"
			endif
		endif
		if(temp[0]=="dModule"||temp[0]=="dTemplate")
			let temp=temp[1]
			let temp=split(temp,"}")
			let temp=temp[0]
			let temp="e ".expand('%:p:h')."/".temp."/script.tex"
			call insert(counter,expand('%:p'),0)
			call insert(position,line('.'),0)
			execute temp
		endif
	endif
elseif line[0]=='T'
	let temp=split(line,":")
	if(temp[0]=="Template")
		if(len(temp)>1)
			let temp=temp[1]
			let temp="e ".expand('%:p:h')."/".temp."/script.tex"
			call insert(counter,expand('%:p'),0)
			call insert(position,line('.'),0)
			execute temp
		endif
	endif
elseif line[0]=='P'
		let temp=split(line,":")
	if(temp[0]=="Paper")
		if(len(temp)>1)
			let temp=temp[1]
			let temp="e ".expand('%:p:h')."/".temp."/ContentList.tex"
			call insert(counter,expand('%:p'),0)
			call insert(position,line('.'),0)
			execute temp
			let line=getline('1')
			if(line[1]!='R')
				call append(line('1'),['\Road{Introduction}','\Road{Abstract}','\Road{Acknowledgement}','\Road{Command/script}','\Road{etc}'])
				execute "!mkdir -p %:h"
				execute "w"
				execute "e ".expand('%:p:h')."/Introduction.tex"
				execute "w"
				execute "e ".expand('%:p:h')."/Abstract.tex"
				execute "w"
				execute "e ".expand('%:p:h')."/Acknowledgement.tex"
				execute "w"
				execute "e ".expand('%:p:h')."/Command/script.tex"
				execute "!mkdir -p %:h"
				execute "w"
				execute temp
			endif
		endif
	endif
elseif line('.')==1 && getline('.')==""
	call append(1,"[返回](".backfilename.")")
	call setline(1,"# ".filetitle)
else
    "echo 'not able to enter'
    let line = getline('.')
let numbers = map(split(line, '#'), 'v:val =~ "^\\d\\+$" ? str2nr(v:val) : -1')
    let numbers = filter(numbers, 'v:val >= 0') " Filter out non-numeric values
    let intersection = filter(copy(numbers), 'index(g:highlightArray1, v:val) != -1')
    if len(intersection) > 0
        let g:highlightArray1 = filter(g:highlightArray1, 'index(intersection, v:val) == -1')
    else
        let g:highlightArray1 += filter(numbers, 'index(g:highlightArray1, v:val) == -1')
    endif

    call ApplyHighlights()
endif
