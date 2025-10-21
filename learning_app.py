import streamlit as st
import os
import json
import markdown
import pandas as pd
from datetime import datetime
import webbrowser
from pathlib import Path
import base64
from typing import Dict, List, Optional, Tuple

# 设置页面配置
st.set_page_config(
    page_title="大模型应用开发学习平台",
    page_icon=":books:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 添加自定义CSS样式
def add_custom_css():
    st.markdown("""
    <style>
    /* 笔记区域样式优化 */
    .stColumns > div:nth-child(2) {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        position: sticky;
        top: 0;
        height: 100vh;
        overflow-y: auto;
    }

    /* 笔记区域标题样式 */
    .stColumns > div:nth-child(2) h3 {
        color: #2c3e50;
        font-size: 1.2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #3498db;
        padding-bottom: 0.5rem;
    }

    /* 笔记输入框样式 */
    .stColumns > div:nth-child(2) .stTextArea {
        border-radius: 8px;
        border: 2px solid #e1e8ed;
    }

    /* 笔记按钮样式 */
    .stColumns > div:nth-child(2) button {
        background-color: #3498db;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px;
        font-weight: bold;
        margin-top: 10px;
    }

    .stColumns > div:nth-child(2) button:hover {
        background-color: #2980b9;
    }

    /* 历史笔记expander样式 */
    .stColumns > div:nth-child(2) .streamlit-expanderHeader {
        background-color: #ecf0f1;
        border-radius: 5px;
        padding: 8px;
        margin-bottom: 5px;
    }

    /* 主内容区域样式 */
    .stColumns > div:nth-child(1) {
        padding-right: 20px;
    }

    /* 响应式设计：小屏幕下隐藏笔记区域 */
    @media (max-width: 768px) {
        .stColumns > div:nth-child(2) {
            display: none;
        }
        .stColumns > div:nth-child(1) {
            padding-right: 0;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# 应用自定义CSS
add_custom_css()

# 创建学习数据目录
LEARN_DATA_DIR = os.path.join(os.path.dirname(__file__), ".learn_data")
if not os.path.exists(LEARN_DATA_DIR):
    os.makedirs(LEARN_DATA_DIR)

# 用户学习进度文件
PROGRESS_FILE = os.path.join(LEARN_DATA_DIR, "user_progress.json")
NOTES_FILE = os.path.join(LEARN_DATA_DIR, "user_notes.json")

# 课程目录结构
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

# 初始化用户进度
def init_user_progress():
    if not os.path.exists(PROGRESS_FILE):
        progress = {}
        for chapter, files in COURSE_STRUCTURE.items():
            for file in files:
                progress[f"{chapter}/{file}"] = {
                    "completed": False,
                    "last_accessed": None,
                    "access_count": 0
                }
        with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
            json.dump(progress, f, ensure_ascii=False, indent=2)

# 加载用户进度
def load_user_progress():
    try:
        if not os.path.exists(PROGRESS_FILE):
            init_user_progress()
        
        # 检查文件是否为空
        if os.path.getsize(PROGRESS_FILE) == 0:
            init_user_progress()
            
        with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            # 验证数据格式
            if not isinstance(data, dict):
                init_user_progress()
                data = load_user_progress()
            return data
            
    except json.JSONDecodeError:
        st.warning("进度数据损坏，正在重新初始化...")
        init_user_progress()
        return load_user_progress()
    except PermissionError:
        st.error("没有权限访问进度文件")
        return {}
    except Exception as e:
        st.error(f"加载进度数据时出错: {str(e)}")
        return {}

# 保存用户进度
def save_user_progress(progress):
    try:
        # 验证数据格式
        if not isinstance(progress, dict):
            raise ValueError("进度数据格式错误")
            
        # 备份现有文件
        if os.path.exists(PROGRESS_FILE):
            backup_file = PROGRESS_FILE + ".backup"
            import shutil
            shutil.copy2(PROGRESS_FILE, backup_file)
            
        with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
            json.dump(progress, f, ensure_ascii=False, indent=2)
            
    except PermissionError:
        st.error("没有权限保存进度文件")
    except Exception as e:
        st.error(f"保存进度数据时出错: {str(e)}")

# 更新学习进度
def update_progress(chapter, file):
    progress = load_user_progress()
    key = f"{chapter}/{file}"
    if key in progress:
        progress[key]["last_accessed"] = datetime.now().isoformat()
        progress[key]["access_count"] += 1
        save_user_progress(progress)

# 标记完成状态
def mark_completed(chapter, file, completed):
    progress = load_user_progress()
    key = f"{chapter}/{file}"
    if key in progress:
        progress[key]["completed"] = completed
        save_user_progress(progress)

# 加载用户笔记
def load_user_notes():
    try:
        if not os.path.exists(NOTES_FILE):
            return {}
            
        # 检查文件是否为空
        if os.path.getsize(NOTES_FILE) == 0:
            return {}
            
        with open(NOTES_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            # 验证数据格式
            if not isinstance(data, dict):
                return {}
            return data
            
    except json.JSONDecodeError:
        st.warning("笔记数据损坏，已重置")
        return {}
    except PermissionError:
        st.error("没有权限访问笔记文件")
        return {}
    except Exception as e:
        st.error(f"加载笔记数据时出错: {str(e)}")
        return {}

# 保存用户笔记
def save_user_notes(notes):
    try:
        # 验证数据格式
        if not isinstance(notes, dict):
            raise ValueError("笔记数据格式错误")
            
        # 备份现有文件
        if os.path.exists(NOTES_FILE):
            backup_file = NOTES_FILE + ".backup"
            import shutil
            shutil.copy2(NOTES_FILE, backup_file)
            
        with open(NOTES_FILE, "w", encoding="utf-8") as f:
            json.dump(notes, f, ensure_ascii=False, indent=2)
            
    except PermissionError:
        st.error("没有权限保存笔记文件")
    except Exception as e:
        st.error(f"保存笔记数据时出错: {str(e)}")

# 添加用户笔记
def add_user_note(chapter, file, note):
    notes = load_user_notes()
    key = f"{chapter}/{file}"
    if key not in notes:
        notes[key] = []
    notes[key].append({
        "content": note,
        "timestamp": datetime.now().isoformat()
    })
    save_user_notes(notes)

# 获取用户笔记
def get_user_notes(chapter, file):
    notes = load_user_notes()
    key = f"{chapter}/{file}"
    return notes.get(key, [])

# 读取Markdown文件内容
def read_markdown_file(file_path):
    try:
        # 检查文件是否存在
        if not os.path.exists(file_path):
            return f"文件不存在: {file_path}"
            
        # 检查文件是否为空
        if os.path.getsize(file_path) == 0:
            return "文件为空"
            
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            if not content.strip():
                return "文件内容为空"
            return content
            
    except UnicodeDecodeError:
        try:
            # 尝试使用其他编码
            with open(file_path, "r", encoding="gbk") as f:
                return f.read()
        except UnicodeDecodeError:
            return "文件编码格式不支持，请使用UTF-8或GBK编码"
    except PermissionError:
        return f"没有权限读取文件: {file_path}"
    except Exception as e:
        return f"读取文件时发生错误: {str(e)}"

# 显示Markdown内容
def render_markdown_content(content):
    # 处理图片路径
    import re
    # 匹配相对路径的图片
    content = re.sub(r'!\\[(.*?)\\]\\(([^http][^)]*?)\\)', lambda m: f"![{m.group(1)}]({os.path.join(os.path.dirname(__file__), m.group(2))})", content)
    st.markdown(content, unsafe_allow_html=True)

# 计算总体进度
def calculate_overall_progress():
    progress = load_user_progress()
    total = len(progress)
    completed = sum(1 for item in progress.values() if item["completed"])
    return completed / total if total > 0 else 0

# 获取下一个/上一个文件
def get_next_prev_file(current_chapter, current_file, direction):
    chapters = list(COURSE_STRUCTURE.keys())
    current_chapter_index = chapters.index(current_chapter)
    
    files_in_current_chapter = COURSE_STRUCTURE[current_chapter]
    current_file_index = files_in_current_chapter.index(current_file)

    if direction == "next":
        if current_file_index < len(files_in_current_chapter) - 1:
            # Next file in current chapter
            return current_chapter, files_in_current_chapter[current_file_index + 1]
        elif current_chapter_index < len(chapters) - 1:
            # Next chapter, first file
            next_chapter = chapters[current_chapter_index + 1]
            return next_chapter, COURSE_STRUCTURE[next_chapter][0]
        else:
            return None, None # End of course
    elif direction == "prev":
        if current_file_index > 0:
            # Previous file in current chapter
            return current_chapter, files_in_current_chapter[current_file_index - 1]
        elif current_chapter_index > 0:
            # Previous chapter, last file
            prev_chapter = chapters[current_chapter_index - 1]
            return prev_chapter, COURSE_STRUCTURE[prev_chapter][-1]
        else:
            return None, None # Beginning of course
    return None, None

# 主应用
def main(initial_chapter=None, initial_file=None):
    # 初始化
    init_user_progress()
    
    # 侧边栏 - 课程导航
    st.sidebar.title("课程导航")
    
    # 显示总体进度
    overall_progress = calculate_overall_progress()
    st.sidebar.markdown(f"### 学习进度: {int(overall_progress * 100)}%")
    st.sidebar.progress(overall_progress)
    
    chapters = list(COURSE_STRUCTURE.keys())

    # Initialize session state for selected chapter and file if not already set
    if 'selected_chapter' not in st.session_state:
        st.session_state['selected_chapter'] = chapters[0]
    if 'selected_file' not in st.session_state:
        st.session_state['selected_file'] = COURSE_STRUCTURE[st.session_state['selected_chapter']][0]

    # Handle initial chapter/file from home page (only process once)
    navigation_key = 'navigation_processed'
    if initial_chapter and initial_chapter in chapters and navigation_key not in st.session_state:
        st.session_state['selected_chapter'] = initial_chapter
        if initial_file and initial_file in COURSE_STRUCTURE[initial_chapter]:
            st.session_state['selected_file'] = initial_file
        else:
            st.session_state['selected_file'] = COURSE_STRUCTURE[initial_chapter][0]
        # Mark navigation as processed to prevent infinite loops
        st.session_state[navigation_key] = True
        # Rerun to apply initial selection immediately
        st.rerun()

    # Display chapters and files in sidebar
    for chapter in chapters:
        # Use expander for each chapter
        expanded = (chapter == st.session_state['selected_chapter']) # Expand current chapter
        with st.sidebar.expander(chapter, expanded=expanded):
            for file in COURSE_STRUCTURE[chapter]:
                # Highlight selected file
                is_selected = (chapter == st.session_state['selected_chapter'] and file == st.session_state['selected_file'])
                
                # Create a button for each file
                if st.button(file, key=f"sidebar_btn_{chapter}_{file}", use_container_width=True):
                    st.session_state['selected_chapter'] = chapter
                    st.session_state['selected_file'] = file
                    st.rerun()
    
    selected_chapter = st.session_state['selected_chapter']
    selected_file = st.session_state['selected_file']

    if selected_chapter and selected_file:
        # 构建文件路径
        file_path = os.path.join(
            os.path.dirname(__file__),
            "notebook",
            selected_chapter,
            selected_file
        )
        
        # 更新学习进度
        update_progress(selected_chapter, selected_file)
        
        # 获取当前文件的学习状态
        progress = load_user_progress()
        key = f"{selected_chapter}/{selected_file}"
        current_progress = progress.get(key, {})
        
        # 主内容区 - 使用分屏布局
        main_col, notes_col = st.columns([3, 1])  # 左侧主内容占3/4，右侧笔记占1/4

        # 左侧：学习内容
        with main_col:
            # Display file content
            st.title(selected_file)

            # Display completion status checkbox
            completed = st.checkbox(
                "标记为已完成",
                current_progress.get("completed", False)
            )
            if completed != current_progress.get("completed", False):
                mark_completed(selected_chapter, selected_file, completed)

            # Render content based on file type
            if selected_file.endswith(".md"):
                content = read_markdown_file(file_path)
                render_markdown_content(content)
            elif selected_file.endswith(".ipynb"):
                st.info("这是一个Jupyter Notebook文件。由于安全限制，无法直接在Streamlit中运行。请在Jupyter环境中打开学习。")
                # Provide download link
                with open(file_path, "rb") as f:
                    bytes_data = f.read()
                st.download_button(
                    label="下载Notebook文件",
                    data=bytes_data,
                    file_name=selected_file,
                    mime="application/x-ipynb+json"
                )

            # Add next/previous page navigation
            st.markdown("---")
            nav_col1, nav_col2 = st.columns(2)
            with nav_col1:
                prev_chapter, prev_file = get_next_prev_file(selected_chapter, selected_file, "prev")
                if prev_chapter and prev_file:
                    if st.button("上一页"):
                        st.session_state['selected_chapter'] = prev_chapter
                        st.session_state['selected_file'] = prev_file
                        st.rerun()
            with nav_col2:
                next_chapter, next_file = get_next_prev_file(selected_chapter, selected_file, "next")
                if next_chapter and next_file:
                    if st.button("下一页"):
                        # Mark current page as completed before moving to next
                        mark_completed(selected_chapter, selected_file, True)
                        st.session_state['selected_chapter'] = next_chapter
                        st.session_state['selected_file'] = next_file
                        st.rerun()

        # 右侧：笔记功能区
        with notes_col:
            st.markdown("### 📝 笔记")

            # 学习信息
            st.markdown("**学习信息**")
            access_count = current_progress.get("access_count", 0)
            st.markdown(f"访问次数: {access_count}")

            last_accessed = current_progress.get("last_accessed", "从未访问")
            if last_accessed != "从未访问":
                last_accessed = datetime.fromisoformat(last_accessed).strftime("%m-%d %H:%M")
            st.markdown(f"上次学习: {last_accessed}")

            st.markdown("---")

            # 笔记输入区域
            st.markdown("**添加笔记**")
            new_note = st.text_area("在这里记录你的想法...", height=150, key="note_input")

            if st.button("💾 保存笔记", use_container_width=True):
                if new_note.strip():
                    add_user_note(selected_chapter, selected_file, new_note)
                    st.success("✅ 已保存")
                    st.rerun()

            # 显示历史笔记
            notes = get_user_notes(selected_chapter, selected_file)
            if notes:
                st.markdown("**历史笔记**")
                for i, note in enumerate(reversed(notes[:5])):  # 只显示最近5条笔记
                    note_time = datetime.fromisoformat(note["timestamp"]).strftime("%m-%d %H:%M")

                    # 使用expander来显示每条笔记，节省空间
                    with st.expander(f"📅 {note_time}", expanded=i==0):  # 只展开最新的笔记
                        st.markdown(note['content'])

                if len(notes) > 5:
                    st.markdown(f"*...还有 {len(notes) - 5} 条历史笔记*")
            else:
                st.markdown("*暂无笔记，开始记录你的学习心得吧！*")
    
    # 底部信息
    st.sidebar.markdown("---")
    st.sidebar.markdown("#### 关于课程")
    st.sidebar.markdown("动手学大模型应用开发 - 面向小白开发者的大模型应用开发教程")

if __name__ == "__main__":
    main()