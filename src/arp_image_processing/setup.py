from setuptools import find_packages, setup

package_name = 'arp_image_processing'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='melih',
    maintainer_email='melihguleyup@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "test_node = arp_image_processing.my_first_node:main",
            "draw_circle = arp_image_processing.draw_circle:main",
            "pose_subscriber = arp_image_processing.pose_subscriber:main",
            "path_planning = arp_image_processing.path_planning:main",
            "map_publisher = arp_image_processing.map_publisher:main",
        ],
    },
)
