import java.io.*; 
import java.util.*; 

void setup() {
  size(800, 800);
  //image(loadImage("test.gif"),0,0);
  noFill();
  stroke(255);
  for (int i=0; i<20; i++) {
    ellipse(random(width), random(height), random(width), random(height));
  }
  loadPixels();
}

void draw() {
}

void mouseReleased() {
  floodFill(
    new Vec2D(mouseX, mouseY), /* current mouse pos as point object */
    0xff<<24|(int)random(0xffffff), /* random colour (need to set alpha too) */
    get(mouseX, mouseY)      /* current colour under mouse position */
    );
  updatePixels();
}

/**
 * (updated) stack friendly scanline flood filler
 */
void floodFill(Vec2D p, int col, int bg) {
  int xx, yy, idx, idxUp, idxDown;
  int h1=height-1;
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
      idx=yy*width+xx;
      idxUp=idx-width;
      idxDown=idx+width;
      scanUp = scanDown = false;
      // fill until left boundary in current scanline...
      // checking neighbouring pixel rows
      while (xx >= 0 && pixels[idx] == bg) {
        pixels[idx] = col;
        if (yy>0) {
          if (pixels[idxUp--]==bg && !scanUp) {
            stack.push(new Vec2D(xx, yy-1));
            scanUp = true;
          } else if (scanUp) scanUp=false;
        }
        if (yy < h1) {
          if (pixels[idxDown--]==bg && !scanDown) {
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
      idx = yy*width+xx;
      idxUp=idx-width;
      idxDown=idx+width;
      scanUp = scanDown = false;
      while (++xx < width && pixels[++idx] == bg) {
        pixels[idx] = col;
        if (yy>0) {
          if (pixels[++idxUp]==bg && !scanUp) {
            stack.push(new Vec2D(xx, yy-1));
            scanUp = true;
          } else if (scanUp) scanUp=false;
        }
        if (yy<h1) {
          if (pixels[++idxDown]==bg && !scanDown) {
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
