from setuptools import find_packages, setup

package_name = 'keyboard_teleop_viz'

setup(
    name=package_name,
    version='1.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Sebastian Zug',
    maintainer_email='sebastian.zug@informatik.tu-freiberg.de',
    description='Zeigt die Tastatur-Vorgabe von keyboard_teleop_cpp als Balken an.',
    license='BSD-3-Clause',
    # Hier wird festgelegt, welcher Befehl hinter `ros2 run keyboard_teleop_viz anzeige` steckt
    entry_points={
        'console_scripts': [
            'anzeige = keyboard_teleop_viz.anzeige:main',
        ],
    },
)
