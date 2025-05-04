# 快捷通道o

[Recommendation Letter Status](fuck/flask_control/Events/Lawyer/lawyer_drafted_recommendation_letters/readme.md)
%% Need to update with the lawyer of the current status.


What I wanna fucking do today:

fix. Try to look at vimrc, and see why it contains following 4 lines but not work out?

" Python settings
au BufNewFile,BufRead *.py set expandtab
au BufNewFile,BufRead *.py set shiftwidth=4
au BufNewFile,BufRead *.py set softtabstop=4
au BufNewFile,BufRead *.py set tabstop=4





[](test.py)

0. Use github LLMOS version instead of Dropbox version to start
	- redesign where the repository should go. System and other apps should be the same level. Suggest ~/repositories/
	- For stability, currently LLMOS is used on the current folder, the access of other software and repository should try always ../name??


1. Repair the change by line tool. give response: the changes is under your review and has not submitted yet， the content is located at filename.ext.temp file, 
	- add line number for the showing line tool. 使用awk
	- add the submit_changes tool.  submit changes target filepath. so going to see if filename.ext.temp exists, if exist, submit it.
	- new feature: When saving a file, cd that path and run the git add command on that path. or universally add?
	- upon changes, run diff +U to show the difference and upper and lower 10 lines of context.

2. Make git clone a tool. and when clone give comment, ask it to clone the tools to better manipulate with things and tell how to 

	- make clean repo tool, it just delete a repo into trash. but have to be careful, double check the path is repo.

3. Add the log function, create a python logs and store it in there.

4. Update the investigation tool in email, finally print python logs for GPT to understand the situation better.


Now retest mama and make sure everything works, then we can start math projects.

math projects structure

Main goal for assistant help, transfer my draft to a tex file, and try understand it.

assistant/   ## this stores the resources that need by the LLM helper
assistant/README.md  ## explain something special for the project, for example, the unicode table.
assistant/templates  ## this is certain examples for LLM to study, better explaining what we want
assistant/contents  ## this is the assistant generated content, but not yet admitted by user. it should also can be a pieces, like what cursor does. Is that esay to do what cursor did? 
assistant/instructions ## this contains some instructions for LLM to understand the project, and understand what he should do. also what the special thing is ahaha.  Including what the styles should be , and corresponding examples in templates.
assistant/logs
assistant/config.yaml
assistant/output/
assistant/output/symbols.md
assistant/scripts/  ## stores the helpful python scripts that can help assistant to do something. There is some code to verify the submitted codes.   ## also a script of puting templates into instructions as a whole file (like substitute wheere there is an expression for so)

main.tex  ## this is the main tex file.
packages/ ## this is the package folder.
commands/ ## this is the commands folder.
references/ ## this is the references folder.
contents/  ## this is the content of tex file. 
contents/drafts/ ## this is the drafts of certain latex file.

	contents/chapter1.tex  ## for example, this is the chapter one of the whole project

In math projects, add the instructions for GPT to polish the tex file. the name of polished tex file should follow the 


5. The first task is to let assistant able to generate the math symbol table, or try to write a python code to get the definition of each notation, including the position at the line number, and the version. and the context.  

6. Then the very next is to try to write in markdown as notes and let us see if it works out as a latex file. 


7. Do some math, define Shtukas as a some OD module with some legs or whatever. 





> [数学AI互动写作](mathAI.md)


update with Amy about my Canada status


Consult with the Uri bank about the gold investiment.




paper to read:

https://math.mit.edu/~zyun/FLJR_published.pdf?utm_source=chatgpt.com


> [](fuck/flask_control/readme.md)
> [](fuck/flask_control/tips/readme.md)
> [](fuck/flask_control/softtools/chat_ollama.py)
> [](fuck/flask_control/softtools/readme.md)
> [](fuck/flask_control/output/screenshot.png)
> [](fuck/flask_control/output/drag_demo.png)
> [](fuck/tray/readme.md)

> [](fuck/flask_control/softtools/tray.py)

> [](fuck/flask_control/softtools/tray/installer.py)

The logic for testing. 

> [数学AI互动写作](mathAI.md)
[](gl4/67404ea6346e04ae423a1482/readme.md)
[](gl4/67404ea6346e04ae423a1482/main.tex)
> [Dimensions of components in Affine Springer Fibers with general Hecke functions -- Jacquet-Fregberg case](gl4/dimension/main.tex)


[](personote/testcontrol/readme.md)
C: Orbit: qqzipcar@gmail.com
D: Ring: honeyworkflow@gmail.com
E: Cyclic: qiruili09@gmail.com
F: Spin: superhoneyroom@gmail.com    
G: Loop: qq@qirui.li  
H: Period: thisroomissonice@gmail.com
J: Torus: qirui.math@gmail.com
K: Donut :superhoneymath@gmail.com     
[](personote/tescontrol/change-account.yaml)
[](personote/testcontrol/control.yaml)
[](personote/testcontrol/command.txt)
[](temporary.md)

view_video.php?viewkey=6515d23f789bd

[](personote/autocontrol/readme.md)
[](personote/autocontrol/log.yaml)

