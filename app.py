import streamlit as st
import importlib.util
import os
from datetime import datetime

# 设置页面配置
st.set_page_config(
    page_title="大模型应用开发学习平台",
    page_icon=":books:",
    layout="wide"
)

# 确保学习数据目录存在
LEARN_DATA_DIR = os.path.join(os.path.dirname(__file__), ".learn_data")
if not os.path.exists(LEARN_DATA_DIR):
    os.makedirs(LEARN_DATA_DIR)

# 自定义CSS样式
def add_custom_css():
    st.markdown("""
    <style>
    /* 主容器样式 */
    .main-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 20px;
    }
    
    /* 标题样式 */
    .title-section {
        text-align: center;
        margin-bottom: 40px;
        padding: 20px;
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); /* 清新渐变色 */
        border-radius: 10px;
        color: #333; /* 深色字体 */
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    .title-section h1 {
        color: #333;
    }

    /* 功能按钮样式 */
    .feature-buttons {
        display: flex;
        justify-content: center;
        gap: 20px;
        margin-bottom: 40px;
    }
    
    .stButton>button { /* Streamlit 按钮的通用样式 */
        padding: 15px 30px;
        border: none;
        border-radius: 8px;
        font-size: 18px;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease;
        text-decoration: none;
        color: white;
        background-color: #6a82fb; /* 清新蓝色 */
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
        background-color: #8a9cfb; /* 悬停颜色 */
    }
    
    /* 介绍卡片样式 */
    .intro-cards {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); /* 调整卡片宽度 */
        gap: 20px;
        margin-bottom: 40px;
    }
    
    .intro-card {
        padding: 20px;
        border-radius: 10px;
        background-color: #ffffff; /* 白色背景 */
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        height: 100%; /* 确保卡片高度一致 */
    }
    
    .intro-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }
    
    .intro-card h3 {
        color: #4CAF50; /* 绿色标题 */
        margin-bottom: 10px;
    }
    
    .intro-card p {
        color: #555;
        font-size: 14px;
        line-height: 1.6;
        flex-grow: 1; /* 让段落占据剩余空间 */
    }

    .intro-card .stButton>button {
        background-color: #4CAF50; /* 卡片内按钮颜色 */
        margin-top: 15px;
        width: 100%; /* 按钮宽度 */
    }

    .intro-card .stButton>button:hover {
        background-color: #6cb36e;
    }
    
    /* 学习提示样式 */
    .learning-tips {
        padding: 20px;
        background-color: #e6f7ff; /* 浅蓝色背景 */
        border-radius: 10px;
        border-left: 4px solid #1890ff; /* 蓝色边框 */
        margin-bottom: 40px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    /* 页脚样式 */
    .footer {
        text-align: center;
        padding: 20px;
        margin-top: 40px;
        background-color: #f0f2f5; /* 浅灰色背景 */
        border-radius: 10px;
        color: #777;
        font-size: 14px;
    }
    </style>
    """, unsafe_allow_html=True)

