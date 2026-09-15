
import java.util.*;

public class Deck implements DeckInterface{
  private Stack<Card>  myDeck;
  private final int capacity = 52;

  public  Deck()
  {
     this.myDeck = new Stack<Card>();
  }
 /**
   * Creates an empty deck of cards.
   */
   public void Deck()
   {
       this.myDeck = new Stack<Card>();
   }
  /**
   *  returns next Card in a deck that is facing down without removing it
   */
    public Card peek()
    {
    if(!isEmpty()) {
    return this.myDeck.peek();}
    else {
        return null;
    }
    }
 /**
   * this method is used to add Cards to a Deck.  The Deck is completely empty when it is initialized.
   */

   public void addCard( Card card ) {

       myDeck.push(card);
   }


 /**
   * returns number of cards on the deck
   * @return int
   */
   public int getSizeOfDeck() {
       return this.myDeck.size();
   }

   /**
   * removes first card on a deck so equivalent to flipping the card off of a eck that is faced down
   * @return <code>null</code> if there are no cards left on the Stack. Otherwise returns Card
   */
   public Card dealCard() {
       //System.out.println("        Added: " + peek());
       return this.myDeck.pop();
   }

 /**
   * removes Card last card placed on a deck so equivalent toremoving card from deck that is faced up
   * @return <code>null</code> if there are no cards left on the deck. Otherwise removes Card
   */
   public Card removeCard() {
      // System.out.println("        Added: " + peek());
       return this.myDeck.pop();

   }

  /**
   * Shuffles the cards present in the deck.
   */
   public void shuffle() {
       Collections.shuffle(myDeck);

   }

  /**
   * Looks for an empty deck.
   * @return <code>true</code> if there are no cards left to be dealt from the deck.
   */
   public boolean isEmpty()
   {
       return this.myDeck.isEmpty();
   }

  /**
   * Restores the deck to being empty and ready to add Cards to
   */
  public void restoreDeck() {
      myDeck = new Stack<Card>();

  }




}
