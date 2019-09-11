from PIL import Image
import numpy as np

a = np.asarray(Image.open('C:/Users/WXYZ/Desktop/小Q书桌-截图/百合心.jpg').convert('L')).astype('float')

#立体效果
#灰度代表图像的明暗变化，而梯度值就是灰度的变化率。我们可以调整像素的梯度值来间接改变图片的明暗程度
#立体效果由添加虚拟深度值来实现。深度值乘以方向梯度值，来添加深度对于梯度的影响因素。
depth = 10.                        # (0-100)
grad = np.gradient(a)              #取图像灰度的梯度值
grad_x, grad_y = grad              #分别取横纵图像梯度值
grad_x = grad_x*depth/100.
grad_y = grad_y*depth/100.
A = np.sqrt(grad_x**2 + grad_y**2 + 1.)
uni_x = grad_x/A
uni_y = grad_y/A
uni_z = 1./A

#明暗效果——灰度
#计算光源对各个坐标轴上的影响因子。这里我们取Elevation为80°，Azimuth为45°。
#dx，dy，dz为光源对x，y，z轴的影响因子，值均在0~1之间。
#个人的理解是dx，dy，dz是光线向量在像素点构成的坐标系上各坐标轴的分量，
#没能理解为什么可以是光源对坐标轴的影响因子并在之后乘以梯度可以添加明暗效果。
vec_el = np.pi/2.2                  # 光源的俯视角度，弧度值
vec_az = np.pi/4.                   # 光源的方位角度，弧度值
dx = np.cos(vec_el)*np.cos(vec_az)  #光源对x 轴的影响
dy = np.cos(vec_el)*np.sin(vec_az)  #光源对y 轴的影响
dz = np.sin(vec_el)                 #光源对z 轴的影响

#图像重建
b = 255*(dx*uni_x + dy*uni_y + dz*uni_z)    #光源归一化
b = b.clip(0,255)
 
im = Image.fromarray(b.astype('uint8')) #重构图像
im.save('C:/Users/WXYZ/Desktop/小Q书桌-截图/百合心_1.jpg')
print('图片已转换！')
