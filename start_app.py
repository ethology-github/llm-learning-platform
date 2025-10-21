import os
import subprocess
import sys
import time

def check_python_version():
    """检查Python版本是否满足要求"""
    required_version = (3, 7)
    current_version = sys.version_info
    if current_version < required_version:
        print(f"错误: Python版本需要 {required_version[0]}.{required_version[1]} 或更高版本，当前版本是 {current_version[0]}.{current_version[1]}")
        return False
    return True

def install_dependencies_with_mirror():
    """使用国内镜像源安装依赖包，解决SSL问题"""
    mirrors = {
        "1": "-i https://pypi.tuna.tsinghua.edu.cn/simple",
        "2": "-i https://mirrors.aliyun.com/pypi/simple/",
        "3": "-i https://pypi.doubanio.com/simple/",
        "0": ""
    }
    
    print("\n检测到可能存在SSL连接问题，建议使用国内镜像源安装依赖")
    print("请选择镜像源(默认为不使用镜像):")
    print("1. 清华大学镜像源")
    print("2. 阿里云镜像源")
    print("3. 豆瓣镜像源")
    print("0. 不使用镜像源")
    
    choice = input("请输入选择(1-3, 默认为0): ") or "0"
    mirror = mirrors.get(choice, "")
    
    packages = ["streamlit", "pandas", "matplotlib", "seaborn"]
    
    print(f"\n正在使用镜像源安装依赖: {choice if choice != '0' else '不使用镜像'}")
    
    # 尝试先升级pip
    try:
        print("正在升级pip...")
        cmd = [sys.executable, "-m", "pip", "install", "--upgrade", "pip"]
        if mirror:
            cmd.extend(mirror.split())
        subprocess.check_call(cmd, shell=os.name == 'nt')
    except Exception as e:
        print(f"升级pip时出错: {str(e)}，继续安装其他依赖")
    
    # 安装所有依赖
    for package in packages:
        try:
            __import__(package)
            print(f"{package} 已经安装")
        except ImportError:
            print(f"正在安装{package}...")
            try:
                cmd = [sys.executable, "-m", "pip", "install", package]
                if mirror:
                    cmd.extend(mirror.split())
                subprocess.check_call(cmd, shell=os.name == 'nt')
                print(f"{package} 安装成功")
            except Exception as e:
                print(f"安装{package}时出错: {str(e)}")
                print(f"尝试使用--trusted-host选项重新安装{package}...")
                try:
                    cmd = [sys.executable, "-m", "pip", "install", package, "--trusted-host", "pypi.org", "--trusted-host", "files.pythonhosted.org"]
                    if mirror:
                        cmd.extend(mirror.split())
                        # 为镜像源添加trusted-host
                        if "tuna.tsinghua" in mirror:
                            cmd.extend(["--trusted-host", "pypi.tuna.tsinghua.edu.cn"])
                        elif "aliyun" in mirror:
                            cmd.extend(["--trusted-host", "mirrors.aliyun.com"])
                        elif "douban" in mirror:
                            cmd.extend(["--trusted-host", "pypi.doubanio.com"])
                    subprocess.check_call(cmd, shell=os.name == 'nt')
                    print(f"{package} 安装成功")
                except Exception as e2:
                    print(f"重新安装{package}失败: {str(e2)}")
                    print(f"\n安装{package}失败，请尝试手动安装:\n{sys.executable} -m pip install {package} {mirror}")
                    return False
    
    return True

def install_dependencies():
    """尝试直接安装依赖，如果失败则使用镜像源"""
    try:
        # 检查是否已经安装了所有依赖
        import streamlit
        import pandas
        import matplotlib
        import seaborn
        print("所有必要的依赖已安装")
        return True
    except ImportError:
        # 尝试直接安装，如果失败则使用镜像源
        try:
            print("尝试直接安装依赖...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit", "pandas", "matplotlib", "seaborn"])
            return True
        except Exception as e:
            print(f"直接安装失败: {str(e)}")
            print("尝试使用国内镜像源重新安装...")
            return install_dependencies_with_mirror()

def run_app():
    """运行Streamlit应用"""
    try:
        # 检查app.py是否存在
        if not os.path.exists("app.py"):
            print("错误: 找不到app.py文件")
            return False
        
        # 运行Streamlit应用
        print("正在启动大模型应用开发学习平台...")
        print("请稍候，浏览器将自动打开应用界面...")
        
        # 在Windows系统上运行streamlit
        if os.name == 'nt':  # Windows系统
            subprocess.Popen([sys.executable, "-m", "streamlit", "run", "app.py"])
        else:  # 其他系统
            subprocess.Popen([sys.executable, "-m", "streamlit", "run", "app.py"])
            
        # 等待浏览器打开
        time.sleep(3)
        print("应用已成功启动！")
        print("如果浏览器没有自动打开，请手动访问 http://localhost:8501")
        return True
    except Exception as e:
        print(f"启动应用时出错: {str(e)}")
        return False

def main():
    """主函数"""
    print("===== 大模型应用开发学习平台 ======")
    
    # 检查Python版本
    if not check_python_version():
        return
    
    # 安装依赖
    install_dependencies()
    
    # 运行应用
    if run_app():
        print("\n使用说明:")
        print("1. 在侧边栏可以切换首页、学习页面和统计页面")
        print("2. 在学习页面可以浏览课程内容、标记完成状态、添加学习笔记")
        print("3. 在统计页面可以查看学习进度和数据统计")
        print("4. 如有问题，请关闭命令窗口后重新运行此脚本")
    
    print("\n按任意键退出...")
    input()

if __name__ == "__main__":
    main()