施工防护结构的静力计算
=====================

分析某路桥施工防护结构中的一个承重桁架，如图1所示。在城市立交桥等市政工程的修建过程中，桥下施工防护经常采用多榀桁架结构来承重。图中两榀桁架通过角钢横撑连接，形成一个组合的空间钢桁架。

![图1 承重桁架的立面图和剖面图](https://github.com/windstriver/ansys-example/blob/master/STATIC-3D-BEAM188%26LINK180-Truss/problem_pic.png)

![](https://github.com/windstriver/ansys-example/blob/master/STATIC-3D-BEAM188%26LINK180-Truss/problem_pic2.png)

在分析过程中，所有弦杆（上、下弦）、端部的竖杆、横向撑杆均采用 BEAM188 单元来模拟，除端部竖杆之外的所有斜腹杆均采用桁架单元 LINK180 来模拟。

本例题说明的问题为：
- 梁、杆单元的混用
- BEAM18X 单元库的使用
- BEAM18X 单元用户自定义任意截面的方法
- BEAM18X 单元定位节点的使用
- 后处理：荷载工况的组合方法

### 1. 创建梁截面文件
由于桁架的上下弦为双角钢组合截面，而在 Mechanical APDL 中提供的标准梁截面库中没有这种现成的截面，因此需要使用自定义截面功能建立截面文件，以供后续结构建模时采用。

```
! 定义双角钢截面的命令流
/PREP7
ET, 1, MESH200 !定义辅助单元类型
KEYOPT, 1, 1, 7

! 建立截面关键点
K, 1, 24
K, 2, 99
K, 3, 99, 8
K, 4, 32, 8
K, 5, 32, 75
K, 6, 24, 75
! 创建双角钢截面
A, 1, 2, 3, 4, 5, 6
ARSYM, X, ALL

! 划分截面网格
AESIZE, ALL, 20  !指定划分面网格的尺寸
AMESH, ALL

! 写梁截面文件
SECWRITE, DLA, sect

FINISH
/CLEAR
```

上述命令执行后，用户自定义截面完成，截面信息写入工作目录下的 DLA.sect 文件中，此截面文件即可在后续的结构分析中引用。创建截面的过程中采用了 Mesh200 单元对面进行划分截面网格，计算中按照截面网格信息来计算截面积、惯性矩以及形心、剪心坐标等几何量。

MESH200 单元的 K1 选择 QUAD 8-NODE 选项，这是由 BEAM18X 的截面积分算法所决定的，可参考单元手册。

遇到的困难：如何自定义有间隙的双肢角钢

### 2. 结构建模与分析
下面进行结构建模、加载与计算，采用 N-mm-t 单位系统，密度的协调单位为 t/mm^3。

桁架底部搁置在钢梁上，分析中采用铰接约束，左端底部两个脚点施加 X、Y、Z三个方向的约束，右端底部两个脚点施加 Y、Z 两个方向的约束。在计算中考虑两种荷载工况：桁架结构的自重、上部活荷载传至桁架节点的集中力。对两个工况分别采用不同的荷载步进行求解，然后在通用后处理器中进行荷载工况的组合计算。

```
!****************************************************************************
! 空间桁架静力分析
!****************************************************************************
/FILNAME, truss
/TITLE, Static Analysis of a 3D Truss

/PREP7
ET, 1, BEAM188
ET, 2, LINK8
R, 1, 1900
R, 2, 960.6
MP, EX, 1, 2.06E5
MP, PRXY, 1, 0.3
MP, DENS, 1, 7.85E-9

! 读入用户自定义截面文件
SECTYPE, 1, BEAM, MESH
SECOFFSET, USER, 0, 37.5
SECREAD, 'DLA', 'sect', , MESH
SECPLOT, 1, 1
SECTYPE, 2, BEAM, CHAN, 
SECOFFSET, USER, 24, 50
SECDATA, 48, 48, 100, 5.3, 5.3, 5.3
SECTYPE, 3, BEAM, L
SECOFFSET, CENT
SECDATA, 50, 50, 5, 5

! 定义下弦两关键点
K, 
K, 33, 19200
KFILL
! 复制形成上弦关键点
KGEN, 2, ALL, , , , 500, ,33, 0

! 创建一榀桁架几何模型的直线
*DO,I,1,32
    L, I, I+1
    L, I+33, I+34
*ENDDO
*DO, I, 1, 31, 2
    L, I, I+34
    L, I+2, I+34
*ENDDO
L, 1, 34
L, 33, 66
! 创建空间梁单元的方向定位关键点
K, 100, 0, 1000
K, 101, 19500
! 指定线的单元属性
LSEL, S, LENGTH, , 600
LATT, 1, 1, 1, , 100, , 1
ALLSEL
LSEL, S, LENGTH, , 500
LATT, 1, 1, 1, , 101, , 2
ALLSEL
LSEL, S, LENGTH, ,700, 800
LSEL, U, LINE, , 65, 96, 31
LATT, 1, 2, 2, , , , 1
ALLSEL
LSEL, S, LINE, , 65, 96, 31
LATT, 1, 1, 2, , , ,1
ALLSEL
LESIZE, ALL, , , 1

LMESH, ALL
! 压缩节点编号
NUMCMP, ALL

! 创建另一榀桁架
NGEN, 2, 132, ALL, , , , , 500, 1
EGEN, 2, 132, ALL, , , , , , , , , , 500

! 创建两桁架间的横撑
TYPE, 1
MAT, 1
REAL, 1
SECNUM, 3
*DO, I, 5, 129, 4
    E, I, I+132
*ENDDO
*DO, I, 7, 127, 4
    E, I, I+132
*ENDDO
E, 4, 136
E, 1, 133
E, 2, 134

EPLOT
/ESHAPE, 1, ON
/REPLOT
FINISH

/SOLU
D, 1, , , , , , UX, UY, UZ
D, 133, , , , , , UX, UY, UZ
D, 127, , , , , , UY, UZ
D, 259, , , , , , UY, UZ

ANTYPE, STATIC
TIME, 1
ACEL, , 9800
SOLVE
TIME, 2
NSEL, S, LOC, Y, 500
F, ALL, FY, -436.4
ALLSEL
ACEL, 0, 0, 0 ! 删除荷载步1中的重力加速度
SOLVE
FINISH

```

### 3. 结构后处理
后处理的操作命令流如下，其中工况定义时按 1.2x恒载+1.4x活载 来指定工况组合系数：

```
! 进入通用后处理器
/POST1
! 观察工况2的结构变形情况
PLNSOL, U, Y, 0, 1.0  ! 观察 Y 方向位移等值线图
! 荷载工况的定义
LCDEF, 1, 1, 1  ! 从结果文件创建荷载工况1
LCDEF, 2, 2, 1  ! 创建荷载工况2
! 定义荷载工况组合比例系数
LCFACT, 1, 1.2  ! 定义荷载工况1的比例因子
LCFACT, 2, 1.4  ! 定义荷载工况2的比例因子
! 读入荷载工况1
LCASE, 1        ! 将一个荷载工况读入数据库
! 荷载工况的组合
LCOPER, ADD, 2
! 定义内力组合后的单元表
ETABLE, AxialF, SMISC, 1 ! 定义显示I端轴力的单元表
! 查看内力组合后的桁架轴力图
PLLS, AxialF, AxialF, 1, 0
! 写入荷载工况组合文件
LCWRITE, 3, Combined Results

FINISH
SAVE
```
