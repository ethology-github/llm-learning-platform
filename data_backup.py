import streamlit as st
import os
import json
import zipfile
import shutil
from datetime import datetime
from pathlib import Path
import tempfile

# 学习数据目录
LEARN_DATA_DIR = os.path.join(os.path.dirname(__file__), ".learn_data")
BACKUP_DIR = os.path.join(os.path.dirname(__file__), ".backups")

# 确保备份目录存在
def ensure_backup_dir():
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)

# 创建数据备份
def create_backup():
    try:
        ensure_backup_dir()
        
        # 检查学习数据目录是否存在
        if not os.path.exists(LEARN_DATA_DIR):
            return False, "学习数据目录不存在"
        
        # 创建备份文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"learning_data_backup_{timestamp}.zip"
        backup_filepath = os.path.join(BACKUP_DIR, backup_filename)
        
        # 创建ZIP备份
        with zipfile.ZipFile(backup_filepath, 'w', zipfile.ZIP_DEFLATED) as backup_zip:
            # 添加所有学习数据文件
            for root, dirs, files in os.walk(LEARN_DATA_DIR):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, LEARN_DATA_DIR)
                    backup_zip.write(file_path, arcname)
        
        # 检查备份文件是否创建成功
        if os.path.exists(backup_filepath):
            return True, f"备份已创建: {backup_filename}"
        else:
            return False, "备份文件创建失败"
            
    except Exception as e:
        return False, f"创建备份时出错: {str(e)}"

# 获取备份文件列表
def get_backup_list():
    try:
        ensure_backup_dir()
        backups = []
        
        for file in os.listdir(BACKUP_DIR):
            if file.startswith("learning_data_backup_") and file.endswith(".zip"):
                file_path = os.path.join(BACKUP_DIR, file)
                # 获取文件信息
                stat = os.stat(file_path)
                size_mb = stat.st_size / (1024 * 1024)  # 转换为MB
                modified_time = datetime.fromtimestamp(stat.st_mtime)
                
                backups.append({
                    "filename": file,
                    "size_mb": round(size_mb, 2),
                    "created_time": modified_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "filepath": file_path
                })
        
        # 按创建时间倒序排列
        backups.sort(key=lambda x: x["created_time"], reverse=True)
        return backups
        
    except Exception as e:
        st.error(f"获取备份列表时出错: {str(e)}")
        return []

# 删除备份文件
def delete_backup(filename):
    try:
        backup_path = os.path.join(BACKUP_DIR, filename)
        if os.path.exists(backup_path):
            os.remove(backup_path)
            return True, "备份已删除"
        else:
            return False, "备份文件不存在"
    except Exception as e:
        return False, f"删除备份时出错: {str(e)}"

