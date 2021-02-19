
# Politiciant faces in NHK TV news

## 1. Backgournd

研究大量新闻视频中政治人物在新闻中出现的creen time的意义。

 - 人物的影响度随时间的变化
 - 政党的影响度随时间的变化
 - 不同政党和政治人物之间的关系
 - 新闻媒体对政党或政治人物有不同的偏向

使用人脸识别和人脸追踪准确获得不同政治人物出现在电视新闻中的creen time。
 - 要比通过从字幕中提出政治人物的名字更有效
 - 深度学习技术的发展使得人脸追踪结果能够快速且准确的完成
 - 方法: 人脸检测 -> 人脸识别
 - 对于海量新闻视频数据的人脸检测的挑战：在长的时间范围内人会随着年龄的不同，脸部会有变化，影响是别的准确度。


人脸是有明显的特征的，所有人的脸都有相同的五官布局。
评估人脸追踪的结果
 - 如何有效的评价人脸追踪的结果
 - 如何评估不同时间的检测结果

## 2. Introduction

本文的主要贡献：
- 强调了对与大型视频数据考虑到能够识别不同时间范围内人脸的重要性，对比了两种不同人脸识别方法。有效识别在不同时期的同一face
- 本文介绍了一种新的评估检测结果在不同时间段一致性判断的方法
- 视觉化对比了日本不同政党及个人在一定时间段内的电视新闻中的曝光度

## 3. Related work

- 政治人物Screen time的研究
- face tracking & recognition
  - Face detection and facial landmark localisation procedure at each frame, then using similarity learning methods.
  - Perform face detection in the first frame and then applies facial landmark localisation at each consecutive frame using the fitting result of the previous frame as initialisation, face detection re-applied in case of failure.
- Evaluate the tracking results

## 4. Method
这一章介绍获得新闻视频中政治人物screen time的方法。因为对于新闻视频数据，Face shape doesn't change abruptly between the consecutive frames。In our method we apply face detection and facial landmark localisation procedure at each frame, then use similarity learning methods. 本章先介绍了人脸检测方法，我们通过使用基于深度学习的MTCNN人脸检测方法，检测出视频每一帧中的人脸。我们然后使用深度学习网络提取检测出的人脸特征，将该特征值与已有的目标人脸特征值进行匹配，从而识别出人脸。结合以上两个步骤，我们获取了目标政治人物的screen time，我们将完整的计算流程图在本章做以介绍。

### 4.1 Face Detection
对于视频的每一帧图像，我们使用了MTCNN(Multi-task Cascaded Convolutional Networks)(ref)去检测人脸五官的位置，MTCNN有着很高的检测成功率，并且运行速度也很快，这就保证了我们可以实时的进行每一帧的facial lanmark localisation. 

、、、
（fig 如图所示，对于每一帧图像，人脸五官的位置被检测出来）
、、、

要获得人脸在视频中持续时间，除了检测每一帧的人脸数据，还需要判断相邻帧中出现的人物是否相同。因为新闻中人脸位置相对稳定，没有突然的距离和形状的变化。所以我们将相邻帧中五官位置和大小相近的两个脸视为同一个人出现在不同的两帧中。当相邻两帧中的人脸数量有变化，或者人脸位置有明显变化的时候，我们需要通过人脸识别的方法来判断相邻两帧中出现的人脸是否统一。

、、、
在连续视频中，如果人物在讲话或者运动，那么随着人头的转动，就可能无法准确检测出面部位置MTCNN能够很好的检测出侧面人脸五官位置，对于极少数的背身或者低头情况，也可以通过完善追踪方法而提高获得视频时间的准确性。在4.3节中会具体介绍如何完善追踪方法。
、、、




、、、

（配图，将同一人，不同的姿势展示，包括低头，如何有效识别该过程的视频时间）
(fig 配图展示了人脸检测的步骤)

、、、

### 4.2 Face Recognition


、、、

对于人脸识别，已经有了很多研究，常用的做法是将人脸通过深度卷积网络（ref）。（facenet介绍。）

facenet 能够有效的比较侧脸和正脸的相似度。如图所示（）

为了识别出我们想要的20位政治人物，首先我们寻找了这20个政治人物的照片作为参照，然后对于视频中提取出来的人物照片与已获得的参照照片进行相似度比较，当相似度达到我们设置的阈值时，我们将视频中的人脸标记为目标人物。
、、、

