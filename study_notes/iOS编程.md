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





