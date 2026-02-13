import com.sun.source.tree.NewArrayTree;
import java.util.*;

public class AccountManager {
    private int accountNumber;
    private int balance;
    private boolean isValid = true;

    public AccountManager(int accountNumber, int balance, boolean isValid) {
        this.accountNumber = accountNumber;
        this.balance = balance;
        this.isValid = isValid;
    }

    List<AccountManager> accounts = NewArrayList<>();
    
    public int getBalance() {
        return this.balance;
    }

    public void updateBalance(int change) {
        this.balance += change;
    }

    public boolean isValidAccount() {
        return this.isValid;
    }

    public void setValidity(boolean validity) {
        this.isValid = validity;
    }
}