function Ai(){

    this.direction = function(){
        this.x = snake.body[0].x - food.x;
        this.y = snake.body[0].y - food.y;
        // food at right
        if(this.x < 0){
            snake.dir(1, 0);
        }
        // food at left
        else if(this.x > 0){
            snake.dir(-1, 0);
        }
        // food at down
        if(this.y < 0){
            snake.dir(0, 1);
        }
        // food at top
        else if(this.y > 0){
            snake.dir(0, -1);
        }

        if(snake.failx){
            if(this.y < 0){
                snake.dir(0, 1);
            }
            else if(this.y > 0){
                snake.dir(0, -1);
            }
            snake.failx = false;
        }
        if(snake.faily){
            if(this.x < 0){
                snake.dir(1, 0);
            }
            else if(this.x > 0){
                snake.dir(-1, 0);
            }
            snake.faily = false;
        }
    }

}