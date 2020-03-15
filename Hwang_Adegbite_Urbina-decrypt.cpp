#include <iostream>
#include <string>
#include <vector>
#include <tuple>
#include <map>
#include <iterator>
#include <algorithm>
#include <utility>
#include <fstream>
using namespace std;

vector<vector<int>>& prep_trials(string&);

const vector<tuple<int,int>> index_of_coincidence_analysis(string&);

const tuple<vector<int>,int>& chi_squared_analysis(string&, int);

string& cipherOpen(const string&);

int main() {
	string ciphertext("sinbyqbenfbka ahdahqhz ajasdgkkkkkaskdkgi");
	vector<tuple<int,int>> top_key_lengths(index_of_coincidence_analysis(ciphertext));
	cout << "Probable keys and their associated chi-squared values:" << endl;
	for (size_t i = 0; i < 3; i++) {
		int key, total_chi;
		tuple<vector<int>, int> res(key, total_chi);
		res = chi_squared_analysis(ciphertext, get<1>(top_key_lengths[i]));
		cout << "key: " << key << "|| Total Chi Squared: " << total_chi << endl;
	}
}

vector<vector<int>>& prep_trials(string& ciphertext) {
	//for key length t{1,..,24}
	vector<vector<int>> trials;
	for (size_t i = 1; i < 25; i++) {
		vector<int> trial_t;
		for (size_t j = 0; j < i; j++) {
			trial_t.push_back(0);
		}
		trials.push_back(trial_t);
	}
	for (size_t i = 0; i < size(ciphertext); i++) {
		for (size_t j = 0; j < size(trials); j++) {
			int t = j + 1;
			trials[j][i % t] = ciphertext[i];
		}
	}
	return trials;
}

//returns the top three key lengths based on how similar the respective index of
//coincidence is to that of the English language
const vector<tuple<int,int>> index_of_coincidence_analysis(string& ciphertext) {
	vector<vector<int>> trials(prep_trials(ciphertext));
	vector<tuple<int,int>> iocS;
	for (size_t i = 0; i < size(trials); i++) {
		//Within each group per key length t, calculate the index of coincidence
		//average the indices of coincidence across groups per key length t
		int t = i + 1;
		int ioc_sum = 0;
		for (const vector<int>& bucket : trials) {
			map<char, int> freqDist;
			for (char letter : bucket) {
				if (freqDist[letter]) {
					freqDist[letter] += 1;
				}
				else {
					freqDist[letter] = 1;
				}
			}
			int ioc(0);
			int N = size(bucket);

			for (map<char, int>::iterator itr = freqDist.begin();
				itr != freqDist.end(); ++itr) {
				if (N > 1) {
					map<char, int>::iterator jtr = prev(itr);
					ioc += (itr->second * (jtr)->second) / (N * (N - 1));
				}
				ioc_sum += ioc;
			}
			int ioc_ave = ioc_sum / t;
			tuple<int, int> combo(ioc_ave, t);
			iocS.push_back(combo);
		}
	}
	vector<tuple<int,int>> ioc_diffs;
	for (const auto& item: iocS) {
		tuple<int,int> combo(abs(get<0>(item) - 0.06), get<1>(item));
		ioc_diffs.push_back(combo);
	}
	for (size_t i = 0; i < size(ioc_diffs) - 1; i++) {
		for (size_t j = 1; j < size(ioc_diffs); j++) {
			if (get<0>(ioc_diffs[i]) < get<0>(ioc_diffs[j])) {
				swap(ioc_diffs[i], ioc_diffs[j]);
			}
		}
	}
	return ioc_diffs;
}

