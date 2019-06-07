#include "simulator.h"

#include <fstream>
#include <iostream>
#include <vector>

// -----------------------------------------------------------------------------

std::vector<std::string> s_operations
{
	"set a 1",
	"add a 2",
	"set b 3",
	"mul a b",
	"mul a -1",
	"add a 1",
	"jnz a -1",
};

// -----------------------------------------------------------------------------

std::vector<std::string> readInput(const char* pFileName)
{
	std::ifstream input(pFileName);
	std::vector<std::string> instructions;
	std::string line;
	while (true)
	{
		std::getline(input, line);
		if (input.eof())
			break;
		instructions.push_back(line);
	}
	return instructions;
}

// -----------------------------------------------------------------------------

int main(int argc, char* pArgv[])
{
	if (argc < 2)
	{
		std::cerr << "Usage: coprocessor <inputfile>\n";
		return 1;
	}
	
	std::vector<std::string> instructions { readInput(pArgv[1]) };
	
	Simulator simulator;
	simulator.run(instructions);
	return 0;
}
