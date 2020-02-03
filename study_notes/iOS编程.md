### iOS编程

需要Mac电脑和Xcode自不必说。

这里我使用swift编程，swift版本：5.1， Xcode版本11.3.1，APP的构建现在还主要使用storyboard，后面可能会考虑使用swiftUI。

初级阶段，我会在swift playground做比较多的东西，包括xcode的swift playground和iPad pro 11英寸版本上面的swift  playground

我不会太多的详细记录我学到的所有内容，只会记录一些重要一点的内容。

### iOS版本问题

在这个版本的xcode中，创建项目默认支持的最低系统版本是iOS13，当选到iOS12.3以下的时候，基本上编译过程就会报错，原因是默认的`AppDelegate.swift`和`SceneDelegate.swift`使用了一些只在iOS13中支持的内容，如何处理？可以参考[这一篇文章](https://www.jianshu.com/p/3de524451fe0)，基本上就是报错信息使用自动纠正全部内容就可以搞定，然后黑屏的情况需要在`AppDelegate.swift`的代码文件里为类增加一个`window`属性



### HTTP网络编程

根据我现在知道的内容，iOS要使用HTTPS，如果想要使用HTTP就必须在`info.plist`加入这个项：

~~~xml
<key>NSAppTransportSecurity</key>
<dict>
    <key>NSAllowsArbitraryLoadsInWebContent</key>
    <true/>
    <key>NSAllowsArbitraryLoads</key>
    <true/>
</dict>
~~~

对于`info.plist`右键以源码形式打开，在xml里面合适位置加入上述即可。

上述内容参考自[这一篇文章](https://www.jianshu.com/p/601f3fa318ed)

对于我们在家里的局域网中自建的HTTP服务器，如建在树莓派上的Flask，如何让APP和服务器之间进行`GET和POST`请求

~~~swift
func get(url: String, _ data_type: IType = .html) {
        do {
            let aim_url = URL(string: url)
            if data_type == .image {
                let data = try Data(contentsOf: aim_url!)
                let _ = UIImage(data: data)
            }
            else if data_type == .html {
                let html = try String(contentsOf: aim_url!)
                print(html)
                show_label.text = html
            }
            else {
                let data = try Data(contentsOf: aim_url!)
                json_parser(data: data)
            }
        } catch {
            print("***\(error)")
            warning_label.alpha = 1
        }
    }
    
    func post(url: String) {
        let url = URL(string: url)
        var request = URLRequest(
            url: url!,
            cachePolicy:.reloadIgnoringLocalAndRemoteCacheData,
            timeoutInterval: 30)
        request.httpBody = "x=5&y=3".data(using: .utf8)
        request.httpMethod = "POST"

        let session = URLSession(configuration: .default)
        let dataTask = session.dataTask(with: request) { (data, response, error) in
            if let data = data {
                let html = String(data: data, encoding: .utf8)
                print(html!)
            }
        }
        dataTask.resume()
    }
    
    func json_parser(data: Data) {

        do {
            let jsonObj = try JSONSerialization.jsonObject(
                with: data,
                options: .allowFragments
            ) as! [[String: Any]]

            for p in jsonObj {
                print("姓名: \(p["姓名"]!)")
                print("年齡: \(p["年齡"]!)")
                if let tels = p["電話"] as? [String: String] {
                    print ("公司電話: \(tels["公司"]!)")
                    print ("住家電話: \(tels["住家"]!)")
                }

                print("----------------")
            }
        } catch {
            print(error.localizedDescription)
        }
    }
~~~

以上是截取的某一段包含了上述两种请求和一段json parser的代码，表述了大概的意思。



### 加速度计与弹球

假设想要实现一个这样的APP，重力方向将会根据加速度计的指示进行调整，小球按照上述重力进行自由落体，并且完成反弹。

这里要做到的基本技术包括：

首先要能够获取屏幕的尺寸，然后要能够设置和获取小球图片的位置，然后重点是在于获取加速度计的结果，并对重力方向进行调整，然后要注意所谓事件循环。

~~~swift
// 在viewcontroller里面通过下述代码可以获取屏幕尺寸
self.width = self.view.frame.size.width
self.height = self.view.frame.size.height
~~~

~~~swift
// 如果小球的ImageView被导入为self.ball，下述代码分别可以获取和设置小球中心坐标
var pos_x: CGFloat = self.ball.frame.midX
var pos_y: CGFloat = self.ball.frame.midY

self.ball.center.x = pos_x
self.ball.center.y = pos_y
~~~



~~~swift
// 下述代码用于获取加速度计的结果
import UIKit
import CoreMotion

class ViewController: UIViewController {

    
    let motionManager = CMMotionManager()
    

    override func viewDidLoad() {
        super.viewDidLoad()

        motionManager.accelerometerUpdateInterval = 0.01 //1.0 / 60.0

        motionManager.startAccelerometerUpdates(to: OperationQueue.current!) {
            (data, error) in
            if let myData = data
            {
                self.g_x = CGFloat(myData.acceleration.x)
                self.g_y = CGFloat(myData.acceleration.y)
            }
        }
    }

}
~~~

如上，需要获取CMMotionManager的实例，设置采样间隔，然后以尾随闭包的形式设置加速度计更新时调用的函数



关于事件循环，一种策略是将小球的坐标更新写入加速度计update的callback里面，但是这种方式并不是特别好，另一种方法是使用定时器，定时触发坐标更新函数，然后循环处罚。

~~~swift
// viewcontroller的如下函数
override func viewDidLoad() {
  super.viewDidLoad()
  let _ = Timer.scheduledTimer(timeInterval: 1.0/60.0, target: self, selector: #selector(self.time_on), userInfo: nil, repeats: true)
}

@objc func time_on() {

}
~~~



基本上综合上述技术，加速度计的callback负责更新重力，timmer的callback负责绘制就能搞定上述目的，接下来还需要一些辅助工作。

辅助工作包括：通过触控设置小球位置，如何检测屏幕旋转，如何处理加速度计的指向和设备指向的关系。

#### 触控事件

~~~swift
override func touchesBegan(_ touches: Set<UITouch>, with event: UIEvent?) {
  var tou_x: CGFloat = 0
  var tou_y: CGFloat = 0
  for t in touches {
    let a = t.location(in: self.view)
    tou_x = a.x
    tou_y = a.y
  }
  self.ball.center.x = tou_x
  self.ball.center.y = tou_y
  self.speed_x = 0
  self.speed_y = 0

}
~~~

viewcontroller又上述方法可以重载，其中的touches存储了一个touch的set，这是因为多点触控的原因，这里我只考虑了单点触控的情形

这些已经暂时够用了，更多的可以去看文档资料

#### 设备旋转

~~~swift
override func viewWillTransition(to size: CGSize, with coordinator: UIViewControllerTransitionCoordinator) {

  let v1 = max(self.width, self.height)
  let v2 = min(self.width, self.height)

  if UIDevice.current.orientation.isPortrait {
    self.width = v2
    self.height = v1
  }
  else {
    self.width = v1
    self.height = v2
  }
~~~

同样是viewcontroller的可重载方法，这个方法会在设备指向旋转的时候被调用。

另外随时可以通过下述代码：

~~~swift
if UIDevice.current.orientation == .portraitUpsideDown
{
  self.g_x = -self.g_x
  self.g_y = -self.g_y
}
else if UIDevice.current.orientation == .landscapeLeft {
  let s = self.g_y
  self.g_y = -self.g_x
  self.g_x = s
}
else if UIDevice.current.orientation == .landscapeRight {
  let s = self.g_y
  self.g_y = self.g_x
  self.g_x = -s
}

~~~

来检测当前屏幕的方向，看文档就能知道屏幕的方向一共会有七种

然后我们应该通过检测设备的状态来调整小球的重力方向，设备宽高之类的。但是实际上我到现在也没搞清楚加速度计的读数和设备方向的关系。我的代码通过逐步调整的方法达到了目的，但是实际我并不是非常理解，这些内容就不做记录了。



### 2D图形绘制

假设，我们想要绘制一个2维的坐标轴来实时在屏幕上指示出加速度计的x,y方向和大小，那么我们应该做些什么？

其实问题只有一个，怎么绘制路径？

这个问题的思路是：首先我们需要在故事板上添加一个UIView，然后为这个view自定义一个类，通过控制这个view的draw来绘制路径。

在storyboard界面的右侧可以设置一个view的custom class，将它设置为我们的自定义view class即可，当然首先我们要为项目新增一个文件，选择cocoa touch class，基类选择UIView。文件代码如下：

~~~swift
import UIKit

class CanvasView: UIView {

    var x_length: CGFloat = 1
    var y_length: CGFloat = 1

    override func draw(_ rect: CGRect) {

        draw_axis()
    }
    
    func set_axis(x: CGFloat, y: CGFloat)
    {
        self.x_length = x
        self.y_length = y
        self.setNeedsDisplay()
    }
    
    
    func draw_axis() {

        let p0: CGPoint = CGPoint(x: 150, y: 150)
        let px: CGPoint = CGPoint(x: p0.x + 100*self.x_length , y: p0.y)
        let py: CGPoint = CGPoint(x: p0.x, y: p0.y + 100*self.y_length)
        
        
        var px_tri: CGFloat = 0
        if self.x_length > 0 {
            px_tri = px.x - 10
        }
        else {
            px_tri = px.x + 10
        }
        
        var py_tri: CGFloat = 0
        if self.y_length > 0 {
            py_tri = py.y - 10
        }
        else {
            py_tri = py.y + 10
        }
        
        let con = UIGraphicsGetCurrentContext()!
        
        con.clear(CGRect(x: 0, y: 0, width: 300, height: 300))
        con.setFillColor(UIColor(red: 1, green: 1, blue: 1, alpha: 0).cgColor)
        
        con.fill(bounds)

        con.setStrokeColor(UIColor(red: 1.0, green: 0, blue: 0, alpha: 1).cgColor)
        con.move(to: p0)
        con.setLineWidth(2)
        con.addLine(to: px)
        con.strokePath()
        
        con.setFillColor(UIColor.red.cgColor)
        con.move(to: CGPoint(x: px_tri, y: 145))
        con.addLine(to: CGPoint(x: px.x, y: 150))
        con.addLine(to: CGPoint(x: px_tri, y: 155))
        con.fillPath()


        con.setStrokeColor(UIColor.green.cgColor)
        con.move(to: p0)
        con.setLineWidth(2)
        con.addLine(to: py)
        con.strokePath()

        con.setFillColor(UIColor.green.cgColor)
        con.move(to: CGPoint(x: 145, y: py_tri))
        con.addLine(to: CGPoint(x: 150, y: py.y))
        con.addLine(to: CGPoint(x: 155, y: py_tri))
        con.fillPath()
        
        self.backgroundColor = UIColor(white: 1, alpha: 0.5)
    }

}

~~~

基本上是这样的，如果外部要控制我们的自定义类进行绘制，那么绘制行为必须发生在draw里面，因为我们要使用`let con = UIGraphicsGetCurrentContext()!`来获取一个context，如果不是在draw里面就无法拿到正确的context，至于剩下的绘制细节看代码吧，没有特别多要解释的。

所以基本思路是这样的，外部通过set_axis来设置绘制参数，然后调用`self.setNeedsDisplay()`来通知要更新绘制。然后draw就会完成绘制工作。



然后又要说一下，我们当然希望绘制所在的那个view的背景是透明的，而绘制其上的内容不是透明的，这个要做的方式就是在storyboard设置那个view的alpha为1，然后在绘制时设置self.backgroundcolor是透明的。诶，我这里怎么写0.5?

然后需要注意的一点是，绘制是一个状态机，所以执行新的绘制之前首先要清空内容，然后再绘制，所以有这些代码：

~~~swift
con.clear(CGRect(x: 0, y: 0, width: 300, height: 300))
con.setFillColor(UIColor(red: 1, green: 1, blue: 1, alpha: 0).cgColor)

con.fill(bounds)
~~~



以上就是这两三天我用到的主要技术。也许会有一些遗漏，后续再说。

我正在做的是socket通信，已经找到理清了一份参考代码，明天会尝试做个实验。



### Socket通信

如果要构建处一个Filer的iOS版本，我需要socket通信。

在swift和iOS上如何进行swift编程？从各个地方似乎能搜索到很多不同的建议和只言片语的例子，有的似乎再说标准的NS框架，也有提到来自IBM的bluesocket这样的第三方框架的，我不知道该怎么好了。我期望找到来自官方的，最为推荐的方式。然后我找到了`Network.Framework`，从我搜集到的资料上来看在WWDC2018上苹果专门有一段[演讲](https://developer.apple.com/videos/play/wwdc2018/715)是关于这个新的框架的介绍，我并没有太多的耐心好好看看这段视频，太长了。

然后我找到了一个[博客](https://rderik.com/blog/building-a-server-client-aplication-using-apple-s-network-framework/)，这个博客给出了一个完整的使用上述框架构建的TCP客户端和服务器的例子，感谢作者的代码。拖延症之下，直到昨天晚上我才依据上述代码完成了一份简易的我的代码，然后做了测试，搞定了。

今天开始，我会尽快搭建出一个可以兼容我之前制定的我的应用层协议的socket框架的swift版本。

下面会简单的介绍一下我学到的`Network.Framework`版本的TCP Socket使用方式。

#### TCP服务器

tcp的监听端口使用一个NWListener实例，每个客户端的新链接都是一个NWConnection实例，所有的状态改变和接收等都使用事件回调的方式处理。接下来我会描述一下处理过程

关于地址，默认情况下tcpz服务器的监听地址似乎都是`0.0.0.0`，不需要设置IP就可以，而端口必须是`NWEndpoint.Port(rawValue: )`的实例。

~~~swift
let port = NWEndpoint.Port(rawValue: 5001)!

let listener = try! NWListener(using: .tcp, on: port)
~~~

这样就创建了一个`listener`，然后需要下述代码:

~~~swift
listener.stateUpdateHandler = self.state_change(to: )
listener.newConnectionHandler = self.accept(new_connection: )
listener.start(queue: .main)
~~~

分别设置状态更新的handler和新链接的handler，然后调用start开始监听。我还没搞懂那个queue是怎么回事。

关于`stateUpdateHandler`，listener的状态有五种枚举量：

~~~swift
.setup    //listener被初始化了但并未启动
.waiting  //listener等待网络可用
.ready
.failed   //严重错误
.cancelled  //被取消
~~~

handler是`((NWListener.State) -> Void)?`

`newConnectionHandler`用于接收新链接，要求是`((NWConnection) -> Void)?`

我看到的例子中关于状态的处理只处理了`ready和failed`

基本上就是这样

##### NWConnection

对于一个client的处理方式就是要为他设置`stateUpdateHandler`，设置接收事件的处理函数，然后`start`就可以了

状态有6种：

~~~swift
.setup
.waiting   //链接等待网络路径改变?
.preparing  //链接正在建立
.ready     //
.failed
.cancelled
~~~

例子中按照失败处理了`waiting和failed`，处理了`ready`，其余的未处理

关于`receive`事件

~~~swift
func receive(minimumIncompleteLength: Int, maximumLength: Int, completion: (Data?, NWConnection.ContentContext?, Bool, NWError?) -> Void)
~~~

关于`send`事件

~~~swift
func send(content: Data?, contentContext: NWConnection.ContentContext, isComplete: Bool, completion: NWConnection.SendCompletion)
~~~



基本上要应对的就是这些，然后还有其他的细节，或者更多的功能，可以去看看文档，或者详细的例子，接下来我会专注于构建出来一个框架。



### TCP Socket框架

因为之前的笔记忘记推送进git了，所以我并记不清这个框架我写了几天了。反正整个socket从开始处理到现在已经五天了。

现在是2020.02.02 19:45，哦吼，原来是这个日子。之前网上一直在说这样的日期是有多么特殊，肯定不少人会选择今天结婚之类的，但是现在的疫情实在是相当严重，大概会少很多吧。

欧科，废话不说了。我究竟做了什么呢？之前我已经基本理清了使用`Network.Framework`做tcp socket编程的基本技术，当然之前我写的代码是一个相当粗糙的原型，也会有各种没能处理的`Error`等等，也基本不存在太多的应用层协议之类的。所以，这两三天我断断续续就是完善这些代码，整理出一个类，方便以后的使用，然后也把我之前制定的我的应用层协议整合进来。所以，基本上就是这些。是的，我的标题起的很大，我已经努力了，但是肯定问题还是很多，大概还不够格称为什么”框架”

这两天里遇到了超级多的问题，从一开始的小段存储的无符号整数的二进制处理，到二进制序列的切片，再到接收问题，还有端口的占用等等一系列问题，还有因为我的swift基础不扎实而遇到的各种缺失值处理等等问题，每一个都还是蛮让我头疼的。无论如何总算写出来了。

所以现在的这个”框架"是什么样子的呢？

现在的这个框架还只有TCP服务器端，客户端还没写，但应该会比较简单。

服务端包括两个类，一个是`Messenger`，这是沿用我的python版的协议里的名字，每个实例就是一个客户端链接，然后协议的解析和构造过程被封装在了这个里面，每当有新的客户端链接过来，生成一个实例，启动即可，`Messenger`会自动负责接收信息，解析，同时也提供了发送方法，和python一样，只需要提供header和body即可，同时也会自动处理错误，关闭清理等等。

然后另一个类是`STCPServer`，这是服务器，使用中不需要直接使用`Messenger`，只需要实例化`STCPServer`即可，所有的状态变化，新的连接，客户端断开，错误处理等等都被包含在内了

然后，最重要的是，状态的传递怎么办？我直接按照原本的样子，提供了一系列的callback，每一个有必要的状态变化，例如服务器准备完成，服务器关闭，新链接，接收数据，发送完成，客户端关闭等等都有一系列的callback，只需要给出这些callback，那么这些事件发生时callback就会被调用。

基本上就是这些吧，代码还是直接看代码比较好，我会把这两个类，还有一个示范性的`ViewController`放进script的socket module里面。下面记录一下我学到的比较重要的东西，或者遇到的问题:

~~~swift
// 如何Data <--> UInt16
func UInt162dada(_ value: UInt16) -> Data {
  var b = value.littleEndian

  let s = Data(bytes: &b, count: MemoryLayout<UInt16>.size)

  return s
}

func Data2UInt16(_ data: Data) -> UInt16 {
  return UInt16(UInt16(data[1])<<8 + UInt16(data[0])) //小端
}

// 如何String <---> Data
String(data: self.data.prefix(Int(self.header_length)), encoding: .utf8)
let h = Data(me.utf8)

// Data如何切片，如何获取前m个字节，以及除去前m个字节之外的全部内容
let d = String(data: self.data.prefix(Int(self.header_length)), encoding: .utf8)
self.data = self.data.dropFirst(Int(self.header_length))
// 就是用prefix和dropFirst，我用过范围索引的语法[..<m]这样的，莫名其妙总会出现几个字节的不符
~~~

关于数字的转换部分[这份代码](https://gist.github.com/bpolania/704901156020944d3e20fef515e73d61)给我提供了重要参考



另外一个最最重要的点，NWConnection的每次receive都需要重新设置receive，每个receive handler的后半部分都可以这样写：

~~~swift
if complete_flag {
  self.close(error: error)
}
else if let error = error {
  self.close(error: error)
}
else {
  //            print("setup recive again")
  self.connection.receive(minimumIncompleteLength: 1, maximumLength: 65536, completion: self.recv_handler)
}
~~~

以上代码都是截取的一些片段，不必执着细节，懂意思即可。



然后还有一点，知道的，如果服务端首先断开连接，那么相同端口会被占用一段时间，怎么检测`NWListener`的端口占用错误呢？当端口被占用时，会触发一次`.failed`状态，处理即可。



必要的时候，多看看[官方文档](https://developer.apple.com/documentation/network/nwconnection)



进度 2020.02.03 今天开始尝试使用swiftui构建出一个界面来，首先我瞄准了聊天界面，距离搞定还有非常远的距离，今天最大的进步是制作出了气泡对话框，难点主要包括了如何让消息有一个最大宽度，诀窍是我自己想出来的，用了一个Spacer(minLength:100)这样的，然后用path绘制的小尾巴，组装出来了左右对话框，然后也做出了一个简单的界面原型，当然问题还多的是，我现在还不知道怎么动态添加消息，滚到到底部也没搞定，等等。