const tuple<vector<int>, int>& chi_squared_analysis(string& ciphertext, int key_length) {
	map<char, int> percents;
	percents.insert(pair<char, int>(' ', 0.1829));
	percents.insert(pair<char, int>('a', 0.0653));
	percents.insert(pair<char, int>('b', 0.0126));
	percents.insert(pair<char, int>('c', 0.0223));
	percents.insert(pair<char, int>('d', 0.0328));
	percents.insert(pair<char, int>('e', 0.01027));
	percents.insert(pair<char, int>('f', 0.0198));
	percents.insert(pair<char, int>('g', 0.0162));
	percents.insert(pair<char, int>('h', 0.0498));
	percents.insert(pair<char, int>('i', 0.0567));
	percents.insert(pair<char, int>('j', 0.0010));
	percents.insert(pair<char, int>('k', 0.0056));
	percents.insert(pair<char, int>('l', 0.0332));
	percents.insert(pair<char, int>('m', 0.0203));
	percents.insert(pair<char, int>('n', 0.0571));
	percents.insert(pair<char, int>('o', 0.0616));
	percents.insert(pair<char, int>('p', 0.0150));
	percents.insert(pair<char, int>('q', 0.0008));
	percents.insert(pair<char, int>('r', 0.0499));
	percents.insert(pair<char, int>('s', 0.0532));
	percents.insert(pair<char, int>('t', 0.0752));
	percents.insert(pair<char, int>('u', 0.0228));
	percents.insert(pair<char, int>('v', 0.0080));
	percents.insert(pair<char, int>('w', 0.0170));
	percents.insert(pair<char, int>('x', 0.0014));
	percents.insert(pair<char, int>('y', 0.0143));
	percents.insert(pair<char, int>('z', 0.0005));

	vector<string> buckets;
	for (size_t i = 0; i < key_length; i++) {
		buckets.push_back("");
	}
	for (size_t i = 0; i < size(ciphertext); i++) {
		buckets[i % key_length] = ciphertext[i];
	}
	vector<int> key;
	int total_chi(0);
	for (string bucket : buckets) {
		string shift_buffer;
		vector<tuple<int,int>> chi_buffer;
		for (size_t shift_amount = 1; shift_amount < 26; shift_amount++) {
			map<char, int> freqDict;
			int chi_squared(0);
			vector<int> chi_shift;

			//shift by one every iteration
			if (!size(shift_buffer)) {
				for (char letter : bucket) {
					if (letter == ' ') {
						shift_buffer += 'a';
					}
					else if (letter == 'z') {
						shift_buffer += ' ';
					}
					else
					{
						shift_buffer += (char)((int)letter + 1);
					}
				}
			}
			else{
				string temp;
				for (char letter : shift_buffer) {
					if (letter == ' ') {
						temp += 'a';
					}
					else if (letter == 'z') {
						temp += ' ';
					}
					else
					{
						temp += (char)((int)letter + 1);
					}
				}
				shift_buffer = temp;
			}

			for (char letter : shift_buffer) {
				if (freqDict[letter]) {
					freqDict[letter] += 1;
				}
				else{
					freqDict[letter] = 1;
				}
			}

			for (pair<char,int> combo: freqDict){
				char char_chi_squared = (combo.second - percents[combo.first]
					* size(bucket)*size(bucket))/(percents[combo.first] * 
						size(bucket));
				chi_squared += char_chi_squared;
			}
			//record chi-squared values for different shift amounts
			tuple<int, int> combo(chi_squared, shift_amount);
			chi_buffer.push_back(combo);
		}
		for (size_t i = 0; i < size(chi_buffer) - 1; i++) {
			for (size_t j = 1; j < size(chi_buffer); j++) {
				if (get<0>(chi_buffer[i]) < get<0>(chi_buffer[j])) {
					swap(chi_buffer[i], chi_buffer[j]); 
				}
			}
		}
		key.push_back(get<1>(chi_buffer[0]));
		total_chi += get<0>(chi_buffer[0]);
	}
	tuple<vector<int>, int> res(key, total_chi);
	return res;
}

string& cipherOpen() {
	cout << "Enter the filename:\n";
	string filename;
	cin >> filename;
	fstream file(filename);
	while (!file) {
		cerr << "Could not open the file. Try again.\n";
		cin >> filename;
		file.open(filename);
	}
	string cipher;
	getline(file, cipher);
	file.close();
	return cipher;
}