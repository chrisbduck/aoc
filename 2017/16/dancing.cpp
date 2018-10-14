#include <algorithm>
#include <cstring>
#include <fstream>
#include <iostream>
#include <memory>
#include <string>
#include <unordered_map>
#include <vector>

using namespace std;

// -----------------------------------------------------------------------------

enum class Operation { Spin, Exchange, Partner };

// -----------------------------------------------------------------------------

// A state is an array of the characters of each programme in the current order.  (a-p = 16 progs)
typedef array<char, 16> State;

// -----------------------------------------------------------------------------

class Move {
public:
	Move() = default;
	virtual ~Move() = default;

	virtual void trace() const = 0;
	virtual State perform(const State& rState) const = 0;

	static unique_ptr<Move> parse(const char* pSrc);

private:
};

// -----------------------------------------------------------------------------

class SpinMove : public Move {
public:
	SpinMove(int offset) {
		m_offset = offset;
	}
	int getProg() const { return m_offset; }

	virtual void trace() const override {
		cout << "spin " << m_offset << endl;
	}

	virtual State perform(const State& rState) const override {
		State newState;
		int size = (int)rState.size();
		for (int index = 0; index < size; ++index) {
			int targetIndex = index + m_offset;
			if (targetIndex >= size)
				targetIndex -= size;
			else if (targetIndex < 0)
				targetIndex += size;
			newState[targetIndex] = rState[index];
		}
		return newState;
	}

private:
	int m_offset;
};

// -----------------------------------------------------------------------------

class ExchangeMove : public Move {
public:
	ExchangeMove(int posA, int posB) {
		m_posA = posA;
		m_posB = posB;
	}

	int getPosA() const { return m_posA; }
	int getPosB() const { return m_posB; }

	virtual void trace() const override {
		cout << "exchange " << m_posA << " " << m_posB << endl;
	}

	virtual State perform(const State& rState) const override {
		State newState(rState);
		newState[m_posA] = rState[m_posB];
		newState[m_posB] = rState[m_posA];
		return newState;
	}

private:
	int m_posA;
	int m_posB;
};

// -----------------------------------------------------------------------------

class PartnerMove : public Move {
public:
	PartnerMove(char idA, char idB) {
		m_idA = idA;
		m_idB = idB;
	}

	int getIDA() const { return m_idA; }
	int getIDB() const { return m_idB; }

	virtual void trace() const override {
		cout << "partner " << m_idA << " " << m_idB << endl;
	}

	virtual State perform(const State& rState) const override {
		State newState(rState);
		int posA = -1, posB = -1;
		for (size_t index = 0; index < newState.size(); ++index) {
			if (rState[index] == m_idA)
				posA = index;
			if (rState[index] == m_idB)
				posB = index;
		}
		if (posA == -1 || posB == -1)
			throw runtime_error("Indices not found");
		newState[posA] = rState[posB];
		newState[posB] = rState[posA];
		return newState;
	}

private:
	char m_idA;
	char m_idB;
};

// -----------------------------------------------------------------------------

unique_ptr<Move> Move::parse(const char* pSrc) {
	char ch = *pSrc;
	if (ch == 's')
		return make_unique<SpinMove>(atoi(pSrc + 1));
	
	const char* pSlashPos = strchr(pSrc, '/');
	if (pSlashPos == nullptr)
		throw runtime_error("Parse error: missing '/'");
	
	switch (ch) {
		case 'x':
			return make_unique<ExchangeMove>(atoi(pSrc + 1), atoi(pSlashPos + 1));
		case 'p':
			return make_unique<PartnerMove>(*(pSrc + 1), *(pSlashPos + 1));
	}
	throw new runtime_error("Unknown instruction");
}

// -----------------------------------------------------------------------------

class Edge;
class Node;

class Node {
public:
	Node(const State& state, int depth) :
		m_state(state),
		m_depth(depth) {
	}

	const State& getState() const { return m_state; }
	int getDepth() const { return m_depth; }

	void addEdge(const shared_ptr<Edge>& rEdge) { m_edges.push_back(rEdge); }

	shared_ptr<Node> findMoveTarget(const shared_ptr<Move>& rMove);

	string getTrace() const {
		std::string out(m_state.size(), ' ');
		char* pOut = out.data();
		for (int index = 0; index < m_state.size(); ++index)
			pOut[index] = m_state[index];
		return out;
	}

	void trace() const {
		cout << getTrace() << endl;
	}

private:
	State m_state;
	int m_depth;
	vector<shared_ptr<Edge>> m_edges;
};

class Edge {
public:
	Edge(const shared_ptr<Node>& rTarget, const shared_ptr<Move>& rMove) :
		m_target(rTarget),
		m_move(rMove) {
	}

	const shared_ptr<Node>& getTarget() const { return m_target; }
	const shared_ptr<Move>& getMove() const { return m_move; }

private:
	shared_ptr<Node> m_target;
	shared_ptr<Move> m_move;
};

