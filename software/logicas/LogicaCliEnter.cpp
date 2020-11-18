#include "LogicaCliEnter.hpp"

LogicaCliEnter::LogicaCliEnter()
	: usuario{"jooj"}, enderecoServer{"127.0.0.1"}, port{8080}
{}

string LogicaCliEnter::makeCommand(string commandName)
{
    json response = {
		{"usuario", usuario},
		{"function", commandName}
	};

	return response.dump();
}

string
LogicaCliEnter::parseResponseString()
{
  const int part_size{255};
  const int buff_size{4*part_size};
      
  int32_t received_from_recv{};
  char received_size{0};

  std::string string_to_return{};
  std::string string_containing_size{}; // first string received
  
  // buffer used as a way of control of what is received
  std::vector<char> string_buff(buff_size);

  // this while gets the actual size of the object
  // that is being received through the socket
  while (true)
    {
      received_from_recv = recv(socket_desc,
				&received_size,
				sizeof(received_size),
				0);
      
      assert(received_from_recv > 0);
      // break the loop if our server sends a newline
      if (received_size == '\n')
	break;
      
      string_containing_size.push_back(received_size);
    }

  // length is based off of the received size "header"
  int32_t length{std::stoi(string_containing_size)};

  // now get the full object
   while(length > 0)
    {
      received_from_recv = recv(socket_desc,
				&string_buff[0],
				string_buff.size(),
				0);
      assert(received_from_recv > 0);
      
      string_to_return.append(string_buff.cbegin(), string_buff.cend());
      length -= received_from_recv;
    }

  return string_to_return;
}

string
LogicaCliEnter::makeRequest(string requestString)
{
  if (send(socket_desc , requestString.c_str(), int(requestString.size()), 0) < 0)
    std::cout << "Send error!" << "\n";
  
  return this->parseResponseString();

}

json LogicaCliEnter::getInfo()
{
    createSocket();
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
	server.sin_port = htons( this->port );

	if (connect(socket_desc , (struct sockaddr *)&server , sizeof(server)) < 0)
		std::cout << "Connection error!" << "\n";
	else
		std::cout << "Connected" << "\n";
}
