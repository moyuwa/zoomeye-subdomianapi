# py3zoomeye_subdomainapi
 zoomeye钟馗之眼子域名查询api脚本，版本v1.0

**当前只支持windows系统使用，linux系统自行修改apikey保存路径**

第一次执行会要求输入apikey，保存在当前用户appdata路径下

![inputapikey](inputapikey.png)

目前只支持子域名查询（关联域名查询不支持），查询结果自动保存到csv文件，命名：[域名]-[类型]-[总数].csv

![search1](search1.png)

批量查询

![list](list.png)

导出结果样式，与zoomeye web界面导出的txt类似

![csv](csv.png)

后续更新：

1、支持linux系统，优化脚本运行流程，添加多线程（加快批量查询速度）

2、支持关联域名查询，并和子域名查询合并去重

3、支持ip存活校验，并支持对常见端口进行存活探测

4、支持简单的web存活探测（存活、状态、标题）
