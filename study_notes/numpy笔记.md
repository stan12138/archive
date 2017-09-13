##### 图片
array(open('test,jpg')),可以将图片转换为numpy的array,使用Image.fromarray(arrray)可以将array转换为Image对象，如a=fromarray(b),a.save('new.jpg')即可将其保存为JPG图像

##### 插值
numpy的线性插值函数interp很有用，用法interp(x,xp,fp),xp,fp相当于一组x,y，直观一点说，相当于会根据xp,fp画出一个曲线，点与点之间以直线连接，x相当于一组给定的横坐标，这个函数会根据已经画出来的曲线，找出这一组x对应的纵坐标值。所以说在灰度值映射的时候，先根据已知函数计算出来把0-255映射给一个新的范围fp,此时，将xp设置为range(256),将已经扁平化的图像的一维数组作为x,传入interp即可

##### 超出范围的uint8
再次说明，numpy中的uint8()的转换是存在缺陷的，例如uint8(-1)=255,uint8(256)=0之类