class StateHash {
public:
	int operator()(const State& rState) const {
		int val = calculateSubhash(rState, 0);
		val *= 137;
		val ^= calculateSubhash(rState, 6);
		val *= 137;
		val ^= calculateSubhash(rState, 11);
		return val;
	}

private:
	int calculateSubhash(const State& rState, int startIndex) const {
		int val = 0;
		int endIndex = startIndex + 6;
		for (int index = startIndex; index < endIndex; ++index)
			val = (val << 5) | rState[index];
		return val;
	}
};

class Graph {
public:
	Graph(const vector<shared_ptr<Move>>& rDance, int repetitions) :
		m_rDance(rDance) {
		State initialState;
		for (int index = 0; index < initialState.size(); ++index)
			initialState[index] = 'a' + index;
		m_current = make_shared<Node>(initialState, 0);
		m_map.insert({ initialState, m_current });
		m_current->trace();
		m_inCycle = false;
		m_depth = 0;
		m_moveIndex = 0;
		m_totalMoveIndex = 0;
		m_totalMoveCount = m_rDance.size() * repetitions;
	}

	bool step() {
		move(m_rDance[m_moveIndex]);
		++m_moveIndex;
		++m_totalMoveIndex;
		if (m_moveIndex >= m_rDance.size())
			m_moveIndex = 0;
		if (m_totalMoveIndex >= m_totalMoveCount)
			return false;
		return true;
	}

	void move(const shared_ptr<Move>& rMove) {
		++m_depth;
		m_current = applyMove(rMove, m_current);
		cout << m_current->getTrace() << " " << m_totalMoveIndex << endl << flush;
	}

	shared_ptr<Node> applyMove(const shared_ptr<Move>& rMove, const shared_ptr<Node>& rStartNode) {
		// Check the current node to see if it already has an edge for the given move
		shared_ptr<Node> rTarget = rStartNode->findMoveTarget(rMove);
		if (rTarget != nullptr) {
			int cycleLength = m_depth - rTarget->getDepth();
			if (!m_inCycle) {
				while (m_totalMoveIndex + cycleLength < m_totalMoveCount)
					m_totalMoveIndex += cycleLength;
				m_inCycle = true;
			}
			cout << "** CYCLE " << cycleLength << endl << flush;
			return rTarget;
		}

		if (m_inCycle)
			throw runtime_error("Not actually a cycle");

		// Perform the move from the current node
		State newState = rMove->perform(rStartNode->getState());

		// See if the new state already exists in the graph, and add it if not
		auto iNodePair = m_map.find(newState);
		if (iNodePair != m_map.end()) {
			rTarget = iNodePair->second;
			cout << rTarget->getTrace() << " state found again" << endl << flush;
		} else {
			// Add a node for the new state to the graph
			rTarget = make_shared<Node>(newState, m_depth);
			m_map.insert({ newState, rTarget });
		}
		
		// Add an edge to the new node
		rStartNode->addEdge(make_shared<Edge>(rTarget, rMove));
		return rTarget;
	}

private:
	unordered_map<State, shared_ptr<Node>, StateHash> m_map;
	shared_ptr<Node> m_current;
	bool m_inCycle;
	int m_depth;
	const vector<shared_ptr<Move>>& m_rDance;
	int64_t m_moveIndex;
	int64_t m_totalMoveIndex;
	int64_t m_totalMoveCount;
};

// -----------------------------------------------------------------------------

shared_ptr<Node> Node::findMoveTarget(const shared_ptr<Move>& rMove) {
	auto iEdge = find_if(m_edges.cbegin(), m_edges.cend(),
						[rMove](const shared_ptr<Edge>& rEdge) { return rEdge->getMove() == rMove; });
	return (iEdge != m_edges.cend()) ? (*iEdge)->getTarget() : nullptr;
}

// -----------------------------------------------------------------------------

vector<shared_ptr<Move>> parseMoves(const string& rInputFileName) {
	vector<shared_ptr<Move>> moves;
	ifstream input(rInputFileName);
	string line;
	getline(input, line);
	vector<char> charLine(line.length() + 1);
	strcpy(charLine.data(), line.c_str());
	char* pToken = strtok(charLine.data(), ",");
	while (pToken != nullptr) {
		moves.push_back(Move::parse(pToken));
		pToken = strtok(nullptr, ",");
	}
	return moves;
}

// -----------------------------------------------------------------------------

int main(int argc, char* pArgV[]) {
	if (argc < 2) {
		cerr << "usage: run <input_file_name>\n";
		return 1;
	}
	string inputFileName = pArgV[1];

	vector<shared_ptr<Move>> dance = parseMoves(inputFileName);
	const int defaultTraceCount = 10;
	int traceCount = (dance.size() < defaultTraceCount) ? dance.size() : defaultTraceCount;
	for (int index = 0; index <  traceCount; ++index)
		dance[index]->trace();
	cout << dance.size() << " moves\n";

	Graph graph(dance, 1000000000);
	while (graph.step())
		;

	return 0;
}
