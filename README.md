# Shrike

Shrike is a project aiming to provide compatibility with ROS1 packages on modern Ubuntu distributions.
We adopt a monorepo approach, with all modules and functionalities inside the same repository.
Currently, we support Ubuntu 24.04.
If there are enough interests, we will add support for more distributions.

For commercial use, custom projects and professional help with migration from ROS1 to ROS2, please contact us at [info@minoic.ai](mailto:info@minoic.ai).

## Build
### Ubuntu 24.04
First, install the dependencies:
```bash
./scripts/install_ubuntu24.sh
```

Then, build the project:
```bash
./src/catkin/bin/catkin_make_isolated --install -DCMAKE_BUILD_TYPE=Release
```

And make sure to source the `setup.bash` file:
```bash
source ./install_isolated/setup.bash
```

Now you can use `roscore` and other ROS1 commands in your terminal.

## Related Projects and Credits
- [rules_ros](https://github.com/mvukov/rules_ros): Build ROS1 with Bazel.

## Disclaimer
Note that this project is not affiliated with OSRF.
ROS is a registered trademark of the Open Source Robotics Foundation.