@echo off
chcp 65001 >nul
cd /d "%~dp0"
python -m formula2manim.gui
pause
