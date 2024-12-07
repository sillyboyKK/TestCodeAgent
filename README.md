### MyCodeAgent
##### 思路：
1. 获取所需调整项目的github地址，并clone到本地。并获取项目结构（用于组装prompt，相当于用较少的token表示项目的全貌）。
2. CodeAgent的整体Pipeline为：（1）根据输入的要求,生成粗糙的步骤 ——> （2）按照分解每一步粗糙的步骤为精细的操作（action）——> （3）按照顺序执行执行action，action的结果会feedback或forward给下一个action ——> （4）自动调用调试，并feedback调整（目前还未做）
3. 之所以没有用到langchain，是因为有很多东西限制自由度比较低，想着自己手撸一个框架能够比较灵活（目前暂时也还没用到知识库索引，所有没有使用langchain）。
4. 时间紧迫，很多feedback和forward都还没有写好，整体也没有达到要求。


##### 使用
```bash
pip install -r requirements.txt
```
```bash
python main.py
```