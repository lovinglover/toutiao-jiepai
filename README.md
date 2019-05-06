# 爬取今日头条街拍图片
自己跟着一些视频和博客学习写的，发现大部分都比较早，于是自己摸索，这里记录一些走过的坑

思路：

网站不是静态形式，如果直接访问街拍网站，会发现html里面根本没有我们想要的内容，需要查看Ajax请求，而实际上我们访问的网站并不是https://www.toutiao.com/search/?keyword=%E8%A1%97%E6%8B%8D ， 而是https://www.toutiao.com/api/search/content/?aid=24&app_name=web_search&offset=0&format=json&keyword=%E8%A1%97%E6%8B%8D&autoload=true&count=20&en_qc=1&cur_tab=1&from=search_tab&pd=synthesis&timestamp=1557111928208 ，会发现多了很多东西。可以在浏览器preview标签卡里看到一堆json格式的数据，我们实际要分析的是这个，接下来就是从这个json形式的数据里提取出每一个组图的连接，再获取到每一个图片的连接。

遇到的问题：

1.获取到组图的连接后访问正常，打印返回的html代码，发现是空，上网查找是cookie的问题，很多人都只提到了要添加user-agent

2.分析组图获取单个图片链接。很多文章都只提到了 gallery: JSON.parse(...) 这种json格式的解析方法，但这种页面不多，大部分还是存放在content下的一串字符，这个就只能用正则去获取了。

3.文件名不合法。会有一些含有":"标题，无法作为文件夹名
