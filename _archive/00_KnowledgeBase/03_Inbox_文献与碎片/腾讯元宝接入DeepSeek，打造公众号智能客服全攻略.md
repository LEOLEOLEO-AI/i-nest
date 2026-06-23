---
title: "腾讯元宝接入DeepSeek，打造公众号智能客服全攻略"
source: "https://mp.weixin.qq.com/s/oRH6OCAtPqkeW41kxgWGHg"
created: 2025-03-03
note_id: "1869360430481300840"
tags:
  - "AI链接笔记"
  - "腾讯元宝"
  - "公众号智能客服"
  - "get-笔记"
  - "学术论文"
---

# 腾讯元宝接入DeepSeek，打造公众号智能客服全攻略

## 摘要

![](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fe41dc55f74c1e9a61b4ff8c0f1f7be40.jpeg?Expires=1780072839&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9

## 正文

见字如面，我是小马哥！35+技术总监，995职场宝爸，探索AI第二曲线，专注AI赋能提效。

![Image](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fcb04a3c1c0c1a7e5186013a9bc5714fc.webp?Expires=1780072868&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=zLaUTev29qmuQvimk5PUjOah0ok%3D)

去年9月的时候，腾讯发布元宝，当时我第一时间就接入公众号，有了一个腾讯版的「AI客服」。

这个客服怎么评价呢？其实回答粉丝的简单问题还是挺好的，但是稍微多问两句，就有点傻乎乎的，经常答非所问。

我自己也不可能经常看公众号后台回复粉丝问题，所以这个AI客服急需升级。

这不，前两天腾讯重磅发布，腾讯元宝已经接入DeepSeek，好家伙，这下我的傻客服终于有救了。

下面分享一下，我是怎么把DeepSeek接入公众号的，体验方式放在文末了，欢迎各位看官试验一下，到底这个客服智商在不在线。

  

01

  

客服创建

首先，我们打开腾讯元器官网：https://yuanqi.tencent.com/my-creation/agent

依次点击【创建智能体】-【用提示词创建】：

![img](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2F17af02c2a3a3fb0972197499168d6913.png?Expires=1780072868&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=wXil5iFtvBSJXiyAhHraAloX6jQ%3D)

根据页面提示，完成智能体配置：

![img](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2F2f7c1ec8a05ca1f37d2e951c084a3b43.png?Expires=1780072868&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=8KcXQZaNfh3jc0day694yF0VjIk%3D)

其中提示词部分如下（需要的朋友可以主页联系我获取）：

![Image](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fb8652714847cd91dc8680e8e95f9705d.png?Expires=1780072868&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=W0ufN1oE5vKvUlQNQN%2FM2CkHsDk%3D)

我给这个客服赋予了三个技能，回答公众号问题的时候就代表我来回复，不是的话就用DeepSeek的身份来互动，这样给粉丝的体验会更好。

完成了基本配置以后，我们需要来到【高级配置】，首先我们需要设置DeepSeek-R1大模型。

![img](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2F20d6603675fb53ca6dc2beccb740bc71.png?Expires=1780072868&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=JONk7pdY1aI5b3OIzPNKbR42DZ8%3D)

接下来我们需要把所有公众号的文章喂给AI，这样他才知道我这些年在公众号平台干了些啥。

![img](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fc5ebf9730be3c7374629b86cb0a84b91.png?Expires=1780072868&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=8DdvYh%2Bm%2B%2FalePVUK8k0o27cr2w%3D)

点击【添加】以后，创建知识库，绑定我公众号的所有文章，这一步需要自己的公众号授权才行。

![img](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fd957b2adbdaf7d184b94dce799515327.png?Expires=1780072868&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=iXt3C%2FiVvHjT7EEAJMtkxiDuTrE%3D)

接下来，大功告成，我们来尝尝鲜，比如让他推荐一些我的文章：

![img](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2F1081cf41904fd215b24dd3addd6fa748.png?Expires=1780072868&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=ziZl%2FCluOukFJh%2BU49gq2O4Etao%3D)

确实不错，推荐的文章都还是比较受欢迎的。

接下来我们就可以发布了，发布时记得选择发布到公众号，后续才能在公众号中使用。

![img](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2F15a7d2e64b72861aefbbf5b97d09dddf.png?Expires=1780072868&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=Jyqi8RRtwSFCLFdxopvddDYQBnc%3D)

发布以后我们点击【使用方式】。

![img](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2F93733ff599cb5740202d2542904ec756.png?Expires=1780072868&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=0RzXLMVuzmryuUGokjEU14%2Bt6h0%3D)

可以看到我们这个智能体有网页、小程序等多种体验方式，这里我们重点复制一下小程序的使用路径，后面会用到。

![img](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2F7f404339bb583c097b33bbfb05cee862.png?Expires=1780072868&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=9rniMBz%2FxlAATr98vQPpwVn00sU%3D)

  

02

  

公众号开通元宝

我们来到微信公众号的后台，依次点击【广告收入】-【小程序管理】，我们可以为公众号绑定一个小程序。

![img](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fea2edaf05543638aa130b3cca611c0ea.png?Expires=1780072868&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=DsV89vBgP4RZlOWHLGKoNk4kDUc%3D)

我们按照页面要求关联【腾讯元宝】小程序。

![img](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2F67040a4ae940bf70bb7c8170e33d4da1.png?Expires=1780072868&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=2l77ue5%2FF51ATrVAjonOHjEdqsQ%3D)

![img](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2F30070c0f6fbef00d58ac298481c66ae0.png?Expires=1780072868&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=K%2FBZq3lsQGGXSHiXIVNZv28%2B1uc%3D)

  

03

  

添加菜单

最后，我们再来到自定义菜单，我们可以添加一个菜单，并且把【消息类型】设置为【跳转小程序】，这里再把我们之前复制的小程序路径复制过来就好了。

![img](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2F2cfc13f126dd74ffe717ba61ca6f6a5b.png?Expires=1780072868&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=IfKJtqlPF1f0Jlq2i4rJR1NLQMI%3D)

就这样，我的公众号也终于有了一个DeepSeek内核的智能助理了。

各位看官可以打开公众号消息页面体验一下效果，和我的客服互动一下吧，我感觉回答的还是挺靠谱的~

![Image](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2F02f112f2f8ac155e2bfbf740532ea668.png?Expires=1780072868&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=v97FmYVk50X019Qjwjw5zIOk%2FyA%3D)

领福利

  

  

  

  

  

最后送个免费福利，最近国内头部 AI 社群「AI 破局俱乐部」推出了 **3天** 体验卡，如果你想学 AI，只需要扫描下方二维码就能 **免费** 加入，绝对干货满满！

![Image](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2F6886c612a6c7a4bfd27701f86fcb53d8.png?Expires=1780072868&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=0kUk%2BfqiPhiyZlwU0riw5UIKT48%3D)

---
*来源：Get笔记 | 类型：link | 入库：2026-04-29 12:41*