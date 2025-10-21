import streamlit as st
import os
import json
import re
from typing import List, Dict, Optional
from datetime import datetime

# 定义课程目录结构 (与 learning_app.py 保持一致)
COURSE_STRUCTURE = {
    "C1 大型语言模型 LLM 介绍": [
        "1.大型语言模型 LLM 理论简介.md",
        "2.检索增强生成 RAG 简介.md",
        "3.LangChain 简介.md",
        "4.开发 LLM 应用的整体流程.md",
        "5.阿里云服务器的基本使用.md",
        "6.GitHub Codespaces 的基本使用（选修）.md",
        "7.环境配置.md"
    ],
    "C2 使用 LLM API 开发应用": [
        "1. 基本概念.md",
        "2. 使用 LLM API.ipynb",
        "3. Prompt Engineering.ipynb"
    ],
    "C3 搭建知识库": [
        "1.词向量及向量知识库介绍.md",
        "2.使用 Embedding API.ipynb",
        "3.数据处理.ipynb",
        "4.搭建并使用向量数据库.ipynb"
    ],
    "C4 构建 RAG 应用": [
        "1.LLM 接入 LangChain.ipynb",
        "2.构建检索问答链.ipynb",
        "3.部署知识库助手.ipynb"
    ],
    "C5 系统评估与优化": [
        "1.如何评估 LLM 应用.ipynb",
        "2.评估并优化生成部分.ipynb",
        "3.评估并优化检索部分.md"
    ]
}

# 读取Markdown文件内容
def read_markdown_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        st.warning(f"无法读取文件 {file_path}: {str(e)}")
        return None

# 搜索功能
def search_content(query: str) -> List[Dict]:
    if not query or len(query.strip()) < 2:
        return []
        
    results = []
    query_lower = query.lower().strip()
    
    for chapter_name, files in COURSE_STRUCTURE.items():
        for file_name in files:
            # 只搜索 Markdown 文件
            if not file_name.endswith(".md"):
                continue

            file_path = os.path.join(
                os.path.dirname(__file__),
                "notebook",
                chapter_name,
                file_name
            )
            
            content = read_markdown_file(file_path)
            if content and not content.startswith("无法读取文件") and not content.startswith("文件不存在"):
                content_lower = content.lower()
                
                # 查找所有匹配项
                matches = list(re.finditer(rf"{re.escape(query_lower)}", content_lower, re.IGNORECASE))
                
                if matches:
                    # 为每个文件只保留最匹配的几个结果
                    file_results = []
                    for i, match in enumerate(matches[:3]):  # 最多3个匹配
                        match_pos = match.start()
                        
                        # 提取更好的匹配片段（按句子分割）
                        sentences = re.split(r'[。！？\n]', content)
                        best_sentence = ""
                        best_sentence_index = -1
                        
                        for j, sentence in enumerate(sentences):
                            if query_lower in sentence.lower():
                                best_sentence = sentence.strip()
                                best_sentence_index = j
                                break
                        
                        if best_sentence:
                            snippet = best_sentence
                            # 获取上下文
                            context_start = max(0, best_sentence_index - 1)
                            context_end = min(len(sentences), best_sentence_index + 2)
                            context = "。".join(sentences[context_start:context_end]).strip()
                            
                            # 高亮匹配词
                            highlighted_snippet = re.sub(
                                rf"({re.escape(query)})", 
                                r"**\1**", 
                                context, 
                                flags=re.IGNORECASE
                            )
                        else:
                            # 回退到原始方法
                            start_idx = max(0, match_pos - 100)
                            end_idx = min(len(content), match_pos + len(query) + 100)
                            snippet = content[start_idx:end_idx]
                            highlighted_snippet = re.sub(
                                rf"({re.escape(query)})", 
                                r"**\1**", 
                                snippet, 
                                flags=re.IGNORECASE
                            )
                        
                        file_results.append({
                            "chapter": chapter_name,
                            "file": file_name,
                            "snippet": highlighted_snippet,
                            "path": file_path,
                            "match_count": len(matches)
                        })
                    
                    results.extend(file_results)
    
    return results

