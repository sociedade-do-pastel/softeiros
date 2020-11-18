#include "LogicaCliEnter.hpp"

LogicaCliEnter::LogicaCliEnter()
	: usuario{"jooj"}, enderecoServer{"127.0.0.1"}, port{8080}
{
	createSocket();
}

string LogicaCliEnter::makeCommand(string commandName)
{
    json response = {
		{"usuario", usuario},
		{"function", commandName}
	};

	return response.dump();
}

string LogicaCliEnter::makeRequest(string requestString)
{
	char resposta[2000];
	
    if (send(socket_desc , requestString.c_str(), int(requestString.size()), 0) < 0)
		std::cout << "Send error!" << "\n";

	if (recv(socket_desc, resposta, 2000, 0) < 0)
		std::cout << "Receive failed" << "\n";

	std::cout << resposta << "\n";

	return resposta;
}

json LogicaCliEnter::getInfo()
{
	json request = json::parse(makeRequest(makeCommand("userGeneralQuery")));

	return request;
}

void LogicaCliEnter::createSocket()
{
	socket_desc = socket(AF_INET , SOCK_STREAM , 0);
	
	if (socket_desc == -1)
		std::cout << "Socket not created" << "\n";

	struct sockaddr_in server;
	server.sin_addr.s_addr = inet_addr(enderecoServer.c_str());
	server.sin_family = AF_INET;
	server.sin_port = htons( 8080 );

	if (connect(socket_desc , (struct sockaddr *)&server , sizeof(server)) < 0)
		std::cout << "Connection error!" << "\n";
	else
		std::cout << "Connected" << "\n";
}
