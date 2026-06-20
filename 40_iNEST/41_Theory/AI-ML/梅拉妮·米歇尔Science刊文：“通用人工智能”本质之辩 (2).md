---
title: 梅拉妮·米歇尔Science刊文：“通用人工智能”本质之辩
tags:
- ai-ml
- artificial-intelligence
- brain
- chiplet
- embodied-ai
- free-energy-principle
- paper
- robotics
---
> 笔记本: 我的剪贴板  
> 创建时间: 2024-04-28  

---

**导语** 
 
    

 
**“通用人工智能”（AGI）近两年受到了广泛关注和热议。近期圣塔菲研究所学者、波特兰州立大学计算机科学教授 Melanie Mitchell 在*Science* 杂志上发表 Expert Voices 文章“Debates on the nature of artificial general intelligence”，再一次把问题导向了对智能的定义问题。这篇文章包含了许多反思，反映了当前大部分人对AGI的认识，然而其中也有许多观点有待商榷。为了更好地理解这篇文章，集智俱乐部「[AGI读书会](http://mp.weixin.qq.com/s?__biz=MzIzMjQyNzQ5MA==&mid=2247672075&idx=1&sn=ff4d57cba83aacb8ac289364dadc516e&chksm=e8997b86dfeef290a91d7c8dcab82f09216ee5832ad55d6e2895b6b0875bc26cbe89c2a2ee0a&scene=21#wechat_redirect)」发起人、天普大学通用人工智能方向博士生徐博文****将其翻译成中文，附上英文原稿供参照，同时也撰写了简短的评论，希望能为AGI的讨论提供更开阔的视角**。  
****  
**关键词：通用人工智能，生物智能，具身智能，社会智能** 
 
**** 
 
****    

 

 
    

   

 Melanie Mitchell **| 作者**
 徐博文** | ****译者**  
 
 

文章题目：Debates on the nature of artificial general intelligence
文章链接：https://www.science.org/doi/full/10.1126/science.ado7069   

 

 
  
   

 
**Response to "Debates on the nature of artificial general intelligence"** 
徐博文 
 2024年3月23日 
  
近期发表的这篇文章 (Mitchell, 2024) 中列举和比较了AI和其他领域（比如认知科学）的主流声音对AGI的理解。在这篇回应中，我将尝试澄清一些误解，并回应作者提出的诘难。  
  
文中作者主要提出了五点： 
- 
一些有名的公司（比如OpenAI、DeepMind）或者研究者对AGI的理解
- 
基于一个对智能的定义（“智能及其相关能力可以被理解是为奖励最大化服务的”），猜测AGI极其危险，因为它可能会“最优化”一个与人类“不对齐”的目标。
- 
生物智能是与物理身体的经验高度相关的，因此智能不能在机器中实现（这一观点否定了超级智能的可能性）
- 
呼吁智能的一般性理论。
-  
AGI的含义不够清晰。   
  
的确，公众对AGI有很多理解，并且我们仍然缺乏一个清晰、严肃的AGI定义。但这不意味着“AGI”这个词语的含义完全不清楚。因为一些历史原因，大部分AI研究者关注于特定领域或问题的专用系统，而“通用”则是强调了“领域无关”的属性（即“通用目的”），反对当时的主流范式。因此“通用智能”包含了“通用目的”的意思 (Wang & Goertzel, 2007) 。我认为大部分AGI研究者都会同意，AGI不等同于超级智能。  
  
第二点中对智能的定义很容易误导人认为AGI系统是要追求单个目标。根据许多长期以来AGI领域的现有工作（比如(Wang & Goertzel, 2012)中提到的，这些工作和文章中列举的相比不那么“出名”），一个AGI系统应当有多个未预先确定的目标，并且目标的含义是从环境中习得的。目标之间可能相互冲突，并且实现目标的资源是受限的。人一样有这些约束。从这个意义上说，AGI系统并不绝对导致人类毁灭，而文中提到的思想实验（比如“回形针AI”）不适用于AGI。值得一提，在最开始的时候AGI学者就已经回应了“AGI十分危险”这一潜在的异议（见(Wang & Goertzel, 2007)的3.8节）。  
  
个体的能力确实是具身化的（即与物理身体高度相关）。然而，具身的经验与AGI系统的“通用目的”并不冲突， 因为“即使AGI系统依赖于特定领域的知识来解决特定领域的问题，它的整体知识管理和学习机制可能仍然是通用的。关键的一点是，一个通用智能[系统]必须……学会掌握它以前从未遇到过的新领域”（ (Wang & Goertzel, 2007) 的3.2节对“AGI根本不存在”这一异议的回应）。事实上，许多AGI研究者早已经意识到，**“智能”是从不同智能系统身上抽象出来的，比如人类智能、动物智能、群体智能，甚至可能存在的外星人智能，而抽象就得有意地忽略生物细节**。  
  
我完全同意我们需要一个智能的理论。我也正在尝试给AGI下一个正式的定义，需要单独一篇论文才可能清楚AGI是什么意思（这基本是个哲学问题）。  
**References** 
Mitchell, M. (2024). Debates on the nature of artificial general intelligence. *Science*, *383*(6689), eado7069. https://doi.org/10.1126/science.ado7069 
Wang, P., & Goertzel, B. (2007). Introduction: Aspects of Artificial General Intelligence. *Proceedings of the 2007 Conference on Advances in Artificial General Intelligence: Concepts, Architectures and Algorithms: Proceedings of the AGI Workshop 2006*, 1–16. 
Wang, P., & Goertzel, B. (Eds.). (2012). *Theoretical Foundations of Artificial General Intelligence* (Vol. 4). Atlantis Press. https://doi.org/10.2991/978-94-91216-62-6  

 
  
    
  
“通用人工智能”（artificial general intelligence，AGI）一词在当前关于人工智能（AI）的讨论中已经无处不在。OpenAI表示，其使命是“确保通用人工智能造福全人类”。DeepMind的公司愿景中强调“通用人工智能有可能推动的是历史上最伟大变革之一” 。在英国政府的《国家人工智能战略》和美国政府的人工智能文件中，AGI也都被提及。微软的研究人员最近声称在大型语言模型GPT-4中有“[AGI火花](http://mp.weixin.qq.com/s?__biz=MzIzMjQyNzQ5MA==&mid=2247661073&idx=4&sn=8ad644985c2bc762e0bcd0eb87238e46&chksm=e8992c9cdfeea58ae0c7eee516e8b5249167673d130a1a5cecb9391859f65674c0d8800e6479&scene=21#wechat_redirect)”的证据，现任和前任谷歌高管宣称“AGI已经出现了”。关于GPT-4是否是“AGI算法”的问题是马斯克（Elon Musk）与OpenAI官司中的核心问题。  
  
人们可能会误认为这个术语的含义已经确立并得到了一致同意，但不能因为这一误解而受到指责，毕竟“AGI”一词在商业、政府和媒体中被广泛使用。然而事实却是，AGI是什么意思，或者它是否有清晰的含义，这在AI社区里一直存在激烈的争论。AGI的含义和可能的后果已经不仅仅是一个“玄妙”术语的学术辩论。世界上最大的科技公司和所有政府都在根据他们认为AGI将带来什么来做出重要决策。但若深入研究关于AGI的种种猜测，就会发现，许多人工智能从业者对“智能之本质”的看法与那些研究人类和动物认知的人截然不同——这种差异对于理解机器智能的现状和预测可能的未来很重要。  
  
人工智能领域的最初目标是让机器具有与人类旗鼓相当的“通用智能”。早期的AI先驱很乐观：1965年，司马赫（Herbert Simon）在他的《人与管理的自动化形态》（*The Shape of Automation for Men and Management*）一书中预测，“20年内，机器将有能力做任何人类能做的工作。”1970年的《生命》（*Life*）杂志引用了明斯基（Marvin Minsky）的话，“3到8年内，我们将拥有一台具有普通人通用智能的机器。我的意思是，一台能够阅读莎士比亚、给汽车加油、办公室里搞小圈子、讲笑话、打架的机器。”  
  
这些乐观的预测并没有成为现实。在接下来的几十年里，成功的AI系统只有专用的没有通用的——它们只能执行单一任务或有限范围的任务（例如，手机上的语音识别软件可以转录你的口述，但不能智能地做出回应）。“AGI”一词是在21世纪初创造的，旨在承AI先驱之遗志，以求恢复对“尝试独立于特定领域来研究和创造智能这个统一体”的关注。  
  
这种追求一直处在人工智能领域的一个不起眼的角落，直到最近，当世界领先的人工智能公司将实现AGI确立为他们的主要目标，并指出，人工智能“末日论者”宣布AGI的生存威胁是他们的头号恐惧。许多人工智能从业者推测了AGI的未来时间线，例如，有人预测，“到2028年，我们有50%的几率实现AGI。”其他人则质疑AGI的前提假设，称其模糊且定义不清；一位著名的研究者在推特上写道：“这整个概念就不科学，人们甚至应该为使用这个词感到羞耻。”  
  
尽管早期的AGI支持者认为，机器很快就会承担所有人类活动，但研究者们已经认识到，创建能在国际象棋中取胜或能回答问题的人工智能系统，比制造一个能叠衣服或修理管道的机器人要容易得多。AGI的定义相应地调整为只包括所谓的“认知任务”。DeepMind联合创始人哈萨比斯（Demis Hassabis）将AGI定义为“**应该能够完成人类可以完成的几乎所有认知任务”的系统**，而OpenAI将其描述为“**在大多数有经济价值的工作中超越人类的、高度自主的系统**”，其中“大多数”排除了需要物理智能的任务，这些任务可能短时间内机器人无法完成。  
  
**在人工智能中，“智能”**（或者叫认知，亦或其它词语）**的概念通常是根据智能体个体“最优化”奖励或目标来构建的**。一篇有影响力的论文将通用智能定义为“一个主体在广泛的环境中实现目标的能力”；另一种说法是，“智能及其相关能力可以被理解为是奖励最大化服务的。”事实上，这就是当今人工智能的工作方式——例如，计算机程序AlphaGo被训练来优化特定的奖励函数（“赢得比赛”），GPT-4被训练来优化另一种奖励函数（“预测短语中的下一个词”）。  
  
这种对智能的看法引发了一些AI研究者的另一种猜测：一旦AI系统达到了AGI，它将通过将其优化能力应用于自己的软件，“递归地”提高自己的智能，并迅速变得“比我们聪明千百万倍”，从而迅速实现超级智能。  
  
这种对优化的关注导致AI社区中的一些人担心，“（价值观）不（与人类）对齐的”AGI可能会严重偏离其创造者的目标，从而给人类带来生存风险。哲学家博斯特罗姆（Nick Bostrom）在2014年出版的《超级智能》（*Superintelligence*）一书中提出了一个当今很有名的思想实验：他想象人类给一个超级智能的人工智能系统设定目标，即优化回形针的生产。按照这个目标的字面意思，人工智能系统会利用它的天赋来控制地球上所有的资源，并把所有的东西都变成回形针。当然，人类并不打算毁灭地球和人类来制造更多的回形针，但他们在指令中忽略了这一点。人工智能研究者 Yoshua Bengio 也提了个思想实验：“我们可以让人工智能解决气候变化问题，它可能会设计出一种病毒，杀死大量人口，因为我们的指令中‘危害’二字的含义不够清楚，而人类实际上是解决气候危机的主要障碍。”  
  
这种对AGI（和“超级智能”）的推测性观点与研究生物智能（尤其是人类认知）的人持有的观点不同。尽管认知科学对“通用智能”没有严格的定义，就人类或任何类型的系统可以拥有“通用智能”的程度而言也没有共识，但大多数认知科学家都会同意，**智能不是可以在单一指标上度量和任意调整的量，而是通用和特定能力的复杂整合，这些能力大部分是适应特定生存环境的**。  
  
许多研究生物智能的人也怀疑，智能的所谓“认知”方面能否从其他方面中单独分离出来，并在一个脱离（人类）身体的（disembodied）机器中重现。心理学家已经表明，**人类智力的重要方面是建立在一个人具身的肉体和情感经验的基础上的**。证据还表明，**个体智力深受其在社会和文化环境中的参与所影响**。与个人的“优化能力”相比，理解他人、与他人协作和向他人学习的能力可能对一个人成功实现目标更为重要。  
  
关于具身智能、社会智能的更多相关文章：  
  
此外，与设想的“回形针最大化”AI不同，人类的智能并不以优化固定目标为中心；相反，一个人的目标是通过“先天需求”和“支撑其智能的社会文化环境”的复杂融合而成。与《超级智能》的“回形针最大化”AI不同，智能的增加恰恰使我们能够更好地洞察他人的意图，以及我们自己行为的可能影响、据此修改这些行为。正如哲学家格蕾丝（Katja Grace）所写的那样，“对于几乎任何人类目标来说，把征服宇宙作为次要步骤的想法都是完全可笑的。那么为什么我们认为人工智能的目标是不同的呢？”  
  
机器改进自己的“软件”，以提高其智能的量级，这种“机器幽灵”也偏离了智能的生物学观点，即**智能是一个高度复杂的“系统”，而不仅限于大脑内部**。如果人类水平的智能需要不同认知能力的复杂融合，以及社会和文化的支持，那么很可能系统的“智能”层次将无法无缝访问“软件”层次，就像我们人类无法轻易地设计我们的大脑（或我们的基因）让自己变得更聪明一样。然而，作为一个群体，我们通过外部工具（如计算机）和建立文化机构（如学校、图书馆和互联网）提高了我们的实际智能。  
  
AGI是什么意思以及它是否是一个含义明确的概念仍在争论中。此外，关于AGI机器能做什么的猜测主要是基于直觉，而不是科学证据。但这种直觉能在多大程度上可信呢？AI的历史一再推翻了我们对智能的直觉。许多早期的AI先驱认为，通过逻辑编程的机器将掌握人类全部智慧。其他学者预测，要让一台机器在国际象棋上击败人类，或者在不同语言之间进行翻译，或者进行对话，需要它具有通用的、人类水平的智能，但事实证明这是错误的。在AI演进中的每一步，人类水平的智能都比研究人员预期的要复杂得多。目前关于机器智能的猜测也会被证明是错误的吗？我们能否发展出一门更严谨、更一般性的智能科学来回答这些问题？  
  
目前尚不清楚AI的科学是更像人类智能的科学，还是更像外太空生物科学（即预测其他星球上的生命可能是什么样子）。对从未见过甚至可能不存在的东西进行预测，无论是外星生命还是超级智能机器，都需要基于一般原理的理论。最终，“AGI”的含义和后果不会通过媒体辩论、官司或我们的直觉和猜测来知晓，而是需要对这些原理的长期科学研究。  
  
  

 

**英文**   
  
**Debates on the nature of artificial general intelligence**  
  
  
The term “artificial general intelligence” (AGI) has become ubiquitous in current discourse around AI. OpenAI states that its mission is “to ensure that artificial general intelligence benefits all of humanity.” DeepMind’s company vision statement notes that “artificial general intelligence…has the potential to drive one of the greatest transformations in history.” AGI is mentioned prominently in the UK government’s National AI Strategy and in US government AI documents. Microsoft researchers recently claimed evidence of “sparks of AGI” in the large language model GPT-4, and current and former Google executives proclaimed that “AGI is already here.” The question of whether GPT-4 is an “AGI algorithm” is at the center of a lawsuit filed by Elon Musk against OpenAI.  
  
Given the pervasiveness of AGI talk in business, government, and the media, one could not be blamed for assuming that the meaning of the term is established and agreed upon. However, the opposite is true: What AGI means, or whether it means anything coherent at all, is hotly debated in the AI community. And the meaning and likely consequences of AGI have become more than just an academic dispute over an arcane term. The world’s biggest tech companies and entire governments are making important decisions on the basis of what they think AGI will entail. But a deep dive into speculations about AGI reveals that many AI practitioners have starkly different views on the nature of intelligence than do those who study human and animal cognition—differences that matter for understanding the present and predicting the likely future of machine intelligence.  
  
The original goal of the AI field was to create machines with general intelligence comparable to that of humans. Early AI pioneers were optimistic: In 1965, Herbert Simon predicted in his book The Shape of Automation for Men and Management that “machines will be capable, within twenty years, of doing any work that a man can do,” and, in a 1970 issue of Life magazine, Marvin Minsky is quoted as declaring that, “In from three to eight years we will have a machine with the general intelligence of an average human being. I mean a machine that will be able to read Shakespeare, grease a car, play office politics, tell a joke, have a fight.”  
  
These sanguine predictions did not come to pass. In the following decades, the only successful AI systems were narrow rather than general—they could perform only a single task or a limited scope of tasks (e.g., the speech recognition software on your phone can transcribe your dictation but cannot intelligently respond to it). The term “AGI” was coined in the early 2000s to recapture the original lofty aspirations of AI pioneers, seeking a renewed focus on “attempts to study and reproduce intelligence as a whole in a domain independent way.”  
  
This pursuit remained a rather obscure corner of the AI landscape until quite recently, when leading AI companies pinpointed the achievement of AGI as their primary goal, and noted AI “doomers” declared the existential threat from AGI as their number one fear. Many AI practitioners have speculated on the timeline to AGI, one predicting, for example, “a 50% chance that we have AGI by 2028.” Others question the very premise of AGI, calling it vague and ill-defined; one prominent researcher tweeted that “The whole concept is unscientific, and people should be embarrassed to even use the term.”  
  
Whereas early AGI proponents believed that machines would soon take on all human activities, researchers have learned the hard way that creating AI systems that can beat you at chess or answer your search queries is a lot easier than building a robot to fold your laundry or fix your plumbing. The definition of AGI was adjusted accordingly to include only so-called “cognitive tasks.” DeepMind cofounder Demis Hassabis defines AGI as a system that “should be able to do pretty much any cognitive task that humans can do,” and OpenAI describes it as “highly autonomous systems that outperform humans at most economically valuable work,” where “most” leaves out tasks requiring the physical intelligence that will likely elude robots for some time.  
  
The notion of “intelligence” in AI—cognitive or otherwise—is often framed in terms of an individual agent optimizing for a reward or goal. One influential paper defined general intelligence as “an agent’s ability to achieve goals in a wide range of environments”; another stated that “intelligence, and its associated abilities, can be understood as subserving the maximisation of reward.” Indeed, this is how current-day AI works—the computer program AlphaGo, for example, is trained to optimize a particular reward function (“win the game”), and GPT-4 is trained to optimize another kind of reward function (“predict the next word in a phrase”).  
  
This view of intelligence leads to another speculation held by some AI researchers: Once an AI system achieves AGI, it will quickly achieve superhuman intelligence by applying its optimization power to its own software, recursively advancing its own intelligence and quickly becoming, in one extreme prediction, “thousands or millions of times more intelligent than we are.”  
  
This focus on optimization has led some in the AI community to worry about the existential risk to humanity from “unaligned” AGI that diverges, maybe crazily, from its creator’s goals. In his 2014 book Superintelligence, philosopher Nick Bostrom proposed a now-famous thought experiment: He imagined humans giving a superintelligent AI system the goal of optimizing the production of paper clips. Taking this goal quite literally, the AI system then uses its genius to gain control over all Earth’s resources and transforms everything into paper clips. Of course, the humans did not intend the destruction of Earth and humanity to make more paper clips, but they neglected to mention that in the instructions. AI researcher Yoshua Bengio provides his own thought experiment: “[W]e may ask an AI to fix climate change and it may design a virus that decimates the human population because our instructions were not clear enough on what harm meant and humans are actually the main obstacle to fixing the climate crisis.”  
  
  
Such speculative views of AGI (and “superintelligence”) differ from views held by people who study biological intelligence, especially human cognition. Whereas cognitive science has no rigorous definition of “general intelligence” or consensus on the extent to which humans, or any type of system, can have it, most cognitive scientists would agree that intelligence is not a quantity that can be measured on a single scale and arbitrarily dialed up and down but rather a complex integration of general and specialized capabilities that are, for the most part, adaptive in a specific evolutionary niche.  
  
Many who study biological intelligence are also skeptical that so-called “cognitive” aspects of intelligence can be separated from its other modes and captured in a disembodied machine. Psychologists have shown that important aspects of human intelligence are grounded in one’s embodied physical and emotional experiences. Evidence also shows that individual intelligence is deeply reliant on one’s participation in social and cultural environments. The abilities to understand, coordinate with, and learn from other people are likely much more important to a person’s success in accomplishing goals than is an individual’s “optimization power.”  
  
Moreover, unlike the hypothetical paper clip–maximizing AI, human intelligence is not centered on the optimization of fixed goals; instead, a person’s goals are formed through complex integration of innate needs and the social and cultural environment that supports their intelligence. And unlike the superintelligent paper clip maximizer, increased intelligence is precisely what enables us to have better insight into other people’s intentions as well as the likely effects of our own actions, and to modify those actions accordingly. As the philosopher Katja Grace writes, “The idea of taking over the universe as a substep is entirely laughable for almost any human goal. So why do we think that AI goals are different?”  
  
  
The specter of a machine improving its own software to increase its intelligence by orders of magnitude also diverges from the biological view of intelligence as a highly complex system that goes beyond an isolated brain. If human-level intelligence requires a complex integration of different cognitive capabilities as well as a scaffolding in society and culture, it is likely that the “intelligence” level of a system will not have seamless access to the “software” level, just as we humans cannot easily engineer our brains (or our genes) to make ourselves smarter. However, we as a collective have increased our effective intelligence through external technological tools, such as computers, and by building cultural institutions, such as schools, libraries, and the internet.  
  
What AGI means and whether it is a coherent concept are still under debate. Moreover, speculations about what AGI machines will be able to do are largely based on intuitions rather than scientific evidence. But how much can such intuitions be trusted? The history of AI has repeatedly disproved our intuitions about intelligence. Many early AI pioneers thought that machines programmed with logic would capture the full spectrum of human intelligence. Other scholars predicted that getting a machine to beat humans at chess, or to translate between languages, or to hold a conversation, would require it to have general human-level intelligence, only to be proven wrong. At each step in the evolution of AI, human-level intelligence turned out to be more complex than researchers expected. Will current speculations about machine intelligence prove similarly wrongheaded? And could we develop a more rigorous and general science of intelligence to answer such questions?  
  
It is not clear whether a science of AI would be more like the science of human intelligence or more like, say, astrobiology, which makes predictions about what life might be like on other planets. Making predictions about something that has never been seen and might not even exist, whether that is extraterrestrial life or superintelligent machines, will require theories grounded in general principles. In the end, the meaning and consequences of “AGI” will not be settled by debates in the media, lawsuits, or our intuitions and speculations but by long-term scientific investigation of such principles.  
  
 

 本文首发于作者知乎：https://zhuanlan.zhihu.com/p/688589140?utm_medium=social&utm_psn=1754823984297066496&utm_source=wechat_session&s_r=0&wechatShare=1    
  

 

 
**AGI读书会**   
  
为了深入探讨 AGI 相关话题，集智俱乐部联合集萃深度感知技术研究所所长岳玉涛、麻省理工学院博士沈马成、天普大学博士生徐博文，共同发起[ AGI 读书会](http://mp.weixin.qq.com/s?__biz=MzIzMjQyNzQ5MA==&mid=2247672075&idx=1&sn=ff4d57cba83aacb8ac289364dadc516e&chksm=e8997b86dfeef290a91d7c8dcab82f09216ee5832ad55d6e2895b6b0875bc26cbe89c2a2ee0a&scene=21#wechat_redirect)，涵盖主题包括：智能的定义与度量、智能的原理、大语言模型与信息世界的智能、感知与具身智能、多视角下的人工智能、对齐技术与AGI安全性、AGI时代的未来社会。读书会已完结，现在报名可加入社群并解锁回放视频权限。 
[ ](http://mp.weixin.qq.com/s?__biz=MzIzMjQyNzQ5MA==&mid=2247672075&idx=1&sn=ff4d57cba83aacb8ac289364dadc516e&chksm=e8997b86dfeef290a91d7c8dcab82f09216ee5832ad55d6e2895b6b0875bc26cbe89c2a2ee0a&scene=21#wechat_redirect) 
详情请见：[AGI 读书会启动：迈向通用人工智能的跨学科路径](http://mp.weixin.qq.com/s?__biz=MzIzMjQyNzQ5MA==&mid=2247672075&idx=1&sn=ff4d57cba83aacb8ac289364dadc516e&chksm=e8997b86dfeef290a91d7c8dcab82f09216ee5832ad55d6e2895b6b0875bc26cbe89c2a2ee0a&scene=21#wechat_redirect) 

 

 
**自由能原理与强化学习读书会启动**   
自由能原理被认为是“自达尔文自然选择理论后最包罗万象的思想”，它试图从物理、生物和心智的角度提供智能体感知和行动的统一性规律，从第一性原理出发解释智能体更新认知、探索和改变世界的机制，从而对人工智能，特别是强化学习世界模型、通用人工智能研究具有重要启发意义。  
集智俱乐部联合北京师范大学系统科学学院博士生牟牧云，南京航空航天大学副教授何真，以及骥智智能科技算法工程师、公众号 CreateAMind 主编张德祥，共同发起「[自由能原理与强化学习读书会](http://mp.weixin.qq.com/s?__biz=MzIzMjQyNzQ5MA==&mid=2247684648&idx=1&sn=31d359ae9b22f282bca47889e403764e&chksm=e89948a5dfeec1b3c61a686df6920c48a55dfe3d59dd974827877cf3d6b83922e42cd58dc591&scene=21#wechat_redirect)」，希望探讨自由能原理、强化学习世界模型，以及脑与意识问题中的预测加工理论等前沿交叉问题，探索这些不同领域背后蕴含的感知和行动的统一原理。读书会从3月10日开始，每周日上午10:00-12:00，持续时间预计8-10周。欢迎感兴趣的朋友报名参与！ 
[ ](http://mp.weixin.qq.com/s?__biz=MzIzMjQyNzQ5MA==&mid=2247684648&idx=1&sn=31d359ae9b22f282bca47889e403764e&chksm=e89948a5dfeec1b3c61a686df6920c48a55dfe3d59dd974827877cf3d6b83922e42cd58dc591&scene=21#wechat_redirect) 
详情请见：[自由能原理与强化学习读书会启动：探索感知和行动的统一原理](http://mp.weixin.qq.com/s?__biz=MzIzMjQyNzQ5MA==&mid=2247684648&idx=1&sn=31d359ae9b22f282bca47889e403764e&chksm=e89948a5dfeec1b3c61a686df6920c48a55dfe3d59dd974827877cf3d6b83922e42cd58dc591&scene=21#wechat_redirect)  
  

 

 
**推荐阅读** 
**1. ****[梅拉妮·米歇尔Science刊文：AI能否自主学习世界模型？](http://mp.weixin.qq.com/s?__biz=MzIzMjQyNzQ5MA==&mid=2247676574&idx=1&sn=6bd883ce1e6448c090cb402145e8b6ed&chksm=e8996813dfeee105948d6d22f7e35cf8fef5cffec84d2cf15a2bc65e8133827c18736f8f74bd&scene=21#wechat_redirect)******  
**2. ****[《复杂》作者梅拉妮·米歇尔发文直指AI四大谬论，探究AI几度兴衰背后的根源](http://mp.weixin.qq.com/s?__biz=MzIzMjQyNzQ5MA==&mid=2247561825&idx=2&sn=59710c6d9b313a7c63aa90ec031110ef&chksm=e896a8ecdfe121fac94b2fdc26d5e12224be6267e90742f29b6e3b9fc0c849b48c6be8745530&scene=21#wechat_redirect)**  
**3. ****[**](http://mp.weixin.qq.com/s?__biz=MzIzMjQyNzQ5MA==&mid=2247660992&idx=1&sn=357e911429e1cb8cc3debf1edd7df5a9&chksm=e8992f4ddfeea65b2bdf87dddef455fec61f5b16a0706a5e9c58e070ff34ef22e706ad5be10c&scene=21#wechat_redirect)**[智能是什么？](http://mp.weixin.qq.com/s?__biz=MzIzMjQyNzQ5MA==&mid=2247675232&idx=1&sn=14a78b15ef1862480360d0e0f320513a&chksm=e89977eddfeefefb1c508b354ccff8bb3da52d35aaba19c63d13a6349dee2a445eae473991f8&scene=21#wechat_redirect)******  
**3. ****[通往具身通用智能：如何让机器从自然模态中学习到世界模型？](http://mp.weixin.qq.com/s?__biz=MzIzMjQyNzQ5MA==&mid=2247678577&idx=1&sn=4c997004608d9c35d47bf413140c3909&chksm=e89960fcdfeee9ea93d96d7acc8292fafb2721138e72efff360309aac99b4c433f48f6ac3143&scene=21#wechat_redirect)**  
**4. ****[张江：第三代人工智能技术基础——从可微分编程到因果推理 | 集智学园全新课程](http://mp.weixin.qq.com/s?__biz=MzIzMjQyNzQ5MA==&mid=2247667315&idx=1&sn=fca3a09806e753fa83d3fd6eb8ccf9d8&chksm=e89914fedfee9de82ae7107592b173d2a1c35141fab0006d3eac2dcb2dd1e74aa78a86e09a93&scene=21#wechat_redirect)**  
******5.**** [龙年大运起，学习正当时！解锁集智全站内容，开启新年学习计划](http://mp.weixin.qq.com/s?__biz=MzIzMjQyNzQ5MA==&mid=2247684525&idx=1&sn=bee7098c0fdf998e7efd72def2442287&chksm=e8994b20dfeec2360074b521111d22ada050fec084bd381175d2ffd708e31b3f94482be0daee&scene=21#wechat_redirect)**  
**6. **[**加入集智，一起复杂！**](http://mp.weixin.qq.com/s?__biz=MzIzMjQyNzQ5MA==&mid=2247667297&idx=2&sn=988b7314df45d949e69e81257801fff2&chksm=e89914ecdfee9dfac76f9245fb1fd0e5b25d567e20790fbdab671234588ad0e88e1acf205711&scene=21#wechat_redirect) 
**点击“阅读原文”，报名读书会**

---
**Tags:** [[BrainInspired]] [[Chiplet]]

---
## 相关笔记 (AI 自动关联)
- [[智能是什么？]]
- [[脑科学启发的持续学习，打造个性化的通用人工智能]]
