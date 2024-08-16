## Redesign

首先，我们要明确我们需要什么。

### main.py

初始化game，初始化声音。屏幕设置模式。clock初始化，并进行刷新率的设置。

新建game_manager。主要在后面的显示中，使用他的update函数来变化。

### game_manager.py

初始化好设置的属性，使用load来加载地图的信息。

load函数：打开我们的配置文件。初始化墙(walls,load_walls），初始化玩家（load_player）。

update函数（主要开放给main使用）：调用player和walls的update。时时刻刻的检测是否有碰撞。显示player和wall。

>区别:blit 和 draw
>
>blit是把一个图像（Surface对象）绘制到另外一个图像上。
>
>```surface.blit(source, dest)```
>
>draw是在Sprite Group上绘制精灵对象。```group.draw(surface)``` 其中，将group对象绘制到surface上面。
>
>举例子就是：```self.walls.draw(self.screen)``` 把walls绘制到screen上面。```self.screen.blit(self.player.image, self.player.rect) ```在屏幕上把player的图片绘制到rect这个位置上面

### player.py

主要设计的部分

#### 属性：

长、宽，旋转角度。image，rect加载。move相关的参数。声音参数

#### 函数

input()函数来控制前后左右，通过控制move_velocity,移动速度和加速度和时间有关。通过控制rotate_velocity来控制左右的移动。

move()函数来控制车辆的移动，通过rotate和move速度之间的关系，以及angle，得到一个可以移动

rotate()函数，通过rotate_velocity和delta_time来得到每帧所要旋转的角度。

move()函数，通过对象当前的move_velocity direction forward_angle来计算得出x和y方向上的速度分量。得到vx和vy然后再乘上时间，得到移动的距离。来更新rect.x和rect.y

Update()函数随时运行，主要来得到delta_time，检测input()，更新move().

Crash()函数，找到函数的时候，直接反向，并且速度不要求过快。

##### 我的理解和优化方向：

对于车的倒车的时候的方向，应该进行修改。

最近开车发现我的倒车水平很一般，可以做一个倒车的游戏。但是如何优化好这个倒车的速度还有方向的控制很关键。

还可以绘制好每一关的内容，把star放在车库里面，看你能停够多少个库。如果碰撞呢？也可以用一个参数记录。时间也可以记录。最后当你完成所有库的停放，或者游戏的时间到了之后，就结束游戏进行结算。

选择关卡的步骤，我们必须通过了当前这一关才能进行下一关。

之后就可以自由的选择关卡。

---

#### 如何切换关卡

从头来分析，首先是我们的main.py函数中一定有所体现。

首先，要有success_time = -1 。每当我的成功的时间大于0的时候，判断是否超过了2秒，之后还需要判断是否有下一关，如果有，那么就应该加载下一关。

#### 判断什么时候游戏进入下一关

运行的时候，running。在每次的update的时候都会判断是否游戏结束，然后获取到结束时候的这个success_time（通过后面一个链条来判断并得到这个时间）。循环中，判断success_time是否改变，改变之后是否当前时间-结束时间>2s，是否有下一关，如果没有就退出。有的话在这里直接跳到下一关（next_level）。

#### 我出现了不能跳出到下一关，问题出现在哪里？

我的success_time 始终没有变化。对问题就出现在这里。在后面我们是通过一个对于update函数来返回true or false，判断是否更新这个success_time.如果这个判断始终进不去，那么就会让success_time 始终没有改变。

最后在代码阅读的时候，通过肉眼判断，调用逻辑上：

##### success_time的逻辑链条

success_time ----> manager_update ----> success(bool) ----> check_collision ----> stars_count == 0 and collision with target.

在这个逻辑链条上，check_collision,需要进行一个判断，但是这里调用了两次。导致第一次的时候判断过了返回值并没有给success。第二次的时候可能产生none。返回给了success导致卡住。







