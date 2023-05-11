#include <iostream>
#include <stdexcept>
using namespace std;

float calcTriPerimeter(float height, float length) { //calculates the perimeter of the triangle
    float side = (float)(0.5 * (sqrt(pow(length, 2) + (4 * pow(height, 2))))); //calculation that finds the sides of an isosceles triangle.
    float perimeter = (2 * side) + length; 
    return perimeter;
}
void printTriangle(float height, float length) { //prints the triangle using stars
    if (((int)length % 2 == 0) || (length > (2 * height))) //checks if triangle can be printed
        cout << "Can not print triangle\n";
    else {
        if (length >= 4) { //prints triangles with a langth of 4 or bigger
            int rowsPerNum = ((int)height - 2) / (((int)length - 2) / 2); //calculates how the rows are divided up
            int topRow = ((int)height - 2) % (int)((length - 2) / 2); //calculates the remainder
            int changes = (length / 2) + 1; 
            int numStars = 1, rowAmount;
            for (int i = 0; i < changes; i++) { //for loop that prints the tower using stars
                if (i == 0 || i == (changes - 1)) rowAmount = 1; //first and last rows
                else if (i == 1) rowAmount = rowsPerNum + topRow; //second row
                else rowAmount = rowsPerNum;
                for (int j = 0; j < rowAmount; j++) { //for loop for an amount of rows for a specific amount of stars
                    int space = (length - numStars) / 2;
                    for (int m = 0; m < space; m++) //for loop that prints spaces so the stars are in the right place
                        cout << " ";
                    for (int k = 0; k < numStars; k++) { //for loop that prints amount of stars in the row
                        cout << "*";
                    }
                    cout << endl;
                }
                numStars = numStars + 2;
            }
        }
        else {
            if (length == 1) { //if there is only one star
                for (int i = 0; i < height; i++) { 
                    cout << "*\n";
                }
            }
            else 
                if (length == 3){ //if there is only three stars
                    for (int i = 0; i < height; i++) {
                        cout << " *\n";
                    }
                    cout << "***\n";
                }
        }
    }
}
float calcRecArea(float height, float length) { //calculates the area of the rectangle
    float area = height * length;
    return area;
}
float calcRecPerimeter(float height, float length) { //calculates the perimeter of the rectangle 
    float perimeter = 2 * (height + length);
    return perimeter;
}
float calculateRec(float height, float length) { //checks if the perimeter or the area of the rectangle should be returned
    float isRectangle = abs(height - length);
    if (isRectangle == 0 || isRectangle > 5) {
        cout << "The rectangles area is: ";
        return calcRecArea(height, length);
    }
    cout << "The rectangles perimeter is: ";
    return calcRecPerimeter(height, length);
}


int main() {
    float height, length;
    int userPick = 0;
    while (userPick != 3) { //list of options for the user to pick from
        cout << "Please pick an option:\n" <<
            "1- a rectangle tower\n" <<
            "2- a triangle tower\n" <<
            "3- exit\n";
        try {
            cin >> userPick;
            if (cin.fail()) {
                cin.clear(); // clear the failbit flag
                cin.ignore(numeric_limits<streamsize>::max(), '\n'); // discard the invalid input
                throw invalid_argument("Invalid input: must be an integer value");
            }
        }
        catch (invalid_argument& e) {
            cout << e.what() << endl;
        }
        if (userPick == 3) //if the user picks 3 it ends the program
            return 0;
        if (userPick == 1 || userPick == 2) { //gets the height and length messurments 
            cout << "Enter the height of the tower\n";
            try {
                cin >> height; 
                if (cin.fail()) {
                    cin.clear(); // clear the failbit flag
                    cin.ignore(numeric_limits<streamsize>::max(), '\n'); // discard the invalid input
                    throw invalid_argument("Invalid input: must be an integer value");
                }
            }
            catch (invalid_argument& e) {
                cout << e.what() << endl;
            }
            if (height <= 2) {
                cout << "Must be a height bigger then 2\n";
                continue;
            }
            cout << "Enter the length of the tower\n";
            try {
                cin >> length;
                if (cin.fail()) {
                    cin.clear(); // clear the failbit flag
                    cin.ignore(numeric_limits<streamsize>::max(), '\n'); // discard the invalid input
                    throw invalid_argument("Invalid input: must be an integer value");
                }
            }
            catch (invalid_argument& e) {
                cout << e.what() << endl;
            }
            if (length <= 0) {
                cout << "Must be a length equal or bigger then 0\n";
                continue;
            }
        }
        if (userPick == 1) //prints information about the rectangle
            cout << calculateRec(height, length) << endl;
        else if (userPick == 2) { //prints information about the triangle
            int flag = 0;
            while (flag == 0) { //repeats again if an invalid option was chosen
                cout << "Pick an option:\n" <<
                    "1 - print triangle perimeter\n" <<
                    "2 - print triangle\n";
                int choice;
                try {
                    cin >> choice;
                    if (cin.fail()) {
                        cin.clear(); // clear the failbit flag
                        cin.ignore(numeric_limits<streamsize>::max(), '\n'); // discard the invalid input
                        throw invalid_argument("Invalid input: must be an integer value");
                    }
                }
                catch (invalid_argument& e) {
                    cout << e.what() << endl;
                }
                flag++;
                if (choice == 1) //prints the perimeter of the triangle
                    cout << "the Triangles perimeter is: " << calcTriPerimeter(height, length) << endl;
                else if (choice == 2) //prints the triangle
                    printTriangle(height, length);
                else {
                    cout << "invalid input\n"; //repeats the option in the event of an invalid input
                    flag = 0;
                }
            }
        }
    }
    return 0;
}
