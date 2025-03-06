// GROUP 4 ASSIGNMENT6_2
// BSCS 1B
// ATM PROTOTYPE

#include <iostream>
#include <string>
using namespace std;

void balance(double &bal);
void deposit(double &bal);
void withdraw(double &bal);
void change_pass(string &old_pass);

int main() {
    string pin_code = "123456";
    string pin_input;
    int counter = 0;
    bool trap = false;
    int transaction;
    double bal = 3000;
    int choice;

    do {
        cout << "\nEnter pincode: ";
        cin >> pin_input;

        if(pin_code == pin_input) {
            cout << "Successfully logged in!" << endl;
            trap = true;
            do {
                cout << "\nEnter choice:\n(1) balance\n(2) deposit\n(3) withdraw\n(4) Change Password\n";
                cin >> transaction;
                switch(transaction) {
                    case 1:
                        balance(bal);
                        break;
                    case 2:
                        deposit(bal);
                        break;
                    case 3:
                        withdraw(bal);
                        break;
                    case 4:
                        change_pass(pin_code);
                        cout << "New pin code: " << pin_code << endl;
                        break;
                    default:
                        cout << "Invalid option!" << endl;
                }
                cout << "\nWould you like to do another transaction? (1) yes (2) no: ";
                cin >> choice;
            } while(choice == 1);

        } else {
            cout << "Invalid Credentials!" << endl;
            counter++;
            cout << "You have " << 3 - counter << " remaining tries." << endl;
            trap = false;
            if(counter >= 3) {
                break;
            }
        }
    } while (!trap);

    return 0;
}

void balance(double &bal) {
    cout << "\nYour balance is: " << bal << endl;
}

void deposit(double &bal) {
    double amount;
    cout << "\nEnter amount to be deposited: ";
    cin >> amount;
    bal += amount;
    cout << "\nYour new balance is: " << bal << endl;
}

void withdraw(double &bal) {
    double amount;
    if(bal >= 1001) {
        cout << "\nEnter amount to be withdrawn: ";
        cin >> amount;
        if(amount > bal - 1000) {
            cout << "Unable to withdraw past maintaining balance of 1000." << endl;
        } else {
            bal -= amount;
            cout << "\nYour new balance is: " << bal << endl;
        }
    } else {
        cout << "Unable to withdraw, maintaining balance must be at least 1000." << endl;
    }
}

void change_pass(string &old_pass) {
    string confirm_pass;
    cout << "\nEnter old password: ";
    cin >> confirm_pass;

    if(old_pass == confirm_pass) {
        string new_pass;
        cout << "\nPlease enter new password: ";
        cin >> new_pass;
        old_pass = new_pass;
        cout << "Password changed successfully!" << endl;
    } else {
        cout << "Old password is incorrect!" << endl;
    }
}