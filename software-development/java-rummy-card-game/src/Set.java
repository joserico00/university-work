public class Set extends Hand
{
    /*
    *    Must override the behavior of the HandInterface so that
    *   a Set only accepts a card if it is of the same rank.
    */
    private char  Myrank;
    private char Mysuit;
    private int count=0;
    private mystack mySet = new mystack(4);
    public  Set(char rank)
    {
        Myrank = rank;
    }

    public void addCard( Card card )
    {
    if (!isFull())
    {
        if (getRank() == card.getRank())
        {
            mySet.push(card);
            count+=1;
        }
    }
    }

    /**
     *   returns the rankIndex of the set
     @return int returns int corresponding to rank as defined in CardInterface
     */
    public int getRankIndex()
    {

        return Card.getRankIndex(Myrank);

    }

   /**
     *   returns the rank of the set
    *  @return char returns char of rank as defined in CardInterface
     */
    public char getRank()
    {
        return Myrank;
    }
  /**
     *  Determines whether Set is contains all four cards.
     @return if true then no more Card may be added to the set
     */
    public boolean isFull()
    {
        if (count==4) {
            return true;
        }
        else {
            return false;
        }
    }
    public int Amount() {
        return count;
    }

    /**
    * Ranks the cards in a set according to their suit
    */



}
