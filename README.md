# NVIDIA Omniverse Light Blending Extension

This extension allows to smoothly interpolate light parameters (i.e. intensity) taking into account current camera position. Typical scenario is a view-dependent light to do separate shots without toggling on and off any light source. 

Supported light types: Sphere Light, Distant Light, Disk Light.

Disk Light is turned into a blinking light to showcase capabilities of the plugin and how easy it is to support different light types.

# Tutorial

Lets set up a scene (you can use Omniverse Astronaut example to quickly see the result):
1. Add two Sphere Lights to your scene
2. Set distinct colors for each light (i.e. Red and Green)
3. Right-click on each of added lights and select "Add Control Light"
4. Set different radiuses for each light (use widget). Notice Blue sphere shows the radius you set.

Now the sphere lights became view-dependent. Try to gradually move in/out of sphere light radiuses and notice how light intensity changes.

# On your own!

* Add a distant light to the scene and see how it behaves
* Add disk light and see how its intensity changes over time
* Support new light type (i.e. Dome Light) by adding new LightModel!
