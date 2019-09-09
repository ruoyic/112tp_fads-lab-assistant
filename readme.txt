My term project FADs Lab Assistant. Is an image processor that helps interpret result images of agarose gel run and yeast transformation plates. 

To launch the app, simply run 'runUI.py' in an editor. The user interaction is all accomplished through mouse clicks and movements and therefore very intuitive. 
By hitting recognize, you can get the opencv-generated marks, which can be removed by a click on it. You can also draw marks by hand to fix the automatic recognition. Customize asks you to provide information on ladder, plates and colony size limits. Analyze generates results that can be saved as png images.
The only weird thing to note is that you have to move the mouse to start in the very first. Please don't load non-image files since there's no crash prevention for that yet.

Some sample images are provided in the folder, but feel free to use your own gel and plate photos (as if people usually have those...)!