import java.util.*;

/**
 * AccountManager stores and manages account balances
 * during a session.
 */
public class AccountManager {

    // Maps account number -> balance
    private Map<String, Double> accounts;

    /**
     * Constructor initializes the account storage.
     */
    public AccountManager() {
        accounts = new HashMap<>();
    }

    /**
     * Returns the current balance of the specified account.
     *
     * @param accountNumber the account identifier
     * @return the current balance
     */
    public double getBalance(String accountNumber) {
        return accounts.getOrDefault(accountNumber, 0.0);
    }

    /**
     * Updates the balance of the specified account.
     *
     * @param accountNumber the account identifier
     * @param newBalance the updated balance
     */
    public void updateBalance(String accountNumber, double newBalance) {
        accounts.put(accountNumber, newBalance);
    }

    /**
     * Checks whether the account exists.
     *
     * @param accountNumber the account identifier
     * @return true if account exists, false otherwise
     */
    public boolean isValidAccount(String accountNumber) {
        return accounts.containsKey(accountNumber);
    }
}