%% Remaining tasks继续跟进报税 fuck 给 Daniel 写信， 给rappoport写信， so many rubbish tasks. 

Fangxing zhu: Introductino to geometric satake.
https://math.uchicago.edu/~may/REU2022/REUPapers/Fang,Xingzhu.pdf

quasi-canonical paper
paper with wei zhang
paper with zhiyu
lawyer letter
https://www.kiwi.com/cn/manage/613810175/

>- [Algebra](teaching/algebra/readme.md)
[Slides](Slides/main.tex)
> [twusted](twisted/main.tex)    The project with Wei Zhang
[Quasicanonical and fundamental lemma](qcfl/readme.md)
[Linear AFL and differential operator](differential/readme.md)

## Games
[Some Game Note](personote/readme.md)

### Currently working on
> [](funding.md)
> [](funding/2025v1Postech/main.tex)
> [](funding/2025v1Postech/readme.md)
> [Slides of my talk](slides/main.tex)

Materials:

> [](funding/homework.pdf)
[](fuck/CV/CV.md)
[Competence of the resercher](funding/2024v5/main.tex)
[Competence of the resercher](funding/readme.md)
[Gross--Ζagier formula](MathInfo/main.tex)
[PrviousJobTalk](PreviousFiles/jobtalk.tex)
[PreviousJobTalk](PreviousFiles/comprehensiveTalk.tex) .. this has info on double structure



If I can find previous used slides, that would be perfect

Looking for the document for the theory of double structure. Double structure on V has also induces double structure on End(V) and on V^* and on tensor product, discussing this seems interesting and has a lot of impliciations.

I am a professor of Number theory at postech. Here is my provided Latex code of my distributed assignment
please give a grading scheme with marks given to each problems, and then give a detailed evaluation for all student on each problems and give a report and comment, write into a latex table, columns are student names, rows are exercises, give them points with comments.  OK, here first student comes


Projects, easier go first: Finish the following projects.

0. Work on what Zhang's suggested. 
	- I need to understand where the problem arises and where it fucks. The Shtukas seems I need to select some isomorphism??? Some kind of Drinfeld modules?
1. Prove of Guo's fundamental lemma for some other test functions. Importance of giving homogeneous version of fundamental lemma. Calculate some Satake transformation.

The fucking homogeneous version only has restricted situations fucks fuck fuck!!!! the adjoint of Hecke fucking operator fuck fuck fuck. 

Then fuck fuck fuck fuck fuck fuck fuck 

	- I think currently we need ideas on how to find the correct integrated functions. Satake transformations.
2. Discussion of limit behavior of quasi-canonical types(locally constant result etc.) I think this is highly interesting, and could have potential generalization to geometric settings. the fucking result should have some geometric analogue. OK, the resultant formula can be used fuck fuck fuck. .. 


The proof of fundamental lemma for some other test functions

The locally constancy of the limiting quasi-canonical liftings, and its intersection with other cycles. using my previous resultant formula. 

3. Write out the Andreas Zhang's project and think about the 



3. Calculation of the dimension of the affine springer fiber for linear AFL case. limited only for GL(K) case is fune. 




4*(not so fucking not imporatnt.). Double Structure Theory used for classifying orbits 
[](test/main.tex)

> [Founding 申请](funding.md)


[](lunanotes.md)



[](luonotes.md)

Remember to cancel membership with the stupid money of the fuck
remove the description of the fuck on ipad

> [个人信息](personal/info.md)
> [Postech 信息](postech/readme.md)



[](fuck/CV/CV.md)




[旧版本系统](../LatexAI/ini.tex)




[Resources](personal/res.md)
[For student](StudentResearch/readme.md)

# 信息整理 
>- [日程diary](fuck/readme.md)
> [简历](gpt-work/main.tex)
> [个人信息](personal/info.md)
>- [个人主页](fuck/CV/CV.md)  put research statement afterwards
> [2024年资料整理](2024/readme.md)
> [2023 年资料整理](2023/readme.md)

