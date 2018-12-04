let size = 20;
let snake;
let food;
let score = 0;
let speed;
let ai;


function setup() {
  createCanvas(1200, 600);
  
  snake = new Snake();
  foodSpawn();
  noStroke();
  textSize(size);

  ai = new Ai();
}

function foodSpawn(){
  var cols = floor(width/size);
  var rows = floor(height/size);
  food = createVector(floor(random(cols)), floor(random(rows)));
  food.mult(size);
}

function draw() {
  // frameRate(speed.value());
  background(51);
  snake.update();
  snake.show();

  fill(255, 10, 80);
  rect(food.x, food.y, size, size);

  if(snake.eat(food)){
    score+=snake.total-1;
    foodSpawn();
  }

  ai.direction();

  text(score, size, width-size);
}

function keyPressed(){
  if(keyCode === UP_ARROW){
    snake.dir(0, -1);
  }
  else if(keyCode === DOWN_ARROW){
    snake.dir(0, 1);
  }
  else if(keyCode === RIGHT_ARROW){
    snake.dir(1, 0);
  }
  else if(keyCode === LEFT_ARROW){
    snake.dir(-1, 0);
  }
}

