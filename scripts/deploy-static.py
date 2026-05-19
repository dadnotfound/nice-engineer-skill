#!/usr/bin/env python3
"""
静态部署脚本
Nice Engineer 核心原则：优先静态托管，零配置部署
"""

import os
import sys
import json
import subprocess
import shutil
from pathlib import Path

class StaticDeployer:
    def __init__(self, project_path, deploy_config=None):
        self.project_path = Path(project_path)
        self.deploy_config = deploy_config or {}
        self.build_dir = self.project_path / 'dist'

    def deploy(self):
        """执行部署"""
        print(f"🚀 开始部署: {self.project_path}")
        print("=" * 50)

        # 1. 检查项目
        self.check_project()

        # 2. 构建项目
        self.build_project()

        # 3. 选择部署平台
        platform = self.deploy_config.get('platform', 'cloudflare')

        if platform == 'cloudflare':
            self.deploy_to_cloudflare()
        elif platform == 'github':
            self.deploy_to_github()
        elif platform == 'netlify':
            self.deploy_to_netlify()
        else:
            print(f"❌ 不支持的部署平台: {platform}")
            return False

        print("\n🎉 部署完成!")
        return True

    def check_project(self):
        """检查项目是否符合部署条件"""
        print("\n📋 检查项目...")

        required_files = ['index.html', 'style.css']
        missing_files = []

        for file in required_files:
            file_path = self.project_path / file
            if not file_path.exists():
                missing_files.append(file)
            else:
                print(f"  ✅ {file}")

        if missing_files:
            print(f"  ❌ 缺少文件: {', '.join(missing_files)}")
            print("  💡 请先确保项目有必要的静态文件")
            sys.exit(1)

        # 检查项目大小
        total_size = sum(f.stat().st_size for f in self.project_path.rglob('*')
                        if f.is_file() and 'node_modules' not in str(f))

        if total_size > 10 * 1024 * 1024:  # 10MB
            print(f"  ⚠️  项目较大: {total_size / 1024 / 1024:.1f} MB")
        else:
            print(f"  ✅ 项目大小: {total_size / 1024 / 1024:.1f} MB")

    def build_project(self):
        """构建项目"""
        print("\n🔨 构建项目...")

        # 创建构建目录
        self.build_dir.mkdir(exist_ok=True)

        # 复制静态文件
        static_files = ['index.html', 'style.css', 'script.js', '*.png', '*.jpg', '*.jpeg', '*.gif']

        for pattern in static_files:
            for file_path in self.project_path.rglob(pattern):
                if 'node_modules' not in str(file_path):
                    relative_path = file_path.relative_to(self.project_path)
                    dest_path = self.build_dir / relative_path
                    dest_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(file_path, dest_path)

        # 优化 HTML
        self.optimize_html()

        # 优化 CSS
        self.optimize_css()

        # 创建 .nojekyll 文件（用于 GitHub Pages）
        (self.build_dir / '.nojekyll').touch()

        print(f"  ✅ 构建完成: {self.build_dir}")

    def optimize_html(self):
        """优化 HTML"""
        html_file = self.build_dir / 'index.html'
        if html_file.exists():
            content = html_file.read_text()

            # 移除注释
            import re
            content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)

            # 移除空白行
            lines = [line.strip() for line in content.split('\n') if line.strip()]
            content = '\n'.join(lines)

            html_file.write_text(content)

    def optimize_css(self):
        """优化 CSS"""
        css_file = self.build_dir / 'style.css'
        if css_file.exists():
            content = css_file.read_text()

            # 移除注释
            import re
            content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)

            # 移除空白
            content = ' '.join(content.split())

            css_file.write_text(content)

    def deploy_to_cloudflare(self):
        """部署到 Cloudflare Pages"""
        print("\n☁️  部署到 Cloudflare Pages...")

        # 检查 wrangler
        try:
            subprocess.run(['npx', 'wrangler', '--version'],
                         check=True, capture_output=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("  ❌ 未安装 wrangler")
            print("  💡 安装: npm install -g wrangler")
            print("  💡 登录: npx wrangler login")
            return False

        # 部署命令
        cmd = ['npx', 'wrangler', 'pages', 'deploy', str(self.build_dir)]

        try:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            print("  ✅ 部署成功!")

            # 提取 URL
            for line in result.stdout.split('\n'):
                if 'https://' in line and 'pages.dev' in line:
                    url = line.strip()
                    print(f"  🌐 访问: {url}")
                    return True

        except subprocess.CalledProcessError as e:
            print(f"  ❌ 部署失败: {e.stderr}")
            return False

    def deploy_to_github(self):
        """部署到 GitHub Pages"""
        print("\n📚 部署到 GitHub Pages...")

        # 检查 git
        try:
            subprocess.run(['git', '--version'], check=True, capture_output=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("  ❌ 未安装 git")
            return False

        # 检查 GitHub 仓库
        repo_url = self.deploy_config.get('github_repo')
        if not repo_url:
            print("  ❌ 需要配置 GitHub 仓库 URL")
            print("  💡 示例: https://github.com/username/repo.git")
            return False

        # 创建临时目录
        temp_dir = Path.cwd() / 'gh-pages-temp'
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
        temp_dir.mkdir()

        # 复制构建文件
        shutil.copytree(self.build_dir, temp_dir)

        # 初始化 git 仓库
        os.chdir(temp_dir)
        subprocess.run(['git', 'init'], check=True)
        subprocess.run(['git', 'add', '.'], check=True)
        subprocess.run(['git', 'commit', '-m', 'Deploy to GitHub Pages'], check=True)

        # 添加远程仓库
        try:
            subprocess.run(['git', 'remote', 'add', 'origin', repo_url], check=True)
        except subprocess.CalledProcessError:
            # 如果已存在，先删除再添加
            subprocess.run(['git', 'remote', 'remove', 'origin'], check=True)
            subprocess.run(['git', 'remote', 'add', 'origin', repo_url], check=True)

        # 推送到 gh-pages 分支
        try:
            subprocess.run(['git', 'branch', '-M', 'main'], check=True)
            subprocess.run(['git', 'push', '-u', 'origin', 'main': 'gh-pages'], check=True)
            print("  ✅ 部署成功!")
            print(f"  🌐 访问: https://username.github.io/repo")
        except subprocess.CalledProcessError as e:
            print(f"  ❌ 部署失败: {e}")
        finally:
            os.chdir(self.project_path.parent)
            shutil.rmtree(temp_dir)

    def deploy_to_netlify(self):
        """部署到 Netlify"""
        print("\n🎯 部署到 Netlify...")

        # 检查 netlify-cli
        try:
            subprocess.run(['netlify', '--version'], check=True, capture_output=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("  ❌ 未安装 netlify-cli")
            print("  💡 安装: npm install -g netlify-cli")
            return False

        # 创建 netlify.toml
        netlify_config = self.build_dir / 'netlify.toml'
        if not netlify_config.exists():
            config = """[build]
  publish = "dist"

[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "DENY"
    X-XSS-Protection = "1; mode=block"
    X-Content-Type-Options = "nosniff"
"""
            netlify_config.write_text(config)

        # 部署命令
        cmd = ['netlify', 'deploy', '--prod', '--dir', str(self.build_dir)]

        try:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            print("  ✅ 部署成功!")

            # 提取 URL
            for line in result.stdout.split('\n'):
                if 'https://' in line and 'netlify.app' in line:
                    url = line.strip()
                    print(f"  🌐 访问: {url}")
                    return True

        except subprocess.CalledProcessError as e:
            print(f"  ❌ 部署失败: {e.stderr}")
            return False

def main():
    if len(sys.argv) < 2:
        print("用法: python deploy-static.py <项目路径> [部署配置]")
        print("\n部署配置示例:")
        print('  {"platform": "cloudflare"}')
        print('  {"platform": "github", "github_repo": "https://github.com/username/repo.git"}')
        print('  {"platform": "netlify"}')
        sys.exit(1)

    project_path = sys.argv[1]
    deploy_config = {}

    if len(sys.argv) > 2:
        try:
            deploy_config = json.loads(sys.argv[2])
        except json.JSONDecodeError:
            print("❌ 配置格式错误")
            sys.exit(1)

    deployer = StaticDeployer(project_path, deploy_config)
    deployer.deploy()

if __name__ == "__main__":
    main()