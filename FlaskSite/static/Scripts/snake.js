function Snake(){
    this.body = [];
    this.body.push(createVector(0, 0));
    this.xspeed = 1;
    this.yspeed = 0;
    this.total = 1;
    this.failx = false;
    this.faily = false;
    

    this.eat = function(pos){
        var d = dist(this.body[0].x, this.body[0].y, pos.x, pos.y);

        if( d < size){
            let tail = createVector(this.body[this.total-1].x, this.body[this.total-1].y);
            this.body.push(tail);
            this.total++;
            return true;
        }
        return false;
    }

    this.dir = function(x, y){
        if(this.xspeed != 0 && x != 0){
            this.failx = true;
            return;
        }
        if(this.yspeed != 0 && y != 0){
            this.faily = true;
            return;
        }
        this.xspeed = x;
        this.yspeed = y;
        this.fail = false;
    }
  
    this.update = function(){
        for(var i = this.total-1; i > 0; --i){
            this.body[i].x = this.body[i-1].x;
            this.body[i].y = this.body[i-1].y;
        }

        this.body[0].x += this.xspeed*size;
        this.body[0].y += this.yspeed*size;

        this.body[0].x = constrain(this.body[0].x, 0, width-size);
        this.body[0].y = constrain(this.body[0].y, 0, height-size);

        

        
    }
  
    this.show = function(){
        fill(255);
        rect(this.body[0].x, this.body[0].y, size, size);
        for(var i = 1; i < this.total; ++i){
            fill(0, 255, 0, 80);
            rect(this.body[i].x, this.body[i].y, size, size);
        }
    }
  }