# 主页面内容
def show_home_page():
    # 添加自定义CSS
    add_custom_css()
    
    # 标题部分
    st.markdown("""
    <div class="title-section">
        <h1>动手学大模型应用开发</h1>
        <p>面向小白开发者的大模型应用开发教程</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 功能按钮部分
    st.markdown("<div class=\"feature-buttons\">", unsafe_allow_html=True)
    col_start, col_stats = st.columns(2)
    with col_start:
        if st.button("开始学习", key="home_start_learning_btn"):
            st.session_state['page'] = '开始学习'
            st.rerun()
    with col_stats:
        if st.button("学习统计", key="home_view_stats_btn"):
            st.session_state['page'] = '学习统计'
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    # 项目介绍部分
    st.header("项目简介")
    st.markdown("""
    本项目是一个面向小白开发者的大模型应用开发教程，旨在基于阿里云服务器，结合个人知识库助手项目，通过一个课程完成大模型开发的重点入门。
    """)
    
    # Hardcoded mapping for intro cards to chapters
    chapter_mapping = {
        "大模型简介": "C1 大型语言模型 LLM 介绍",
        "调用大模型 API": "C2 使用 LLM API 开发应用",
        "知识库搭建": "C3 搭建知识库",
        "构建 RAG 应用": "C4 构建 RAG 应用",
        "验证迭代": "C5 系统评估与优化"
    }

    card_data = [
        {"title": "大模型简介", "description": "了解什么是大模型、大模型特点是什么、LangChain 是什么，如何开发一个 LLM 应用的基础知识。"},
        {"title": "调用大模型 API", "description": "学习国内外知名大模型产品 API 的多种调用方式，包括调用原生 API、封装为 LangChain LLM 等。"},
        {"title": "知识库搭建", "description": "掌握不同类型知识库文档的加载、处理，以及向量数据库的搭建方法。"},
        {"title": "构建 RAG 应用", "description": "学习将 LLM 接入到 LangChain 构建检索问答链，使用 Streamlit 进行应用部署。"},
        {"title": "验证迭代", "description": "了解大模型开发如何实现验证迭代，掌握一般的评估方法。"}
    ]

    st.markdown("<div class=\"intro-cards\">", unsafe_allow_html=True)
    cols = st.columns(len(card_data))
    for i, col in enumerate(cols):
        with col:
            st.markdown(f"""
            <div class="intro-card">
                <h3>{card_data[i]['title']}</h3>
                <p>{card_data[i]['description']}</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"进入学习 {card_data[i]['title']}", key=f"card_btn_{i}"):
                st.session_state['page'] = '开始学习'
                st.session_state['initial_chapter'] = chapter_mapping[card_data[i]['title']]
                st.session_state['initial_file'] = None # learning_app will pick the first file
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    # 学习提示部分
    with st.expander("💡 学习指南与提示", expanded=True):
        st.markdown("""
        ### 🎯 学习目标
        - 掌握大模型应用开发的核心技能
        - 学会使用各种大模型 API
        - 理解 RAG 技术的原理与应用
        - 能够独立开发大模型应用
        
        ### 📚 学习路径
        1. **基础知识** - 了解大模型和 LangChain
        2. **API 调用** - 学习使用各种大模型服务
        3. **知识库** - 搭建向量数据库和知识检索
        4. **应用开发** - 构建完整的 RAG 应用
        5. **优化迭代** - 评估和改进应用性能
        
        ### ⚡ 快速开始
        - 🎯 **零基础友好**：无需 AI 背景，只需 Python 基础
        - 🔄 **循序渐进**：从理论到实践，逐步深入
        - 💾 **进度跟踪**：自动记录学习进度和笔记
        - 🔍 **内容搜索**：快速查找所需知识点
        """)
    
    # 页脚部分
    st.markdown("""
    <div class="footer">
        <p>© 2024 大模型应用开发学习平台 | 基于 Datawhale 的动手学大模型应用开发项目</p>
    </div>
    """, unsafe_allow_html=True)

# 加载并显示学习应用
def load_learning_app(initial_chapter=None, initial_file=None):
    # 尝试导入并运行学习应用
    try:
        # 检查文件是否存在
        if not os.path.exists("./learning_app.py"):
            st.error("学习应用文件 learning_app.py 不存在")
            st.info("请确保所有必要的文件都在项目目录中。")
            return
            
        # 动态导入学习应用模块
        spec = importlib.util.spec_from_file_location("learning_app", "./learning_app.py")
        if spec is None or spec.loader is None:
            st.error("无法加载学习应用模块")
            return
            
        learning_app = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(learning_app)
        
        # 运行主函数，并传递初始章节和文件
        if hasattr(learning_app, "main"):
            learning_app.main(initial_chapter=initial_chapter, initial_file=initial_file)
        else:
            st.error("学习应用模块缺少 main 函数")
            
    except ImportError as e:
        st.error(f"导入学习应用时出错: {str(e)}")
        st.info("请检查所有必要的依赖包是否已安装。")
    except Exception as e:
        st.error(f"加载学习应用时出现未知错误: {str(e)}")
        st.info("请检查 learning_app.py 文件是否存在且正确。")

