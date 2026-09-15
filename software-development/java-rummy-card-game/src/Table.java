        import java.awt.*;
import javax.swing.*;
import java.awt.event.*;
import java.util.*;
/**
*    This GUI assumes that you are using a 52 card deck and that you have 13 sets in the deck.
*    The GUI is simulating a playing table
    @author Patti Ordonez
*/
public class Table extends JFrame implements ActionListener
{
    final static int numDealtCards = 9;
    JPanel player1;
    JPanel player2;
    JPanel deckPiles;
    JLabel deck;
    JLabel stack;
    JList p1HandPile;
    JList p2HandPile;
    Deck cardDeck;
    Deck stackDeck;
    Hand play1= new Hand();
    Hand play2= new Hand();
    boolean emptyflag = false;
    boolean game = true;


    SetPanel [] setPanels = new SetPanel[13];
    JLabel topOfStack;
    JLabel deckPile;
    JButton p1Stack;
    JButton p2Stack;

    JButton p1Deck;
    JButton p2Deck;

    JButton p1Lay;
    JButton p2Lay;

    JButton p1LayOnStack;
    JButton p2LayOnStack;

    DefaultListModel p1Hand;
    DefaultListModel p2Hand;

    private void deal(Card [] cards)
    {
        for(int i = 0; i < cards.length; i ++)
            cards[i] = (Card)cardDeck.dealCard();
    }

