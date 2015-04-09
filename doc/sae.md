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

 

    