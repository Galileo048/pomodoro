"""
动画渲染工具
使用方法：python 渲染动画.py <源码文件> <场景类名> [质量]
质量参数：ql=低质量预览, qh=高质量成品
"""
import subprocess
import sys
import os

def render_animation(source_file, scene_name, quality="qh"):
    """渲染Manim动画"""
    # 添加MiKTeX到PATH
    miktex_path = r"C:\Program Files\MiKTeX\miktex\bin\x64"
    if miktex_path not in os.environ.get("PATH", ""):
        os.environ["PATH"] = miktex_path + ";" + os.environ.get("PATH", "")

    # 构建渲染命令
    cmd = ["python", "-m", "manim", "render", f"-{quality}", source_file, scene_name]

    print(f"开始渲染: {source_file} -> {scene_name}")
    print(f"质量: {'高质量' if quality == 'qh' else '低质量'}")
    print("-" * 50)

    # 执行渲染
    result = subprocess.run(cmd, capture_output=False)

    if result.returncode == 0:
        print("-" * 50)
        print("✅ 渲染完成！")
        print(f"视频在: media/videos/{os.path.splitext(source_file)[0]}/{scene_name}.mp4")
    else:
        print("❌ 渲染失败！")
        return False

    return True

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("使用方法: python 渲染动画.py <源码文件> <场景类名> [质量]")
        print("示例: python 渲染动画.py 01_匀变速直线运动.py UniformAcceleration qh")
        sys.exit(1)

    source = sys.argv[1]
    scene = sys.argv[2]
    quality = sys.argv[3] if len(sys.argv) > 3 else "qh"

    render_animation(source, scene, quality)
