## Web编辑器

我打算在页面中嵌入编辑器，主要是两种，代码编辑器ace，markdown编辑器editor.md

前者用于在线编写代码，如果打算做一个博客式的页面，必须要有一个富文本编辑器，因而需要后者。

这两个编辑器都是js的，因而它是在页面中动态生成内容的，需要掌握的内容就是两个，如何将编辑器嵌入到页面中，如何获取生成的内容。



### ace代码编辑器

直接去官网，根据链接到github下载ace-builds压缩包，解压，我们只需要其中的`src-min-noconflict`文件夹即可。

根据官网的例子即可嵌入：

~~~html
<!DOCTYPE html>
<html lang="en">
<head>
<title>ACE in Action</title>
<style type="text/css" media="screen">
    #editor { 
        position: absolute;
        top: 0;
        right: 0;
        bottom: 0;
        left: 0;
    }
</style>
</head>
<body>

<div id="editor"></div>
    
<script src="/ace-builds/src-noconflict/ace.js" type="text/javascript" charset="utf-8"></script>
<script>
    var editor = ace.edit("editor");
    editor.setTheme("ace/theme/monokai");
    editor.getSession().setMode("ace/mode/javascript");
</script>
</body>
</html>
~~~

为了分离，我们可以将其中的样式表和js代码分离出来：

~~~html
<!DOCTYPE html>
<html lang="en">
  <head>
  <title>ACE in Action</title>
  <link rel="stylesheet" type="text/css" href="editor_test.css">
  </head>
  <body>

  <div id="editor"></div>

  <script src="statics/src-min-noconflict/ace.js" type="text/javascript" charset="utf-8">		   </script>
  <script type="text/javascript" src="editor_test.js"></script>
  </body>
</html>
~~~

然后你需要将第一个例子里面的样式和js加入到外部文件中，根据需要，可以再为两个文件增加需要的内容。

你所编写的代码将有ace动态加入到上述代码的div中。

我们可以直接在js中通过`editor.setTheme("ace/theme/monokai");`和`editor.getSession().setMode("ace/mode/c_cpp");`设置主题和代码种类，那么究竟支持什么主题和代码呢？

打开`src-min-noconflict`文件夹，其中以`theme`开头的js文件就是主题，例如`theme-chaos.js`这里面的`choas`就是一个主题，想要设置为这个主题，只需要写`editor.setTheme("ace/theme/choas");`即可，代码种类与此是同样的，`mode-c_cpp.js`文件表示`c_cpp`格式，写`editor.getSession().setMode("ace/mode/c_cpp");`即可设置。

因此，一般而言，我们会在网页中嵌入两个选项，然后使用js设置选项的`onchange`事件，在事件的响应函数中设置editor的主题和格式。

代码编辑完成之后，如何获取代码内容呢？

直接看官网上的`How To Guide`部分，写的很清楚`editor.getValue(); `拿到的就是代码的字符串。

所以，我们也会设置一个表单，并隐藏一个textarea，然后使用js监视提交，由js负责将代码字符串传递给textarea，然后提交表单即可。

~~~html
        <form id="form1" method="post">
            input filename
            <input name="name" id="name">
            <textarea name="content" id="content" hidden></textarea>
            <button id="submit">Submit</button>

        </form>
~~~

~~~javascript
var editor = ace.edit("editor");
editor.setTheme("ace/theme/monokai");
editor.getSession().setMode("ace/mode/python");

var btn = document.getElementById("submit");

btn.onclick = function() {
	var form = document.getElementById("form1");
	var co = editor.getValue();
	alert(co);
	var con = form.elements["content"];
	con.value = co;

	form.submit();
}

var mode = document.getElementById("mode");
mode.onchange = function() {
	alert(mode.value);
	editor.getSession().setMode(mode.value);
}


var them = document.getElementById("theme");
them.onchange = function() {
	alert(them.value);
	editor.setTheme(them.value);
}
~~~

这样最基本的内容就完成了，关于页面的装饰就可以自行完成了。

总而言之，ace编辑器是一个相当友好，相当好用，文档齐全的开源编辑器。

