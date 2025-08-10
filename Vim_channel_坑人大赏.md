# Vim channel 坑人大赏 🎉💥

写在前面：  
—— 本文写于我被 Vim channel + JSON 回调机制 坑到血压飙升之后！如果你也踩了坑，请勇敢分享，让我们一起警醒后来人！！

## ⚡ 坑点全览

### 1️⃣ 文档误导：callback 以为会自动触发，实际上不触发！
Vim 官方文档写的示例：
```vim
let ch = ch_open("localhost:8765", {"callback": "Handle"})
call ch_sendexpr(ch, "hello!")
```
看起来好像：
👉 只要 server 发回来消息，Handle 就会被调用，对吧？

**错了！！！**  
如果你的 server 发回：
```json
[2, {...}]
```
Vim 会丢掉这条消息，连个提示都没有，回调不会触发！

### 2️⃣ 真相：必须 ID = 0 才会触发 channel 的通用回调
你 server 必须发：
```json
[0, {...}]
```
否则 Vim 认为消息是给专属回调的（找不到就丢了），根本不走你 ch_open 配的回调。

### 3️⃣ Vim 不提示，不报错，不警告
你看不到任何提示，只会发现回调没触发。  
除非你手动开启：
```vim
:call ch_logfile('/tmp/vim_channel.log', 'w')
```
去翻日志，才能看到：
```
Dropping message 2 without callback
```
**这是什么反人类设计啊！！！👊**

## 💣 我的血泪教训
为了搞懂这个，我：
- 改 server 改 Vim 改端口改 socket，通宵 debug。
- 用 `nc` 测数据流，开 `ch_logfile` 翻日志。
- 最后靠网友和多年血泪经验总结出来：ID 必须是 0。

## 📝 给后来人忠告
⚠ 如果你用 Vim channel + JSON：  
✅ server 主动发的消息一定要 ID = 0。  
✅ 开启日志，不要等着 Vim 提示你哪里错了，它不会的。  
✅ 不要轻信文档示例，一定自己测清楚！

## 🙏 给 Vim 作者的一句话
> Vim 是好编辑器，但 channel JSON 回调这块文档写得不清楚，设计也不友好！坑死人不偿命啊！  
> 希望有一天 Vim 能好好改进，不要再坑后来人了！

## 🌟 致敬和感谢
向所有被这个坑坑过的开发者致敬，愿我们不再掉坑！