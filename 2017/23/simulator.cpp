#include "simulator.h"

#include <iostream>
#include <locale>
#include <stdexcept>

// -----------------------------------------------------------------------------

static std::string removeWhiteSpace(const std::string& rSource)
{
	std::string output;
	size_t startPos = 0;
	while (true)
	{
		size_t nextPos = rSource.find_first_of(" \t\r\n", startPos);
		if (nextPos == std::string::npos)
			break;
		output.append(rSource.substr(startPos, nextPos - startPos));
		startPos = nextPos + 1;
	}
	output.append(rSource.substr(startPos));
	return output;
}

// -----------------------------------------------------------------------------

Simulator::Simulator()
	: m_ip(0)
	, m_mulCount(0)
{
	m_operations["set"] = &Simulator::set;
	m_operations["add"] = &Simulator::add;
	m_operations["sub"] = &Simulator::sub;
	m_operations["mul"] = &Simulator::mul;
	m_operations["mod"] = &Simulator::mod;
	m_operations["jgz"] = &Simulator::jgz;
	m_operations["jnz"] = &Simulator::jnz;
}

// -----------------------------------------------------------------------------

void Simulator::run(const std::vector<std::string>& rInstructions)
{
	size_t numInstructions = rInstructions.size();
	
	while (m_ip >= 0 && m_ip < numInstructions)
	{
		const std::string& rOperation = rInstructions[m_ip];
		
		auto opEndIndex = rOperation.find(' ');
		if (opEndIndex == std::string::npos)
			throw std::runtime_error("Invalid rOperation");
		
		std::string op = rOperation.substr(0, opEndIndex);
		
		auto regEndIndex = rOperation.find(' ', opEndIndex + 1);
		auto count = ((regEndIndex == std::string::npos) ? rOperation.length() : regEndIndex) - (opEndIndex + 1);
		std::string reg = rOperation.substr(opEndIndex + 1, count);
		
		std::string val = removeWhiteSpace((regEndIndex == std::string::npos) ? std::string() : rOperation.substr(regEndIndex + 1));
		
		std::cout << op << " " << reg << " " << val << std::endl;
		
		auto iOp = m_operations.find(op);
		if (iOp == m_operations.cend())
			throw std::runtime_error("Unknown operation");
		
		OpFunc opFunc = iOp->second;
		(this->*opFunc)(reg, val);
		
		++m_ip;
	}
}

// -----------------------------------------------------------------------------

int Simulator::getRegisterValue(const std::string& rRegName) const
{
	auto iReg = m_registers.find(rRegName);
	return (iReg != m_registers.end()) ? iReg->second : 0;
}

// -----------------------------------------------------------------------------

void Simulator::setRegisterValue(const std::string& rRegName, int value)
{
	m_registers.insert_or_assign(rRegName, value);
	std::cout << rRegName << " := " << getRegisterValue(rRegName) << std::endl;
}

// -----------------------------------------------------------------------------

int Simulator::getOpValue(const std::string& rValue) const
{
	if (rValue.length() == 0)
		return 0;
	
	char first = rValue.front();
	return isalpha(first) ? getRegisterValue(rValue) : atoi(rValue.c_str());
}

// -----------------------------------------------------------------------------

void Simulator::set(const std::string& rRegName, const std::string& rValue)
{
	setRegisterValue(rRegName, getOpValue(rValue));
}

// -----------------------------------------------------------------------------

void Simulator::add(const std::string& rRegName, const std::string& rValue)
{
	setRegisterValue(rRegName, getRegisterValue(rRegName) + getOpValue(rValue));
}

// -----------------------------------------------------------------------------

void Simulator::sub(const std::string& rRegName, const std::string& rValue)
{
	setRegisterValue(rRegName, getRegisterValue(rRegName) - getOpValue(rValue));
}

// -----------------------------------------------------------------------------

void Simulator::mul(const std::string& rRegName, const std::string& rValue)
{
	setRegisterValue(rRegName, getRegisterValue(rRegName) * getOpValue(rValue));
	++m_mulCount;
	std::cout << "mul count: " << m_mulCount << std::endl;
}

// -----------------------------------------------------------------------------

void Simulator::mod(const std::string& rRegName, const std::string& rValue)
{
	setRegisterValue(rRegName, getRegisterValue(rRegName) % getOpValue(rValue));
}

// -----------------------------------------------------------------------------

void Simulator::jgz(const std::string& rRegName, const std::string& rValue)
{
	if (getRegisterValue(rRegName) > 0)
		m_ip += getOpValue(rValue) - 1;
}

// -----------------------------------------------------------------------------

void Simulator::jnz(const std::string& rRegName, const std::string& rValue)
{
	if (getRegisterValue(rRegName) != 0)
		m_ip += getOpValue(rValue) - 1;
}

// -----------------------------------------------------------------------------