# 恢复数据备份
def restore_backup(backup_filepath):
    try:
        # 创建临时恢复目录
        with tempfile.TemporaryDirectory() as temp_dir:
            # 解压备份文件到临时目录
            with zipfile.ZipFile(backup_filepath, 'r') as backup_zip:
                backup_zip.extractall(temp_dir)
            
            # 备份当前数据（如果存在）
            if os.path.exists(LEARN_DATA_DIR):
                current_backup = os.path.join(BACKUP_DIR, f"current_data_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
                shutil.copytree(LEARN_DATA_DIR, current_backup)
            
            # 删除当前学习数据目录
            if os.path.exists(LEARN_DATA_DIR):
                shutil.rmtree(LEARN_DATA_DIR)
            
            # 复制恢复的数据
            shutil.copytree(temp_dir, LEARN_DATA_DIR)
            
        return True, "数据恢复成功"
        
    except Exception as e:
        return False, f"恢复数据时出错: {str(e)}"

# 清理旧备份（保留最近10个）
def cleanup_old_backups():
    try:
        backups = get_backup_list()
        if len(backups) > 10:
            # 删除最旧的备份
            for backup in backups[10:]:
                delete_backup(backup["filename"])
            return True, f"已清理 {len(backups) - 10} 个旧备份"
        return True, "无需清理备份"
    except Exception as e:
        return False, f"清理备份时出错: {str(e)}"

# 显示备份管理界面
def show_backup_manager():
    st.title("📦 数据备份与恢复")
    st.write("管理您的学习进度和笔记数据的备份。")
    
    # 创建选项卡
    tab1, tab2, tab3 = st.tabs(["📤 创建备份", "📥 恢复数据", "📋 备份管理"])
    
    with tab1:
        st.subheader("创建数据备份")
        st.write("将您当前的学习进度和笔记数据打包备份。")
        
        if st.button("🚀 立即创建备份", type="primary"):
            with st.spinner("正在创建备份..."):
                success, message = create_backup()
                if success:
                    st.success(message)
                    st.balloons()
                else:
                    st.error(message)
        
        st.info("💡 **提示**: 备份文件保存在 `.backups` 目录中，建议定期创建备份以防数据丢失。")
    
    with tab2:
        st.subheader("恢复数据备份")
        st.write("从之前的备份文件中恢复学习数据。")
        
        backups = get_backup_list()
        if backups:
            st.warning("⚠️ **注意**: 恢复数据将覆盖当前的学习进度和笔记，建议先创建当前数据的备份。")
            
            # 选择备份文件
            backup_options = {f"{b['filename']} ({b['created_time']}, {b['size_mb']}MB)": b for b in backups}
            selected_backup = st.selectbox("选择要恢复的备份文件", list(backup_options.keys()))
            
            if selected_backup:
                backup_info = backup_options[selected_backup]
                st.markdown(f"**文件名**: {backup_info['filename']}")
                st.markdown(f"**创建时间**: {backup_info['created_time']}")
                st.markdown(f"**文件大小**: {backup_info['size_mb']} MB")
                
                if st.button("🔄 恢复数据", type="secondary"):
                    with st.spinner("正在恢复数据..."):
                        success, message = restore_backup(backup_info['filepath'])
                        if success:
                            st.success(message)
                            st.info("请刷新页面以查看恢复后的数据。")
                        else:
                            st.error(message)
        else:
            st.info("没有找到备份文件。请先创建备份。")
    
    with tab3:
        st.subheader("备份文件管理")
        st.write("查看和管理所有备份文件。")
        
        backups = get_backup_list()
        if backups:
            # 显示备份统计
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("备份文件数量", len(backups))
            with col2:
                total_size = sum(b['size_mb'] for b in backups)
                st.metric("总大小", f"{total_size:.2f} MB")
            with col3:
                if backups:
                    latest_time = backups[0]['created_time']
                    st.metric("最新备份", latest_time)
            
            # 显示备份列表
            st.markdown("### 备份文件列表")
            for i, backup in enumerate(backups):
                with st.expander(f"📄 {backup['filename']}", expanded=i < 3):
                    col1, col2, col3 = st.columns([2, 1, 1])
                    with col1:
                        st.markdown(f"**创建时间**: {backup['created_time']}")
                        st.markdown(f"**文件大小**: {backup['size_mb']} MB")
                    with col2:
                        if st.button("📥 下载", key=f"download_{i}"):
                            # 提供下载功能
                            with open(backup['filepath'], 'rb') as f:
                                st.download_button(
                                    label="确认下载",
                                    data=f.read(),
                                    file_name=backup['filename'],
                                    mime="application/zip"
                                )
                    with col3:
                        if st.button("🗑️ 删除", key=f"delete_{i}"):
                            success, message = delete_backup(backup['filename'])
                            if success:
                                st.success(message)
                                st.rerun()
                            else:
                                st.error(message)
            
            # 清理旧备份
            st.markdown("### 清理备份")
            if len(backups) > 5:
                if st.button("🧹 清理旧备份（保留最近10个）"):
                    success, message = cleanup_old_backups()
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
            else:
                st.info("备份文件数量较少，无需清理。")
        else:
            st.info("没有找到备份文件。")
        
        # 手动清理选项
        st.markdown("### 危险操作")
        with st.expander("⚠️ 危险：删除所有备份", expanded=False):
            st.warning("此操作将删除所有备份文件，且无法恢复！")
            if st.button("🗑️ 删除所有备份", type="secondary"):
                if st.checkbox("我确认要删除所有备份文件"):
                    try:
                        shutil.rmtree(BACKUP_DIR)
                        ensure_backup_dir()
                        st.success("所有备份文件已删除")
                        st.rerun()
                    except Exception as e:
                        st.error(f"删除备份时出错: {str(e)}")

if __name__ == "__main__":
    show_backup_manager()