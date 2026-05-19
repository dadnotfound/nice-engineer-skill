#!/usr/bin/env python3
"""
最小可运行实现检查工具
Nice Engineer 核心原则：先写最简单能运行的实现
"""

import os
import sys
import json
from pathlib import Path

class MinimalProjectChecker:
    def __init__(self, project_path):
        self.project_path = Path(project_path)
        self.issues = []
        self.scores = {
            'simplicity': 0,
            'functionality': 0,
            'deployability': 0,
            'maintainability': 0
        }

    def check(self):
        """执行检查"""
        print(f"🔍 检查项目: {self.project_path}")
        print("=" * 50)

        # 基础结构检查
        self.check_structure()

        # 代码规模检查
        self.check_code_scale()

        # 依赖检查
        self.check_dependencies()

        # 功能完整性检查
        self.check_functionality()

        # 部署准备检查
        self.check_deployability()

        # 输出结果
        self.report()

    def check_structure(self):
        """检查项目结构"""
        print("\n📁 检查项目结构...")

        required_files = {
            'index.html': '主页',
            'style.css': '样式文件',
            'script.js': '脚本文件'
        }

        for file, desc in required_files.items():
            file_path = self.project_path / file
            if file_path.exists():
                print(f"  ✅ {desc}: {file}")
            else:
                self.issues.append(f"❌ 缺少 {desc}: {file}")
                print(f"  ❌ 缺少 {desc}: {file}")

    def check_code_scale(self):
        """检查代码规模"""
        print("\n📏 检查代码规模...")

        max_lines = 800
        max_function_lines = 20

        for ext in ['.html', '.css', '.js']:
            for file_path in self.project_path.rglob(f"*{ext}"):
                if 'node_modules' in str(file_path):
                    continue

                try:
                    lines = len(file_path.read_text(encoding='utf-8').splitlines())

                    if lines > max_lines:
                        self.issues.append(f"❌ {file_path} 超过 {max_lines} 行 ({lines} 行)")
                        print(f"  ❌ {file_path.name}: {lines} 行 (建议 < {max_lines})")
                    else:
                        print(f"  ✅ {file_path.name}: {lines} 行")

                    # 检查函数长度
                    if ext == '.js':
                        self.check_function_lengths(file_path)

                except Exception as e:
                    self.issues.append(f"❌ 读取文件失败 {file_path}: {e}")

    def check_function_lengths(self, file_path):
        """检查函数长度"""
        content = file_path.read_text(encoding='utf-8')
        lines = content.splitlines()

        in_function = False
        function_start = 0
        indent_level = 0
        current_indent = 0

        for i, line in enumerate(lines):
            stripped = line.strip()

            # 跳过注释
            if stripped.startswith('//') or stripped.startswith('/*') or stripped.startswith('*'):
                continue

            # 计算缩进
            if line:
                current_indent = len(line) - len(line.lstrip())

            # 函数开始
            if (stripped.startswith('function ') or
                stripped.startswith('async function ') or
                '=>' in stripped and '=' in stripped):
                in_function = True
                function_start = i
                indent_level = current_indent

            # 函数结束
            elif in_function and current_indent <= indent_level and stripped:
                function_length = i - function_start
                if function_length > 20:
                    self.issues.append(f"❌ {file_path.name} 函数过长 {function_length} 行")
                    print(f"  ⚠️  函数过长: ~{function_length} 行")
                in_function = False

    def check_dependencies(self):
        """检查依赖"""
        print("\n📦 检查依赖...")

        # 检查 package.json
        package_json = self.project_path / 'package.json'
        if package_json.exists():
            deps = json.loads(package_json.read_text())
            dependencies = deps.get('dependencies', {})
            dev_dependencies = deps.get('devDependencies', {})

            total_deps = len(dependencies) + len(dev_dependencies)

            if total_deps > 3:
                self.issues.append(f"⚠️  依赖过多 ({total_deps} > 3)")
                print(f"  ⚠️  依赖过多: {total_deps} 个")
            else:
                print(f"  ✅ 依赖数量: {total_deps}")

            # 列出依赖
            for dep, version in dependencies.items():
                print(f"    - {dep}: {version}")
        else:
            print("  ✅ 无依赖 (纯静态)")

    def check_functionality(self):
        """检查功能完整性"""
        print("\n🎯 检查功能完整性...")

        # 检查关键功能
        checks = [
            ('index.html', '主页面存在'),
            ('有基本样式', 'CSS样式'),
            ('有交互功能', 'JavaScript功能'),
            ('响应式设计', '移动端适配')
        ]

        for check, desc in checks:
            if self.check_feature(check):
                print(f"  ✅ {desc}")
                self.scores['functionality'] += 25
            else:
                self.issues.append(f"❌ 缺少 {desc}")
                print(f"  ❌ 缺少 {desc}")

    def check_feature(self, feature):
        """检查特定功能"""
        if feature == 'index.html':
            return (self.project_path / 'index.html').exists()

        elif feature == '有基本样式':
            css_files = list(self.project_path.rglob('*.css'))
            return len(css_files) > 0

        elif feature == '有交互功能':
            js_files = list(self.project_path.rglob('*.js'))
            if not js_files:
                return False

            # 检查是否有事件监听器
            for js_file in js_files:
                content = js_file.read_text()
                if 'addEventListener' in content or 'onclick' in content:
                    return True
            return False

        elif feature == '响应式设计':
            # 检查CSS是否有媒体查询
            css_files = list(self.project_path.rglob('*.css'))
            for css_file in css_files:
                content = css_file.read_text()
                if '@media' in content:
                    return True
            return False

        return False

    def check_deployability(self):
        """检查可部署性"""
        print("\n🚀 检查可部署性...")

        # 检查静态文件
        static_files = ['index.html', 'style.css', 'script.js']
        has_static = all((self.project_path / f).exists() for f in static_files)

        if has_static:
            print("  ✅ 可以静态部署")
            self.scores['deployability'] = 100

            # 检查构建脚本
            if (self.project_path / 'build.sh').exists() or (self.project_path / 'package.json').exists():
                print("  ✅ 有构建配置")
        else:
            self.issues.append("❌ 缺少必要的静态文件")
            print("  ❌ 无法静态部署")

    def report(self):
        """生成报告"""
        print("\n" + "=" * 50)
        print("📊 检查报告")
        print("=" * 50)

        # 评分
        total_score = sum(self.scores.values())
        print(f"\n总分: {total_score}/400")

        for category, score in self.scores.items():
            print(f"{category}: {score}/100")

        # 评级
        if total_score >= 300:
            grade = "优秀"
        elif total_score >= 200:
            grade = "良好"
        elif total_score >= 100:
            grade = "及格"
        else:
            grade = "需要改进"

        print(f"\n评级: {grade}")

        # 建议
        print("\n💡 建议:")
        if self.issues:
            for issue in self.issues[:3]:  # 只显示前3个主要问题
                print(f"  - {issue}")
        else:
            print("  ✅ 项目符合 Nice Engineer 标准!")

        # 行动计划
        print("\n🎯 行动计划:")
        if total_score < 300:
            print("1. 简化代码结构")
            print("2. 减少外部依赖")
            print("3. 确保核心功能完整")
            print("4. 添加部署配置")

def main():
    if len(sys.argv) != 2:
        print("用法: python execute-minimal.py <项目路径>")
        sys.exit(1)

    project_path = sys.argv[1]
    checker = MinimalProjectChecker(project_path)
    checker.check()

if __name__ == "__main__":
    main()