很优秀。



### Editor.md编辑器

据网上所说，这个编辑器和其他编辑器相比是很优秀的，也是国人所写，但是已经有两年多没有维护了。并且文档不是特别完善，接口也不够清楚，友好，但是，唉，只能这样了。



我解决了很多问题，做了很多探索，学了不少的技能，但是最终我失败了，至少我认为我无法以一种优雅的方式实现，最终我放弃了。作者为什么放弃了维护？也许与此有一点关系。



首先，面对的第一个问题是，源码默认从云端获取katex的样式表和js，但是这些文件已经被从云端移除了，所以，需要找到`editormd.js`的源码，修改加载的路径，自己下载katex的文件，从本地加载。

然后，我们基本上可以实现了这个编辑器，接下来的问题是如何拿到合适的markdown文件对应的html文件，然后我们才可以将其嵌入呈现的页面中。

实现方式有两种，第一种是根据官网上的说法，在一个textarea中生成html的字符串，这个字符串的js获取也是要小心，因为通过class拿到这个标签之后，例如`var txt=document.getElementsByClassName("");`，然后`txt[0].innerText`就是文本。

但是，真正的问题在于，我们如何才能正确的把这一段代码嵌入到一个html页面中，我按照官网的说法链接了所有的样式表和js文件，但是页面并未能完美显示，据网友的说法，似乎是生成的代码有某些问题，这里，主要是公式的渲染有问题，所以，这里可以进一步做一点新学到的手段进行文件请求测试的，有一定的可能解决。



第二种加载方式是讲你输入的md格式内容保存为md文件，然后从本地加载，经由markdowntoHTML渲染动态自动加入网页，官网上的例子就使用了这种方法，由jQuery向服务器请求本地md文件，我们必须要搞一个服务器，因此flask上场。

但是这里的问题在于，js动态请求了太多的字体等文件，flask应对这些请求很麻烦，我几乎只能手动处理每一个url。

我现在有的最有力的工具就是chrome的network分析工具，它可以监视网页从头至尾请求了什么内容，以及请求内容，url等。根据这个我将可以获取官网上html展示页面的完整加载过程，以及每一段的结果。

我现在唯有的突破点就是利用这个工具逐个检测对比，也许我会发现问题出在哪里，也许我将可以解决。



其实现在还有第三个方法，在编辑页面，结果的html已经显示出来了，所以，如果我能够把这一段动态生成的页面代码截取下来，也许我可以配上相应的样式表，js等，直接把它重现。就这样吧。我还有其他的事情要做，所以这些工作可能会被推迟几天。



我搞定了，终于，太他喵的不容易了。

其实难点并不多，我现在用的是第二种加载方法，然后从官网上搞到了最原始的作为容器的html页面，然后把md文件加载，难点就在于响应所有的请求，因为很多请求不知道具体的是谁发出的，所以我被动的手工处理了很多请求。

虽然有些不够优雅，但是暂时到此还算很完美。



下一步还有很多事情可做，其实。首先有很多请求是向云端发出的，我要想办法把它变成本地的，然后我要想办法搞定本地图片上传的问题，最后如果我能把那些不受控的字体文件的请求变成可控的就好了。



哈哈哈，我终于定位到了这些请求的位置，在`editormd.preview.css`中



我重新做了更加系统化的修改，现在同时有了两个页面，编辑页面和展示页面，同时把它们定制成了flask的，然后也完成了所有文件均本地化的修改，但是修改还不够彻底，因为现在的文件处于一种比较杂乱的状态，统一堆在了static文件夹下面，如果某一天想要系统化的话，记住我需要修改js文件和css文件，而文件的范围绝对不会超过editormd，也就是说修改的文件目标就是`editormd.preview.css`和`editormd.min.css`或者`editormd.js`

然后其实还有一个页面，应该是重新编辑页面，这个页面其实完全可以是编辑页面，只需要把md文件的内容放到特定的那一个textarea里面就好，同理，编辑完成之后想要存储到数据库里面也是存md文件。

总而言之，现在的成型方案就是一切以md文件为基准，存储，重新编辑，展示都用的是md文件。