    public Table()
    {
        super("The Card Game of the Century");

        setLayout(new BorderLayout());
        setSize(1200,700);


        cardDeck = new Deck();

        ImageIcon img;
        for(int i = 0; i < Card.suit.length; i++){
            for(int j = 0; j < Card.rank.length; j++){
                Card card = new Card(Card.suit[i],Card.rank[j]);

                img= new ImageIcon(card.getImageFile());

                card = new Card(Card.suit[i],Card.rank[j],img);
                cardDeck.addCard(card);
            }
        }

        cardDeck.shuffle();

        stackDeck = new Deck();

        JPanel top = new JPanel();

        for (int i = 0; i < Card.rank.length;i++)
            setPanels[i] = new SetPanel(Card.getRankIndex(Card.rank[i]));


        top.add(setPanels[0]);
        top.add(setPanels[1]);
        top.add(setPanels[2]);
        top.add(setPanels[3]);

        player1 = new JPanel();

        player1.add(top);




        add(player1, BorderLayout.NORTH);
        JPanel bottom = new JPanel();


        bottom.add(setPanels[4]);
        bottom.add(setPanels[5]);
        bottom.add(setPanels[6]);
        bottom.add(setPanels[7]);
        bottom.add(setPanels[8]);

        player2 = new JPanel();




        player2.add(bottom);
        add(player2, BorderLayout.SOUTH);


        JPanel middle = new JPanel(new GridLayout(1,3));

        p1Stack = new JButton("Stack");
        p1Stack.addActionListener(this);
        p1Deck = new JButton("Deck ");
        p1Deck.addActionListener(this);
        p1Lay = new JButton("Lay  ");
        p1Lay.addActionListener(this);
        p1LayOnStack = new JButton("LayOnStack");
        p1LayOnStack.addActionListener(this);


        Card [] cardsPlayer1 = new Card[numDealtCards];
        deal(cardsPlayer1);
        p1Hand = new DefaultListModel();
        for(int i = 0; i < cardsPlayer1.length; i++) {
            p1Hand.addElement(cardsPlayer1[i]);
            play1.addCard(cardsPlayer1[i]);
            }
        p1Hand.clear();
        for(Card i : play1.getList() )
        {
            p1Hand.addElement(i);
        }
        p1HandPile = new JList(p1Hand);


        middle.add(new HandPanel("Player 1", p1HandPile, p1Stack, p1Deck, p1Lay, p1LayOnStack));

        deckPiles = new JPanel();
        deckPiles.setLayout(new BoxLayout(deckPiles, BoxLayout.Y_AXIS));
        deckPiles.add(Box.createGlue());
        JPanel left = new JPanel();
        left.setAlignmentY(Component.CENTER_ALIGNMENT);


        stack = new JLabel("Stack");
        stack.setAlignmentY(Component.CENTER_ALIGNMENT);

        left.add(stack);
        topOfStack = new JLabel();
        topOfStack.setIcon(new ImageIcon(Card.directory + "blank.gif"));
        topOfStack.setAlignmentY(Component.CENTER_ALIGNMENT);
        left.add(topOfStack);
        deckPiles.add(left);
        deckPiles.add(Box.createGlue());

        JPanel right = new JPanel();
        right.setAlignmentY(Component.CENTER_ALIGNMENT);

        deck = new JLabel("Deck");

        deck.setAlignmentY(Component.CENTER_ALIGNMENT);
        right.add(deck);
        deckPile = new JLabel();
        deckPile.setIcon(new ImageIcon(Card.directory + "b.gif"));
        deckPile.setAlignmentY(Component.CENTER_ALIGNMENT);
        right.add(deckPile);
        deckPiles.add(right);
        deckPiles.add(Box.createGlue());
        middle.add(deckPiles);


        p2Stack = new JButton("Stack");
        p2Stack.addActionListener(this);
        p2Deck = new JButton("Deck ");
        p2Deck.addActionListener(this);
        p2Lay = new JButton("Lay  ");
        p2Lay.addActionListener(this);
        p2LayOnStack = new JButton("LayOnStack");
        p2LayOnStack.addActionListener(this);

        Card [] cardsPlayer2 = new Card[numDealtCards];
        deal(cardsPlayer2);
        p2Hand = new DefaultListModel();

        for(int i = 0; i < cardsPlayer2.length; i++) {
            p2Hand.addElement(cardsPlayer2[i]);
            play2.addCard(cardsPlayer2[i]);}
        p2Hand.clear();
        for(Card i : play2.getList() )
        {
            p2Hand.addElement(i);
        }
        play2.changeDiscard(1);
        play2.changeDraw(1);
        emptyflag = true;
        boolean game = true;
        System.out.println("Initial Player 1 : "+ play1.toString());
        System.out.println("Initial Player 2 : "+ play2.toString());
        System.out.println("Player 1 ");

        p2HandPile = new JList(p2Hand);

        middle.add(new HandPanel("Player 2", p2HandPile, p2Stack, p2Deck, p2Lay, p2LayOnStack));

        add(middle, BorderLayout.CENTER);

        JPanel leftBorder = new JPanel(new GridLayout(2,1));


        setPanels[9].setLayout(new BoxLayout(setPanels[9], BoxLayout.Y_AXIS));
        setPanels[10].setLayout(new BoxLayout(setPanels[10], BoxLayout.Y_AXIS));
        leftBorder.add(setPanels[9]);
        leftBorder.add(setPanels[10]);
        add(leftBorder, BorderLayout.WEST);

        JPanel rightBorder = new JPanel(new GridLayout(2,1));

        setPanels[11].setLayout(new BoxLayout(setPanels[11], BoxLayout.Y_AXIS));
        setPanels[12].setLayout(new BoxLayout(setPanels[12], BoxLayout.Y_AXIS));
        rightBorder.add(setPanels[11]);
        rightBorder.add(setPanels[12]);
        add(rightBorder, BorderLayout.EAST);

    }