新闻中的人脸能够较快且准确的检测出来，但是识别出检测的人脸是谁就是一个相对而言更难得问题。一方面是因为我们所采用的视频分辨率不够高，另一方面是因为在较长的时间，人的面容是有所改变的。对于同一视频中的同一人脸，我们能够较准确的判断出是否是同一个人，因为在一个新闻视频中，人脸并不会发生较大的改变。但是不同的视频中，人脸是有改变的。

、、、

我们使用了两个不同的trained model去完成人脸识别。
在最初的研究中，我们使用resnet-v1 architecture 基于普通的人脸数据库进行的训练，但是取得的最后准确度却不高，我们意识到，对于10年的视频数据，时间是比较长久的，不同时期的视频中，人脸还是有或多或少的改变。

（如图所示，我们节选了不同时期的**的照片，虽然人可以很直接的识别出这是同一个人，但如何让电脑有效的准确识别出这是同一个人是有难度的）


我们可以通过准备不同年龄政治人物的照片模板，将视频中人脸与各个不同时期的模板进行比较，但这无疑增加了工作的繁琐度，并且不一定能够提高准确度。为此一个能够识别不同年龄的model就很必要。
随着训练数据的完善，已经有了跨年龄的数据集，for example VGGFace2 is a large-scale face recognition dataset. Images are downloaded from Google Image Search and have large variations in pose, age, illumination, ethnicity and profession ()。
我们使用了vggFace2训练的model，将其用到了我们人脸识别的过程中，而这种跨年龄的识别模型，可以有效的提高数据的识别准确率。在后面的研究中，我们详细对比了两中不同模型所检测结果的差别。


、、、

本文中是将人脸特征值转换为128维向量，然后计算向量之间的cos距离。

如何有效的提取人脸特征值。


 - Facenet
 - VGG2 face dataset

有两种方法
 - 有个不同时期的人脸的ground truth 照片，将每帧中的人脸和同一人的不同时期的脸比较
 - 拿不同人脸的数据训练，让计算机能够认出不同时期的同一个人。

是否训练能否识别不同时期的同一人的脸部数据是很重要的，对比了识别结果。


、、、


、、、

### 4.3 Tracking method

结合前两部分的技术，我们系统就能够追踪到目标政治人物的screen time了，这里具体介绍流程。

本文使用第一种方法，
 - 选择了需要识别的20个政治人物，学习每个脸的特征值
 - 我们在每帧使用mtcnn提取每个人脸的五官位置
 - 相邻帧的五官的位置如果没有发生，我们就认为其是同一个人，
 - 如果相邻帧的五官位置发生了较大的变化，将新检测出的人脸与前一帧中的人脸对比，如果是第一次出现，提取该面部的特征值，将其与第一步学习到的20个脸的特征值进行对比，如果符合20个脸的阈值，将其进行标记。

、、、
1. 学习目标20个政治人物的面部特征，获得每个人物的面部特征向量 (template vector)，我们追踪的过程就是寻找视频每一帧里与template vecotr相似的人脸。
2. 对于视频的每一帧图像，使用MTCNN dector检测 facial localisation，将检测到的localisation与前一帧中的人脸五官位置比较，如果与前一帧的五官位置相同，则默认该面部与前一帧相同位置的面部五官位置是同一个人。
3. 如果这一帧的人脸数量与前一帧相比发生了改变或者脸部位置发生了较大改变，则将这一帧提取的人脸与前一帧中的人脸进行特征比较，如果满足一定相似度，则标记为与前一帧的人脸相同。如果与前一帧中的人脸不同的话，则将该脸与视频中之前出现的其他人脸进行相似度测试，如果有相同的人脸的话则标记为已知的人，如果没有的话，则将面部特征与20个target template vector进行比较，如果有满足相似度的，则标记为target人物，如果没有满足相似度的话，则将该人物标记为非目标人物。
4. 为了提高 tracking performance. 每一个视频的检测过程中，我们建立人脸vector栈，当有与前一帧不匹配的人脸出现时，首先将其与该视频人脸vector栈中的人脸进行匹配，当有匹配的面部数据时，则将确认为已知人物，如果与vecotor栈中的人脸不匹配或vector栈为空的话，则将其与20个template vector进行匹配，如果有匹配的，则将该脸标记为target face‘s name，并且将其vector放入人脸vector栈中。如果没有匹配的话，则将其标记为非目标人物，也将其facial vector放入vector栈中。


