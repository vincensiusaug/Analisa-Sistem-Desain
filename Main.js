// let width = 800;
// let height = width / 16 * 9;
let login;

function setup() {
  createCanvas(600 , 600);
  login = new Login(300);
}

function draw() {
  background(50);
  // fill(0);
  // rect(50, 50, 50, 50);
  login.Show();
  
}