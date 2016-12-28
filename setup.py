# _*_ coding:utf-8 _*_

from setuptools import setup, find_packages

setup(
    name="osapi",          # 包名
    version="1.0",              # 版本信息
    packages=['osapi', 'osapi.sdnapi'],  # 要打包的项目文件夹
    include_package_data=True,    # 自动打包文件夹内所有数据
    zip_safe=True,                # 设定项目包为安全，不用每次都检测其安全性

    install_requires=[          # 安装依赖的其他包
        'requests',
    ],

    # 设置程序的入口为hello
    # 安装后，命令行执行hello相当于调用hello.py中的main方法
    entry_points={

    },

    # 如果要上传到PyPI，则添加以下信息
    # author = "Me",
    # author_email = "me@example.com",
    # description = "This is an Example Package",
    # license = "MIT",
    # keywords = "hello world example examples",
    # url = "http://example.com/HelloWorld/",
)
