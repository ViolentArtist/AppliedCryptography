#include <iostream>
#include <string>
#include <cstddef>
using namespace std;

int main() {
    cout << "Enter the ciphertext:\n";
    std::string cipher;
    getline(cin, cipher);  // read characters into cipher
    std::string plaintext = shift(cipher);
    cout << "My plaintext guess is:\n" << plaintext;
    return 0;
}

char shift(cipher) {
    std::string guess;
    int len = cipher.size();
    char c_space = " abcdefghijklmnopqrstuvwxyz";
    int ciph_num_key = create_ciph_num_key(cipher, len, c_space);
    do {
        for (int k=1; k<26; k++) {
            std::string guess_tmp;
            for (int i=0; i<=len; i++) {
                if (ciph_num_key[i] == 0) {  // check for spaces
                    guess_tmp.append(" ");}
                else {
                    int tmp = ciph_num_key[i] + k;
                    if (i <= 26) {
                        guess_tmp.append(c_space[tmp]);}
                    else {
                        tmp -= 26;
                        guess_tmp.append(c_space[tmp]);}
                }
            }
            guess = guess_tmp;
        }
    }
    while (testExpression(guess));
    return guess;
}

int create_ciph_num_key(cipher, len, c_space) {  // create an array of characters' numbers (' '=0, 'z'=26)
    int ciph_num_key [len];
    for (i=0; i<=len; i++) {    
        tmp_num = c_space.find_first_of(cipher[i]);
        ciph_num_key[i] = tmp_num;
    }
    return ciph_num_key;
}


bool testExpression(guess) {
    if (guess is in dictionary) {  // <- THIS IS NOT HOW YOU DO THE THING.  SOMEONE ELSE DO THE THING
        return false;}
    else {return true;}
}

main();