# 加载并显示学习统计
def load_learning_stats():
    try:
        # 检查文件是否存在
        if not os.path.exists("./learning_stats.py"):
            st.error("学习统计文件 learning_stats.py 不存在")
            st.info("请确保所有必要的文件都在项目目录中。")
            return
            
        # 动态导入学习统计模块
        spec = importlib.util.spec_from_file_location("learning_stats", "./learning_stats.py")
        if spec is None or spec.loader is None:
            st.error("无法加载学习统计模块")
            return
            
        learning_stats = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(learning_stats)
        
        # 运行显示统计函数
        if hasattr(learning_stats, "show_statistics"):
            learning_stats.show_statistics()
        else:
            st.error("学习统计模块缺少 show_statistics 函数")
            
    except ImportError as e:
        st.error(f"导入学习统计时出错: {str(e)}")
        st.info("请检查所有必要的依赖包是否已安装。")
    except Exception as e:
        st.error(f"加载学习统计时出现未知错误: {str(e)}")
        st.info("请检查 learning_stats.py 文件是否存在且正确。")

# 加载并显示搜索应用
def load_search_app():
    try:
        # 检查文件是否存在
        if not os.path.exists("./search_app.py"):
            st.error("搜索应用文件 search_app.py 不存在")
            st.info("请确保所有必要的文件都在项目目录中。")
            return
            
        spec = importlib.util.spec_from_file_location("search_app", "./search_app.py")
        if spec is None or spec.loader is None:
            st.error("无法加载搜索应用模块")
            return
            
        search_app = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(search_app)
        if hasattr(search_app, "main"):
            search_app.main()
        else:
            st.error("搜索应用模块缺少 main 函数")
            
    except ImportError as e:
        st.error(f"导入搜索应用时出错: {str(e)}")
        st.info("请检查所有必要的依赖包是否已安装。")
    except Exception as e:
        st.error(f"加载搜索应用时出现未知错误: {str(e)}")
        st.info("请检查 search_app.py 文件是否存在且正确。")

# 加载并显示数据备份管理
def load_backup_manager():
    try:
        # 检查文件是否存在
        if not os.path.exists("./data_backup.py"):
            st.error("数据备份管理文件 data_backup.py 不存在")
            st.info("请确保所有必要的文件都在项目目录中。")
            return
            
        spec = importlib.util.spec_from_file_location("data_backup", "./data_backup.py")
        if spec is None or spec.loader is None:
            st.error("无法加载数据备份管理模块")
            return
            
        backup_manager = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(backup_manager)
        if hasattr(backup_manager, "show_backup_manager"):
            backup_manager.show_backup_manager()
        else:
            st.error("数据备份管理模块缺少 show_backup_manager 函数")
            
    except ImportError as e:
        st.error(f"导入数据备份管理时出错: {str(e)}")
        st.info("请检查所有必要的依赖包是否已安装。")
    except Exception as e:
        st.error(f"加载数据备份管理时出现未知错误: {str(e)}")
        st.info("请检查 data_backup.py 文件是否存在且正确。")

# 主函数
def main():
    # Initialize session_state
    if 'page' not in st.session_state:
        st.session_state['page'] = '首页'
    if 'initial_chapter' not in st.session_state:
        st.session_state['initial_chapter'] = None
    if 'initial_file' not in st.session_state:
        st.session_state['initial_file'] = None

    # Create page selector in sidebar
    page_options = ["首页", "开始学习", "学习统计", "搜索", "数据备份"]
    
    # Find the index of the current page in the options list
    try:
        current_page_index = page_options.index(st.session_state['page'])
    except ValueError:
        current_page_index = 0 # Default to home if not found

    selected_page_from_sidebar = st.sidebar.selectbox(
        "选择页面",
        page_options,
        index=current_page_index,
        key='sidebar_page_select'
    )
    
    # If sidebar selection changes, update session_state and rerun
    if selected_page_from_sidebar != st.session_state['page']:
        st.session_state['page'] = selected_page_from_sidebar
        st.rerun()

    # Render page based on session_state
    if st.session_state['page'] == "首页":
        show_home_page()
    elif st.session_state['page'] == "开始学习":
        load_learning_app(initial_chapter=st.session_state['initial_chapter'], initial_file=st.session_state['initial_file'])
        # Reset initial chapter/file after loading to prevent re-navigation on rerun
        st.session_state['initial_chapter'] = None
        st.session_state['initial_file'] = None
        # Also reset navigation processed flag
        if 'navigation_processed' in st.session_state:
            del st.session_state['navigation_processed']
    elif st.session_state['page'] == "学习统计":
        load_learning_stats()
    elif st.session_state['page'] == "搜索":
        load_search_app()
    elif st.session_state['page'] == "数据备份":
        load_backup_manager()

if __name__ == "__main__":
    main()