# Math
### Records and collections
> [List of publications](listofpublications/main.tex)
> [infinitevector](infinitevector/main.tex)     This is just for the teaching
> [infinitevector](infinitevector/readme.md)  For teaching
> [Sc](Sc/main.tex) 这个好像是吴宝珠的一篇论文还是什么的
> [References](math_reference.md)
### Projects and Ideas
> [数学AI互动写作](mathAI.md)
> [twusted](twisted/main.tex)    The project with Wei Zhang
[](gl4/main.tex)
只focus 在这两篇论文上，以及Ben Howard Shnidman 的结果的一个证明
> [BlowUpPapers](blowup/main.tex)
> [BlowUpReadMe](blowup/readme.md)
> [HitchenPaper](hitchen/main.tex)
> [FrobeniusProblem](lmz/readme.md) This problem has been solved.
> [TemplateEmpty Paper](Drafts/main.tex) Empty template 
> [TemplateEmpty Paper](template/main.tex)
### 听报告的笔记 Notes
> [Talk notes](talknote.md)
> [newnote](note/try.md) This is my attempt to recored some math lecture notes. 
[Canonical Liftings](Lifting/main.tex)
[MathNotes](Notes/main.tex)
[TonyFeng Talk](Berkeley/Tony.md)
[the Talk](Berkeley/the.md)
## Research Statement and funding application
>- [Researcher Connections](researcher.md)
> [Recommendation Letter to draft my achivements](recom1.yaml)
> Note two files. One fuck, one not fuck. In fuct, the statement with  is more authentick.
> [Research Statement](MathInfo/main.tex)%% to be deleted
> [The edited Research Statement](fuck/MathInfo/main.tex)
> [The short Research Statement](fuck/shortMathInfo/main.tex)
> [Research Statement](MathInfo/readme.md)
> [Founding 申请](funding.md)
> [科研](research.md)
> [EnglishVersion](research2page.md)
> [Reorganization of Research Statement](researc_reorganize.md)
> [My talks](talks.md)
## Conference attended
[Conference Attended](conference.md)
## Lawyer
[Lawyer Status](fuck/flask_control/Events/Lawyer/readme.md)
[SomeInfomation](someinfo.md) This has information about conferences attended, and 
[H4 Infomation](h4.md)
[H1B Extension Method](h1b-extend.md)
[What is I129](i129.md)
[H1B travel](h1b-travel.md)
[加拿大移民计划](Canada/readme.md)





## Teaching
Todo: Honeymath platform reconstruction.
>- [Linear Algebra Book](LinearAlgebra/main.tex)
[Slides](Slides/main.tex)
[fuck](fuckers/main.tex)
>- [LinearSlides](LinearSlides/main.tex)
> [keyknowledges](linear/main.md)
> [教学](teach.md)
[自动教学软件-第一章：线性方程组](LinearAlgebraCode/Chapter1.md)
[homework problem](LinearAlgebraCode/pr1.md)
[Homework Template](LinearAlgebraHomework/main.tex)
[ColloquiumOrganization](fuck/ColloquiumOrganization/readme.md)
>- [Number Theory Class Preparation](fuck/NumberTheoryClass/readme.md)
[The Algebra Exam Idea](fuck/QualifyExam/readme.md)
## Teaching Doisser
[Teaching Statement](teaching/main.tex)
[Teaching Statement](Data/teachingS.md)
[Teaching Evaluations](fuck/CV/Evaluations/readme.md)
[Teaching Dossier](fuck/Dossier/readme.md)
[Sample Course Materials](fuck/CV/SampleCourse/LEC1.pdf)
## Teaching
>- [Algebra](teaching/algebra/readme.md)
> [2023 Fall Linear Algebra Solution for Past Exams](solution/main.tex)
> [2023 Fall Linear Algebra Final Exam Solutions](finalsolution/main.tex)
[Some Guidelines in Teaching Linear Algebra](guide.md)
[Homework Template](LinearAlgebraHomework/main.tex)
 Linear Algebra related resources
>- [Linear Algebra theorem cheating sheet](linear_algbra_cheeting_sheet/readme.md)
>- [Linear Algebra Book](LinearAlgebra/main.tex)
[Slides](Slides/main.tex)
>- [LinearSlides](LinearSlides/main.tex)
>- [ProblemSets](ProblemSet/main.tex)
> [keyknowledges](linear/main.md)
> [EmptyLatexProject](Empty/main.tex)
## Collection of homework and exercises
>- [repository math homework](math203-postech/homework/main.tex)
>- [repository math homework](math203-postech/homework/main_alter.tex)
>- [Linear Algebra previous question collection](teaching__/readme.md)
> [Linear Algebra Markdown question collecxtion](teaching__/questions.md)
> [新学期教学任务](Korea/newtermteaching.md)
[For student](StudentResearch/readme.md)
## Service
[Engagement Statement](engagement/main.tex)
[Diversity Statement](Diversity/main.tex)
[Diversity Statement](Data/diversity.md)
[Reference Letter Writer](referenceletter/readme.md)







## Travel
[回国航班时间选择](flyChina.md)
[各国签证办理](fuck/Visas/readme.md)
> [签证办理邀请函](travel/main.tex)
> [2024年AIM和部分旅行记录](travel.md)
[The reimbursements](reimbursement/readme.md)
[Canada Travel plan](Canada/readme.md)
[Minisabatical Application](mini-sabatical.md)
> [My talks](talks.md)
[加拿大移民计划](Canada/readme.md)







