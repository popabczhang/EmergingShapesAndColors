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
 * a stack friendly scanline flood filler
 * based on some old atari turbobasic code
 */
void floodFill(Vec2D p, int col, int prevCol) {
  int xx, idx;
  int h1=height-1;
  boolean scanUp, scanDown;

  // don't run if fill colour the same as bg
  if (prevCol==col) return;

  // use the default java stack:
  // http://java.sun.com/j2se/1.4.2/docs/api/java/util/Stack.html
  Stack stack=new Stack();

  // the Stack class is throwing exceptions
  // when we're trying to pop() too often...
  // so we need to wrap code inside a try - catch block
  try {
    while (p!=null) {
      xx = p.x;
      // compute current index in pixel buffer array
      idx=p.y*width+xx;
      // find left boundary in current scanline...
      while (xx >= 0 && pixels[idx] == prevCol) {
        xx--;
        idx--;
      }
      scanUp = scanDown = false;
      // ...now continue scanning/filling to the right,
      // checking neighbouring pixel rows
      while (++xx < width && pixels[++idx] == prevCol) {
        pixels[idx] = col;
        if (!scanUp && p.y > 0 && pixels[idx-width] == prevCol) {
          stack.push(new Vec2D(xx, p.y-1));
          scanUp = true;
        } else if (scanUp && p.y > 0 && pixels[idx-width] != prevCol) {
          scanUp = false;
        }
        if (!scanDown && p.y < h1 && pixels[idx+width] == prevCol) {
          stack.push(new Vec2D(xx, p.y+1));
          scanDown = true;
        } else if (scanDown && p.y < h1 && pixels[idx+width] != prevCol) {
          scanDown = false;
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
