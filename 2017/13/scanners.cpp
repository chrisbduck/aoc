//
// Day 13: Packet Scanners
// https://adventofcode.com/2017/day/13
//

#include <algorithm>
#include <fstream>
#include <iostream>
#include <map>
#include <memory>
#include <numeric>
#include <sstream>
#include <tuple>
#include <vector>

using namespace std;

class Scanner {
public:
	Scanner(int range) {
		m_y = 0;
		m_dir = 1;
		m_range = range;
	}

	int getY() const { return m_y; }
	int getRange() const { return m_range; }
	void advance() {
		if (m_dir == -1) {
			if (m_y == 0)
				m_dir = 1;
		}
		else {	// m_dir == 1
			if (m_y == m_range - 1)
				m_dir = -1;
		}
		m_y += m_dir;
	}

private:
	int m_y;
	int m_dir;
	int m_range;
};

// -----------------------------------------------------------------------------

map<int, unique_ptr<Scanner>> parseScanners(const vector<string>& rInputLines) {
	map<int, unique_ptr<Scanner>> rScanners;
	for (const string& rLine: rInputLines) {
		stringstream sstream(rLine);
		int distance, range;
		sstream >> distance;
		sstream.ignore(2);
		sstream >> range;
		rScanners[distance] = make_unique<Scanner>(range);
	}
	return rScanners;
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

void traceScanners(const map<int, unique_ptr<Scanner>>& rScanners) {
	cout << "State: ";
	for_each (rScanners.cbegin(), rScanners.cend(),
				[](const auto& iScannerPair) { cout << iScannerPair.first << ":" << iScannerPair.second->getY() << " "; });
	cout << endl;
}

// -----------------------------------------------------------------------------

enum class InstantExit { Enable, Disable };

int getSeverity(const map<int, unique_ptr<Scanner>>& rScanners, int leaveOnCycle = 0,
				InstantExit instantExitOption = InstantExit::Disable) {
	int packetX = -1;
	int largestScannerX = accumulate(rScanners.cbegin(), rScanners.cend(), 0,
									[](int largest, const auto& rCurrent) { return max(largest, rCurrent.first); });
	int severity = 0;

	//traceScanners(rScanners);

	while (packetX < largestScannerX) {
		if (leaveOnCycle > 0)
			--leaveOnCycle;
		else {
			++packetX;
			auto iScannerPair = rScanners.find(packetX);
			if (iScannerPair != rScanners.cend()) {
				const unique_ptr<Scanner>& currentLayer = iScannerPair->second;
				if (currentLayer->getY() == 0) {
					//cout << "Hit packet at distance " << packetX << " with range " << currentLayer->getRange() << endl;
					severity += currentLayer->getRange() * packetX;
					if (instantExitOption == InstantExit::Enable)
						return 1;
				}
			}
		}

		for_each(rScanners.begin(), rScanners.end(), [](const auto& rScanner) { rScanner.second->advance(); });
		//traceScanners(rScanners);
	}

	return severity;
}

// -----------------------------------------------------------------------------

// For each scanner, we'll get caught if (leaving time + distance) % ((range - 1) * 2) == 0
bool isCaught(const map<int, unique_ptr<Scanner>>& rScanners, int delay) {
	return any_of(rScanners.cbegin(), rScanners.cend(),
		[delay](const auto& iScannerPair) {
			int distance = iScannerPair.first;
			int range = iScannerPair.second->getRange();
			return (delay + distance) % ((range - 1) * 2) == 0;
		});
}

// -----------------------------------------------------------------------------

int getLowestXForZeroSeverity(const map<int, unique_ptr<Scanner>>& rScanners) {
	for (int delay = 0; ; ++delay) {
		if (!isCaught(rScanners, delay)) {
			cout << endl;
			return delay;
		}

		if (delay % 1000 == 0)
			cout << "." << flush;
	}
}

// -----------------------------------------------------------------------------

int main(int argc, char* ppArgv[]) {
	if (argc < 2) {
		cerr << "Usage: " << ppArgv[0] << " <input file>\n";
		return 1;
	}

	vector<string> inputLines = readFile(ppArgv[1]);
	map<int, unique_ptr<Scanner>> rScanners = parseScanners(inputLines);
	cout << "Read " << rScanners.size() << " rScanners\n";
	cout << "Severity of leaving immediately = " << getSeverity(rScanners) << endl;
	cout << "Delay to not get caught = " << getLowestXForZeroSeverity(rScanners) << endl;

	return 0;
}
