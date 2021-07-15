# 自动驾驶汽车数据集的历史和三个可视化的开源 Python 应用程序

来源：[The history of autonomous vehicle datasets and 3 open-source Python apps for visualizing them | by plotly | Plotly | Medium](https://medium.com/plotly/the-history-of-autonomous-vehicle-datasets-and-3-open-source-python-apps-for-visualizing-them-afee9d13f58a)

```{describe} AV
autonomous vehicles
```

## 从 KITTI 到 Motional 和 Lyft：为 AV 社区提供 7 年的开放数据集

[KITTI Vision](http://www.cvlibs.net/datasets/kitti/) 基准于 2012 年作为一篇 [研究论文](http://ww.cvlibs.net/publications/Geiger2013IJRR.pdf) 发表，它是第一个公开可用的评估基于汽车导航的计算机视觉模型的基准。通过在 [德国的一个乡村小镇](https://www.google.com/maps/place/Karlsruhe,+Germany/@49.0158279,8.3394947,25288m/data=!3m2!1e3!4b1!4m5!3m4!1s0x47970648a2e07809:0xb6fc55734cb7ee7f!8m2!3d49.0072492!4d8.404541) 上行驶 6 个小时，它收集了实时传感器数：GPS 坐标、视频反馈和点云(通过激光扫描仪)。此外，它还提供了3D边界框注释、光流、立体和各种其他任务。通过建立能够准确预测这些标注的模型，研究人员可以帮助自动驾驶汽车系统准确地定位车辆/行人，并预测物体/道路的距离。

2019 年，[Motional](https://motional.com/) 的研究人员发布了 [nuScenes](https://www.nuscenes.org/，这是一个在新加坡和波士顿收集的超过 1000 个场景的开放数据集。在不同气象条件下(雨夜时间)共采集 1.5M 彩色图像和 40 万激光雷达点云。为了帮助浏览这个数据集，作者还发布了一个 [Python 开发工具](https://github.com/nutonomy/nuscenes-devkit)，用于方便地检索和读取给定场景中收集到的传感器数据。它还包括绘制每个图像上点云的静态 2D 渲染的功能。

同年，Lyft 发布了他们的 Level 5 (L5) 感知数据集，包含超过 [350 个场景和超过 130 万个边框](https://self-driving.lyft.com/level5/perception/)。为了探索这个新的数据集，他们创建了一个 nuScenes devkit 的[分支](https://github.com/lyft/nuscenes-devkit)，并在 Plotly 中添加了转换工具、视频渲染改进和交互式可视化。为了鼓励社区利用数据集建立能够在 3D 世界中检测物体的模型，他们在Kaggle 上发布了 [一项竞赛](https://www.kaggle.com/c/3d-object-detection-for-autonomous-vehicles)，奖金总额为 2.5 万美元。

在 Motional 和 Lyft 的贡献之后，许多汽车公司发布了自己的 AV 数据集，包括 [Argo](https://www.argoverse.org/data.html), [Audi](https://www.a2d2.audi/a2d2/en/dataset.html), [Berkeley](https://bdd-data.berkeley.edu/), [Ford](https://avdata.ford.com/), [Waymo](https://github.com/waymo-research/waymo-open-dataset) 等。

## 基于 Web 的激光雷达点云和边界框可视化工具

学术和行业研究人员发布的数据集不仅庞大，而且高度复杂，需要能够处理其多模态的可视化工具。虽然视频可以逐帧有效地显示，但点云和 3D 边界框需要更复杂的解决方案才能完全显示它们。尽管您可以使用自上而下的视图或将它们投影到视频帧中来将它们可视化，但如果不能通过移动和缩放与数据进行交互，就很难完全理解给定时间点上发生的所有事情。

可以用来解决这个问题的一个库是 [deck.gl](https://deck.gl/)。它由 Uber 创建并由 [vis.gl 团队](https://vis.gl/) 维护，提供交互式 3D 可视化，可以通过 [Mapbox](https://medium.com/vis-gl/deckgl-and-mapbox-better-together-47b29d6d4fb1) 直接与地图集成。在众多的[图层类型](https://deck.gl/docs/api-reference/layers)中，可以找到[点云](https://deck.gl/docs/api-reference/layers/point-cloud-layer)和[多边形](https://deck.gl/docs/api-reference/layers/polygon-layer)，分别用来显示和交互 LIDAR 点云和 3D 边框注释。

虽然由 deck.gl 提供的各种工具是可定制的，可以在各种应用程序中使用，你仍然需要自己实现一切，以构建一个可视化 AV 场景的用户界面。为了简化这一过程，并加快自定义 AV 仪表盘的开发，deck.gl 同一团队幕后建造的 [streetscape.gl](https://avs.auto/#/streetscape.gl/overview/introduction) (也被称为自治可视化系统，或 AVS)，这是一个 React 组件的集合，可以让你用几百行 JavaScript 构建一个完全自定义的 AV 仪表板。当使用 XVIZ 格式记录的数据时，您可以预先生成一个完整的场景并将其加载到客户机的浏览器中，从而实现整个片段的流畅回放。

除了可视化点云和边界框，您还可以创建自定义对象，如汽车网格，记录指标，如加速度和速度，并提供可控制的设置给最终用户，使更细粒度的控制直接在 UI 中。

尽管这两个库对于 AV 研究非常有用，但它们要求用户对 JavaScript、React、Node.js 和 webpack 有一定的熟悉程度。这使得没有专业的前端技术的研究人员和工程师定制解决方案变得更加困难，且减缓 AV 新特性的开发周期，并使这些可视化工具难以与现有的 AV 工具和  Python 中可用的 ML 库集成。基于这些原因，以下 Dash 模板应用程序，可以通过抽象、精简和统一各种开源 AV 库和数据集，帮助 AV 软件、系统和工具的研发。

## Dash1：Dash 中的自动可视化系统(AVS)

Dash 的所有核心组件以及[许多流行的社区组件](https://plotly.com/dash-community-components/)都是使用 React.js 构建的，这与 streetscape.gl 的接口框架是相同的。因此，我们可以先创建一个 React UI 应用，然后使用 [Dash 组件样板](https://github.com/plotly/dash-component-boilerplate) 文件将其包装为自定义的 Dash 组件。这使得您的 UI 使用 `streetscape.gl` 可直接用于用 Python、R 或 Julia 构建的 Dash 应用程序。

在 [Dash AVS 应用程序](http://dash-gallery.plotly.host/dash-avs-explorer)中，你可以播放一个包含场景的交互式剪辑，这是一个汽车旅行的一部分，数据来自激光雷达传感器、摄像头、GPS、汽车本身，以及人类注释(例如边界框注释)。在任何时候，你都可以停止剪辑：

- 通过拖动查看器来四处移动
- 用滚轮放大或缩小
- 通过按住 CTRL 和鼠标拖动倾斜或旋转

通过使用 Dash 的[核心组件](https://dash.plotly.com/dash-core-components)或[社区构建组件](https://plotly.com/dash-community-components/)(如 [Dash Bootstrap](https://dash-bootstrap-components.opensource.faculty.ai/))，你还可以创建自定义组件，让用户对可视化内容有更多控制。你可以直接选择各种地图样式，数据集和场景 URL，以及你是否想使用基本版或高级版的 UI。有了这些输入，您可以简单地创建一个 `BasicUI` 或 `AdvancedUI` 组件，并将包含日志的 URL 作为参数传递。

整个应用程序用不到 200 行 Python 代码编写，可以通过 [Dash Enterprise 的应用程序管理器](https://plotly.com/dash/app-manager/)轻松部署和扩展。

## Dash2：用 dash-deck 可视化 Lyft Perception 数据集

第二个应用程序可以让你探索来自 [Lyft 感知数据集](https://self-driving.lyft.com/level5/data/) 的特定场景。你可以通过点击其中一个按钮或拖动滑块来在帧之间导航来设置场景的确切时间。通过 [dash-deck](https://community.plotly.com/t/initial-release-of-dash-deck-a-library-for-rendering-webgl-3d-maps-with-pydeck-and-deck-gl-in-dash/44528)，交互式查看器在给定的框架上显示点云和边界框注释，与第一个应用程序类似。你可以在不同的地图视图、LIDAR 设备、摄像头之间进行选择，并在图像上切换各种叠加。

这个应用程序和第一个应用程序之间的区别是显而易见的，一旦你看了实现细节。如果您希望在可视化中获得更大的灵活性，并希望使用完全面向 Python 的解决方案，您可能会对使用 [pydeck](https://pydeck.gl/) 感兴趣，这是一个用于呈现 deck.gl 的 Python 接口。虽然需要更多的调整和定制,你可以有更多的控制应用程序的开发过程中。例如,您可以决定哪些颜色每个点云，点云的不透明度，网状的确切形状物体，相机的起始位置和角度(可轨道（orbit），第一人称或地图视图)。

另一个主要的区别是，Dash AVS 要求您首先将数据转换为 XVIZ，然后再服务或流媒体场景给用户。另一方面，这个应用程序可以很容易地修改为使用任何可能的数据格式，只要你能将输入预处理为 pydeck 或 [dash-deck](https://community.plotly.com/t/initial-release-of-dash-deck-a-library-for-rendering-webgl-3d-maps-with-pydeck-and-deck-gl-in-dash/44528) 所接受的格式。这背后的原因是，所有事情都是动态地、实时地完成的。事实上，每当用户选择特定的帧时，就会发生这样的情况：

1. [Lyft/nuScenes SDK](https://github.com/lyft/nuscenes-devkit) 检索当前帧，并加载点云、注释和摄像头捕获的图像
2. [Pandas](https://pandas.pydata.org/) 用于对点云进行预处理
3. Pydeck 构造点云和多边形层
4. [Pyquarternion](https://pypi.org/project/pyquaternion/) 将点云和方框投射到图像上
5. [Dash Deck](https://github.com/plotly/dash-deck) 和 [Plotly Express](https://plotly.com/python/imshow/) 分别渲染甲板查看器和图像图形

所有这六个库都可以通过 Python 访问。事实上，前四个库并不是专门为 Dash 设计的。它们只是开箱即用，因为 Dash 被设计成可以与大多数 Python 用例无缝工作。这意味着你可以很容易地修改这个应用程序来执行实时处理，例如使用 PointNet 在显示帧之前进行 [3D 网格生成](https://towardsdatascience.com/5-step-guide-to-generate-3d-meshes-from-point-clouds-with-python-36bad397d8ba)或 [边界框预测](https://towardsdatascience.com/deep-learning-on-point-clouds-implementing-pointnet-in-google-colab-1fd65cd3a263)。

## Dash3：视频帧的对象检测和可编辑注释

第三个应用程序可以让你回放从[伯克利 DeepDrive 数据集](https://bdd-data.berkeley.edu/)的驾驶场景，其中包含 1100 小时的驾驶视频。视频增强了由 [MobileNet v2](https://ai.googleblog.com/2018/04/mobilenetv2-next-generation-of-on.html) 生成的 2D 边框注释，生成并嵌入到视频中。除了重播场景，您可以在任何时间停止视频，实时运行 MobileNet 算法和交互式编辑或添加新的边界框在那个确切的时间戳。一旦您对注释感到满意，您就可以转移到下一个框架或下一个场景，并下载更新的和新的注释作为 CSV 文件。

这款应用程序是我们最喜欢的计算机视觉算法与人类注释器一起使用的例子，以加速数据收集过程。由于该应用完全是用 Python 构建的，并且只使用 [dash-player](https://github.com/plotly/dash-player)、[Plotly.py](https://plotly.com/python/shapes/) 和 [TensorFlow Hub](https://www.tensorflow.org/hub) 的内置特性，你可以轻松地对其进行个性化，以使用更复杂的模型，并满足技术注释需求，这些需求实际上只受 Python 库选择的限制。例如，您可以决定将所有新的注释存储在 SQL 数据库中(它们自动包含在 [Dash Enterprise](https://plotly.com/dash/#pricing) 中)，使用 [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) 之类的库将它们导出到云存储中，或者生成工作会话的[快照](https://plotly.com/dash/snapshot-engine/)，以便与其他注释器共享。

## 更多用于增强自动驾驶汽车可视化的 Dash 应用程序

除了这三个应用，还开发了各种开源的 Dash 应用，可以用来支持自动驾驶汽车的开发：

- Dash Deck Explorer([演示](https://dash-gallery.plotly.host/dash-deck-explorer/)，[代码](https://github.com/plotly/dash-deck))：这个 Explorer 可以让你尝试所有可能的层，你可以使用 pydeck 构建并使用 Dash-Deck 渲染。简短的描述和源代码都包括在内！
- Dash DETR([demo](https://dash-gallery.plotly.host/dash-detr/) — [code](https://github.com/plotly/dash-detr))：这个应用程序可以让你输入一个图像的 URL，并使用检测变压器([DETR](https://github.com/facebookresearch/detr))应用实时目标检测，一个由 Facebook 人工智能研究创建的神经网络模型。该代码可以很容易地重用并集成到 2D 对象检测的各种工作流中，例如使用 [PyTorch hub](https://pytorch.org/hub/) 检测图像中的行人和车辆。
- 对象检测资源管理器([demo](https://dash-gallery.plotly.host/dash-object-detection/) — [code](https://github.com/plotly/dash-sample-apps/tree/master/apps/dash-object-detection))：类似于视频检测应用程序，这个应用程序让你回放视频，以前注释了 MobileNet 检测器。它不是在框架上运行模型，而是读取检测器生成的日志来获得有用的信息，比如图像中的行人数量，以及当前屏幕上出现的物体的信心热图。
- Dash Uber Rides([demo](https://dash-gallery.plotly.host/dash-uber-rides-demo/) — [code](https://github.com/plotly/dash-sample-apps/blob/master/apps/dash-uber-rides-demo/app.py))：监控和检查自动驾驶汽车的行程将成为一个重要的任务，以确保自动驾驶系统在各种条件和地点的可靠性。这款应用程序可以让你可视化优步在纽约市的行程，并提供各种控制，快速缩小行程的特定子集。