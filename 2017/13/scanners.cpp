//
// Day 13: Packet Scanners
// https://adventofcode.com/2017/day/13
//

#include <algorithm>
#include <fstream>
#include <iostream>
#include <map>
#include <memory>
#include <sstream>
#include <tuple>
#include <vector>

using namespace std;

class Scanner {
public:
	Scanner(int range) {
		m_y = 0;
		m_range = range;
	}

	int getY() const { return m_y; }
	int getRange() const { return m_range; }

private:
	int m_y;
	int m_range;
};

// -----------------------------------------------------------------------------

map<int, unique_ptr<Scanner>> parseScanners(const vector<string>& rInputLines) {
	map<int, unique_ptr<Scanner>> scanners;
	for (const string& rLine: rInputLines) {
		stringstream sstream(rLine);
		int distance, range;
		sstream >> distance;
		sstream.ignore(2);
		sstream >> range;
		scanners[distance] = make_unique<Scanner>(range);
	}
	return scanners;
}

// -----------------------------------------------------------------------------

vector<string> readFile(const string& rFileName) {
	ifstream inputFile(rFileName);
	vector<string> output;
	char buffer[1024];
	while (true) {
		inputFile.getline(buffer, sizeof(buffer));
		if (!inputFile.good())
			return output;
		output.push_back(string(buffer));
	}
}

// -----------------------------------------------------------------------------

int main(int argc, char* ppArgv[]) {
	if (argc < 2) {
		cerr << "Usage: " << ppArgv[0] << " <input file>\n";
		return 1;
	}

	vector<string> inputLines = readFile(ppArgv[1]);
	map<int, unique_ptr<Scanner>> scanners = parseScanners(inputLines);
	for (auto kvp = scanners.cbegin(); kvp != scanners.cend(); ++kvp)
		cout << "Scanner: distance " << kvp->first << ", range " << kvp->second->getRange() << endl;

	return 0;
}
