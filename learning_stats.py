import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

# 设置中文字体
plt.rcParams["font.family"] = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC"]

# 学习数据目录
LEARN_DATA_DIR = os.path.join(os.path.dirname(__file__), ".learn_data")
PROGRESS_FILE = os.path.join(LEARN_DATA_DIR, "user_progress.json")
NOTES_FILE = os.path.join(LEARN_DATA_DIR, "user_notes.json")

# 课程结构
COURSE_STRUCTURE = {
    "C1 大型语言模型 LLM 介绍": ["1.大型语言模型 LLM 理论简介.md", "2.检索增强生成 RAG 简介.md", "3.LangChain 简介.md", "4.开发 LLM 应用的整体流程.md", "5.阿里云服务器的基本使用.md", "6.GitHub Codespaces 的基本使用（选修）.md", "7.环境配置.md"],
    "C2 使用 LLM API 开发应用": ["1. 基本概念.md", "2. 使用 LLM API.ipynb", "3. Prompt Engineering.ipynb"],
    "C3 搭建知识库": ["1.向量及向量知识库介绍.md", "2.使用 Embedding API.ipynb", "3.数据处理.ipynb", "4.搭建并使用向量数据库.ipynb"],
    "C4 构建 RAG 应用": ["1.LLM 接入 LangChain.ipynb", "2.构建检索问答链.ipynb", "3.部署知识库助手.ipynb"],
    "C5 系统评估与优化": ["1.如何评估 LLM 应用.ipynb", "2.评估并优化生成部分.ipynb", "3.评估并优化检索部分.md"]
}

# 加载用户进度
def load_user_progress():
    if not os.path.exists(PROGRESS_FILE):
        return {}
    try:
        with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