对于这个tracking流程有以下三点需要补充解释的：
在第二步中，出现在连续帧中同一位置的人脸默认为同一个人，以减少计算量，提高运行时间，只要当相邻帧中人脸位置发生较大改变或人脸数量发生改变时，才通过相似度比较来确认是否为同一个人。
facial vector栈的目的是减少匹配次数，每条新闻视频中出现的人物数量多数情况下少于20个的，当有新的未知人脸出现，只需要与之前出现的人脸先对比，而不用每次都和20个template比较。

在视频中，当目标人物正在演讲时，有可能因为其头部运动，比如低头或转头，而发生无法检测到人脸的情况，如图所示。在实际的tracking过程中，如果个别帧目标人脸丢失，但是目标人脸再次出现在相同屏幕位置且与上次出现的时间差小于1秒，统计该人脸出现的screen time的时候忽略中间人脸检测缺失的情况，认为其一直出现在视频中。
(fig 如何有效处理检测不到人脸的情况)

、、、

### 4.3 Comparison
将识别结果与 ground truth进行判断。

 - General comparison
 - Kendall tau rank correlation coefficient time domian

## 5. Results

## 5.1 Validation the tracking results

ground truth data进行比较

## 5.2 Comparisons of tracking results



## 6. Discussion


1. 文字提及次数和人脸数据的不匹配
2. 人物的政治倾向，电视台的政治倾向，如何随着时间变化。（不同政党的时间区域面积图）
3. 各个政党中不同人物所占的比例
4. 视频中的时间和出现在视频中的次数的相关性。
5. 提及姓名与视频出现在同一个segment的相关性研究。（Pearson correlation coefficient）


## 6.1 The necessity of using face tracking

## 6.2 What learned from tracking results

## 7. Clusion



人脸检测的有效性

人脸检测的准确性

考虑到人脸随时间变化的必要性

如何对比大的数据集的测试结果是随着时间发生的变化。

分析追踪后的结果准确性

分析追踪后的影响力分析

1.介绍

1. Backbone

a. 目的

人脸追踪用于研究政治人物在视频中露脸的时间，是一种研究政治人物或政党影响力的有效途径。研究新闻视频中政治人物的出现时间主要有两个步骤，一个是人脸检测，确定每一帧人脸的位置，然后是人脸识别，鉴别出所检测出的人脸是否是所需要的目标任务。对于海量的新闻视频数据，因为新闻中的人脸会受到pose以及遮掩物的影响，并且在较长的时间范围中，多个不同视频中的同一个人的脸是有变化的，如何有效的检测追踪海量数据中的人脸并准确识别出人脸是一个挑战。对于追踪检测结果，如何有效的评价检测的准确率又是一项挑战。在本文中，对比了两种不同的人脸追踪方法，展示了一种对比不同时间范围内检测结果准确性的方法。并通过人脸的screen time研究不同政治人物以及政党在不同时间的影响力，以及他们之间的相关性。


b. 方法
人脸检测和追踪可以通过深度神经网络来准确快速的实现。在文中使用不同的人脸识别方法，强调了对于大的视频数据，要提高人脸追踪识别的准确性，必须考虑到人脸在较长的时间是有变化的，要结合新的方法以提高追踪的准确率。

c. 结论

对于长期的不同年龄的人脸数据也越发的完善，文中讨论了对于大的视频数据采用across age的识别前后结果的差异。人脸识别在用于分析screen time中的必要性，研究人物的screen time比研究其名字出现在新闻中的次数更能准确了解新闻人物的影响度。文中将人脸出现的次数和字幕提及的人物名次数进行了相关性研究，以证明

获取视频新闻中人物的方法，通过文字或语音识别从字幕中提取人物的名字，或者通过face detection and tracking 识别出现在新闻中的人物。

通过配音来追踪新闻中出现的人物有两个问题，第一个是无法获得人物出现在视频中的确切时间，第二个是新闻中介绍人名并非全名，称呼也会随着其职位的变动而发生变化，比如日本首相在视频中会被称为等多种不同的形式，而在。所以说在长期的数据中，并不能通过检测政治人物的名称来获得视频中人物出现的时间。论文中将

2. Result

Experiments


3. Face tracking

3.1 Face detection

3.2 Face Recognition


Tracking by detection


4. Evaluation

4.1 Evaluate the results over time

5. Results interpretation

6. Conclusion


相关性研究

truth face times 823
same face time 529
face total time 672
missing face time 294
wrong face times 143