#### 方法一
使用[读取隐写信息脚本](https://github.com/cjcslhp/wheels/tree/master/b64stego)  
给**data.txt末行添加换行**并更名为stego.txt，运行b64b64DeStego.py即可

```
In [122]: !python b64DeStego.py
     flag{BASE64_i5_amaz1ng}
```

#### 方法二
手动提取隐写内容，按照隐写原理，填充两个'='隐写四位信息，填充一个'='隐写两位信息，将编码按照[base64对照表](https://ctf-wiki.github.io/ctf-wiki/misc/encode/computer/#base)还原，然后每8位转成字符即可，具体实现可参考方法一提供的源码或wiki中的脚本；  
以最后一个字符为例：  

```
IEEtWn==
IC3=
IGFuZCBfIGFzIGFkZGl0aW9uYWwgY2hhcmFjdGVycy5=
```
字符隐写在这三行之中，分别解码('n','3','5')得到(39，55，57)取其二进制后(4，2，2)位得到`0b01111101`(125)ASCII编码对应字符为'}'。  
