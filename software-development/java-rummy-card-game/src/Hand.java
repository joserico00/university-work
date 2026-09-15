
import java.util.*;

/**
 * Represents the basic functionality of a hand of cards.
 * Extensions of this class will provide the
 * definition of what constitutes a hand for that game and how hands are compared
 * to one another by overriding the <code>compareTo</code> method.
 */
public class Hand implements HandInterface
{
    private ArrayList<Card> HandArray= new ArrayList<Card>() ;
    private int player = 0;
    private int Draw = 0;
    private int Discard = 0;
  /**
   * Adds a card to this hand.
   * @param card card to be added to the current hand.
   */
   public void addCard( Card card )
   {

       this.HandArray.add(card);
       sort();
   }


  /**
   * Obtains the card stored at the specified location in the hand.  Does not
   * remove the card from the hand.
   * @param index position of card to be accessed.
   * @return the card of interest, or the null reference if the index is out of
   * bounds.
   */
   public Card getCard( int index ) {
       return this.HandArray.get(index);
   }


  /**
   * Removes the specified card from the current hand.
   * @param card the card to be removed.
   * @return the card removed from the hand, or null if the card
   * was not present in the hand.
   */
   public Card removeCard( Card card ) {
       Card temp = card;
       if (this.HandArray.remove(card))
       {
           //System.out.println("Discarded: " + temp);
           return temp;
       }
       else
       {
           return null;
       }
   }

  /**
   * Removes the card at the specified index from the hand.
   * @param index poisition of the card to be removed.
   * @return the card removed from the hand, or the null reference if
   * the index is out of bounds.
   */
   public Card removeCard( int index )      {
   Card temp = HandArray.remove(index);
   if ( temp != null)
   {
      // System.out.println("Discarded: " + temp);
       return temp;
   }
   else
   {
       return null;
   }
}



  /**
   * The number of cards held in the hand.
   * @return number of cards currently held in the hand.
   */
   public int getNumberOfCards() {
       return this.HandArray.size();
   }


  /**
   * Sorts the card in the hand.
   * Sort is performed according to the order specified in the {@link Card} class.
   */
   public void sort()
   {

    if(getNumberOfCards()>1)
    {
    Card card;
    Card card2;

        for(int i = 0; i < getNumberOfCards(); i++)
        {
            int index=i;
            for(int j = i ; j< getNumberOfCards(); j++)
            {
                card=getCard(j);
                card2=getCard(index);
                if(card.compareTo(card2)<0 )
                        {
                            index=j;
                        }


            }
            if(index != i)
            {
                Card sortedCard = getCard(index);
                HandArray.set(index, getCard(i));
                HandArray.set(i, sortedCard);
            }

        }
    }

    }



  /**
   * Checks to see if the hand is empty.
   * @return <code>true</code> is the hand is empty.
   */
   public boolean isEmpty() {
       return this.HandArray.isEmpty();
   }


  /**
   * Determines whether or not the hand contains the specified card.
   * @param card the card being searched for in the hand.
   * @return <code>true</code> if the card is present in the hand.
   */
   public boolean containsCard( Card card ) {
       return this.HandArray.contains(card);
   }

  /**
   * Searches for the first instance of the specified card in the hand.
   * @param card card being searched for.
   * @return position index of card if found, or <code>-1</code> if not found.
   */
   public int findCard( Card card ) {
       return this.HandArray.indexOf(card);
   }

  /**
   * Searches for the first instance of a set (3 or 4 Cards of the same rank) in the hand.
   * @return  returns Card [] of Cards found in deck or <code>-null </code> if not found.
   */
   //public Card [] findSet( );

  /**
   *  Compares two hands.
   *  @param otherHandObject the hand being compared.
   *  @return < 0 if this hand is less than the other hand, 0 if the two hands are
   *  the same, or > 0 if this hand is greater then the other hand.
   */
   public int compareTo( Object otherHandObject )
   {
       Hand otherHand = (Hand) otherHandObject;
       int myHand =this.evaluateHand() ;
       int other=otherHand.evaluateHand();
       int result = myHand - other;
       System.out.println("Points: " + myHand + " to " + other);
       if(result == 0)
       {
           return 0;
       }
       else if (result < 0)
       {
           return -1;
       }
       else
       {
           return 1;
       }
       }




  /**
   *  Evaluates the hand.  Must be defined in the subclass that implements the hand
   *  for the game being written by the client programmer.
   *  @return an integer corresponding to the rating of the hand.
   */
  //not sure we have to do this.....because we are just laying down the cards.....
   public int evaluateHand() {
       int rating = 0;
       for (int i =0; i<getNumberOfCards(); i++) {

       Card evacard= getCard(i);
        rating = rating + Card.getRankIndex(evacard.getRank() )+ 1;
   }
       return rating;
       }

  /**
    * Returns a description of the hand.
    * @return a list of cards held in the hand.
    */
    public String toString()
    {
    String cardList="";
    Card temp ;
    char rank;
    char suit;
    for (int i =0; i<getNumberOfCards(); i++)
    {
        temp= getCard(i);
        rank=temp.getRank();
        suit=temp.getSuit();
        cardList+=rank;
        cardList+=suit;
        cardList+=" ";

    }
    return cardList;
    }
    public void Play(  ) {
    if (player ==0 && !this.isEmpty()) {
        player=1;
    }
    if (player ==1) {
        player=0;
    }
    }
    public int getDraw()
    {
    return Draw;
    }
    public void changeDraw(int i)
    {
    Draw=i;
    }
    public int getDiscard()
    {
    return Discard;
    }


public void changeDiscard(int i)
{
    Discard = i;
    }

public ArrayList<Card> getList() {
    return HandArray;
}

}
