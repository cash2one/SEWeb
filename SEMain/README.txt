强烈建议在linux 下开发，Tornado　采用了epoll 异步IO ，window 下不支持，但可以模拟运行，性能远不如linux ,项目中应用Multiprocessing
进程池进行多进程并发来加速CPU密集型任务（搜索结果过滤），window 下可能无法运行（windows 只支持在__main__ 模块下调用Multiprocessing 进程池）

目前开发的版本已经部署到网信办的服务器，postgresql 数据库也已经部署好了，测试的网址是　http://111.202.27.164:8888/　

为了避免ssh 连接断开后，当前bash 运行的进程被关闭，需要screen  来进行管理会话

启动程序命令　
v-wxb-chai@data111 $ cd /home/v-wxb-chai/workspace/webserver/SearchEngine
v-wxb-chai@data111 $ screen -S  WebEngine  (该会话已创建并在服务器上运行，请先结束或创建新的会话)
v-wxb-chai@data111 $ python  app.py

按住　ctrl+A+D　可退出当前会话


查看tornado 服务器后台日志命令：


v-wxb-chai@data111 $ 　 screen  -ls

bash output:             There is a screen on:
                                     9164.WebEngine  (Detached)

v-wxb-chai@data111 $ 　 screen  -r 9164
即可进入　WebEngine　会话(服务器上运行的tornado进程的会话)



服务器　postgres用户密码是pgsql911 　数据库中postgres用户密码也是pgsql911 　启动及停止数据库需要切换到postgres用户　

postgresql　数据库数据库存放目录　/usr/local/database/postgresql/data

启动postgresql 数据库命令:


postgres@data111 $  cd  /usr/local/database/postgresql/data
postgres@data111 $  ../bin/pg_ctl  -D ./ -l logfile start


停止postgresql 数据库命令:

postgres@data111 $ 　export  PGDATA=/usr/local/database/postgresql/data

postgres@data111 $  /usr/local/database/postgresql/bin/pg_ctl stop


建议先安装Anaconda(python 的科学计算环境，可以免去安装很多扩展库的麻烦，尤其是一些需要依赖C扩展并编译安装的库，安装Anaconda后，
可以通过conda 或pip　安装其他的扩展库)，网信办的服务器已经安装Anaconda了


工程目录及文件介绍：

　　　.idea目录及SearchEngine.iml 为Intellij Idea(目前开发所用的IDE)工程生成的文件，也可用其他的IDE 或编辑器开发
      static 目录存放静态文件(.css .js .jpg 等文件)
      templates 目录主要存放.html 文件　及模板文件
      app.py tornado服务后台的主程序
      info_search.py  搜索引擎数据抓取及处理的程序

代码已经有比较详细的注释，在这里不再赘述








