[](../../readme.md)
## Vim Configuration

This `.vimrc` configuration enables advanced navigation capabilities within Vim, allowing you to quickly enter a folder view or escape from a file using specific keybindings.

[](.vimrc)
[](.vimrc_windows)
[](LICENSE)

## AI Tool Configuration

To enable integration with local/remote AI tools, modify and save the following configuration according to your environment:

[Write this file with following](config.ini)
```ini
[server]
host = 192.168.2.1
port = 8765
```

To verify that the server is accessible, run the following command in your terminal, for example:

```bash
nc -vz 192.168.2.1 8765
```

If your server is using macOS and want to determine your local IP address, use the following:

```bash
ifconfig getifaddr en0
```

If `en0` does not work, try:

```bash
ifconfig getifaddr en1
```

To load this configuration in Vim, assuming you've cloned the repository into `~/repositories`, add the following to your `~/.vimrc` file:

```vim
let g:local_path = '~/repositories/vimconfig'
"let g:python_name = '/Users/qiruili/miniconda3/envs/ai/bin/python'
source ~/repositories/vimconfig/.vimrc'
```
Here python_name just in case if you have a different python or you wanna worker to run with a different python

Note that if your server and local machine are different, then both your server and local machine need to be configured, it is suggested that your server uses '0.0.0.0' as ip address

### Keybindings

- Press `\` to enter a markdown-like navigation view.
- Press `Option+\` to escape back out of a file.


For example, try using the keybindings on the following markdown link:
[](tools/ex1.md)
