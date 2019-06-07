#include <functional>
#include <string>
#include <unordered_map>

class Simulator
{
public:
	Simulator();
	
	void run(const std::vector<std::string>& rOperations);
	
private:
	typedef std::unordered_map<std::string, int> RegisterMap;
	typedef void (Simulator::*OpFunc)(const std::string&, const std::string&);
	typedef std::unordered_map<std::string, OpFunc> OpMap;
	
	int getRegisterValue(const std::string& rRegName) const;
	void setRegisterValue(const std::string& rRegName, int value);
	int getOpValue(const std::string& rValue) const;
	
	void set(const std::string& rRegName, const std::string& rValue);
	void add(const std::string& rRegName, const std::string& rValue);
	void sub(const std::string& rRegName, const std::string& rValue);
	void mul(const std::string& rRegName, const std::string& rValue);
	void mod(const std::string& rRegName, const std::string& rValue);
	void jgz(const std::string& rRegName, const std::string& rValue);
	void jnz(const std::string& rRegName, const std::string& rValue);
	
	RegisterMap m_registers;
	OpMap m_operations;
	int m_ip;
	
	int m_mulCount;
};
