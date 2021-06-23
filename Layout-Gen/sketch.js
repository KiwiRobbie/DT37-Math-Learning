var bg;
var fg_1, fg_2;
var fontRegular, fontItalic, fontBold;

function setup() 
{
	colorMode(HSB, 360, 100, 100);


	bg = color(220,5,15);
	fg = color('#da8972');

	fg_1 = color(40,100,100);
	fg_2 = color(10,100,100);


	createCanvas(370, 490);
	translate(5,5)
	background(0);
	noFill();
	strokeWeight(2);
	stroke(255);

	rect(0,0,360,480,10)

	line(0,420,360,420)
	line(120,420,120,480)
	line(240,420,240,480)

	line(0,30,360,30)

	blendMode(MULTIPLY);
	setGradient(-5,-5,370,490,fg_1,fg_2,2)
	blendMode(LIGHTEST);
	mainfont = loadFont("assets/OpenSans-Regular.ttf");
	text("Font Style Normal", 10, 30);
	background(bg)

}

function draw()
{

}


function setGradient(x, y, w, h, c1, c2, axis) {
	noFill();
  
	if (axis === 1) {
	  // Top to bottom gradient
	  for (let i = y; i <= y + h; i++) {
		let inter = map(i, y, y + h, 0, 1);
		let c = lerpColor(c1, c2, inter);
		stroke(c);
		line(x, i, x + w, i);
	  }
	} else if (axis === 2) {
	  // Left to right gradient
	  for (let i = x; i <= x + w; i++) {
		let inter = map(i, x, x + w, 0, 1);
		let c = lerpColor(c1, c2, inter);
		stroke(c);
		line(i, y, i, y + h);
	  }
	}
  }
  