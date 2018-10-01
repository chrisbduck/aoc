//
// Day 3: Spiral Memory
// https://adventofcode.com/2017/day/3
//

#include <iostream>
#include <tuple>
#include <vector>

using namespace std;

typedef std::tuple<int, int> Coord;

// -----------------------------------------------------------------------------

Coord getCoord(int squareIndex, int ring, int squaresInRing) {
	int squaresInQuadrant = squaresInRing / 4;
	int quadrant = squareIndex / squaresInQuadrant;
	int offset = squareIndex % squaresInQuadrant + 1;
	//cout << "Quadrant " << quadrant << ", offset " << offset << endl;
	switch (quadrant) {
		case 0:		return Coord(ring, -ring + offset);
		case 1:		return Coord(ring - offset, ring);
		case 2:		return Coord(-ring, ring - offset);
		case 3:		return Coord(-ring + offset, -ring);
		default:
			cerr << "Unexpected quadrant: " << quadrant << endl;
			throw new runtime_error("Unexpected quadrant");
	}
}

// -----------------------------------------------------------------------------

int countDistance(int squareIndex) {
	if (squareIndex < 2)
		return 0;

	// Subtract 2 from square numbers and input, so the [+1, 0] square is index 0.
	squareIndex -= 2;

	// Ring 1 = 4 x 2 squares
	// Ring 2 = 4 x 4 squares
	// Ring n = 4 x 2n squares

	// Determine ring number by subtracting numbers of squares in each ring until the number is less than
	// the size of the next ring.  The number is then the index in the given ring, starting at coordinate
	// [+r, -r + 1], going up in y to [+r, +r], down in x to [-r, +r], down in y to [-r, -r], then
	// up in x to [+r, -r].

	int ring = 1;
	int squaresInRing;
	while (true) {
		squaresInRing = (4 * 2) * ring;
		if (squareIndex < squaresInRing)
			break;
		squareIndex -= squaresInRing;
		++ring;
	}

	//cout << endl;
	cout << "Ring " << ring << " has " << squaresInRing << " squares; index is " << squareIndex << endl;
	Coord coord = getCoord(squareIndex, ring, squaresInRing);
	//cout << "Coord: " << get<0>(coord) << ", " << get<1>(coord) << endl;

	return abs(get<0>(coord)) + abs(get<1>(coord));
}

// -----------------------------------------------------------------------------

static const int maxX = 1024;
static const int maxY = 1024;
static const int totalSize = maxX * maxY;
static const int midX = maxX / 2;
static const int midY = maxY / 2;

int getValue(const vector<int>& rValues, int x, int y) {
	return rValues[(y + midY) * maxX + x + midX];
}

void setValue(vector<int>& rValues, int x, int y, int value) {
	rValues[(y + midY) * maxX + x + midX] = value;
}

// -----------------------------------------------------------------------------

int getFirstValueAboveInput(int input) {

	vector<int> values(totalSize);
	fill(values.begin(), values.end(), 0);
	setValue(values, 0, 0, 1);

	for (int ring = 1; ring < maxX / 2; ++ring) {
		int squaresInRing = (4 * 2) * ring;
		for (int squareIndex = 0; squareIndex < squaresInRing; ++squareIndex) {
			Coord coord = getCoord(squareIndex, ring, squaresInRing);
			int x = get<0>(coord);
			int y = get<1>(coord);
			int newValue = 0;
			for (int ny = y - 1; ny <= y + 1; ++ny) {
				for (int nx = x - 1; nx <= x + 1; ++nx) {
					newValue += getValue(values, nx, ny);
				}
			}
			cout << "Setting value at [" << x << ", " << y << "] to " << newValue << endl;
			if (newValue > input) {
				cout << "This is the first value above the input value.\n";
				return newValue;
			}

			setValue(values, x, y, newValue);
		}
	}

	return 0;
}

// -----------------------------------------------------------------------------

int main(int argc, char* ppArgv[]) {
	if (argc < 1) {
		cerr << "Usage: " << ppArgv[0] << " <square index>\n";
		return 1;
	}

	int input = atoi(ppArgv[1]);

	cout << "Distance to square " << input << ": " << countDistance(input) << endl;
	cout << "First value above input: " << getFirstValueAboveInput(input) << endl;

	return 0;
}
