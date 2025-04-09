media_export
------------

This empty package exists to allow ROS packages to export media paths
to each other.

The inspiration has been OGRE media paths, but the system could be
used for any system that needs paths to be exported.

In practice, all one needs to do to *export* a path is something like this:
(in rosbuild, put this in the manifest.xml)

    <depend package="media_export"/>
    <export>
      <media_export ogre_media_path="${prefix}/Media/materials/scripts:${prefix}/Media/textures"/>
    </export>

In a catkin package, put this in the package.xml:

    <run_depend>media_export</run_depend>
    <export>
      <media_export ogre_media_path="${prefix}/Media/materials/scripts:${prefix}/Media/textures"/>
    </export>

Then on the command-line you can do

    rospack plugins --attr=ogre_media_path media_export

to see all the ogre_media_paths exported by all packages in your current ROS environment.

The export attribute is named "ogre_media_path" instead of just "path"
because there may be media paths for other software libraries than
Ogre, and it would be a waste to mix them all together.

The first use of media_export is for Ogre meshes which reference Ogre
material scripts.  These can be loaded both by rviz and by other code
which processes URDF files.
