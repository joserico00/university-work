import javax.swing.SwingUtilities;

public class RummyGame extends Table {
    public static void main(String args[])
    {
        SwingUtilities.invokeLater(() -> {
            Table table = new Table();
            table.setDefaultCloseOperation(Table.EXIT_ON_CLOSE);
            table.setVisible(true);
        });
    }
}
