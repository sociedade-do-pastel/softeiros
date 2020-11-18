#ifndef LOGICA_CLIENTER
#define LOGICA_CLIENTER

#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <nlohmann/json.hpp>
#include <assert.h>

using json = nlohmann::json;
using namespace std;

class LogicaCliEnter
{
public:
    LogicaCliEnter();
	json getInfo();

private:
	string usuario;
	string enderecoServer;
	int socket_desc;
	int port;
	
	string makeCommand(string commandName);
	string makeRequest(string requestString);
        string parseResponseString();
	void createSocket();
};

#endif
