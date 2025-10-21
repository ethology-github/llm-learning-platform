@echo off

:: 设置命令行编码为UTF-8，确保中文显示正常
chcp 65001 >nul

:: 显示欢迎信息
cls
echo ===================================================================
echo                    大模型应用开发学习网站
echo ===================================================================
echo.
echo 本程序将帮您启动学习网站，支持课程浏览、学习进度跟踪和笔记功能。
echo.
echo 正在准备启动环境...
echo.

:: 检查Python是否已安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未找到Python。请先安装Python 3.7或更高版本。
    echo 安装完成后，请将Python添加到系统环境变量中。
    echo.
    echo 按任意键退出...
    pause >nul
    exit /b 1
)

:: 运行启动脚本
python start_app.py

:: 如果出现问题，提供手动启动选项
if %errorlevel% neq 0 (
    echo.
    echo 启动失败！尝试手动启动应用...
    echo.
    call :manual_start
)

:: 保持窗口打开
:end
    echo.
    echo 应用程序已退出。
    echo 按任意键关闭窗口...
    pause >nul
    exit /b 0

:: 手动启动函数
:manual_start
    echo 请选择操作:
    echo 1. 尝试直接启动Streamlit应用
    echo 2. 安装依赖后启动
    echo 3. 取消
    
    set /p choice=请输入选择(1-3): 
    
    if "%choice%" == "1" (
        echo 正在启动Streamlit应用...
        python -m streamlit run app.py
    ) else if "%choice%" == "2" (
        echo 请选择国内镜像源:
        echo 1. 清华大学 (https://pypi.tuna.tsinghua.edu.cn/simple)
        echo 2. 阿里云 (https://mirrors.aliyun.com/pypi/simple/)
        echo 3. 豆瓣 (https://pypi.doubanio.com/simple/)
        
        set /p mirror_choice=请输入选择(1-3): 
        
        set "mirror="
        if "%mirror_choice%" == "1" set "mirror=-i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn"
        if "%mirror_choice%" == "2" set "mirror=-i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com"
        if "%mirror_choice%" == "3" set "mirror=-i https://pypi.doubanio.com/simple/ --trusted-host pypi.doubanio.com"
        
        echo 正在安装依赖...
        python -m pip install --upgrade pip %mirror%
        python -m pip install streamlit pandas matplotlib seaborn %mirror%
        
        echo 依赖安装完成，正在启动应用...
        python -m streamlit run app.py
    )
    
    goto end