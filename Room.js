function Room(id, number, capacity){
    this.id = id;
    this.number = number;
    this.capacity = capacity;
    this.schedule = [];
    this.bookId = null;
    

    this.reserve = function(bookId, time){
        this.bookId = bookId;
        this.time.push(time);
    }
} 