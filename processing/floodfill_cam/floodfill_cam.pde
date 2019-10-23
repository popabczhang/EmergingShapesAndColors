import java.io.*; 
import java.util.*; 

import gab.opencv.*;
import processing.video.*;
import java.awt.*;

Capture video;
OpenCV opencv;

int threshold = 120;

PGraphics preCapture;
PImage colorBlobs;

float step = 1.0;

void setup() {
  size(1920, 1080);

  video = new Capture(this, 1920, 1080);
  opencv = new OpenCV(this, 1920, 1080);

  preCapture = createGraphics(int(1920/step), int(1080/step));

  preCapture.beginDraw();
  preCapture.background(0);
  preCapture.endDraw();

  video.start();

  background(0);
}

void draw() {

  //opencv.loadImage(video);
  //image(video, 0, 0, 620, 480);

  opencv.loadImage(video);

  opencv.threshold(threshold);
  PImage processedImage = opencv.getSnapshot();

  //image(processedImage, 620, 0, 620, 480);
  image(processedImage, 0, 0, 320*2.5, 280*2.5);

  preCapture.beginDraw();
  preCapture.image(processedImage, 0, 0, int(1920/step), int(1080/step));
  preCapture.endDraw();
  colorBlobs = preCapture;

  colorBlobs.loadPixels();

  for (int x = 0; x < colorBlobs.width; x+=10) {
    // Loop through every pixel row
    for (int y = 0; y < colorBlobs.height; y+=10) {
      Vec2D pos = new Vec2D(x, y); /* current mouse pos as point object */
      color imgColor = colorBlobs.get(x, y);  /* current colour under mouse position */
      color randColor = 0xff<<24|(int)random(0xffffff); /* random colour (need to set alpha too) */

      floodFill(pos, randColor, imgColor, colorBlobs);
    }
  }
  //colorBlobs.updatePixels();



  image(colorBlobs, 320*2.2, 0, 320*2, 280*2.5);

  //proces fluid.


  text(frameRate, 20, 20);
}

void captureEvent(Capture c) {
  c.read();
}

void keyPressed() {
  if (key == 'a') {
    colorBlobs.loadPixels();

    for (int x = 0; x < colorBlobs.width; x+=30) {
      // Loop through every pixel row
      for (int y = 0; y < colorBlobs.height; y+=30) {
        Vec2D pos = new Vec2D(x, y); /* current mouse pos as point object */
        color imgColor = colorBlobs.get(x, y);  /* current colour under mouse position */
        color randColor = 0xff<<24|(int)random(0xffffff); /* random colour (need to set alpha too) */

        floodFill(pos, randColor, imgColor, colorBlobs);
      }
    }
    //colorBlobs.updatePixels();
  }
}


void mouseReleased() {
}

/**
 * (updated) stack friendly scanline flood filler
 */
void floodFill(Vec2D p, int col, int bg, PImage img) {
  int xx, yy, idx, idxUp, idxDown;
  int h1=img.height-1;
  boolean scanUp, scanDown;

  // don't run if fill colour the same as bg
  if (bg==col) return;

  // use the default java stack:
  // http://java.sun.com/j2se/1.4.2/docs/api/java/util/Stack.html
  Stack stack=new Stack();

  // the Stack class is throwing an exception
  // when we're trying to pop() too often...
  // so we need to wrap code inside a try - catch block
  try {
    while (true) {
      xx = p.x;
      yy = p.y;
      // compute current index in pixel buffer array
      idx=yy*img.width+xx;
      idxUp=idx-img.width;
      idxDown=idx+img.width;
      scanUp = scanDown = false;
      // fill until left boundary in current scanline...
      // checking neighbouring pixel rows
      while (xx >= 0 && img.pixels[idx] == bg) {
        img.pixels[idx] = col;
        if (yy>0) {
          if (img.pixels[idxUp--]==bg && !scanUp) {
            stack.push(new Vec2D(xx, yy-1));
            scanUp = true;
          } else if (scanUp) scanUp=false;
        }
        if (yy < h1) {
          if (img.pixels[idxDown--]==bg && !scanDown) {
            stack.push(new Vec2D(xx, yy+1));
            scanDown = true;
          } else if (scanDown) scanDown=false;
        }
        xx--;
        idx--;
      }
      // ...now continue scanning/filling to the right
      xx = p.x;
      yy = p.y;
      idx = yy*img.width+xx;
      idxUp=idx-img.width;
      idxDown=idx+img.width;
      scanUp = scanDown = false;
      while (++xx < img.width && img.pixels[++idx] == bg) {
        img.pixels[idx] = col;
        if (yy>0) {
          if (img.pixels[++idxUp]==bg && !scanUp) {
            stack.push(new Vec2D(xx, yy-1));
            scanUp = true;
          } else if (scanUp) scanUp=false;
        }
        if (yy<h1) {
          if (img.pixels[++idxDown]==bg && !scanDown) {
            stack.push(new Vec2D(xx, yy+1));
            scanDown = true;
          } else if (scanDown) scanDown=false;
        }
      }
      p=(Vec2D)stack.pop();
    }
  }
  // catch exceptions...
  // stack is empty when we're finished filling, so just ignore
  catch(EmptyStackException e) {
  }
  // catch other exceptions
  // e.g. OutOfMemoryException, though shouldn't be caused by filler
  catch(Exception e) {
  }
} 

/**
 * simple 2D coordinate wrapper
 */
class Vec2D {
  public int x, y;

  Vec2D(int x, int y) {
    this.x=x;
    this.y=y;
  }
} 
