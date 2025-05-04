if(len(counter)>0)
	let a=expand('%:t')
	execute "e ".counter[0]
	call remove(counter,0)
	execute position[0]
	call remove(position,0)
	call search(a)
else
	execute "e " .local_path. "/readme.md"
endif