    public void actionPerformed(ActionEvent e)
    {


        Object src = e.getSource();
        if(game) {
        if(((p1Deck == src|| p2Deck == src) && !cardDeck.isEmpty()) )
        {

            Card card= cardDeck.peek() ;

            if (card != null )
            {
                if(src == p1Deck )
                {

                    //p1Hand.addElement(card);
                    if( play1.getDraw()==0)
                    {
                        card = cardDeck.dealCard();
                        p1Hand.clear();
                        play1.changeDraw(1);
                        play1.addCard(card);
                        for(Card i : play1.getList() )
                            {
                            p1Hand.addElement(i);
                            }
                        System.out.println("    Added: " +  card.toString());

                    }
                }
                else
                {

                    if( play2.getDraw()==0)
                    {
                        card = cardDeck.dealCard();
                        p2Hand.clear();
                        play2.changeDraw(1);
                        play2.addCard(card);
                        for(Card i : play2.getList() )
                        {
                            p2Hand.addElement(i);
                        }
                        System.out.println("    Added: " +  card.toString());
                     }
                }
                }
            }

            if(cardDeck.getSizeOfDeck() == 0)
                deckPile.setIcon(new ImageIcon(Card.directory + "blank.gif"));



        if(p1Stack == src || p2Stack == src)
        {
            Card card = stackDeck.peek();
            //System.out.print(card);

            if(card != null){

                if(p1Stack == src)
                {

                    if( play1.getDraw()==0)
                    {
                    card = stackDeck.removeCard();
                    p1Hand.clear();
                    play1.changeDraw(1);
                    play1.addCard(card);
                    for(Card i : play1.getList() )
                        {
                            p1Hand.addElement(i);
                        }
                     System.out.println("    Added: " +  card.toString());
                    }
                }
                else
                {
                    if( play2.getDraw()==0)
                    {
                        card = stackDeck.removeCard();
                        p2Hand.clear();
                        play2.changeDraw(1);
                        play2.addCard(card);
                        for(Card i : play2.getList() )
                        {
                            p2Hand.addElement(i);
                        }
                        System.out.println("    Added: " +  card.toString());}
                }
                Card topCard = stackDeck.peek();
                if (topCard != null)
                    topOfStack.setIcon(topCard.getCardImage());
                else
                    topOfStack.setIcon(new ImageIcon(Card.directory + "blank.gif"));




            }

        }

        if(p1Lay == src && play1.getDraw()==1 && play1.getDiscard()==0){
            Object [] cards = p1HandPile.getSelectedValues();
            boolean flag = false;
            String dis= new String()  ; //To get the layed cards
            if (cards.length == 3 || cards.length ==4 ) {
                Card card1 = (Card)cards[0];
                 Set rum=new Set(card1.getRank());
                    for(int j = 0; j < cards.length; j++)
                    {
                        Card cardset = (Card)cards[j];
                        if (rum.getRank()== cardset.getRank() )
                        {
                            //System.out.print(cardset);
                            rum.addCard(cardset);
                            flag=true;
                            dis= dis  +cardset.toString() + ", ";
                        }
                        else {
                            flag=false;
                            break;
                        }

                        }
                    if (rum.Amount()>=3 && flag) {
                        System.out.println("    "
                                + "Discarded: "+ dis);;
                    }
                for(int i = 0; i < cards.length; i++)
                {

                     card1 = (Card)cards[i];


                    if (rum.Amount()>=3 && flag)
                    {
                        layCard(card1);
                        p1Hand.removeElement(card1);
                        play1.removeCard(card1);
                }
                    else {
                        System.out.println("not valid");
                        break;
                    }
                    }

            }
        }

        if(p2Lay == src && play2.getDraw()==1 && play2.getDiscard()==0){
            Object [] cards = p2HandPile.getSelectedValues();
            boolean flag = false;
            String dis= new String();
            if (cards.length == 3 || cards.length ==4 ) {
                Card card = (Card)cards[0];
                 Set rum=new Set(card.getRank());
                    for(int j = 0; j < cards.length; j++)
                    {
                        Card cardset = (Card)cards[j];
                        if (rum.getRank()== cardset.getRank() )
                        {
                            //System.out.print(cardset);
                            rum.addCard(cardset);
                            flag=true;
                            dis= dis + " , " +cardset.toString();
                        }
                        else {
                            flag=false;
                            break;
                        }
                        }
                    if (rum.Amount()>=3 && flag) {
                        System.out.println("    Discarded: "+ dis);;
                    }
                for(int i = 0; i < cards.length; i++)
                {

                     card = (Card)cards[i];


                    if (rum.Amount()>=3 && flag)
                    {
                        layCard(card);
                        p2Hand.removeElement(card);
                        play2.removeCard(card);
                }
                    else {
                        System.out.println("not valid");
                        break;
                    }
                    }

            }
        }


        if(p1LayOnStack == src  && play1.getDraw()==1 && play1.getDiscard()==0){
            int [] num  = p1HandPile.getSelectedIndices();
            if (num.length == 1)
            {
                Object obj = p1HandPile.getSelectedValue();
                if (obj != null)
                {
                    p1Hand.removeElement(obj);
                    Card card = (Card)obj;
                    play1.removeCard(card);

                    stackDeck.addCard(card);
                    topOfStack.setIcon(card.getCardImage());
                    play2.changeDraw(0);
                    play2.changeDiscard(0);
                    play1.changeDiscard(1);
                    System.out.println("    Discarded: " + card.toString());
                    System.out.println("    Hand now: "+ play1.toString());

                    if(cardDeck.isEmpty() && emptyflag && game) {
                        int winner= 0;
                        winner = play1.compareTo(play2);
                        if (winner== 0 ) {
                            System.out.println("It's a tie");

                            }

                        else if( winner == 1 )
                        {
                            System.out.println("Player 2 wins");
                        }
                        else {
                            System.out.println("Player 1 wins");
                        }
                        game=false;
                    }
                    else {
                    System.out.println("Player 2 " );}
                }
            }
        }


        if(p2LayOnStack == src && play2.getDraw()==1 && play2.getDiscard()==0){

            int [] num  = p2HandPile.getSelectedIndices();
            if (num.length == 1)

            {
                Object obj = p2HandPile.getSelectedValue();
                if (obj != null)
                {

                    p2Hand.removeElement(obj);
                    Card card = (Card)obj;
                    play2.removeCard(card);
                    stackDeck.addCard(card);
                    topOfStack.setIcon(card.getCardImage());
                    play1.changeDraw(0);
                    play1.changeDiscard(0);
                    play2.changeDiscard(1);
                    System.out.println("    Discarded: " + card.toString());
                    System.out.println("    Hand now: "+ play2.toString());

                    if(cardDeck.isEmpty() && emptyflag && game) {
                        int winner= 0;
                        winner = play1.compareTo(play2);
                        if (winner== 0 ) {
                            System.out.println("It's a tie");

                            }

                        else if( winner == 1 )
                        {
                            System.out.println("Player 2 wins");
                        }
                        else {
                            System.out.println("Player 1 wins");
                        }
                        game=false;
                    }
                    else {
                     System.out.println("Player 1 " );}
                }
            }
        }

        //needs emptyflag just so that at the it doesnt end the game at the start and  game is a flag just in case to make you only win once
            if (play1.isEmpty() && emptyflag && game){
                System.out.println("Player 1 wins");
                game=false;
            }
            if (play2.isEmpty()&& emptyflag && game){
                System.out.println("Player 2 wins");
                game=false;
            }

    }}