def main():
    st.title("🔍 内容搜索")
    st.write("在课程内容中搜索您感兴趣的技术细节和知识点。")
    
    # 搜索历史
    if 'search_history' not in st.session_state:
        st.session_state['search_history'] = []
    
    # 搜索界面
    col1, col2 = st.columns([3, 1])
    with col1:
        search_query = st.text_input("输入搜索关键词", key="search_input", placeholder="例如：RAG、API、向量数据库...")
    with col2:
        st.write("")
        st.write("")
        search_button = st.button("🔍 搜索", type="primary")
    
    # 显示搜索历史
    if st.session_state['search_history']:
        with st.expander("🕐 搜索历史"):
            history_cols = st.columns(min(5, len(st.session_state['search_history'])))
            for i, term in enumerate(st.session_state['search_history']):
                with history_cols[i % 5]:
                    if st.button(term, key=f"history_{i}"):
                        st.session_state['search_input'] = term
                        st.rerun()
    
    # 执行搜索
    if (search_query and search_query.strip()) or search_button:
        query = search_query.strip()
        
        if len(query) < 2:
            st.warning("请输入至少2个字符进行搜索")
        else:
            # 添加到搜索历史
            if query not in st.session_state['search_history']:
                st.session_state['search_history'].insert(0, query)
                st.session_state['search_history'] = st.session_state['search_history'][:10]  # 保留最近10次
            
            with st.spinner(f"正在搜索 '{query}'..."):
                results = search_content(query)
            
            if results:
                st.success(f"找到 {len(results)} 个相关结果")
                
                # 按章节分组显示结果
                results_by_chapter = {}
                for result in results:
                    chapter = result['chapter']
                    if chapter not in results_by_chapter:
                        results_by_chapter[chapter] = []
                    results_by_chapter[chapter].append(result)
                
                for chapter, chapter_results in results_by_chapter.items():
                    with st.expander(f"📚 {chapter} ({len(chapter_results)} 个结果)", expanded=True):
                        for i, result in enumerate(chapter_results):
                            col_left, col_right = st.columns([4, 1])
                            
                            with col_left:
                                st.markdown(f"**📄 {result['file']}**")
                                st.markdown(f"📝 {result['snippet']}")
                                
                                if 'match_count' in result:
                                    st.caption(f"共 {result['match_count']} 处匹配")
                            
                            with col_right:
                                st.write("")
                                if st.button("前往学习", key=f"go_to_learning_{chapter}_{i}"):
                                    st.session_state['page'] = '开始学习'
                                    st.session_state['initial_chapter'] = result['chapter']
                                    st.session_state['initial_file'] = result['file']
                                    st.rerun()
                            
                            if i < len(chapter_results) - 1:
                                st.divider()
                
            else:
                st.info("😔 没有找到匹配的结果")
                st.markdown("**建议：**")
                st.markdown("- 尝试使用不同的关键词")
                st.markdown("- 检查拼写是否正确")
                st.markdown("- 使用更通用的词汇")
                
                # 推荐相关搜索
                suggested_terms = ["RAG", "API", "LangChain", "向量数据库", "大模型", "提示工程"]
                st.markdown("**试试这些搜索词：**")
                cols = st.columns(3)
                for i, term in enumerate(suggested_terms[:6]):
                    with cols[i % 3]:
                        if st.button(term, key=f"suggest_{i}"):
                            st.session_state['search_input'] = term
                            st.rerun()
    
    # 搜索提示
    with st.expander("💡 搜索提示"):
        st.markdown("""
        - **关键词搜索**: 输入您感兴趣的技术术语或概念
        - **中英文都支持**: 可以搜索中文或英文关键词
        - **模糊匹配**: 系统会自动查找相关内容
        - **结果排序**: 按章节分组显示相关结果
        - **快速跳转**: 点击"前往学习"按钮直接跳转到对应内容
        
        **推荐搜索词**：
        - RAG、检索增强生成
        - API、OpenAI、智谱AI
        - LangChain、链式调用
        - 向量数据库、Chroma
        - 提示工程、Prompt
        - 大模型、LLM
        """)

if __name__ == "__main__":
    main()