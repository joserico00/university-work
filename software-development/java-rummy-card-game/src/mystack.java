
import java.util.*;

public class mystack {
    private Card[]       array;
    private int Maxsize;
    private int first;

    public mystack(int n) {
        first = 0;
        Maxsize = n;
        array= new Card[n];

    }

    public void push(Card s) {
        if(!isFull()) {
        array[first ]= s;
        first= first +1;
        }
        else {
            System.out.print("full");
        }
    }
    public Card pop() {
        if(!isEmpty()) {
            first=first-1;
            return array[first];
        }
        else {
            return null;
        }
    }
    public Card peek(){
        if(!isEmpty()) {
        return array[first-1];
        }
        else {
            return null;
        }
    }
    public boolean isEmpty(){
        if (first == 0)
        {
            return true;
        }
        else {
            return false;
            }
    }
    public boolean isFull(){
        if (first == this.Maxsize)
        {
            return true;
        }
        else {
            return false;
            }
    }
    public int count() {
        return this.first;
    }

       public void shuffle() {
           List<Card> tempArr= Arrays.asList(this.array);

           Collections.shuffle(tempArr);
           tempArr.toArray(this.array);
       }
}
