var bg;
var fg_1, fg_2;

function setup() 
{
	bg = color('#212329');
	fg = color('#ff7b2e');

	fg_1 = fg//color(40,100,100);
	fg_2 = fg//color(10,100,100);


	createCanvas(360, 200);

	background(0);
	noFill();
	strokeWeight(4);
	stroke(255);

	line(0,0,360,0)

	line(0,0,0,200)
	line(360,0,360,200)


	blendMode(MULTIPLY);
	background(fg_1)
	blendMode(LIGHTEST);
	background(bg)
	saveCanvas('download', 'png');

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
  