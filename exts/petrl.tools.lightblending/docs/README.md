# NVIDIA Omniverse Light Blending Extension

This extension allows to smoothly interpolate light parameters (i.e. intensity) taking into account current camera position. Typical scenario is a view-dependent light to do separate shots without toggling on and off any light source. 

Supported light types: Sphere Light, Distant Light, Disk Light.

Disk Light is turned into a blinking light to showcase capabilities of the plugin and how it is to add more light types.

# Tutorial

Please follow the steps below to introduce yourself to how this extension works:
1. Add two Sphere Lights to your scene
2. Set distinct colors for each light (i.e. Red and Green)
3. Set different radiuses for each light
4. Right-click on each of added lights and select "Add Control Light"

Now the lights became view-dependent. Try to gradually move out of sphere light radius and notice how light intensity droppes to zero

# On your own!

* Add a distant light to the scene and notice how slider allows you to control the radius
* Add disk light and see how its intensity changes over time
* Support new light type (i.e. Dome Lights) by adding new light model
