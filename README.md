ZFTP Server V1.1
===========

http://swzry.com/

本项目本是为swzry.com专门开发，通用性并不强，您使用时可能需要酌情修改部分内容。
本项目按照MIT License 发行。

### 使用方法 ###
1、将该项目解压到一个合适的目录，为方便讲解，这里以/home/zftpd为例
2、编辑zftpd文件，将第九行的zftpPath="/home/ftpd/"设置为你存放ZFTP Server的路径，例如/home/zftpd/
	（注意：如果该程序在传播过程中文件权限信息丢失，请赋予zftpd文件执行权限，例如chmod 777 zftpd）
3、编辑配置文件。配置文件内有注释，请照着注释根据实际情况进行配置。
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
4、测试：
	cd /home/zftpd
	./zftpd start
	测试完毕后使用./zftpd stop停止服务
5、安装为系统守护进程
	将zftpd文件拷贝到/etc/init.d/目录下（可能因系统而异）
6、设置守护进程自启动
	使用chkconfig之类的工具进行配置，使zftpd自启动

### 注意事项 ###
1、目前版本对中文文件名的支持尚不是很可靠，如果遇到含中文文件名的目录无法列出，请重启ZFTP Server
2、ZFTP Server运行过程中您可以更改配置文件中的用户信息等配置项目，生效时间间隔由配置文件中的ttl配置项决定

