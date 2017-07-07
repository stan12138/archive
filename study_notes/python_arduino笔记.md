###python与arduino

---

现在，我是使用`serial`库完成python与arduino之间的通信的
通信自然分为两个方向，python->arduino,  arduino->python

我觉得后者简单，前者复杂

下面将会记录两段代码，然后就不再详细解释了


	python端

	import serial
	import time
	
	
	s=serial.Serial("COM5",timeout=5)
	serial.Serial()
	time.sleep(5) # wait a couple seconds
	l = ['hello','this','is','stan','bye']
	for i in range(5) :
	    a = l[i].encode('ascii')
	    s.write(a)
	    c = s.readline()
	    print(c.decode('utf-8'))
	
	s.close()


	arduino端


	String co = "";
	String c = "hello";
	boolean flage = false;
	
	
	void setup()
	{
	    Serial.begin(9600);
	}
	
	void loop()
	{   
	    while(Serial.available()>0)
	    {
	        co += char(Serial.read());
	        delay(2);
	    }
	    if(co.length()>0)
	    {
	        Serial.print(co);
	        Serial.print("\n");
	        co="";
	    }
	}


第二段


	python端

	import serial
	import time


	s=serial.Serial("COM5",timeout=5)

	time.sleep(5) # wait a couple seconds

	while True :
    	a = input("please:\n")
    	if a=='stop' :
        	s.write(b'0')
        	break
    	else :
        	a = a.encode('utf-8')
        	s.write(a)
	s.close()


	arduino端


	int a=0;
	boolean flage = false;
	void setup()
	{
	    Serial.begin(9600);
	    pinMode(13,OUTPUT);
	}
	
	void loop()
	{   
	    while(Serial.available())
	    {
	        a = Serial.parseInt();
	        flage = true;
	    }
	    if(flage)
	    {
		    if(a==1) digitalWrite(13,1);
		    if(a==0) digitalWrite(13,0);
		    flage = false;
	    }
	}

稍微解释一下，arduino接收字符串的话，使用read()往原有的字符串后增加，使用available()来持续接收，但是要注意延时很重要，十分重要，不延时的话available()无法拿到准确的剩余字节数，从而会收到一个字符就跳出，有些词不达意，大概就是这个意思，另外，暂时不清楚原因，不建议使用println()来产生带有换行的发送数据，因为使用这个python收到的数据总是会带有两个换行标志，所以建议手动产生

第二段很明显针对的是发送整数，此时python发送的依旧需要是二进制字符串，接收部分直接使用parseInt()

其他的暂时就不说了



###arduino通信技术

串行与并行通信的差异无需多言。 
arduino配备的串行通信技术有：通用同步/异步串行收发器（USART）,串行外设接口（SPI），两线数据接口（TWI）  
另外还有一个名词：在线系统编程（ISP）  
至于同步异步，全双工，非归零码就不再多说  
RS-232系统一个重要的特性是所谓电平特性，它不使用5V/0V的电平，而是为了应对远距离信号传输使用了+12V/-12V，可以通过MAX232芯片完成这种电平转换  
电脑上已经没有RS-232接口了，该接口有两种类型，9针和25针，只需要知道里面有信号地，RXD,TXD三根线  
所谓TTL电平就是标准的5V/0V的电平  
USB接口四根线，分别是vcc，gnd,data+,data-  

####USART
UART是只有异步的，通信速率低。   
USART是全双工的

####SPI
SPI更快，但是需要一根额外的时钟线，LCD和SD卡均使用这种方法。  
四根线MOSI/MISO负责数据传输，SCK负责时钟，SS负责片选，一块芯片的片选被拉至低电平时被选中。


所谓ISP在线编程并不同于平时使用的USB编程