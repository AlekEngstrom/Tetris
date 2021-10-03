
#include <iostream>
#include <string>
#include <vector>
#include "point.h"
#include <chrono>


using namespace std;



void displayBoard(int rows, int columns, int gameBoard[20][10]){
    for (int y = rows - 1; y >= 0; y--) {
        for (int x = 0; x < columns; x++) {
        cout << gameBoard[y][x];
        }
        cout << endl;
    }
}

int replaceRow(int rows, int columns, int gameBoard[20][10]){
    bool runs;
    bool ran = false;
    do {
        int topRow = 20;
        int bottomRow = 0;
        runs = false;
        for (int y = 0; y < rows; y++) {

            int bottomCount = 0;
            for (int x = 0; x < columns; x++) {
                if (gameBoard[y][x] == 1) {
                    bottomCount++;
                }
                if (bottomCount == 10 && bottomRow == 0) {
                    bottomRow = y;
                    runs = true;
                    ran = true;
                }
            }

        }
        for (int y = bottomRow; y < topRow - 1; y++) {
            for (int x = 0; x < columns; x++) {
                gameBoard[y][x] = gameBoard[y + 1][x];
            }
        }
        if (runs) {
            for (int y = 0; y < 10; y++) {
                gameBoard[19][y] = 0;
            }
        }
        topRow = 20;
        bottomRow = 0;
        runs = false;
        for (int y = 0; y < rows; y++) {

            int bottomCount = 0;
            for (int x = 0; x < columns; x++) {
                if (gameBoard[y][x] == 1) {
                    bottomCount++;
                }
                if (bottomCount == 10 && bottomRow == 0) {
                    bottomRow = y;
                    runs = true;
                }
            }
        }
    }while (runs);
    if (ran){
        displayBoard(rows, columns, gameBoard);
        cout << endl;
    }
    return gameBoard[20][10];
}


void createBoard(int rows, int columns, int gameBoard[20][10]){
    for (int y = rows - 1; y >= 0; y--) {
        for (int x = 0; x < columns; x++) {
        gameBoard[y][x] = 0;
        }
    }

}


void placePiece(char letter, int rows, int columns, int gameBoard[20][10], int x, int r, int n){
    if (letter == 't'){

        if (r == 0){
            for (int y = rows - 1; y >= 0; y--){
                if (gameBoard[y][x - 1] == 1 || gameBoard[y][x] == 1 || gameBoard[y][x+1] == 1){
                    gameBoard[y+1][x - 1] = n;
                    gameBoard[y+1][x+1] = n;
                    gameBoard[y+1][x] = n;
                    gameBoard[y+2][x] = n;
                    break;
                }
                else if (y == 0){
                    gameBoard[0][x - 1] = n;
                    gameBoard[0][x+1] = n;
                    gameBoard[0][x] = n;
                    gameBoard[1][x] = n;
                    break;
                }
            } //normal rotation
        }
        if (r == 1){
            for (int y = rows - 1; y >= 0; y--){
                if (y != 0 && (gameBoard[y-1][x] == 1|| gameBoard[y][x+1] == 1)){
                    gameBoard[y+2][x] = n;
                    gameBoard[y][x] = n;
                    gameBoard[y+1][x] = n;
                    gameBoard[y+1][x+1] = n;
                    break;
                }
                else if (gameBoard[y][x] == 1 ){
                    gameBoard[y+3][x] = n;
                    gameBoard[y+1][x] = n;
                    gameBoard[y+2][x] = n;
                    gameBoard[y+2][x+1] = n;
                    break;
                }
                else if (y == 0){
                    gameBoard[2][x] = n;
                    gameBoard[1][x] = n;
                    gameBoard[0][x] = n;
                    gameBoard[1][x+1] = n;
                    break;
                }
            } //face right
        }
        if (r == 2){
            for (int y = rows - 1; y >= 0; y--){
                if (y != 0 && (gameBoard[y-1][x-1] == 1 || gameBoard[y-1][x+1] == 1)){
                    gameBoard[y][x] = n;
                    gameBoard[y][x-1] = n;
                    gameBoard[y][x+1] = n;
                    gameBoard[y-1][x] = n;
                    break;
                }
                else if (y != 0 && gameBoard[y-1][x] == 1){
                    gameBoard[y][x] = n;
                    gameBoard[y+1][x-1] = n;
                    gameBoard[y+1][x+1] = n;
                    gameBoard[y+1][x] = n;
                    break;
                }
                else if (y == 0){
                    gameBoard[0][x] = n;
                    gameBoard[1][x] = n;
                    gameBoard[1][x-1] = n;
                    gameBoard[1][x+1] = n;
                    break;
                }
            } //face down
        }
        if (r == 3){
            for (int y = rows - 1; y >= 0; y--){
                if (y != 0 && (gameBoard[y-1][x] == 1|| gameBoard[y][x-1] == 1)){
                    gameBoard[y+2][x] = n;
                    gameBoard[y][x] = n;
                    gameBoard[y+1][x] = n;
                    gameBoard[y+1][x-1] = n;
                    break;
                }
                else if (gameBoard[y][x] == 1 ){
                    gameBoard[y+3][x] = n;
                    gameBoard[y+1][x] = n;
                    gameBoard[y+2][x] = n;
                    gameBoard[y+2][x-1] = n;
                    break;
                }
                else if (y == 0){
                    gameBoard[2][x] = n;
                    gameBoard[1][x] = n;
                    gameBoard[0][x] = n;
                    gameBoard[1][x-1] = n;
                    break;
                }
            } //face left
        }
    }
}
int findSpot(char letter, int rows, int columns, int gameBoard[20][10]){
    int r = 0;
    int y = 0;
    int x = 0;
    int n = 0;
    point xR = point(x, y);
    if (letter == 't' ) {
        while (r!=4) {
            for (y = rows - 2; y >= 0; y--) {
                for (x = 0; x < columns - 2; x++) {
                    if (gameBoard[y][x] == 0 && gameBoard[y][x + 1] == 0 && gameBoard[y][x + 2] == 0 &&
                        gameBoard[y + 1][x + 1] == 0 && r == 0) {
                        n = 2;
                        placePiece(letter, rows, columns, gameBoard, x, r, n);
                    }
                }
            }
            r++;
        }
    }
    return r;
}

int main() {

    auto start = std::chrono::high_resolution_clock::now();

    const int columns = 10;
    const int rows = 20;
    int gameBoard[rows][10];
    bool gameOver = false;
    createBoard(rows, columns, gameBoard);
    displayBoard(rows, columns, gameBoard);
    cout << endl;
    int n = 1;
    char letter = 't';
    int x = 1;
    int r = 0;
    bool lost = false;
        replaceRow(rows, columns, gameBoard);
        placePiece(letter, rows, columns, gameBoard, x, r, n);
        displayBoard(rows, columns, gameBoard);

    x = 1;
    r = 3;
    placePiece(letter, rows, columns, gameBoard, x, r, n);
    displayBoard(rows, columns, gameBoard);

    auto finish = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed = finish - start;
    std::cout << "Elapsed time: " << elapsed.count() << " s\n";

    return 0;
}