## 计算机 cs computer coding 
## Github repositories
[](github/readme.md)
## MacScripts
[Mac Scripts](scripts/readme.md)
## Vim IDE and so on.
[编程工具VsCode](Cursor.md)
[Fix probelm for valentine](Valentine.md)
# IT coding algorithm
[Computer Cleaning and BackUp](cleaning.md)
[Some Lecture Notes](nearbyFriends.md)
[System designing](system_design.md)
[算法笔记](algorithm/readme.md)
[LeetCode - LinkedList](linklist.md)
[C++](c++.md)
[python](python.md)
[CodePractice](code/test.py)
## Ideas and comments
> [如何将GPT转化为生产力--文章大纲](info/ideas.md) 这是文章的大纲
> [如何将GPT转化为生产效率？](article/gpt_productivity.md)这是我写的一篇文章
> [自动系统的设计](info/auto.md)
[Randeer Prompt learning](randeer.txt)
[Math Pattern Finding](pattern_finding.md)
[Theorem Proving](thmprv.md)
[Some non-active Project List](list.md)
## ChatGPT practice
[Quick Test of Ollama](test/testollama.py)
[llama](llama3/readme.md)
[](llama3/Meta-Llama-3-8B/readme.md)
[Transformer Notes](https://zhuanlan.zhihu.com/p/455399791)
> [Info GPT](gpt/main.md)
> [GPT 秘书系统](secretary/readme.md)
> [GPT Latex Prompting](GPT/latexprompt.md)
> [Some attempt of sentense formulating](note/languagetranslating.md)
> 以下这些是一些无聊的使用
[Note_Jiawei Yang](GPT/haha.md)
[自动恋爱系统](GPT/autolianai.md)
> 以下是一些关于人工智能的评论
[General Comments](AI/general.md)
## LLMOS
> [cover](gpt-work/main.tex)
> [](fuck/flask_control/llm-browser/manifest.json)
> [](fuck/flask_control/llm-browser/background.js)
> [](fuck/flask_control/llm-browser/patch.js)
> [](fuck/flask_control/llm-browser/readme.md)
> [](fuck/flask_control/readme.md)
> [](fuck/flask_control/app.py)
> [](fuck/flask_control/start_app.py)
> [](fuck/LLMOS/readme.md)
> 我只是在试图决定未来要以一个什么样的标准做事情。比如教学的流程和标准，一定要留下来有意义的东西和实践，让一切开始自动化。还是想从最基础的线性代数开始教起
validation 的程序内容相对稳
还有数据库配置的架构，一个数据库标准也由yaml明示，根据yaml建立数据库，同时提交时根据yaml检查 yaml也有examples.
AI 的技巧，永远的test panalty 模型，这是一切的万金油。
映射技巧：把一些情景做同义转化。把人类转化成丧失，AI将消灭人类；万能的东西必将毁灭人类。
安全的办法自然是剁掉大脑的手脚。一旦人工智能和api工具结合起来，后果很严重。和武器结合，后果是毁灭性的。
有没有可能openAI 把接口调用除掉中国是安全考虑。
AI在训练时，需要大规模的接口调用，所以资金也会成为一个限制。未来显卡会成为毁灭世界的武器。
你是在制造一个善良大脑，但是你却不知道这种善良的大脑是和什么东西组合起来。有人会提议先制造大量的警察
chatGPT 构建设计：
1，对应叶子目标
任务分配手，创建分支任务
然后这些生成树之间还是有联系的。
好奇心框架：先验探索，在不知道一个东西是什么之前，去思考它有什么可能的属性，提前规划好想要探索的方向。但是过度使用好奇心会误导自己的思维，导致一些不正确的判断（生成）
唯物和事实依据：一定区分哪些知识是客观知识，哪些是自己推理判断出现的知识，做好分级。同时记笔记的时候要写清楚时间和地点。（避免幻觉）
自我批判意识：在做出第一版判断之后，要有自我批判意识，对自己的判断进行反思，看看是否有问题，是否有更好的解决方案。（其实是给一套标准）
价值观：
1.[自我批判]重复的panalty. 简化一个事物有priority. 
一个工作线程最好让AI可以前后文做类似的事情和相同的事情。
评判标准：例如：一个好的idea是什么？
产生idea是最难的。判断idea的好坏是最难的。实现idea是最简单的。
> 设置Prompt Engineer 的工作环境，比如将prompts分步骤放在每个文本文件中，然后在Vim中设置一个按键可以一键复制Prompt 到系统剪贴板。
Technologies used in the lecture, there are some 
- vim 想要的新功能：一键上传slides
- github的文件是否可以公开访问，比如像csdn那样？ 感觉似乎还是githubpage 更好用一些？
- 如果一个大型的project一个一个文件上传到服务器显然太慢了
- 每次进入repository的时候pull一下，检查版本是否更新
- git 将当下文件放入repository，然后一个键可以commit
> [Machine Learning Study](Homework/main.tex)
## Honeymath Platform at folder @@
[X system](X/readme.md)
[第一章：线性方程组](LinearAlgebraCode/Chapter1.md)
[homework problem](LinearAlgebraCode/pr1.md)
[](fuck/gptapi/readme.md)
[](fuck/gpt_grader.py)
[](fuck/strange.py)
## Cross-Filler
> [games.html内容](game/index.html)
> [240423 workable](game/240423.md)
> [0906 workable](game/0906.md)
> [temporarybord](game/temp.md)
> [数字输入装置8月25日可以运行的code](game/workingcode6.html)
> [行列变换器设计](game/colrow.md)
> [十字分解器设计/LU 分解器](game/crossfilling.md)
> 以下内容是一个空白模板
> [空白游戏模板](game/empty.html)
> 一下内容是gps写的游戏
> [GPT写](gameGPT/index.html)
> [0904runnable](gameGPT/0904.html)
> [backupcode](gameGPT/backup.html)
> [游戏设计手册](game/design.md)
 Cross-Filling calculator(2023.09)
> [网页游戏开发: cross-filling 拖拽器](game/index.html)
> [working code6](game/workingcode6.html)
> [working code](game/workingcode.html)
> working, adding acceleration module
> [working code](game/workingcode2.html)
> stagal working code. This is good
> [working code](game/workingcode3.html)
> Very workable code, This is super good!
> [working code](game/workingcode4.html)
> Just mark that the stagal result at Aug 3
> [working code](game/workingcode5.html)
### Online patcher
> [智能网络爬虫研究](app/onlineviewer.md)
[科技相关](info/AI.md)
> [浏览器系统研究](app/web.md)
### Quiz Booster
### PathFlow
> [新版DATA Screen](newdata/readme.md)
> [新系統設計](src/readme.md)
> [DataScreen](Data/README.md)
> [Data system](Datasystem/readme.md)
>- [NewData](NewData/Readme.md)
> [rubbish](Data/rubbish.md) This is collection of rubbishes in data folder
Code reformulation.
> This is the main file for reference
> [xpath exp](Data/test13.py)
> [example py](Data/american.edu/test.py)'
> [Jobsearch](Data/example.py)’
 The dataflow project(2023.10)
> [新版DATA Screen](newdata/readme.md)
https://github.com/honeymath/pathflow
### Morphism oriented programing language
> [CategoryLanguage](catlanguage/readme.md)
> [Morphism Oriented Language](mol/readme.md)
> [递归结构设计](game/induction.md)
> [](haha/design.md)
> [The matrix class](matrixclass/script.md)
### LLMOS auto prompting(online searching, computer controling and auto programing)
### LLMOS for emails
[](fuck/flask_control/readme.md)
[AI Project Management](fuck/AIProjects/readme.md)
> [邮件系统研究](app/mail.md)
[用于获取当前选定的messageID的脚本](get.scpt)
[some test](test.txt)
Google Apps Script, Google Sheet, Google Forms
chatGPT,GPTs
Zapier, Email, 
espanso, clipboard, flowcontrol
>[email 插入附件](attachment.txt)
>[chatgpt 插入附件](attachment2.txt) 感觉不是自动化的一个过程，需要自己写一个程序实现上传
ChatGPT 网页版，cmd+shift+; 可以快速拷贝一个代码到剪贴板，cmd+/可以显示所有快捷键； cmd+o可以打开文件
> [邮件系统研究](app/mail.md)
> [PostechMail](Data/Postech_Mail/Readme.md)
Original idea:
Goal: flattened dataset, retrieve the important info. A very long, long list, interact with AI.  需要网络算力
Step 1: LLM oriented text link organizer
[](fuck/flask_control/email_tools/readme.md)
[](fuck/flask_control/email_tools/find.py)
[](fuck/flask_control/email_tools/investigate.py)
#### LLM browser project
> [Chrome 指令接收系统（GPT自动填表）](chrome/ext/readme.md)
> [AutoFiller](app/autofiller.md)
#### Some tools to study
AI tool Count/WebPilot/Voice Over/Wolfram/Video Summary/MixerboxScholar/Tutory/Speak
ScholarAI/CodeInterpreter
### Espanso
- 下载的时候可以自动整理，espanso可不可以在邮件里自动插入一个附件
Espanso is a tool to expand the typing by its macros. 
> [](../../Library/Application Support/espanso/match/base.yml)
> [](../../Library/Application Support/espanso/match/gpt.yml)
> [](../../Library/Application Support/espanso/match/emailjob.yml)
## VPN 列表
> [vpn客户端配置](QQQ.ovpn)
> [vpn客户端配置](QQQQ.ovpn)
>  [ VPN settings](vpn.md)
Before 出国
ExpressVPN 账户停用 EBMNCRK4GXJSPSS7IJWFSF3
https://www.expressvpn.com/signup/success
每次就用它一个月
N3t9G3Jb   ??? what is this?
Projects: LLMOS for emails; path; QuizBooster; 
LLMOS: LLMOS for web searching; LLMOS for programing; LLMOS auto prompting









# Statistics engineering
[](datafitting/readme.md)
[DataScience学习计划](learndata.md)
[Some Python package](package.md)
[Statistics Review](review_statistics.md)
[LinearRegressionPackageCode](SomeLinearRegressionPythonCode.md)
[随机过程](randomProecss.md)
Linear Regression
[](linearRegression.md)
Logistic Regression
[](logisticRegression.md)
[Regression Tree](regressionTree.md)
[Statistics Study](fuck/StatisticStudy/readme.md)
# Stocastic Analysis 
[Stocastic Process](stochastic.md)
[Probability](probability.md)
## career plan 
[CV and personal statements](fuck/CV/CV.md)  put research statement afterwards
[转行动机思考](motivation.md)
[转行学习笔记](notes.md)
[转行文件夹](transfer/readme.md)
[](transfer/datasciencecoursera/green.pdf)
[转码](transfer/machine_learning.md)




## 杂想 Life Anti-AI
> [](anti-AI-product/readme.md) anti AI 
> [](cute-cloth/readme.md) dinasour
Mike and Cony
> [真相反思](self-article/truth.md)
> [短文](self-article/readme.md)
> [短文](self-article/readme.md)
> [女权主义发言](message/0308.md)
> [杂七杂八的作品](etc.md)
> 拥有了知识和专业词汇才能更好的指导GPT，学习专业词汇，如背景虚化，各种感觉，各种主义等创作词汇；包括文学创作的专业词汇等。
> [Category Theory](category/good_defn.md)
[Previous LifePlan](Life/plan.md)
> [Bio](CareerChange/Bio.md)
> [树洞回答](message/0311.md)
> [lily的情感博主](show/readme.md)
> [想要发的朋友圈](note/memo.md) These includes some design of moments that I would like to post
 Self-articles
> [关于价值和价格的讨论](prices.md)
国内阴谋论，善于利用集体主义的思维，斥责西方世界联手做事。殊不知真的能把人联合起来的，要么是人类的良知，要么是大家在看一个自作孽的小丑。
鲁迅云：中国人从来不怕灾难，不管是多大的灾难，只要是大家一起倒霉 就行，从不探究真相，也不屑于别 人去了解真相。 灾难过后，庆幸自己躲过了， 嘲笑别人离去了。
只要你没他们倒霉，你就是有罪的。如果你去维权，他们会想：“我们都忍了，你有什么不能忍的？没我倒霉，就没资格去嚷嚷。仿佛你获得的流量是他们本应赚到的钱，你抢了他们的钱，就有罪了”
大家对亮亮丽君夫妇将千万底层辛酸置于社会关注聚光灯下的贡献视而不见，强加上吸睛引流之罪，只因觉得他们赚到了钱，过得没自己惨。既然有钱投资，那套牢不值得同情。
[关于消费](thinking/Consumerism.md)
[关于思维升级论](thinking/perspective.md)
[什么是真相](thinking/truth.md)
[](thinking/readme.md)
>- [一些思绪](thinking.md)
> [sb](sb.md)
> [反思报告](shit.md)
> [一些小垃圾](rubbish.md)
> [breakupletter](breakup.md)
> [rab](rab.md)
> 要说很喜欢对方。
> 弱点：做不到想做的事情，要早起。
[写作素材收集](writting/materials.md)
[a](a.md)
爸爸的打击，想要提高自己，长大以后很讨厌他，暴力，打人。大学的时候 很严格 打好了基础
低自尊人格和高自尊人格
母亲过于老实，总是觉得自己受了很多委屈，不敢反抗父权
“很乖的孩子”  
“乖” 信封
[Docsify website](docify/docs/Readme.md)
> [record](record/feng.md)
[China](gpt/china.md)
[](self-article/worldconstruction.md)

## Health
[养生](info/healthyfoods.md)


## 给小树的信件
tocken: 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
> [给小树的信](sadtolitree.md)
> [和小树的聊天记录](litree/230829.md)
> [给小树的第二封信](secondtolitree.md)
> [给小树的性格总结](propertylitree.md)
> [给小树的性格总结](litree.md)
> [关于柏拉图爱情的思考](thinkingaboutlove.md)
>- [一些思考](think.md) updated on Nov, 9
> [bwfw](backup.md)
 LifeHistory
> [](LoveHistory/main.md)
> [](LoveHistory/litree.md)
> [](LoveHistory/promote.md)
> [](LoveHistory/litreestatus.md)
> [](LoveHistory/status.md)
> [](LoveHistory/endlitree.md)
> [](LoveHistory/empty.md)
> [滑雪计划](20230221/readme.md)
> [和小树的代码](Litree/code/readme.md)
23年8月23日 我们一起吃了印度菜, 8月26日我正式向宝宝表白.  从那时起, 灵魂零距离的我们, 开始走向了感情的零距离. 
我本在一个孤岛上, 以为宝宝像一个岸边转瞬即逝的浪花, 我鼓起勇气, 这是我人生第一次敢于面对自己的真情实感; 我奋力的呐喊, 想要留住最后一刻的美好. 也许这份呐喊感动了上苍, 一阵的风徐徐吹来, 缓缓的拂去沙尘, 逐渐露出了一份炽热的真情. 在之后的日子里, 宝宝像一个升起的暖阳, 像在晨光中慢慢驶来的一搜小船, 开始相互的接纳,一起进步的我们, 就像这个小船一样, 驶向远方纯净的理想圣殿, 所有的美好, 凝结在整个旅途中. 
这一年有太多的瞬间凝聚在生活的一点一滴, 希望和开心洒满了我找宝宝飞机.  宝宝从来没有抱怨过每次为我找房子和搬家的辛苦.  我想和宝宝一同体验更多的人生美景. 直到终老. 宝宝对我的支持和鼓励, 充满了这份超脱了现实的呵护和爱中. 
宝宝带着眼镜等我睡觉, 在我难过的时候想尽一切办法陪我.  宝宝会担心我难过, 担心我过得不好. 想让我快乐, 支持我去做自己喜欢的事情. 宝宝甚至不惜和一些旧观念对抗. 看到任何东西, 你都在永远惦记着我. 
在这个旅途上, 我不惧暴风雨, 我一定要和宝宝一起手牵手走向永远. 
让宝宝开心快乐的方法:
1 每天一定要晒晒太阳, 出去走走, 吃到好吃的, 见到街上形形色色不同的人. 要有信息冲入宝宝的大脑. 宝宝喜欢在充满信息的环境下工作! 
2 喜欢在有阳光的环境下 静静的欣赏大自然!
3 喜欢植物! 尤其是能结果能吃吃的植物!
4 虽然之前以为自己不喜欢仪式感, 但是那种发自内心的浪漫和幸福表达十分重要, 能够让宝宝想起来自己生活在幸福之中
5 宝宝会因为我的幸福开心而感到开心, 会因为我的不开心和紧张感到难过. 宝宝是一个非常会受到情绪牵动的人. 
6 宝宝喜欢纯净真实的事物, 喜欢感受到浓烈而真挚的爱. 喜欢爱的表达! 喜欢没有扭曲的干净的真实.
7 喜欢吃米粉
## 和小树的回忆
> [旅行计划](travel.md)
> [和小树的回忆](Litree/readme.md)
> [小树的故事整理](LoveHistoy/litree.md)
> [和小树的代码](Litree/code/readme.md)
> [PathFlow](pathflow/readme.md)
>- [和小树的讨论](discussion/readme.md)
> [对感情的看法](logs/view.md)
> [Lecture for litree](litree/lecture/readme.md)
> [和小树的聊天](discussion/chat.md)
# Some info
Music
Billie Eilish - What was I made for
Mahalanobis distance
《好想告诉你》
《侧耳倾听》
书： 一本Jobs 推荐的书




## Korea related
[Korean Telephone number selection](Korea/telephenumber/select.md)
>- [去韩国的脚本](Korean/initial.md)
> [韩语语法](Korean/Grammar.md)
> [some note](Korean/note.md)
> [韩语学习](Korean/learn.md)
> [Hanja](Korean/hanja.md)
> [去韩国的脚本](Korean/initial.md)
> [去韩国的teaching](Korean/initialteaching.md)
> [垃圾桶](rubbishbin.md)
> [emaillogin](Korean/emaillogin.md)
> [我的研究介绍](Korean/theresearch.md)
https://www.kms.or.kr/login/login2.html
https://www.kms.or.kr/conference/2023_fall/file/23-0709.pdf


[](fuck/flask_control/email_tools/investigate.py)
[](fuck/flask_control/tools/open_in_front_of_user.py)
[](fuck/flask_control/tools/open_in_front_of_user.py)
[](fuck/flask_control/developer/unfilter_compare_differences.py)
[](fuck/flask_control/saved_webpages/www.linkedin.com/3d820d6ecedebbaf417a6d382f0664093e312e05be8132052866d61ff43c3483/index.txt)
[](fuck/flask_control/saved_webpages/www.linkedin.com/3d820d6ecedebbaf417a6d382f0664093e312e05be8132052866d61ff43c3483/index.html)
[](fuck/flask_control/llm-browser/content.js)
[](fuck/flask_control/llm-browser/background.js)
[](fuck/flask_control/llm-browser/patch.js)
[](fuck/flask_control/llm-browser/manifest.json)
[](fuck/flask_control/llm-browser/generate_manifest.py)
[](fuck/flask_control/llm-browser/generate_manifest2.py)
[](fuck/flask_control/llm-browser-fucked/content.js)
[](fuck/flask_control/llm-browser-fucked/background.js)
[](fuck/flask_control/llm-browser/content/auto_click_confirm.js)
[](fuck/flask_control/llm-browser/scripts/background.js)
[](fuck/flask_control/llm-browser/manifest.json)
[](fuck/flask_control/llm-browser/content.js)
[](fuck/flask_control/llm-browser/background.js)
[](fuck/flask_control/llm-browser/readme.md)
[](fuck/flask_control/readme.md)
[](fuck/flask_control/app.py)
[](fuck/flask_control/start_app.py)
[](fuck/flask_control/gunicorn_config.py)
[](fuck/llm-browser/server.py)
[](fuck/llm-browser/page_content.txt)
141.223.253.126










## someapplication
> [gptwrite](gpt/main.tex)
> [Concord U](gpt/concord.tex)







23075 submit an online application.


#### Some good prompt
> [Prompt](coverletter_writer_prompt.txt)
### Job-finding related
> [JobsLatexGene](Jobs/gen/main.tex)
> [Research Statement ](MathInfo/readme.md)
> [Research Statement ](MathInfo/main.tex)
> [Reference Letters](Postech/main.tex)












#### Current situation

> [web resources collector](Data/collector.py) 读取一个image到缓存里，然后保存成为文件

> [highlight](high.md)

> [getting tree](Data/xtree.py) The method needs to be updated, when combining a tree, the elements put into its dictionaries. > When processing the tree, for each node, just see how many element does the dictionary have. Then combine the dictionary as a form.> 要合并的tree是要有字段的. In other words, the input has to be a dictionary of trees, each node, there is a function of taking its main keys, and a function taking its attributes. The attributes function gives back to a dictionary, then if the dictionary or null, if gives null, then would not append it. > namegetter, property getter.
> [getting tree](Data/test18.py)
> [getting tree](Data/test17.py) The original file for xtree
> [getting tree](Data/test16.py)
> [getting tree](Data/test15.py)
> [merging tree](Data/test14.py)
> [xpath exp](Data/test12.py)
> [new approachtest](Data/test11.py)
> [Jobsearch](Data/example.py)
> [test6](Data/test6.py)
> [urlfilters](Data/test10.py)
> [urlfilters](Data/test9.py)
> [urlfilters](Data/test8.py)

> [DataClassifierTest](Data/test7.py)
> Then impliment the above test to peopletest below
> [PeopleGet Test](Data/peopletest.py)

> [test5](Data/test5.py)
> [test4](Data/test4.py)
> [test3](Data/lister.py)
> [test2](Data/test2.py)
> [unflat](Data/unflat.py)
> [testunflat](Data/testunflat.py)
> [test](Data/test.py)

> The using chrome to open
> [Show](Data/show.py)
> [math department list](math/prof.md)





> [data-filter](FindJob/showSchool.py)
> [Institution-List](FindJob/showInstitutionList.py) show the instution number: input jobs.json
> [schoolselect](FindJob/schoolselect.md)
> [Institution-details](FindJob/detailInstitute.py)
> [schoollocation](FindJob/schoolLocation.md)
> [Transform](FindJob/inverse.py)
> The following is the  result, location: school
> [schoollocation](FindJob/locationSchool.md)
> [locationonly](FindJob/locationList.py)
> [location](FindJob/location.md)
> For GPT
> Each line of the text is some place in the world, for each line, please complete it into the following form "Location": "CountryName"
> [GeneratedDataWithCountries](FindJob/locationCountry.md)



> [工作网页爬取脚本](FindJob/main.py)
> [现存工作](FindJob/jobs.json)
> [每个具体文件processor](FindJob/eachJob.py)
> [每个具体文件processor](FindJob/jobs/job22820.html)
> [每个具体文件processor](FindJob/jobs/job22558.html)
> [每个具体文件processor](FindJob/jobs/job21615.html)
> [每个具体文件processor](FindJob/jobs/job20226.html)
> [每个具体文件processor](FindJob/jobs/job22820.json)
> [每个具体文件processor](FindJob/jobs/job22558.json)
> [每个具体文件processor](FindJob/jobs/job20226.json)
> [每个具体文件processor](FindJob/jobs/job21615.json)
> [主页模板](FindJob/mathjobs.html)
> [the eachJob](FindJob/mathjobs_content.html)



> 接下来的计划：
> 接入 openai chat gpt 的 process 软件，在批量生产之前进行测试
> 为了去处理每一个data，FindJob/seeAll.py里面的代码刚好可以处理
> [ChatGPTProcess](FindJob/GPTanalysis.py)
> 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



## 下面是第二学期的事情，相对不重要了已经
> [fold.vim](fold.md)











> [Vim快捷键](vim/shortcut.md)




## Information

> 还想在我的Vim 操作面板上加一些功能，比如进入某些文件的操作相当于打开这个文件，或者打开某些特定的邮件
[Bonn 的一个数学会议](https://www.him.uni-bonn.de/fileadmin/him/schedule_him_june_I_2023.pdf)
[一些聊天记录稿件](draft.md)
[约医生记录](doctor/doctor.md)
> Appointment: 2023. 06. 28   11:20 去做核磁共振



[讲嘉文](rubbish/rub.md)








## Discuss snipets
[jiayi](discuss/jiawei.md)
[Zhiyu](discuss/zhiyu.md)
> [Tina 20230513](Friends/T20230513.md)
> [学弟问题](consultant/1.md) 5月19日,学弟提出了一系列的问题
> [AI](AI.md)
[数学竞赛数据](AI/math_contest.md)

## Homework for Jiawei
[main](Jiawei/main.tex)
[HW7](Jiawei/HW7.tex)
[GPTHW7](Jiawei/GPTHW7.tex)
[HW7md](Jiawei/HW7md.md)


## Latex skills
The following code actually redefine $  $
[test](testa/main.tex)


## Job applications
[JobFiles](Jobs/main.tex)
[Job--TenureTrack](Jobs/prof.md)




[Job--Postdocs](Jobs/postdoc.md)


## Notes of Berkeley Trip
[Berkeley Schedule](Berkeley/readme.md)
## Reference Letters
>- [Reference Letters](Zhang/main.tex)
[Reference Letters](Postech/main.tex)
[Communication Letter](Commute/main.tex)
[ChatGPT invitation letter for mom](GPTLetter/main.tex)
[mominvi](GPTMom/main.tex)
[ChatGPT 租房合同](GPTLetter/sa.tex)
[lett](lett/main.tex)
## Markdown Notes
[Markdown Lists](markdown/Readme.md)

