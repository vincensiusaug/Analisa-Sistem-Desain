function Room(id, number, capacity){
    this.id = id;
    this.number = number;
    this.capacity = capacity;
    this.schedule = [];
    this.bookId = null;
     for(int i = 0; i < 10; ++i){
         
     }

    this.reserve = function(bookId, time){
        this.bookId = bookId;
        this.time.push(time);
    }
} 