# 加载用户笔记
def load_user_notes():
    if not os.path.exists(NOTES_FILE):
        return {}
    try:
        with open(NOTES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

# 计算总体进度
def calculate_overall_progress():
    progress = load_user_progress()
    total = len(progress)
    if total == 0:
        return 0
    completed = sum(1 for item in progress.values() if item["completed"])
    return completed / total

# 计算各章节进度
def calculate_chapter_progress():
    progress = load_user_progress()
    chapter_progress = {}
    
    for chapter, files in COURSE_STRUCTURE.items():
        chapter_files = [f"{chapter}/{file}" for file in files]
        chapter_total = len(chapter_files)
        chapter_completed = sum(1 for file in chapter_files if file in progress and progress[file]["completed"])
        chapter_progress[chapter] = chapter_completed / chapter_total if chapter_total > 0 else 0
    
    return chapter_progress

# 获取学习活动数据
def get_learning_activity_data():
    progress = load_user_progress()
    activities = []
    
    for file_path, data in progress.items():
        if data["last_accessed"]:
            # 提取章节信息
            chapter = file_path.split("/")[0]
            file_name = file_path.split("/")[1]
            
            activity = {
                "章节": chapter,
                "文件": file_name,
                "访问次数": data["access_count"],
                "最后访问时间": data["last_accessed"],
                "是否完成": data["completed"]
            }
            activities.append(activity)
    
    # 按最后访问时间排序
    activities.sort(key=lambda x: x["最后访问时间"], reverse=True)
    return activities

# 生成学习时间统计
def get_learning_time_statistics():
    activities = get_learning_activity_data()
    if not activities:
        return None
    
    # 转换时间格式
    for activity in activities:
        activity["最后访问时间"] = datetime.fromisoformat(activity["最后访问时间"])
    
    # 按日期分组统计
    date_stats = {}
    for activity in activities:
        date_str = activity["最后访问时间"].strftime("%Y-%m-%d")
        if date_str not in date_stats:
            date_stats[date_str] = 0
        date_stats[date_str] += 1
    
    # 转换为DataFrame
    df = pd.DataFrame(list(date_stats.items()), columns=["日期", "学习次数"])
    df = df.sort_values("日期")
    return df

# 生成笔记统计
def get_notes_statistics():
    notes = load_user_notes()
    note_counts = {}
    
    for file_path, file_notes in notes.items():
        chapter = file_path.split("/")[0]
        if chapter not in note_counts:
            note_counts[chapter] = 0
        note_counts[chapter] += len(file_notes)
    
    return note_counts

# 主统计页面
def show_statistics():
    st.title("我的学习统计")
    
    # 总体进度卡片
    overall_progress = calculate_overall_progress()
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("总体完成进度", f"{int(overall_progress * 100)}%")
    
    with col2:
        progress_data = load_user_progress()
        total_files = len(progress_data)
        completed_files = sum(1 for item in progress_data.values() if item["completed"])
        st.metric("已完成学习材料", f"{completed_files}/{total_files}")
    
    with col3:
        notes_data = load_user_notes()
        total_notes = sum(len(notes) for notes in notes_data.values())
        st.metric("我的笔记总数", total_notes)
    
    # 各章节进度图表
    st.subheader("各章节学习进度")
    chapter_progress = calculate_chapter_progress()
    
    if chapter_progress:
        fig, ax = plt.subplots(figsize=(10, 6))
        chapters = list(chapter_progress.keys())
        progress_values = list(chapter_progress.values())
        
        bars = ax.barh(chapters, progress_values, color='skyblue')
        ax.set_xlabel('完成进度')
        ax.set_xlim(0, 1)
        
        # 添加百分比标签
        for bar, value in zip(bars, progress_values):
            ax.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height()/2, 
                    f'{int(value*100)}%', va='center')
        
        st.pyplot(fig)
    else:
        st.info("暂无学习进度数据")
    
    # 学习活动表格
    st.subheader("最近学习活动")
    activities = get_learning_activity_data()
    
    if activities:
        # 转换时间格式以便显示
        for activity in activities:
            activity["最后访问时间"] = datetime.fromisoformat(activity["最后访问时间"]).strftime("%Y-%m-%d %H:%M:%S")
            activity["是否完成"] = "是" if activity["是否完成"] else "否"
        
        df_activities = pd.DataFrame(activities)
        st.dataframe(df_activities, use_container_width=True)
    else:
        st.info("暂无学习活动数据")
    
    # 学习时间趋势
    st.subheader("学习时间趋势")
    time_stats = get_learning_time_statistics()
    
    if time_stats is not None and not time_stats.empty:
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.lineplot(data=time_stats, x="日期", y="学习次数", ax=ax)
        ax.set_xlabel("日期")
        ax.set_ylabel("学习次数")
        plt.xticks(rotation=45)
        st.pyplot(fig)
    else:
        st.info("暂无学习时间统计数据")
    
    # 笔记统计
    st.subheader("笔记统计")
    notes_stats = get_notes_statistics()
    
    if notes_stats:
        fig, ax = plt.subplots(figsize=(10, 6))
        chapters = list(notes_stats.keys())
        note_counts = list(notes_stats.values())
        
        bars = ax.bar(chapters, note_counts, color='lightgreen')
        ax.set_xlabel('章节')
        ax.set_ylabel('笔记数量')
        plt.xticks(rotation=45, ha='right')
        
        # 添加数值标签
        for bar, value in zip(bars, note_counts):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                    str(value), ha='center')
        
        st.pyplot(fig)
    else:
        st.info("暂无笔记统计数据")
    
    # 学习建议
    st.subheader("学习建议")
    if overall_progress < 0.3:
        st.info("您刚刚开始学习之旅！建议先从C1章节的基础内容开始，逐步建立对大模型的理解。")
    elif overall_progress < 0.6:
        st.info("不错的进展！继续保持学习节奏，建议多实践代码示例，加深理解。")
    elif overall_progress < 0.9:
        st.info("已经掌握了大部分内容！建议尝试完成项目实践，巩固所学知识。")
    else:
        st.success("恭喜您！已经完成了大部分学习内容。可以尝试开发自己的大模型应用了！")

if __name__ == "__main__":
    show_statistics()