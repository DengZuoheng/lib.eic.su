## sae account
- sae account:kanonwind@163.com
- password:INNER_PEACE
- app name:libeicsu
- Access Key:5k0l0xlmkj
- Secret Key:1z2w0h50yij5w3l5lyjy5w511y5mm24kk0kklw45

## sae shell 
在sae中, 要使用django的syncdb的话, 需要使用sae提供的shell工具, 步骤如下:

- 修改server/index.wsgi, 将
    <pre>
    #from sae.ext.shell import ShellMiddleware
    #application = sae.create_wsgi_app(ShellMiddleware('libeicsu'))
    </pre>
    的注释取消
- svn上传代码
- 浏览器上打开`http://libeicsu.sinappp.com/_sae/shell`
- 执行如下命令(如/server/sae_shell.sh):
    <pre>
    from django.core.management import execute_from_command_line
    execute_from_command_line(["","syncdb"])
    </pre>
- 然后就可以了

## sae storage
图片和备份文件的储存都用过sae storage服务实现, 但是sae storage的python接口的文档实在太难看, 所以并没有完全照着文档写;

所有使用到sae stroage的代码都集中在/server/library/service.py

注意, domain是需要自己在sae后台手动创建的. 目前建了两个domain, 一个是images, 一个是backups;

## 分词
分词使用的是sae的服务, 但是sae服务只能在sae中请求, 为了在本地调试分词相关功能, 本项目提供了一个分词的view, 作为代理访问sae的分词,
要使用这个分词, 首先得把代码放到sae上正常运行, 并且打开sae的分词服务; 相当于本地调试的时候, 分词服务用的是本项目的服务, 而本项目在sae上运行时, 分词服务用的是sae的服务
 

    