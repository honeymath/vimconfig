This is a text file editing with AI.

Note that the symbol '```' is in markdown the standard comment symbol.

```ai: help me to modify the following
This is an example area that is a block, which ai can modify.
```

Sometimes, there is a see block inside ai block, in which the ai can not modify.

```ai: modify the following
Here is one content that ai can modify
```see: do you have any comment?
This is a holy fucking area that AI cann not modify
```end
OK, you have anything in mind?
```end

As showed in above, each ai block should be under the see block, and each see block should be under ai block. 

Sometimes, we are inside the 'see' block, but would like the ai to pay more attention to it, we can use this trick:

```ai:
```see: please pay attention to the following
AN IMPORTANT MESSAGE
```end
```end

However, this is quite redundant, we will combine it as the watch block:

```watch: please pay attention to the following
AN IMPORTANT MESSAGE
```end

Therefore, in practical, watch is equivalent as ai:see: and it helps us to avoid writing end twice.

In princile , there is a hidden syntax called 'context', but we would not explicitly used it here. In the most strict situation, either ai block and see block are not allowed to contain content. Only context can do. For example, the classical things like

```ai:prompt
content
```end

is in fact in the strict sense shold be

> ```ai:prompt
> ```context
> content
> ```end
> ```end

The context block is designed to carry the content and carry the conversation with AI. In principle,  either ai block or see block can not contain content and conversation history, ai block or see block can only contain a sequence of context blocks.

In the case that ai block or see block contains multiple context blocs, for example, in principle, the following structure

> ```ai:prompt
> ```context1
> content1
> ```end
> ```context2
> content2
> ```end
> ```end

is simplified as

```ai:prompt
content1
```ai:prompt2
content2
```end

In other words, if ai block appears inside ai block, the inner ai block is considered as ```end old context ```begin new context. Same thing happens for see block. For example

```see: summaize the following
context 1
```see: at this point, what is the good of the
context 2
```end.

Note that this would not arise any conflict since we are not allow see block inside see, and ai block inside ai, so when the block of the same type starts, we switch our interpretion to be the boundary of the new context.

## The use of watch block

The watch block is desined as follows: 

```see: prompt
```watch: pay attention to the following
instruction
```end
```end

is equivalent to

```see: prompt
```ai:
```see: pay attention to the following
instruction
```end
```end
```end

If used inside ai block, the watch block is equivalent to the see blcok.

```ai: prompt
```watch: pay attention to the following
instruction
```end
```end

is equivalent to

```ai: prompt
```see: pay attention to the following
instruction
```end
```end

The design of this is to avoid the redundant writing of end, and make it user friendly while we are keeping the rules. Note that when using watch under the see, the ai block does not have any context subblocks, its only block is a see block, which contains a context block. And any conversation is carry by the context block. So essentially it obeys the rule of alternating ai and see block, also give the flexibility of using context block.

An explaination from the user side is that watch block asks the AI to pay attention to the content inside.

## The entire document
Note that the whole document is automatically considered as context under a see block. Therefore, we may only use ai block and watch block initially, and only write see block inside ai block.

For example, directly writing this is prohibited

> ```see: what is this
> content
> ```end

Instead, we shuold write like

> ```watch: what is this
> content
> ```end

## reply: the conversation history.

The ai could reply with a short summary of the conversation and is collect and write in the reply as a one line.

```see: summarize this?
```reply: this is a summary of the conversation.
```see: So what do you mean by a summary?
```reply: A summary is a miaomiao
Content
```end

## metadata: 

Each metadata can only be associated with the context block, and it can use some keywords, for example, name or data, and write each by oneline.

```see: what is this
```name: specific
```date: 2025-01-01
Content
```end

Note, the meta data can appear between lines of conversation, essentially, conversation is also a part of metadata. The metadata can only assigned to the context block.

## The parsing tree

With the given structure, we will end up with a tree, there are two kinds of nodes, one is the context node, the other is a non-context node. Let us say the root node to be in level 0. Therefore we have the following consequnces:

> Any level 2n context node is essentially an editable node under the AI.
> Any level 2n+1 context node is essentially a non-editable node under the AI.
> Any level 2n non-context node must be see node.
> Any level 2n+1 non-context node must be ai node.

> Only non-context node can have children nodes.
> Any node without children have to be a context node(so that non-context node without a children is not allowed).


## The comment syntax and escape syntax in other languages
We have to made it as a comment excutable language. The adaption of each scripts is essential

In this markdown file, we use '>' at the beginging of the line to represent escape syntax, when the parseer see it, it will treat it as a normal line without any function. The comment syntax is '```' which would trigger the parser to construct the tree.

Note: In markdown, the '```' does not realy work as a comment, we do this to avoid complication with '<!-- -->' which is essentially not user friendly to type in.

In py file, the comment syntax is '#', while I have not decided the escape syntax yet, it could be '##', or '"""' or "'''".

In latex file, the comment syntax is '%', while I have not decided the escape syntax yet, it could be '{'.