    void layCard(Card card)
    {
        char rank = card.getRank();
        char suit = card.getSuit();
        int suitIndex =  Card.getSuitIndex(suit);
        int rankIndex =  Card.getRankIndex(rank);
        setPanels[rankIndex].array[suitIndex].setText(card.toString());
        //System.out.println("laying " + card);
        setPanels[rankIndex].array[suitIndex].setIcon(card.getCardImage());
    }


}

class HandPanel extends JPanel
{

    public HandPanel(String name,JList hand, JButton stack, JButton deck, JButton lay, JButton layOnStack)
    {
        //model = hand.createSelectionModel();

        setLayout(new BoxLayout(this, BoxLayout.Y_AXIS));
//        add(Box.createGlue());
        JLabel label = new JLabel(name);
        label.setAlignmentX(Component.CENTER_ALIGNMENT);
        add(label);
        stack.setAlignmentX(Component.CENTER_ALIGNMENT);
//        add(Box.createGlue());
        add(stack);
        deck.setAlignmentX(Component.CENTER_ALIGNMENT);
//        add(Box.createGlue());
        add(deck);
        lay.setAlignmentX(Component.CENTER_ALIGNMENT);
        add(lay);
        layOnStack.setAlignmentX(Component.CENTER_ALIGNMENT);
        add(layOnStack);
        add(Box.createGlue());
        add(hand);
        add(Box.createGlue());
    }

}
class SetPanel extends JPanel
{
    private Set data;
    JButton [] array = new JButton[4];

    public SetPanel(int index)
    {
        super();
        data = new Set(Card.rank[index]);

        for(int i = 0; i < array.length; i++){
            array[i] = new JButton("   ");
            add(array[i]);
        }
    }

}
