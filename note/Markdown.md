Markdown 备忘
===

Index
---
<!-- TOC -->

- [换行](#换行)
- [目录](#目录)
    - [自动更新插件（VSCode）](#自动更新插件vscode)
- [图片居中](#图片居中)
- [隐藏块](#隐藏块)
- [HTML 表格](#html-表格)
- [Latex 公式](#latex-公式)
    - [Latex for Markdown](#latex-for-markdown)

<!-- /TOC -->

## 换行
```markdown
<br/>
```

## 目录
```markdown
<!-- TOC -->

- [A](#A)
    - [a](#a)
- [B](#B)
    - [b](#b)
    
<!-- /TOC -->
```

### 自动更新插件（VSCode）
- VSCode 插件 [`Markdown TOC`](https://marketplace.visualstudio.com/items?itemName=AlanWalk.markdown-toc)

## 图片居中

<style> 
.test{width:300px; align:"center"; overflow:hidden} 
.test img{max-width:300px;_width:expression(this.width > 300 ? "300px" : this.width);} 
</style> 

- 不带链接
    ```
    <div align="center"><img src="./_assets/xxx.png" height="300" /></div>
    ```
- 带链接
    ```
    <div align="center"><a href=""><img src="./_assets/xxx.png" height="300" /></a></div>
    ```
- `height`用于控制图片的大小，一般不使用，图片会等比例缩放；

## 隐藏块
```
<details><summary><b>示例：动态序列（点击展开）</b></summary> 

// 代码块，注意上下都要保留空行

</details>
<br/> <!-- 如果间隔太小，可以加一个空行 -->
```

## HTML 表格
```
<table style="width:80%; table-layout:fixed;">
    <tr>
        <th align="center">普通卷积</td>
        <th align="center">空洞卷积</td>
    </tr>
    <tr>
        <td><img width="250px" src="./res/no_padding_no_strides.gif"></td>
        <td><img width="250px" src="./res/dilation.gif"></td>
    </tr>
</table>
```

## Latex 公式
> [【LaTeX】LaTeX符号大全_Ljnoit-CSDN博客_latex 绝对值符号](https://blog.csdn.net/ljnoit/article/details/104264753)

> 在线 LaTeX 公式编辑器 http://www.codecogs.com/latex/eqneditor.php

**绝对值**

$$ \left | a-b \right |
$$

**函数名**
- 如果是预定义好的，直接 `\max(x)`，否则使用 `\operatorname{f}(x)`，示例：

$$ \operatorname{f}(x)
$$

```
-- 斜体加粗
\boldsymbol{x}

-- 期望
\mathbb{E}

-- 矩阵对齐
\begin{array}{ll}
 & \\
 & \\
\end{array}

-- 转置
^\mathsf{T}

-- 省略号
水平方向    \cdots   
竖直方向    \vdots   
对角线方向  \ddots

-- 按元素相乘
\circ
或
\odot

-- 右箭头
\rightarrow 
-- 左箭头
\leftarrow 

```

### Latex for Markdown
> markdown 专用
- 在 markdown 内使用：行内使用 `$` 包围，独立行使用 `$$` 包围

**参考和引用**

$[1]$ [xxx](xxx) <br/>

引用$^{[1]}$