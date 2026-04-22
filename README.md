# Rizline Canvas SpeedKeyPoints Batch Editor

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

一个用于 **Rizline 自制谱面** 的批量速度节点编辑工具。

## 📌 项目背景

在使用官方 Rizline Editor 制谱时，向画布（Canvas）添加 `speedKeyPoints`（速度节点）需要逐个手动操作。当画布数量多、节点密集时，效率非常低。

本工具通过直接解析 `.json` 谱面文件的 JSON 结构，实现**一次性向画布批量插入速度节点**，极大提升制谱效率。

## ✨ 功能特性

- 🚀 向画布添加速度节点
- 📝 支持自定义时间点速度值
- 🔧 基于 Python 原生库，无需额外安装复杂依赖
- ✅ 保持 JSON 结构与官方编辑器完全兼容

## 📦 使用前准备

1. 安装 Python 3.8 或更高版本
2. 克隆本仓库或下载 `main.py`

```bash
git clone https://github.com/你的用户名/Rizline-Canvas-SpeedKeyPoints-Batch-Editor.git