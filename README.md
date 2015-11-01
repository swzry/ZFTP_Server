ZFTP Server V1.1
===========

本项目本是为swzry.com专门开发使用的FTP服务端，开发时未考虑过多关于通用性方面的内容，您使用时可能需要根据自己的需求酌情修改。
本项目按照MIT License 发行。

（2016年6月9日后本人的部分开源项目可提供定制开发，详情请访问http://coding.swzry.com/）

作者网站：http://www.swzry.com/
代码仓库：http://git.swzry.com/
代码服务：http://coding.swzry.com/

### 使用方法 ###
1、将该项目解压到一个合适的目录，为方便讲解，这里以/home/zftpd为例
2、编辑配置文件。配置文件内有注释，请照着注释根据实际情况进行配置。
	附：权限字符串的说明
		读取相关权限:
         - "e" = 更改目录 (CWD命令)
         - "l" = 列出文件 (LIST, NLST, STAT, MLSD, MLST, SIZE, MDTM命令)
         - "r" = 从服务器上读取文件 (RETR命令)

        写入相关权限:
         - "a" = 追加数据到已存在文件 (APPE命令)
         - "d" = 删除文件或目录 (DELE, RMD命令)
         - "f" = 重命名文件或目录 (RNFR, RNTO命令)
         - "m" = 创建目录 (MKD命令)
         - "w" = 上传文件到服务器 (STOR, STOU命令)
         - "M" = 修改文件权限 (SITE CHMOD命令)
3、测试：
	cd /home/zftpd
	python zftpd.py start
	测试完毕后使用python zftpd.py stop停止服务

### 命令行说明 ###
python zftpd.py start|stop|restart

### 在Linux上部署为系统服务 ###
（以下说明以使用sysv的Linux发行版为例说明）
1、编辑zftpd文件，将第九行的zftpPath="/home/ftpd/"设置为你存放ZFTP Server的路径，例如/home/zftpd/
   （注意：如果该程序在传播过程中文件权限信息丢失，请赋予zftpd文件执行权限，例如chmod 777 zftpd）
2、将zftpd文件拷贝到/etc/init.d/目录下（可能因系统而异）
3、使用chkconfig或sysv-rc-conf之类的工具进行配置，使zftpd自启动

### 注意事项 ###
1、目前版本对中文文件名的支持尚不是很可靠，如果遇到服务端长时间运行后，含中文文件名的目录无法列出，请重启ZFTP Server.
   这个问题的根源是来自引用的库pyzftpdlib，虽然本人目前暂无时间继续维护本项目，但您可以试着去github等地方寻找新版或者由其他人完善过的pyzftpdlib，替换项目中的pyzftpdlib解决这个问题，待本人有空将更新该项目内的库为可靠的新版本。
   还有一个比较简单粗暴的解决方法就是使用crontab定期重启ZFTP Server。
2、ZFTP Server运行过程中您可以更改配置文件中的用户信息等配置项目，生效时间间隔由配置文件中的ttl配置项决定
